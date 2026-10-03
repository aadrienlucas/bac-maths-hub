"""Hermes — BAC Math Study Hub (Première, spécialité maths).

Flask app organised by chapter: course summary, Yvan Monka video + PDF course,
graded exercises, formula sheets, mock exams and progress tracking.
Content lives in content.py. Progress is stored per visitor in a signed,
long-lived session cookie (no database needed).
"""
import copy
import json
import os
import random
from datetime import date, timedelta

from flask import Flask, abort, jsonify, render_template, request, session
from jinja2 import DictLoader

from content import CHAPTERS, DOMAINS, MONKA_SEARCH, MONKA_SITE

app = Flask(__name__)

DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-insecure-key-change-me')
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=not DEBUG,
    PERMANENT_SESSION_LIFETIME=timedelta(days=365),
)

# --------------------------------------------------------------------------
# Content indexes
# --------------------------------------------------------------------------
CHAPTERS_BY_ID = {c['id']: c for c in CHAPTERS}
DOMAIN_LABELS = {d[0]: (d[1], d[2]) for d in DOMAINS}
LEVELS = {1: ('Facile', '⭐'), 2: ('Moyen', '⭐⭐'), 3: ('Difficile', '⭐⭐⭐')}

EXERCISES_BY_ID = {}
for _c in CHAPTERS:
    for _n, _ex in enumerate(_c['exercises'], 1):
        _ex['chapter_id'] = _c['id']
        _ex['chapter'] = _c['title']
        _ex['num'] = _n
        EXERCISES_BY_ID[_ex['id']] = _ex
TOTAL_EXERCISES = len(EXERCISES_BY_ID)

EXAM_TEMPLATES = {
    'bac_blanc': {
        'name': 'BAC Blanc',
        'blurb': "5 exercices sur les grands chapitres du programme, niveau BAC.",
        'duration': 240,
        'parts': [('derivation', (2, 3), 5), ('exponentielle', (2, 3), 4), ('suites-arith-geo', (2, 3), 4),
                  ('probas-conditionnelles', (2, 3), 4), ('produit-scalaire', (2, 3), 3)],
    },
    'controle': {
        'name': 'Contrôle',
        'blurb': "Un contrôle de 1h30 : second degré, dérivation, suites, binomiale.",
        'duration': 90,
        'parts': [('second-degre', (2, 3), 5), ('derivation', (2,), 5), ('suites-arith-geo', (2,), 5),
                  ('variables-aleatoires', (2,), 5)],
    },
    'quiz_rapide': {
        'name': 'Quiz Rapide',
        'blurb': "10 questions mélangées (niveaux facile et moyen), tous chapitres.",
        'duration': 20,
        'parts': None,
    },
}


def fmt_duration(minutes):
    h, m = divmod(minutes, 60)
    return f'{h}h{m:02d}' if h and m else (f'{h}h' if h else f'{m} min')


# --------------------------------------------------------------------------
# Per-visitor progress
# --------------------------------------------------------------------------
DEFAULT_PROGRESS = {
    'chapters_completed': [],
    'exercises_done': [],
    'exams_taken': 0,
    'formula_sheets_generated': 0,
    'streak': 0,
    'last_active': None,
    'today': {},
}


def get_progress():
    """Load (and sanitise) the visitor's progress from their session cookie."""
    raw = session.get('progress')
    p = copy.deepcopy(DEFAULT_PROGRESS)
    if isinstance(raw, dict):
        p['chapters_completed'] = [c for c in raw.get('chapters_completed', []) if c in CHAPTERS_BY_ID]
        p['exercises_done'] = sorted({i for i in raw.get('exercises_done', []) if i in EXERCISES_BY_ID})
        p['exams_taken'] = int(raw.get('exams_taken', 0) or 0)
        p['formula_sheets_generated'] = int(raw.get('formula_sheets_generated', 0) or 0)
        p['streak'] = int(raw.get('streak', 0) or 0)
        p['last_active'] = raw.get('last_active')
        p['today'] = raw.get('today') or {}
    today = date.today().isoformat()
    if p['today'].get('date') != today:  # daily goals reset every day
        p['today'] = {'date': today, 'exercises': 0, 'chapters': [], 'sheets': 0}
    p['today'].setdefault('chapters', [])
    session.permanent = True
    return p


def save_progress(p):
    session['progress'] = p
    session.modified = True


def touch(p):
    """Update the day streak when the visitor does something."""
    today = date.today()
    if p['last_active'] != today.isoformat():
        yesterday = (today - timedelta(days=1)).isoformat()
        p['streak'] = p['streak'] + 1 if p['last_active'] == yesterday else 1
        p['last_active'] = today.isoformat()


def summary(p):
    done = len(p['exercises_done'])
    return {'done': done, 'total': TOTAL_EXERCISES,
            'percent': round(100 * done / TOTAL_EXERCISES) if TOTAL_EXERCISES else 0}


def chapter_stats(p):
    done = set(p['exercises_done'])
    out = {}
    for c in CHAPTERS:
        n = len(c['exercises'])
        d = sum(1 for e in c['exercises'] if e['id'] in done)
        out[c['id']] = {'done': d, 'total': n, 'percent': round(100 * d / n) if n else 0,
                        'mastered': c['id'] in p['chapters_completed']}
    return out


@app.context_processor
def inject_globals():
    p = get_progress()
    return {
        'NAV': [('/', 'Accueil'), ('/chapters', 'Parcours'), ('/exercises', 'Exercices'),
                ('/formulas', 'Formules'), ('/exams', 'Examens'), ('/videos', 'Vidéos'),
                ('/progress', 'Progression')],
        'nav_progress': summary(p), 'streak': p['streak'], 'fmt_duration': fmt_duration,
        'LEVELS': LEVELS, 'DOMAIN_LABELS': DOMAIN_LABELS, 'MONKA_SITE': MONKA_SITE,
        'monka_search': lambda t: MONKA_SEARCH + t.replace(' ', '+'),
    }


# --------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------
LAYOUT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Révise les maths de Première spécialité : cours résumés, vidéos de Yvan Monka, 100 exercices corrigés, fiches de formules, examens blancs et suivi de progression. Gratuit.">
<meta name="theme-color" content="#4f46e5">
<title>{% block title %}Hermes · BAC Maths Hub{% endblock %}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🎓%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<style>
:root{
  --bg:#f4f5fb; --surface:#fff; --surface-2:#f1f3f9; --text:#1e2235; --muted:#667085;
  --primary:#4f46e5; --primary-2:#7c3aed; --ok:#10b981; --warn:#f59e0b; --info:#0ea5e9; --danger:#ef4444;
  --border:#e4e7f0; --shadow:0 4px 18px rgba(30,34,53,.07);
}
@media (prefers-color-scheme: dark){
  :root{ --bg:#0f1220; --surface:#181c2f; --surface-2:#20253b; --text:#e8eaf6; --muted:#9aa3c0;
         --primary:#818cf8; --primary-2:#a78bfa; --border:#2a3050; --shadow:0 4px 18px rgba(0,0,0,.35); }
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:80px}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}
a{color:var(--primary)}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;background:var(--surface);padding:8px 12px;border-radius:8px;z-index:100}
:focus-visible{outline:3px solid var(--primary);outline-offset:2px;border-radius:6px}

.topbar{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--surface) 88%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}
.topbar-inner{max-width:1100px;margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.brand{font-weight:800;letter-spacing:-.02em;text-decoration:none;color:var(--text);display:flex;gap:8px;align-items:center;white-space:nowrap}
.brand span{background:linear-gradient(135deg,var(--primary),var(--primary-2));-webkit-background-clip:text;background-clip:text;color:transparent}
.nav{display:flex;gap:2px;flex-wrap:wrap;flex:1}
.nav a{text-decoration:none;color:var(--muted);font-weight:600;font-size:.9rem;padding:7px 11px;border-radius:10px;transition:.15s}
.nav a:hover{background:var(--surface-2);color:var(--text)}
.nav a.active{background:var(--primary);color:#fff}
.chips{display:flex;gap:8px;align-items:center;font-size:.85rem;font-weight:600;color:var(--muted)}
.chip{background:var(--surface-2);border-radius:999px;padding:5px 12px;white-space:nowrap}

main{max-width:1100px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:clamp(1.6rem,3.5vw,2.3rem);letter-spacing:-.02em;line-height:1.2}
h2{font-size:1.3rem;margin-bottom:12px;letter-spacing:-.01em}
h3{font-size:1.05rem;margin-bottom:10px}
.lead{color:var(--muted);margin-top:6px;max-width:64ch}
.hero{background:linear-gradient(135deg,var(--primary),var(--primary-2));color:#fff;border-radius:22px;padding:34px;margin-bottom:26px;box-shadow:var(--shadow)}
.hero .lead{color:rgba(255,255,255,.9)}
.hero .bar{background:rgba(255,255,255,.25)}
.hero .btn{background:#fff;color:var(--primary)}
.hero .btn.ghost{background:rgba(255,255,255,.18);color:#fff}
.page-head{margin-bottom:24px}
.back{display:inline-block;margin-bottom:10px;text-decoration:none;font-weight:600;font-size:.92rem}
.section{margin-top:34px}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:20px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:8px}
.card.link{transition:transform .2s;text-decoration:none;color:inherit}
.card.link:hover{transform:translateY(-4px)}
.card .icon{font-size:1.7rem}
.card p{color:var(--muted);font-size:.93rem}
.grow{flex:1}
.meta{font-size:.85rem;color:var(--muted)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:24px;box-shadow:var(--shadow);margin-bottom:22px}
.domain-title{display:flex;align-items:center;gap:10px;margin:30px 0 14px}
.num{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--primary);color:#fff;font-weight:800;font-size:.9rem;flex-shrink:0}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;background:linear-gradient(135deg,var(--primary),var(--primary-2));color:#fff;border:0;border-radius:12px;padding:10px 20px;font:inherit;font-weight:700;font-size:.95rem;cursor:pointer;text-decoration:none;transition:.15s}
.btn:hover{transform:translateY(-1px);box-shadow:0 8px 18px rgba(79,70,229,.28)}
.btn.sm{padding:7px 14px;font-size:.85rem}
.btn.ghost{background:var(--surface-2);color:var(--text)}
.btn.ghost:hover{box-shadow:none;background:var(--border)}
.btn.ok,.btn.done{background:var(--ok)}
.btn.danger{background:var(--danger)}
.btn-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}

.bar{height:10px;background:var(--border);border-radius:999px;overflow:hidden}
.bar > i{display:block;height:100%;background:linear-gradient(90deg,var(--ok),#34d399);border-radius:999px;transition:width .4s}
.goal{background:var(--surface-2);border-radius:14px;padding:16px}
.goal b{display:block;margin-bottom:6px}
.goal .big{font-weight:800;font-size:1.3rem}

.pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.pill{border:1px solid var(--border);background:var(--surface);color:var(--text);padding:7px 14px;border-radius:999px;font:inherit;font-size:.88rem;font-weight:600;cursor:pointer}
.pill[aria-pressed=true]{background:var(--primary);color:#fff;border-color:var(--primary)}
input[type=search],textarea{width:100%;font:inherit;color:var(--text);background:var(--surface);border:2px solid var(--border);border-radius:12px;padding:10px 14px}
input[type=search]:focus,textarea:focus{border-color:var(--primary);outline:none}
textarea{min-height:90px;resize:vertical}

.tabs{position:sticky;top:57px;z-index:30;background:var(--bg);display:flex;gap:6px;flex-wrap:wrap;padding:8px 0 12px;margin-bottom:8px}
.tabs a{text-decoration:none;font-weight:700;font-size:.9rem;color:var(--text);background:var(--surface);border:1px solid var(--border);padding:8px 16px;border-radius:999px}
.tabs a:hover{border-color:var(--primary);color:var(--primary)}

.ex{background:var(--surface);border:1px solid var(--border);border-left:5px solid var(--primary);border-radius:14px;padding:16px 18px;margin-bottom:12px}
.ex.is-done{border-left-color:var(--ok)}
.ex-top{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;flex-wrap:wrap}
.tag{display:inline-block;font-size:.74rem;font-weight:700;background:var(--surface-2);color:var(--muted);border-radius:999px;padding:2px 10px;margin:0 6px 4px 0}
.tag.l1{background:#dcfce7;color:#166534}.tag.l2{background:#fef3c7;color:#92400e}.tag.l3{background:#fee2e2;color:#991b1b}
@media (prefers-color-scheme: dark){.tag.l1{background:#14532d;color:#bbf7d0}.tag.l2{background:#78350f;color:#fde68a}.tag.l3{background:#7f1d1d;color:#fecaca}}
details{margin-top:10px}
summary{cursor:pointer;font-weight:700;color:var(--primary);font-size:.93rem}
.solution{margin-top:8px;padding:12px 14px;background:var(--surface-2);border-radius:10px;white-space:pre-line}
.hint{margin-top:8px;padding:10px 14px;background:var(--surface-2);border-left:4px solid var(--warn);border-radius:8px;font-size:.93rem}

.course-item{border-left:4px solid var(--primary);padding:6px 0 6px 16px;margin-bottom:16px}
.course-item h3{margin-bottom:4px}
.formula{background:var(--surface-2);border-radius:10px;padding:10px 16px;margin:8px 0;overflow-x:auto}
.pitfall{background:#fff7ed;border-left:4px solid var(--warn);border-radius:8px;padding:10px 14px;margin:8px 0;font-size:.94rem}
@media (prefers-color-scheme: dark){.pitfall{background:#3b2a12}}
pre{background:#0f172a;color:#e2e8f0;border-radius:12px;padding:16px;overflow-x:auto;font-size:.88rem;line-height:1.5}
.video{position:relative;width:100%;aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:#000;box-shadow:var(--shadow)}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.thumb{display:block;position:relative;border-radius:14px;overflow:hidden;aspect-ratio:16/9;background:#111}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.thumb::after{content:'▶';position:absolute;inset:0;display:grid;place-items:center;font-size:2.4rem;color:#fff;background:rgba(0,0,0,.28);transition:.2s}
.thumb:hover::after{background:rgba(0,0,0,.1)}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.stat{font-size:2.3rem;font-weight:800;text-align:center;letter-spacing:-.02em}
.timer{font-size:2.2rem;font-weight:800;font-variant-numeric:tabular-nums;color:var(--primary)}
.timer.low{color:var(--danger)}
.exam-bar{position:sticky;top:57px;z-index:20;background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:12px 20px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px;box-shadow:var(--shadow)}
.empty{color:var(--muted);text-align:center;padding:30px}
.pager{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:30px}
footer{text-align:center;color:var(--muted);font-size:.85rem;padding:0 20px 36px;max-width:760px;margin:0 auto}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:var(--text);color:var(--bg);padding:10px 18px;border-radius:12px;font-weight:600;opacity:0;pointer-events:none;transition:.25s;z-index:99}
.toast.show{opacity:1}
.katex{font-size:1.06em}

@media (max-width:760px){
  .two-col{grid-template-columns:1fr}.hero{padding:24px}.chips{display:none}
  .exam-bar,.tabs{top:0}
}
@media print{
  .topbar,footer,.no-print,.btn-row,.toast,.tabs{display:none !important}
  body{background:#fff;color:#000}.panel,.formula{box-shadow:none;border-color:#ccc}
}
@media (prefers-reduced-motion: reduce){*{transition:none !important;scroll-behavior:auto !important}}
</style>
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<header class="topbar"><div class="topbar-inner">
  <a class="brand" href="/">🎓 <span>Hermes</span> BAC Maths</a>
  <nav class="nav" aria-label="Navigation principale">
    {% for href, label in NAV %}<a href="{{ href }}" {% if (active or '') == href %}class="active" aria-current="page"{% endif %}>{{ label }}</a>{% endfor %}
  </nav>
  <div class="chips">
    <span class="chip" title="Jours d'affilée avec de l'activité">🔥 {{ streak }} j</span>
    <span class="chip" id="nav-progress">{{ nav_progress.done }}/{{ nav_progress.total }} exercices</span>
  </div>
</div></header>
<main id="main">{% block content %}{% endblock %}</main>
<footer>
  Hermes · Maths de Première spécialité · Ta progression est enregistrée sur cet appareil.<br>
  Les vidéos et les cours PDF sont l'œuvre de <a href="{{ MONKA_SITE }}" target="_blank" rel="noopener">Yvan Monka</a> (maths-et-tiques.fr). Hermes n'est pas affilié à Yvan Monka.
</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<script>
const TOTAL = {{ nav_progress.total }};
function typeset(el){
  if(!window.renderMathInElement) return;
  renderMathInElement(el||document.body,{delimiters:[{left:'\\\\(',right:'\\\\)',display:false},{left:'$$',right:'$$',display:true}],throwOnError:false});
}
window.addEventListener('load',()=>typeset());
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toast._t);toast._t=setTimeout(()=>t.classList.remove('show'),2200)}
async function api(action, data={}){
  const r = await fetch('/api/progress',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,...data})});
  if(!r.ok) throw new Error('Erreur réseau');
  const j = await r.json();
  const n = document.getElementById('nav-progress');
  if(n) n.textContent = j.exercises_done.length + '/' + TOTAL + ' exercices';
  return j;
}
</script>
{% block scripts %}{% endblock %}
</body>
</html>"""

MACROS = """{% macro level_tag(l) %}<span class="tag l{{ l }}" title="{{ LEVELS[l][0] }}">{{ LEVELS[l][1] }} {{ LEVELS[l][0] }}</span>{% endmacro %}

{% macro progress_bar(percent) %}<div class="bar" role="progressbar" aria-valuenow="{{ percent }}" aria-valuemin="0" aria-valuemax="100"><i style="width:{{ percent }}%"></i></div>{% endmacro %}

{% macro exercise(ex, done, show_chapter=True) %}
<article class="ex {{ 'is-done' if ex.id in done else '' }}" id="exercise-{{ ex.id }}" data-id="{{ ex.id }}" data-chapter="{{ ex.chapter_id }}" data-level="{{ ex.level }}" data-text="{{ (ex.question ~ ' ' ~ ex.chapter)|lower|striptags }}">
  <div class="ex-top">
    <div style="flex:1;min-width:220px">
      {{ level_tag(ex.level) }}{% if show_chapter %}<a class="tag" href="/chapter/{{ ex.chapter_id }}" style="text-decoration:none">{{ ex.chapter }}</a>{% endif %}<br>
      <strong>Exercice {{ ex.num }}.</strong> {{ ex.question|safe }}
    </div>
    <button class="btn sm {{ 'done' if ex.id in done else 'ghost' }}" data-check="{{ ex.id }}" aria-pressed="{{ 'true' if ex.id in done else 'false' }}">{{ '✓ Fait' if ex.id in done else 'Marquer comme fait' }}</button>
  </div>
  {% if ex.hint %}<details><summary>💡 Indice</summary><div class="hint">{{ ex.hint|safe }}</div></details>{% endif %}
  <details><summary>Voir la solution</summary><div class="solution">{{ ex.solution|safe }}</div></details>
</article>
{% endmacro %}

{% macro check_script() %}
<script>
document.querySelectorAll('[data-check]').forEach(b=>b.addEventListener('click',async()=>{
  const id = b.dataset.check;
  const r = await api('exercise_toggle',{id});
  const on = r.exercises_done.includes(id);
  b.className = 'btn sm ' + (on ? 'done' : 'ghost');
  b.textContent = on ? '✓ Fait' : 'Marquer comme fait';
  b.setAttribute('aria-pressed', on);
  document.getElementById('exercise-'+id).classList.toggle('is-done', on);
  const upd = document.getElementById('chapter-done');
  if(upd){ const n = r.exercises_done.filter(x=>x.startsWith(upd.dataset.prefix)).length;
           upd.textContent = n + '/' + upd.dataset.total; document.getElementById('chapter-bar').style.width = Math.round(100*n/upd.dataset.total)+'%'; }
  toast(on ? 'Bien joué ! 💪' : 'Exercice remis à faire');
}));
</script>
{% endmacro %}"""

HOME = """{% extends 'layout.html' %}
{% from 'macros.html' import progress_bar with context %}
{% block content %}
<section class="hero">
  <h1>Prépare ton BAC de maths,<br>un chapitre à la fois.</h1>
  <p class="lead">{{ total }} exercices corrigés, 10 chapitres du programme de Première spécialité, les vidéos de cours de Yvan Monka, des fiches de formules et des examens blancs.</p>
  <div style="margin:22px 0 8px;max-width:440px">
    <div class="meta" style="color:rgba(255,255,255,.88);margin-bottom:6px">{{ s.done }} / {{ s.total }} exercices terminés ({{ s.percent }} %)</div>
    {{ progress_bar(s.percent) }}
  </div>
  <div class="btn-row">
    <a class="btn" href="/chapter/{{ next_chapter.id }}">{{ 'Continuer' if stats[next_chapter.id].done else 'Commencer' }} : {{ next_chapter.title }} →</a>
    <a class="btn ghost" href="/chapters">Voir tout le parcours</a>
  </div>
</section>

<div class="panel">
  <h2>🎯 Objectifs du jour</h2>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
    {% for g in goals %}
    <div class="goal">
      <b>{{ '✅' if g.value >= g.target else '⬜' }} {{ g.label }}</b>
      <div class="big" style="color:{{ g.color }}">{{ [g.value, g.target]|min }}/{{ g.target }}</div>
      <div class="bar" style="margin-top:8px"><i style="width:{{ (100 * [g.value, g.target]|min / g.target)|round }}%;background:{{ g.color }}"></i></div>
    </div>
    {% endfor %}
  </div>
</div>

<div class="section">
  <h2>Le programme en un coup d'œil</h2>
  {% for dkey, dlabel, dicon in domains %}
  <div class="domain-title"><span style="font-size:1.4rem">{{ dicon }}</span><h3 style="margin:0">{{ dlabel }}</h3></div>
  <div class="grid">
    {% for c in chapters if c.domain == dkey %}
    <a class="card link" href="/chapter/{{ c.id }}">
      <div style="display:flex;gap:10px;align-items:center"><span class="num">{{ c.num }}</span><strong>{{ c.title }}</strong></div>
      <p class="grow">{{ c.tagline }}</p>
      {{ progress_bar(stats[c.id].percent) }}
      <div class="meta">{{ stats[c.id].done }}/{{ stats[c.id].total }} exercices {{ '· ✅ maîtrisé' if stats[c.id].mastered }}</div>
    </a>
    {% endfor %}
  </div>
  {% endfor %}
</div>

<div class="section grid">
  <div class="card"><div class="icon">🎬</div><h3 style="margin:0">Cours en vidéo</h3><p class="grow">Un cours complet de Yvan Monka par chapitre, avec les fiches PDF correspondantes.</p><a class="btn sm" href="/videos">Voir les vidéos</a></div>
  <div class="card"><div class="icon">📝</div><h3 style="margin:0">Fiches de formules</h3><p class="grow">Choisis tes chapitres, génère ta fiche, imprime-la ou enregistre-la en PDF.</p><a class="btn sm" href="/formulas">Créer une fiche</a></div>
  <div class="card"><div class="icon">⏱️</div><h3 style="margin:0">Examens blancs</h3><p class="grow">Contrôle, BAC blanc ou quiz rapide — avec correction et auto-évaluation.</p><a class="btn sm" href="/exams">Passer un examen</a></div>
</div>
{% endblock %}"""

CHAPTERS_PAGE = """{% extends 'layout.html' %}
{% from 'macros.html' import progress_bar with context %}
{% block title %}Parcours · Hermes BAC Maths{% endblock %}
{% block content %}
<div class="page-head"><h1>🗺️ Ton parcours de Première</h1><p class="lead">Les 10 chapitres du programme de spécialité, dans l'ordre conseillé. Chaque chapitre regroupe cours, vidéo, fiche PDF et exercices.</p></div>
{% for dkey, dlabel, dicon in domains %}
<div class="domain-title"><span style="font-size:1.4rem">{{ dicon }}</span><h2 style="margin:0">{{ dlabel }}</h2></div>
<div class="grid">
  {% for c in chapters if c.domain == dkey %}
  <a class="card link" href="/chapter/{{ c.id }}">
    <div style="display:flex;gap:10px;align-items:center"><span class="num">{{ c.num }}</span><strong>{{ c.title }}</strong></div>
    <p class="grow">{{ c.tagline }}</p>
    <div class="meta">🎬 1 vidéo · 📄 {{ c.pdfs|length }} fiche{{ 's' if c.pdfs|length > 1 }} · ✏️ {{ c.exercises|length }} exercices</div>
    {{ progress_bar(stats[c.id].percent) }}
    <div class="meta">{{ stats[c.id].done }}/{{ stats[c.id].total }} faits {{ '· ✅ maîtrisé' if stats[c.id].mastered }}</div>
  </a>
  {% endfor %}
</div>
{% endfor %}
{% endblock %}"""

CHAPTER_PAGE = """{% extends 'layout.html' %}
{% from 'macros.html' import exercise, check_script, progress_bar with context %}
{% block title %}{{ c.title }} · Hermes BAC Maths{% endblock %}
{% block content %}
<a class="back" href="/chapters">← Tous les chapitres</a>
<div class="page-head">
  <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap"><span class="num" style="width:40px;height:40px;font-size:1.1rem">{{ c.num }}</span><h1>{{ c.icon }} {{ c.title }}</h1></div>
  <p class="lead">{{ c.tagline }}</p>
  <div style="max-width:420px;margin-top:14px">
    <div class="meta" style="margin-bottom:4px"><span id="chapter-done" data-prefix="{{ prefix }}" data-total="{{ c.exercises|length }}">{{ st.done }}/{{ st.total }}</span> exercices faits</div>
    <div class="bar"><i id="chapter-bar" style="width:{{ st.percent }}%"></i></div>
  </div>
</div>

<nav class="tabs" aria-label="Sections du chapitre">
  <a href="#video">🎬 Vidéo</a><a href="#cours">📖 Cours</a><a href="#formules">🧮 Formules</a><a href="#pieges">⚠️ Pièges</a><a href="#exercices">✏️ Exercices</a>
</nav>

<section id="video" class="section" style="margin-top:8px">
  <h2>🎬 Le cours en vidéo</h2>
  <div class="two-col" style="grid-template-columns:1.6fr 1fr;align-items:start">
    <div>
      <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{{ c.video.id }}" title="{{ c.video.title }}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
      <p class="meta" style="margin-top:8px">{{ c.video.title }} — Yvan Monka</p>
    </div>
    <div class="panel" style="margin:0">
      <h3>Pour aller plus loin</h3>
      <div class="btn-row" style="flex-direction:column;align-items:stretch">
        <a class="btn sm" href="https://youtu.be/{{ c.video.id }}" target="_blank" rel="noopener">▶ Ouvrir sur YouTube</a>
        {% for p in c.pdfs %}<a class="btn sm ghost" href="{{ p.url }}" target="_blank" rel="noopener">📄 {{ p.label }}</a>{% endfor %}
        <a class="btn sm ghost" href="{{ monka_search(c.title + ' première') }}" target="_blank" rel="noopener">🔎 Exercices corrigés en vidéo</a>
      </div>
    </div>
  </div>
</section>

<section id="cours" class="section">
  <h2>📖 Cours : l'essentiel</h2>
  <div class="panel">
    {% for title, text in c.cours %}
    <div class="course-item"><h3>{{ title|safe }}</h3><div>{{ text|safe }}</div></div>
    {% endfor %}
  </div>
  {% if c.code %}<h3>🐍 {{ c.code[0] }}</h3><pre>{{ c.code[1] }}</pre>{% endif %}
</section>

<section id="formules" class="section">
  <h2>🧮 Formules à connaître</h2>
  {% for f in c.formulas %}<div class="formula">{{ f|safe }}</div>{% endfor %}
</section>

<section id="pieges" class="section">
  <h2>⚠️ Pièges classiques</h2>
  {% for t in c.pitfalls %}<div class="pitfall">{{ t|safe }}</div>{% endfor %}
</section>

<section id="exercices" class="section">
  <h2>✏️ Exercices ({{ c.exercises|length }})</h2>
  <div class="pills" role="group" aria-label="Filtrer par niveau">
    <button class="pill" data-level="all" aria-pressed="true">Tous</button>
    {% for l in (1, 2, 3) %}<button class="pill" data-level="{{ l }}" aria-pressed="false">{{ LEVELS[l][1] }} {{ LEVELS[l][0] }}</button>{% endfor %}
  </div>
  <div id="list">{% for ex in c.exercises %}{{ exercise(ex, done, False) }}{% endfor %}</div>
  <div class="btn-row no-print">
    <a class="btn" href="/quiz/{{ c.id }}">⏱️ Mini-test de 5 questions</a>
    <button class="btn sm {{ 'done' if st.mastered else 'ghost' }}" id="master" aria-pressed="{{ 'true' if st.mastered else 'false' }}">{{ '✓ Chapitre maîtrisé' if st.mastered else 'Marquer le chapitre comme maîtrisé' }}</button>
  </div>
</section>

<div class="pager no-print">
  {% if prev %}<a class="btn ghost" href="/chapter/{{ prev.id }}">← {{ prev.num }}. {{ prev.title }}</a>{% else %}<span></span>{% endif %}
  {% if nxt %}<a class="btn" href="/chapter/{{ nxt.id }}">{{ nxt.num }}. {{ nxt.title }} →</a>{% endif %}
</div>
{% endblock %}
{% block scripts %}
{{ check_script() }}
<script>
document.querySelectorAll('.pill[data-level]').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.pill[data-level]').forEach(x=>x.setAttribute('aria-pressed',x===b));
  document.querySelectorAll('#list .ex').forEach(el=>{ el.hidden = !(b.dataset.level==='all' || el.dataset.level===b.dataset.level) });
}));
document.getElementById('master').addEventListener('click',async e=>{
  const r = await api('chapter_toggle',{chapter:'{{ c.id }}'});
  const on = r.chapters_completed.includes('{{ c.id }}');
  e.target.className = 'btn sm ' + (on ? 'done' : 'ghost');
  e.target.textContent = on ? '✓ Chapitre maîtrisé' : 'Marquer le chapitre comme maîtrisé';
  toast(on ? 'Chapitre maîtrisé 🎉' : 'Chapitre remis à réviser');
});
</script>
{% endblock %}"""

EXERCISES_PAGE = """{% extends 'layout.html' %}
{% from 'macros.html' import exercise, check_script with context %}
{% block title %}Exercices · Hermes BAC Maths{% endblock %}
{% block content %}
<div class="page-head"><h1>✏️ Banque d'exercices</h1><p class="lead">{{ exercises|length }} exercices corrigés, classés par chapitre et par niveau. Cherche d'abord, ouvre la solution ensuite.</p></div>
<div class="pills" role="group" aria-label="Filtrer par chapitre">
  <button class="pill" data-chapter="all" aria-pressed="true">Tous les chapitres</button>
  {% for c in chapters %}<button class="pill" data-chapter="{{ c.id }}" aria-pressed="false">{{ c.num }}. {{ c.title }}</button>{% endfor %}
</div>
<div class="pills" role="group" aria-label="Filtrer par niveau">
  <button class="pill" data-lvl="all" aria-pressed="true">Tous niveaux</button>
  {% for l in (1, 2, 3) %}<button class="pill" data-lvl="{{ l }}" aria-pressed="false">{{ LEVELS[l][1] }} {{ LEVELS[l][0] }}</button>{% endfor %}
  <button class="pill" data-lvl="todo" aria-pressed="false">À faire seulement</button>
</div>
<input type="search" id="q" placeholder="Rechercher (ex : tangente, binomiale, discriminant…)" aria-label="Rechercher" style="margin-bottom:18px">
<p class="meta" id="count" style="margin-bottom:10px"></p>
<div id="list">{% for ex in exercises %}{{ exercise(ex, done) }}{% endfor %}</div>
<p class="empty" id="none" hidden>Aucun exercice ne correspond. 🤔</p>
{% endblock %}
{% block scripts %}
{{ check_script() }}
<script>
let fc='all', fl='all';
function apply(){
  const q=document.getElementById('q').value.trim().toLowerCase();let n=0;
  document.querySelectorAll('#list .ex').forEach(el=>{
    const okC = fc==='all' || el.dataset.chapter===fc;
    const okL = fl==='all' || (fl==='todo' ? !el.classList.contains('is-done') : el.dataset.level===fl);
    const ok = okC && okL && (!q || el.dataset.text.includes(q));
    el.hidden = !ok; if(ok) n++;
  });
  document.getElementById('none').hidden = n>0;
  document.getElementById('count').textContent = n + ' exercice' + (n>1?'s':'') + ' affiché' + (n>1?'s':'');
}
document.querySelectorAll('[data-chapter].pill').forEach(b=>b.addEventListener('click',()=>{
  fc=b.dataset.chapter; document.querySelectorAll('[data-chapter].pill').forEach(x=>x.setAttribute('aria-pressed',x===b)); apply();
}));
document.querySelectorAll('[data-lvl]').forEach(b=>b.addEventListener('click',()=>{
  fl=b.dataset.lvl; document.querySelectorAll('[data-lvl]').forEach(x=>x.setAttribute('aria-pressed',x===b)); apply();
}));
document.getElementById('q').addEventListener('input',apply);
document.addEventListener('click',e=>{ if(e.target.matches('[data-check]')) setTimeout(apply,50) });
const p0=new URLSearchParams(location.search);
if(p0.get('f')==='todo'){ document.querySelector('[data-lvl="todo"]').click(); }
const c0=p0.get('c'); if(c0){ const b=document.querySelector('.pill[data-chapter="'+c0+'"]'); if(b) b.click(); }
apply();
</script>
{% endblock %}"""

FORMULAS_PAGE = """{% extends 'layout.html' %}
{% block title %}Fiches de formules · Hermes BAC Maths{% endblock %}
{% block content %}
<div class="page-head no-print"><h1>📝 Fiches de révision</h1><p class="lead">Sélectionne tes chapitres, génère ta fiche, puis imprime-la ou enregistre-la en PDF.</p></div>
<div class="panel no-print">
  <h3>Chapitres à inclure</h3>
  <div class="pills">
    {% for c in chapters %}<label class="pill" style="display:inline-flex;gap:8px;align-items:center"><input type="checkbox" name="chap" value="{{ c.id }}" checked> {{ c.num }}. {{ c.title }}</label>{% endfor %}
  </div>
  <div class="btn-row"><button class="btn" id="gen">🚀 Générer ma fiche</button></div>
</div>
<div class="panel" id="sheet-panel">
  <h2 id="sheet-title">Ta fiche apparaîtra ici</h2>
  <div id="sheet"><p class="empty">Choisis tes chapitres puis clique sur « Générer ma fiche ».</p></div>
  <div class="btn-row no-print" id="sheet-actions" hidden>
    <button class="btn ghost" onclick="window.print()">🖨️ Imprimer / PDF</button>
    <button class="btn ghost" id="copy">📋 Copier le texte (LaTeX)</button>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const CH = {{ chapters_json|safe }};
function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function selected(){return [...document.querySelectorAll('input[name=chap]:checked')].map(x=>x.value)}
document.getElementById('gen').addEventListener('click',async()=>{
  const sel=selected();
  if(!sel.length){toast('Sélectionne au moins un chapitre');return}
  document.getElementById('sheet-title').textContent='Fiche de formules — Maths Première spécialité';
  const html = sel.map(id=>'<h3 style="margin-top:16px">'+esc(CH[id].num+'. '+CH[id].title)+'</h3>'+CH[id].formulas.map(f=>'<div class="formula">'+esc(f)+'</div>').join('')).join('');
  const box=document.getElementById('sheet'); box.innerHTML=html; typeset(box);
  document.getElementById('sheet-actions').hidden=false;
  try{await api('formula_generated')}catch(e){}
  toast('Fiche générée ✨');
});
document.getElementById('copy').addEventListener('click',async()=>{
  const txt=selected().map(id=>(CH[id].num+'. '+CH[id].title).toUpperCase()+'\\n'+CH[id].formulas.map(f=>'• '+f).join('\\n')).join('\\n\\n');
  try{await navigator.clipboard.writeText(txt);toast('Copié dans le presse-papiers')}catch(e){toast('Copie impossible sur ce navigateur')}
});
</script>
{% endblock %}"""

VIDEOS_PAGE = """{% extends 'layout.html' %}
{% block title %}Vidéos · Hermes BAC Maths{% endblock %}
{% block content %}
<div class="page-head"><h1>🎬 Cours en vidéo — Yvan Monka</h1>
<p class="lead">Un cours complet par chapitre, présenté par Yvan Monka (professeur de maths, auteur de maths-et-tiques.fr). Clique sur une vignette pour ouvrir la vidéo, ou va sur la page du chapitre pour la regarder avec le cours et les exercices.</p></div>
<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr))">
{% for c in chapters %}
  <div class="card">
    <a class="thumb" href="https://youtu.be/{{ c.video.id }}" target="_blank" rel="noopener" aria-label="Regarder : {{ c.video.title }}"><img loading="lazy" alt="" src="https://i.ytimg.com/vi/{{ c.video.id }}/mqdefault.jpg"></a>
    <div style="display:flex;gap:8px;align-items:center"><span class="num">{{ c.num }}</span><strong>{{ c.title }}</strong></div>
    <p class="meta grow">{{ c.video.title }}</p>
    <div class="btn-row">
      <a class="btn sm" href="/chapter/{{ c.id }}">Voir le chapitre</a>
      {% for p in c.pdfs %}<a class="btn sm ghost" href="{{ p.url }}" target="_blank" rel="noopener" title="{{ p.label }}">📄 PDF{{ ' ' ~ loop.index if c.pdfs|length > 1 }}</a>{% endfor %}
    </div>
  </div>
{% endfor %}
</div>
<div class="panel" style="margin-top:28px">
  <h3>Toutes les ressources de Yvan Monka</h3>
  <p class="meta">Cours, exercices corrigés et vidéos sur son site et sa chaîne YouTube.</p>
  <div class="btn-row"><a class="btn" href="{{ MONKA_SITE }}" target="_blank" rel="noopener">maths-et-tiques.fr — Première</a><a class="btn ghost" href="{{ monka_search('Première spécialité maths') }}" target="_blank" rel="noopener">Chercher sur YouTube</a></div>
</div>
{% endblock %}"""

EXAMS_PAGE = """{% extends 'layout.html' %}
{% block title %}Examens · Hermes BAC Maths{% endblock %}
{% block content %}
<div class="page-head"><h1>⏱️ Examens blancs</h1><p class="lead">Les sujets sont tirés au hasard dans la banque d'exercices. Une fois ta copie rendue, la correction s'affiche et tu peux t'auto-évaluer.</p></div>
<div class="grid">
{% for eid, e in exams.items() %}
  <div class="card">
    <h3 style="margin:0">{{ e.name }}</h3>
    <p>{{ e.blurb }}</p>
    <p class="meta grow">{{ fmt_duration(e.duration) }} · {{ e.n }} question{{ 's' if e.n > 1 }} · {{ e.total }} points</p>
    <a class="btn" href="/exam/{{ eid }}">Commencer</a>
  </div>
{% endfor %}
</div>
<div class="section"><h2>Mini-tests par chapitre</h2><p class="meta" style="margin-bottom:12px">5 questions, 15 minutes : idéal pour tester un chapitre fraîchement révisé.</p>
<div class="pills">{% for c in chapters %}<a class="pill" href="/quiz/{{ c.id }}" style="text-decoration:none">{{ c.num }}. {{ c.title }}</a>{% endfor %}</div></div>
{% endblock %}"""

EXAM_PAGE = """{% extends 'layout.html' %}
{% block title %}{{ exam.name }} · Hermes BAC Maths{% endblock %}
{% block content %}
<div class="exam-bar">
  <div><strong>{{ exam.name }}</strong><div class="meta">{{ questions|length }} question{{ 's' if questions|length > 1 }} · {{ total }} points</div></div>
  <div class="timer" id="timer" role="timer">--:--:--</div>
  <div class="btn-row" style="margin:0"><button class="btn ok" id="submit">Rendre ma copie</button><a class="btn ghost" href="/exams" id="quit">Quitter</a></div>
</div>
<div class="panel" id="score" hidden><h2 style="margin:0">Ton score : <span id="score-val">0</span> / {{ total }}</h2><p class="meta">Coche « Je l'avais juste » pour chaque question réussie.</p></div>
{% for q in questions %}
<section class="panel">
  <span class="tag">{{ q.chapter }}</span><span class="tag l{{ q.level }}">{{ LEVELS[q.level][1] }}</span><span class="tag">{{ q.points }} pt{{ 's' if q.points > 1 }}</span>
  <h3>Question {{ loop.index }}</h3>
  <p>{{ q.question|safe }}</p>
  <textarea placeholder="Ta réponse (brouillon)…" aria-label="Réponse à la question {{ loop.index }}"></textarea>
  <div class="correction" hidden style="margin-top:12px">
    <div class="solution"><strong>Correction :</strong>
{{ q.solution|safe }}</div>
    <label style="display:inline-flex;gap:8px;align-items:center;margin-top:10px;font-weight:600"><input type="checkbox" class="got" data-pts="{{ q.points }}"> Je l'avais juste</label>
    <a class="btn sm ghost" style="margin-left:10px" href="/chapter/{{ q.chapter_id }}#cours">Revoir le cours</a>
  </div>
</section>
{% endfor %}
{% endblock %}
{% block scripts %}
<script>
let left = {{ exam.duration }} * 60, finished = false;
const el = document.getElementById('timer');
function render(){
  const h=Math.floor(left/3600), m=Math.floor(left%3600/60), s=left%60;
  el.textContent=[h,m,s].map(n=>String(n).padStart(2,'0')).join(':');
  el.classList.toggle('low', left <= 300);
}
function score(){ let t=0; document.querySelectorAll('.got:checked').forEach(c=>t+=+c.dataset.pts); document.getElementById('score-val').textContent=t; }
function finish(auto){
  if(finished) return; finished = true; clearInterval(tick);
  document.querySelectorAll('.correction').forEach(s=>s.hidden=false);
  document.getElementById('score').hidden=false;
  document.querySelectorAll('.got').forEach(c=>c.addEventListener('change',score));
  document.getElementById('submit').disabled = true;
  document.getElementById('quit').textContent = 'Retour aux examens';
  typeset();
  toast(auto ? 'Temps écoulé — voici la correction' : 'Copie rendue — compare avec la correction');
  api('exam_taken').catch(()=>{});
  window.scrollTo({top:0,behavior:'smooth'});
}
const tick = setInterval(()=>{ left--; render(); if(left<=0){ left=0; render(); finish(true) } },1000);
render();
document.getElementById('submit').addEventListener('click',()=>{ if(confirm('Rendre ta copie maintenant ?')) finish(false) });
window.addEventListener('beforeunload',e=>{ if(!finished){ e.preventDefault(); e.returnValue='' } });
</script>
{% endblock %}"""

PROGRESS_PAGE = """{% extends 'layout.html' %}
{% from 'macros.html' import progress_bar with context %}
{% block title %}Progression · Hermes BAC Maths{% endblock %}
{% block content %}
<div class="page-head"><h1>📊 Ta progression</h1><p class="lead">Série actuelle : <strong>🔥 {{ p.streak }} jour{{ 's' if p.streak != 1 }}</strong></p></div>
<div class="grid" style="margin-bottom:22px">
  <div class="card"><h3 style="margin:0">Exercices</h3><div class="stat" style="color:var(--primary)">{{ s.done }}/{{ s.total }}</div>{{ progress_bar(s.percent) }}<p class="meta" style="text-align:center">{{ s.percent }} % terminé</p></div>
  <div class="card"><h3 style="margin:0">Chapitres maîtrisés</h3><div class="stat" style="color:var(--ok)">{{ p.chapters_completed|length }}/{{ chapters|length }}</div>{{ progress_bar((100 * p.chapters_completed|length / chapters|length)|round) }}</div>
  <div class="card"><h3 style="margin:0">Examens rendus</h3><div class="stat" style="color:var(--warn)">{{ p.exams_taken }}</div><p class="meta" style="text-align:center">copies rendues</p></div>
  <div class="card"><h3 style="margin:0">Fiches générées</h3><div class="stat" style="color:var(--info)">{{ p.formula_sheets_generated }}</div><p class="meta" style="text-align:center">fiches de formules</p></div>
</div>
<div class="panel">
  <h2>Par niveau de difficulté</h2>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
    {% for l in (1, 2, 3) %}<div class="goal"><b>{{ LEVELS[l][1] }} {{ LEVELS[l][0] }}</b><div class="big">{{ by_level[l].done }}/{{ by_level[l].total }}</div>{{ progress_bar(by_level[l].percent) }}</div>{% endfor %}
  </div>
</div>
<div class="panel">
  <h2>Détail par chapitre</h2>
  {% for c in chapters %}
  <div style="margin:14px 0">
    <div style="display:flex;justify-content:space-between;gap:10px"><a href="/chapter/{{ c.id }}" style="font-weight:700;text-decoration:none"><span class="num" style="width:24px;height:24px;font-size:.75rem;margin-right:6px">{{ c.num }}</span>{{ c.title }} {{ '✅' if stats[c.id].mastered }}</a><span class="meta">{{ stats[c.id].done }}/{{ stats[c.id].total }}</span></div>
    <div style="margin-top:6px">{{ progress_bar(stats[c.id].percent) }}</div>
  </div>
  {% endfor %}
  <div class="btn-row" style="margin-top:20px"><a class="btn sm" href="/exercises?f=todo">Continuer mes exercices</a><button class="btn sm danger" id="reset">Réinitialiser ma progression</button></div>
</div>
{% endblock %}
{% block scripts %}
<script>
document.getElementById('reset').addEventListener('click',async()=>{
  if(!confirm('Effacer toute ta progression ? Cette action est définitive.')) return;
  await fetch('/api/reset',{method:'POST'}); location.reload();
});
</script>
{% endblock %}"""

NOT_FOUND = """{% extends 'layout.html' %}
{% block content %}<div class="empty" style="padding:70px 0"><h1>404</h1><p class="lead" style="margin:10px auto 20px">Cette page n'existe pas (ou plus).</p><a class="btn" href="/">Retour à l'accueil</a></div>{% endblock %}"""

app.jinja_loader = DictLoader({
    'layout.html': LAYOUT, 'macros.html': MACROS, 'home.html': HOME, 'chapters.html': CHAPTERS_PAGE,
    'chapter.html': CHAPTER_PAGE, 'exercises.html': EXERCISES_PAGE, 'formulas.html': FORMULAS_PAGE,
    'videos.html': VIDEOS_PAGE, 'exams.html': EXAMS_PAGE, 'exam.html': EXAM_PAGE,
    'progress.html': PROGRESS_PAGE, '404.html': NOT_FOUND,
})


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
def make_question(ex, points):
    return {**ex, 'points': points}


def build_exam(tpl):
    """Draw a random set of questions for an exam template."""
    questions, used = [], set()
    if tpl['parts']:
        for cid, levels, pts in tpl['parts']:
            pool = [e for e in CHAPTERS_BY_ID[cid]['exercises'] if e['level'] in levels and e['id'] not in used]
            ex = random.choice(pool)
            used.add(ex['id'])
            questions.append(make_question(ex, pts))
    else:
        pool = [e for e in EXERCISES_BY_ID.values() if e['level'] <= 2]
        questions = [make_question(e, 1) for e in random.sample(pool, 10)]
    return questions


def exam_card_info():
    out = {}
    for eid, t in EXAM_TEMPLATES.items():
        n = len(t['parts']) if t['parts'] else 10
        total = sum(p[2] for p in t['parts']) if t['parts'] else 10
        out[eid] = {**t, 'n': n, 'total': total}
    return out


@app.route('/')
def home():
    p = get_progress()
    stats = chapter_stats(p)
    next_chapter = next((c for c in CHAPTERS if stats[c['id']]['percent'] < 100), CHAPTERS[0])
    t = p['today']
    goals = [
        {'label': 'Faire 3 exercices', 'value': t['exercises'], 'target': 3, 'color': '#10b981'},
        {'label': 'Réviser 1 chapitre', 'value': len(t['chapters']), 'target': 1, 'color': '#f59e0b'},
        {'label': 'Générer 1 fiche', 'value': t['sheets'], 'target': 1, 'color': '#0ea5e9'},
    ]
    return render_template('home.html', active='/', chapters=CHAPTERS, domains=DOMAINS, stats=stats,
                           s=summary(p), goals=goals, next_chapter=next_chapter, total=TOTAL_EXERCISES)


@app.route('/chapters')
def chapters():
    p = get_progress()
    return render_template('chapters.html', active='/chapters', chapters=CHAPTERS, domains=DOMAINS,
                           stats=chapter_stats(p))


@app.route('/chapter/<chapter_id>')
def chapter(chapter_id):
    c = CHAPTERS_BY_ID.get(chapter_id)
    if not c:
        abort(404)
    p = get_progress()
    if chapter_id not in p['today']['chapters']:  # visiting a chapter counts as revising it today
        p['today']['chapters'].append(chapter_id)
        touch(p)
        save_progress(p)
    i = c['num'] - 1
    return render_template('chapter.html', active='/chapters', c=c, st=chapter_stats(p)[chapter_id],
                           done=set(p['exercises_done']), prefix=c['exercises'][0]['id'][:2],
                           prev=CHAPTERS[i - 1] if i > 0 else None,
                           nxt=CHAPTERS[i + 1] if i + 1 < len(CHAPTERS) else None)


@app.route('/topic/<chapter_id>')  # old URL kept alive
def legacy_topic(chapter_id):
    return chapter(chapter_id) if chapter_id in CHAPTERS_BY_ID else abort(404)


@app.route('/exercises')
def exercises():
    p = get_progress()
    return render_template('exercises.html', active='/exercises', exercises=list(EXERCISES_BY_ID.values()),
                           chapters=CHAPTERS, done=set(p['exercises_done']))


@app.route('/formulas')
def formulas():
    data = {c['id']: {'num': c['num'], 'title': c['title'], 'formulas': c['formulas']} for c in CHAPTERS}
    return render_template('formulas.html', active='/formulas', chapters=CHAPTERS,
                           chapters_json=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))


@app.route('/videos')
def videos():
    return render_template('videos.html', active='/videos', chapters=CHAPTERS)


@app.route('/exams')
def exams():
    return render_template('exams.html', active='/exams', exams=exam_card_info(), chapters=CHAPTERS)


@app.route('/exam/<exam_id>')
def exam(exam_id):
    tpl = EXAM_TEMPLATES.get(exam_id)
    if not tpl:
        abort(404)
    qs = build_exam(tpl)
    return render_template('exam.html', active='/exams', exam=tpl, questions=qs,
                           total=sum(q['points'] for q in qs))


@app.route('/quiz/<chapter_id>')
def quiz(chapter_id):
    c = CHAPTERS_BY_ID.get(chapter_id)
    if not c:
        abort(404)
    qs = [make_question(e, 1) for e in random.sample(c['exercises'], min(5, len(c['exercises'])))]
    tpl = {'name': f"Mini-test · {c['title']}", 'duration': 15}
    return render_template('exam.html', active='/exams', exam=tpl, questions=qs, total=len(qs))


@app.route('/progress')
def progress():
    p = get_progress()
    done = set(p['exercises_done'])
    by_level = {}
    for l in (1, 2, 3):
        ids = [e['id'] for e in EXERCISES_BY_ID.values() if e['level'] == l]
        d = sum(1 for i in ids if i in done)
        by_level[l] = {'done': d, 'total': len(ids), 'percent': round(100 * d / len(ids)) if ids else 0}
    return render_template('progress.html', active='/progress', p=p, s=summary(p), chapters=CHAPTERS,
                           stats=chapter_stats(p), by_level=by_level)


@app.route('/api/progress', methods=['GET', 'POST'])
def api_progress():
    p = get_progress()
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        action = data.get('action')
        if action == 'exercise_toggle':
            ex_id = data.get('id')
            if ex_id not in EXERCISES_BY_ID:
                return jsonify(error='unknown exercise'), 400
            if ex_id in p['exercises_done']:
                p['exercises_done'].remove(ex_id)
                p['today']['exercises'] = max(0, p['today']['exercises'] - 1)
            else:
                p['exercises_done'].append(ex_id)
                p['today']['exercises'] += 1
                touch(p)
        elif action == 'chapter_toggle':
            cid = data.get('chapter')
            if cid not in CHAPTERS_BY_ID:
                return jsonify(error='unknown chapter'), 400
            if cid in p['chapters_completed']:
                p['chapters_completed'].remove(cid)
            else:
                p['chapters_completed'].append(cid)
                touch(p)
        elif action == 'exam_taken':
            p['exams_taken'] += 1
            touch(p)
        elif action == 'formula_generated':
            p['formula_sheets_generated'] += 1
            p['today']['sheets'] += 1
            touch(p)
        else:
            return jsonify(error='unknown action'), 400
        save_progress(p)
    return jsonify(p)


@app.route('/api/reset', methods=['POST'])
def api_reset():
    session.pop('progress', None)
    return jsonify(status='reset')


@app.route('/healthz')
def healthz():
    return 'ok'


@app.errorhandler(404)
def not_found(_e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=DEBUG, host='0.0.0.0', port=port)
