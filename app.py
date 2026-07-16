from flask import Flask, request, jsonify, session
import json
import random
import os
from datetime import datetime

app = Flask(__name__)
# Secret key signs the session cookie. Set a real SECRET_KEY env var in production
# (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-insecure-key-change-me')

# Default/blank progress shape. Each visitor gets their own copy stored in their
# signed session cookie, instead of everyone sharing one global dict.
DEFAULT_PROGRESS = {
    'topics_completed': [],
    'exercises_solved': 0,
    'exams_taken': 0,
    'formula_sheets_generated': 0
}

def get_progress():
    """Load the current visitor's progress from their session cookie."""
    if 'progress' not in session:
        session['progress'] = json.loads(json.dumps(DEFAULT_PROGRESS))  # deep copy
    return session['progress']

def save_progress(progress):
    """Persist changes back to the visitor's session cookie."""
    session['progress'] = progress
    session.modified = True

# Math topics for Première BAC
MATH_TOPICS = {
    'fonctions': {
        'title': 'Fonctions',
        'description': 'Fonctions affines, carrées, inverses, racines carrées',
        'exercises': [
            {'id': 1, 'question': 'Déterminer f(x) telle que f(2)=5 et f(5)=11', 'solution': 'f(x) = 2x + 1'},
            {'id': 2, 'question': 'Résoudre f(x) = 0 pour f(x)=x²-4', 'solution': 'x = 2 ou x = -2'},
            {'id': 3, 'question': 'Dériver f(x)=3x²+2x-5', 'solution': "f'(x)=6x+2"}
        ],
        'formulas': [
            'Formule générale: f(x)=ax+b',
            'Formule quadratique: f(x)=ax²+bx+c',
            'Forme canonique: a(x-α)²+β'
        ]
    },
    'derivation': {
        'title': 'Dérivation',
        'description': 'Dérivées, taux de variation, tangentes',
        'exercises': [
            {'id': 4, 'question': 'Dériver f(x)=sin(x)+cos(x)', 'solution': "f'(x)=cos(x)-sin(x)"},
            {'id': 5, 'question': 'Trouver la pente de la tangente à f(x)=x² en x=3', 'solution': 'pente = 6'},
            {'id': 6, 'question': 'Dériver f(x)=ln(x)', 'solution': "f'(x)=1/x"}
        ],
        'formulas': [
            '(u+v)\' = u\' + v\'',
            '(uv)\' = u\'v + uv\'',
            '(u/v)\' = (u\'v - uv\')/v²'
        ]
    },
    'probabilites': {
        'title': 'Probabilités',
        'description': 'Probabilités conditionnelles, arbres, loi binomiale',
        'exercises': [
            {'id': 7, 'question': 'P(A)=0.3, P(B)=0.4, P(A∩B)=0.1. Calculer P(A∪B)', 'solution': '0.6'},
            {'id': 8, 'question': 'Lancer un dé 5 fois. Probabilité d\'avoir au moins un 6?', 'solution': '1-(5/6)^5 ≈ 0.598'},
            {'id': 9, 'question': 'P(A|B)=0.7, P(B)=0.5. Calculer P(A∩B)', 'solution': '0.35'}
        ],
        'formulas': [
            'P(A∪B)=P(A)+P(B)-P(A∩B)',
            'P(A|B)=P(A∩B)/P(B)',
            'Loi binomiale: P(X=k)=C(n,k)×p^k×(1-p)^{n-k}'
        ]
    },
    'suites': {
        'title': 'Suites',
        'description': 'Suites arithmétiques, géométriques, récurrentes',
        'exercises': [
            {'id': 10, 'question': 'Suite arithmétique: u0=3, r=5. Calculer u10', 'solution': 'u10 = 53'},
            {'id': 11, 'question': 'Suite géométrique: v0=2, q=3. Calculer v5', 'solution': 'v5 = 486'},
            {'id': 12, 'question': 'Un+1=0.5Un+1, U0=10. Calculer U3', 'solution': 'U3 = 2.875'}
        ],
        'formulas': [
            'Suite arithmétique: Un = U0 + n×r',
            'Suite géométrique: Vn = V0 × q^n',
            'Somme arithmétique: S = n×(U0+Un)/2'
        ]
    },
    'geometrie': {
        'title': 'Géométrie',
        'description': 'Vecteurs, produits scalaires, configurations',
        'exercises': [
            {'id': 13, 'question': 'Vecteurs u(2,3) et v(4,-1). Calculer u·v', 'solution': '5'},
            {'id': 14, 'question': 'Distance entre A(1,2) et B(4,6)', 'solution': '5'},
            {'id': 15, 'question': 'Équation droite passant par (1,2) et (3,8)', 'solution': 'y=3x-1'}
        ],
        'formulas': [
            'Distance: d=√((x2-x1)²+(y2-y1)²)',
            'Produit scalaire: u·v=x1x2+y1y2',
            'Équation droite: y=mx+p'
        ]
    }
}

# Exam templates
EXAM_TEMPLATES = {
    'bac_blanc': {
        'name': 'BAC Blanc (4 exercices)',
        'duration': 240,  # minutes
        'exercises': [
            'Fonctions (analyse)',
            'Probabilités (statistiques)',
            'Géométrie (espace)',
            'Algorithmique'
        ],
        'points': [5, 5, 5, 5]
    },
    'controle': {
        'name': 'Contrôle (3 exercices)',
        'duration': 90,
        'exercises': [
            'Dérivation',
            'Suites',
            'Fonctions'
        ],
        'points': [4, 4, 4]
    },
    'qcm_rapide': {
        'name': 'QCM Rapide (20 questions)',
        'duration': 45,
        'exercises': ['Questions à choix multiples'],
        'points': [1] * 20
    }
}

def generate_header():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BAC Math Study Hub - Première</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }
            .nav {
                display: flex;
                gap: 20px;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            .nav a {
                text-decoration: none;
                background: #4f46e5;
                color: white;
                padding: 12px 24px;
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .nav a:hover {
                background: #4338ca;
                transform: translateY(-2px);
            }
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                margin-top: 30px;
            }
            .card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 16px;
                padding: 25px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
                transition: transform 0.3s ease;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .card h3 {
                color: #4f46e5;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .progress-bar {
                height: 10px;
                background: #e5e7eb;
                border-radius: 5px;
                margin: 15px 0;
                overflow: hidden;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #10b981, #34d399);
                border-radius: 5px;
            }
            .btn {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                cursor: pointer;
                text-decoration: none;
                transition: all 0.3s ease;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            .exercise-item {
                background: #f8fafc;
                border-left: 4px solid #4f46e5;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
            }
            .topic-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .topic-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            }
            .timer {
                font-size: 2rem;
                font-weight: bold;
                color: #4f46e5;
                text-align: center;
                margin: 20px 0;
            }
            .formula {
                font-family: 'Courier New', monospace;
                background: #f1f5f9;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
            }
            @media (max-width: 768px) {
                .container { padding: 15px; }
                .header { padding: 20px; }
                .dashboard-grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="container">
    """

def generate_footer():
    return """
        </div>
        <script>
            // Timer functionality
            let examTimer = null;
            let examSeconds = 0;
            
            function startTimer(minutes) {
                examSeconds = minutes * 60;
                clearInterval(examTimer);
                examTimer = setInterval(updateTimer, 1000);
                updateTimer();
            }
            
            function updateTimer() {
                if (examSeconds <= 0) {
                    clearInterval(examTimer);
                    alert("Temps écoulé !");
                    return;
                }
                examSeconds--;
                const hours = Math.floor(examSeconds / 3600);
                const mins = Math.floor((examSeconds % 3600) / 60);
                const secs = examSeconds % 60;
                const timerDisplay = document.getElementById('timer-display');
                if (timerDisplay) {
                    timerDisplay.textContent = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
                }
            }
            
            // Exercise solution toggling
            function toggleSolution(exerciseId) {
                const solution = document.getElementById(`solution-${exerciseId}`);
                if (solution) {
                    solution.style.display = solution.style.display === 'none' ? 'block' : 'none';
                }
            }
            
            // Formula sheet generation
            function generateFormulaSheet() {
                const topics = document.querySelectorAll('input[name="topic"]:checked');
                const selectedTopics = Array.from(topics).map(t => t.value);
                
                if (selectedTopics.length === 0) {
                    alert("Sélectionnez au moins un thème !");
                    return;
                }
                
                let formulas = [];
                selectedTopics.forEach(topic => {
                    if (window.MATH_TOPICS && window.MATH_TOPICS[topic]) {
                        formulas = formulas.concat(window.MATH_TOPICS[topic].formulas);
                    }
                });
                
                const sheetContent = formulas.map(f => `<div class="formula">${f}</div>`).join('');
                document.getElementById('formula-sheet-output').innerHTML = sheetContent;
                
                // Update progress
                fetch('/api/progress?action=formula_generated');
            }
            
            // Track exercise completion
            function completeExercise(exerciseId) {
                fetch(`/api/progress?action=exercise_completed&id=${exerciseId}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById(`exercise-${exerciseId}`).style.opacity = '0.7';
                        document.getElementById(`exercise-${exerciseId}`).innerHTML += '<br><small>✓ Complété</small>';
                        updateProgressBar();
                    });
            }
            
            function updateProgressBar() {
                fetch('/api/progress')
                    .then(response => response.json())
                    .then(data => {
                        const totalExercises = Object.values(window.MATH_TOPICS || {}).reduce((sum, topic) => sum + topic.exercises.length, 0);
                        const percentage = totalExercises > 0 ? Math.min(100, (data.exercises_solved / totalExercises) * 100) : 0;
                        document.getElementById('progress-fill').style.width = `${percentage}%`;
                        document.getElementById('progress-text').textContent = `${data.exercises_solved}/${totalExercises} exercices`;
                    });
            }
            
            // Initialize MATH_TOPICS global variable
            window.MATH_TOPICS = """ + json.dumps(MATH_TOPICS, ensure_ascii=False) + """;
            
            // Initialize progress on page load
            document.addEventListener('DOMContentLoaded', function() {
                updateProgressBar();
            });
        </script>
    </body>
    </html>
    """

@app.route('/')
def home():
    user_progress = get_progress()
    progress_percentage = min(100, (user_progress['exercises_solved'] / 15) * 100) if 15 > 0 else 0
    
    content = f"""
    <div class="header">
        <h1>🎓 BAC Math Study Hub - Première</h1>
        <p>Plateforme complète de préparation aux mathématiques du BAC français</p>
        
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/topics">Thèmes</a>
            <a href="/exercises">Exercices</a>
            <a href="/formulas">Formules</a>
            <a href="/exams">Examens</a>
            <a href="/progress">Progression</a>
        </div>
        
        <div style="margin-top: 30px; background: #f0f9ff; padding: 20px; border-radius: 12px;">
            <h3>📊 Votre Progression</h3>
            <div class="progress-bar">
                <div id="progress-fill" class="progress-fill" style="width: {progress_percentage}%"></div>
            </div>
            <p id="progress-text">{user_progress['exercises_solved']}/15 exercices complétés</p>
        </div>
    </div>
    
    <div class="dashboard-grid">
        <div class="card">
            <h3>📚 Thèmes Mathématiques</h3>
            <p>Explorez les 5 thèmes principaux du programme de Première :</p>
            <ul style="margin: 15px 0; padding-left: 20px;">
                <li>Fonctions</li>
                <li>Dérivation</li>
                <li>Probabilités</li>
                <li>Suites</li>
                <li>Géométrie</li>
            </ul>
            <a href="/topics" class="btn">Voir les thèmes</a>
        </div>
        
        <div class="card">
            <h3>✏️ Exercices Interactifs</h3>
            <p>{len([ex for topic in MATH_TOPICS.values() for ex in topic['exercises']])} exercices avec solutions détaillées</p>
            <div style="margin: 15px 0;">
                <div class="exercise-item">
                    <strong>Exemple:</strong> Dériver f(x)=sin(x)+cos(x)
                    <br><small>Cliquez pour voir la solution</small>
                </div>
            </div>
            <a href="/exercises" class="btn">Commencer les exercices</a>
        </div>
        
        <div class="card">
            <h3>📝 Générateur de Fiches</h3>
            <p>Créez vos propres fiches de révision avec les formules essentielles</p>
            <ul style="margin: 15px 0; padding-left: 20px;">
                <li>Formules par thème</li>
                <li>Export PDF</li>
                <li>Personnalisation</li>
            </ul>
            <a href="/formulas" class="btn">Créer une fiche</a>
        </div>
        
        <div class="card">
            <h3>⏱️ Examens Blancs</h3>
            <p>Testez vos connaissances avec des examens chronométrés</p>
            <ul style="margin: 15px 0; padding-left: 20px;">
                <li>BAC Blanc (4h)</li>
                <li>Contrôle (1h30)</li>
                <li>QCM Rapide (45min)</li>
            </ul>
            <a href="/exams" class="btn">Passer un examen</a>
        </div>
    </div>
    
    <div style="margin-top: 30px; background: white; padding: 25px; border-radius: 16px;">
        <h3>🎯 Objectifs du Jour</h3>
        <div style="display: flex; gap: 20px; margin-top: 15px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px; background: #f0fdf4; padding: 15px; border-radius: 10px;">
                <strong>✓ Compléter 3 exercices</strong>
                <div style="margin-top: 10px;">
                    <span style="color: #10b981;">{user_progress['exercises_solved']}/3</span>
                    <div style="height: 8px; background: #d1fae5; border-radius: 4px; margin-top: 5px;">
                        <div style="height: 100%; width: {(user_progress['exercises_solved']/3)*100 if user_progress['exercises_solved'] <= 3 else 100}%; background: #10b981; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 200px; background: #fef3c7; padding: 15px; border-radius: 10px;">
                <strong>✓ Réviser 2 thèmes</strong>
                <div style="margin-top: 10px;">
                    <span style="color: #f59e0b;">{len(user_progress['topics_completed'])}/2</span>
                    <div style="height: 8px; background: #fef3c7; border-radius: 4px; margin-top: 5px;">
                        <div style="height: 100%; width: {(len(user_progress['topics_completed'])/2)*100 if len(user_progress['topics_completed']) <= 2 else 100}%; background: #f59e0b; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 200px; background: #e0f2fe; padding: 15px; border-radius: 10px;">
                <strong>✓ Générer 1 fiche</strong>
                <div style="margin-top: 10px;">
                    <span style="color: #0ea5e9;">{user_progress['formula_sheets_generated']}/1</span>
                    <div style="height: 8px; background: #e0f2fe; border-radius: 4px; margin-top: 5px;">
                        <div style="height: 100%; width: {user_progress['formula_sheets_generated']*100}%; background: #0ea5e9; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return generate_header() + content + generate_footer()

@app.route('/topics')
def topics():
    user_progress = get_progress()
    content = """
    <div class="header">
        <h1>📚 Thèmes Mathématiques - Première</h1>
        <p>Sélectionnez un thème pour explorer les concepts, exercices et formules</p>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/topics">Thèmes</a>
            <a href="/exercises">Exercices</a>
            <a href="/formulas">Formules</a>
            <a href="/exams">Examens</a>
        </div>
    </div>
    
    <div class="topic-grid">
    """
    
    for topic_id, topic in MATH_TOPICS.items():
        completed = topic_id in user_progress['topics_completed']
        content += f"""
        <div class="topic-card">
            <h3>{topic['title']}</h3>
            <p>{topic['description']}</p>
            <div style="margin: 15px 0;">
                <strong>{len(topic['exercises'])} exercices disponibles</strong>
                <br>
                <small>{len(topic['formulas'])} formules essentielles</small>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 15px;">
                <a href="/topic/{topic_id}" class="btn" style="flex: 1; text-align: center;">Explorer</a>
                <button onclick="completeTopic('{topic_id}')" class="btn" style="flex: 1; background: {'#10b981' if completed else '#6b7280'}">
                    {'✓ Complété' if completed else 'Marquer comme fait'}
                </button>
            </div>
        </div>
        """
    
    content += """
    </div>
    
    <script>
        function completeTopic(topicId) {
            fetch(`/api/progress?action=topic_completed&topic=${topicId}`)
                .then(response => response.json())
                .then(data => {
                    location.reload();
                });
        }
    </script>
    """
    
    return generate_header() + content + generate_footer()

@app.route('/topic/<topic_id>')
def topic_detail(topic_id):
    if topic_id not in MATH_TOPICS:
        return "Thème non trouvé", 404
    
    topic = MATH_TOPICS[topic_id]
    
    exercises_html = ""
    for exercise in topic['exercises']:
        exercises_html += f"""
        <div class="exercise-item" id="exercise-{exercise['id']}">
            <strong>Exercice {exercise['id']}:</strong> {exercise['question']}
            <br>
            <button onclick="toggleSolution({exercise['id']})" class="btn" style="margin-top: 10px; padding: 8px 16px; font-size: 0.9rem;">
                Voir la solution
            </button>
            <button onclick="completeExercise({exercise['id']})" class="btn" style="margin-top: 10px; padding: 8px 16px; font-size: 0.9rem; background: #10b981;">
                Marquer comme complété
            </button>
            <div id="solution-{exercise['id']}" style="display: none; margin-top: 10px; padding: 10px; background: #f8fafc; border-radius: 8px;">
                <strong>Solution:</strong> {exercise['solution']}
            </div>
        </div>
        """
    
    formulas_html = ""
    for formula in topic['formulas']:
        formulas_html += f"""
        <div class="formula">
            {formula}
        </div>
        """
    
    content = f"""
    <div class="header">
        <h1>{topic['title']}</h1>
        <p>{topic['description']}</p>
        <div class="nav">
            <a href="/topics">← Retour aux thèmes</a>
            <a href="/exercises">Exercices</a>
            <a href="/formulas">Formules</a>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px;">
        <div>
            <h3>Exercices</h3>
            {exercises_html}
        </div>
        
        <div>
            <h3>Formules Essentielles</h3>
            {formulas_html}
        </div>
    </div>
    """
    
    return generate_header() + content + generate_footer()

@app.route('/exercises')
def exercises():
    all_exercises = []
    for topic_id, topic in MATH_TOPICS.items():
        for exercise in topic['exercises']:
            exercise['topic'] = topic['title']
            all_exercises.append(exercise)
    
    exercises_html = ""
    for exercise in all_exercises:
        exercises_html += f"""
        <div class="exercise-item" id="exercise-{exercise['id']}">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <strong>Exercice {exercise['id']} ({exercise['topic']})</strong>
                    <br>{exercise['question']}
                </div>
                <div style="display: flex; gap: 10px;">
                    <button onclick="toggleSolution({exercise['id']})" class="btn" style="padding: 8px 16px; font-size: 0.9rem;">
                        Solution
                    </button>
                    <button onclick="completeExercise({exercise['id']})" class="btn" style="padding: 8px 16px; font-size: 0.9rem; background: #10b981;">
                        ✓
                    </button>
                </div>
            </div>
            <div id="solution-{exercise['id']}" style="display: none; margin-top: 10px; padding: 15px; background: #f8fafc; border-radius: 8px; border-left: 4px solid #4f46e5;">
                <strong>Solution détaillée:</strong>
                <br>{exercise['solution']}
            </div>
        </div>
        """
    
    content = f"""
    <div class="header">
        <h1>✏️ Exercices Interactifs</h1>
        <p>Pratiquez avec {len(all_exercises)} exercices corrigés - Cliquez sur "Solution" pour voir la réponse</p>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/topics">Thèmes</a>
            <a href="/exercises">Exercices</a>
            <a href="/formulas">Formules</a>
        </div>
    </div>
    
    <div style="margin-top: 30px;">
        <div style="background: white; padding: 25px; border-radius: 16px;">
            <h3>Tous les exercices ({len(all_exercises)} disponibles)</h3>
            {exercises_html}
        </div>
    </div>
    """
    
    return generate_header() + content + generate_footer()

@app.route('/formulas')
def formulas():
    content = """
    <div class="header">
        <h1>📝 Générateur de Fiches de Révision</h1>
        <p>Sélectionnez les thèmes pour générer votre fiche personnalisée</p>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/topics">Thèmes</a>
            <a href="/exercises">Exercices</a>
            <a href="/formulas">Formules</a>
        </div>
    </div>
    
    <div style="margin-top: 30px; background: white; padding: 25px; border-radius: 16px;">
        <h3>Sélectionnez les thèmes à inclure:</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0;">
    """
    
    for topic_id, topic in MATH_TOPICS.items():
        content += f"""
            <div style="background: #f8fafc; padding: 15px; border-radius: 10px; min-width: 200px;">
                <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input type="checkbox" name="topic" value="{topic_id}" checked>
                    <strong>{topic['title']}</strong>
                </label>
                <small style="display: block; margin-top: 5px;">{len(topic['formulas'])} formules</small>
            </div>
        """
    
    content += """
        </div>
        
        <button onclick="generateFormulaSheet()" class="btn" style="margin: 20px 0; padding: 15px 30px;">
            🚀 Générer ma fiche
        </button>
        
        <div style="margin-top: 30px;">
            <h3>Votre fiche de révision:</h3>
            <div id="formula-sheet-output" style="margin-top: 15px; padding: 20px; background: #f8fafc; border-radius: 12px; min-height: 200px;">
                <p style="color: #6b7280; text-align: center;">Votre fiche apparaîtra ici après sélection</p>
            </div>
            
            <div style="margin-top: 20px; display: flex; gap: 15px;">
                <button onclick="printSheet()" class="btn" style="background: #6b7280;">
                    🖨️ Imprimer
                </button>
                <button onclick="downloadPDF()" class="btn" style="background: #10b981;">
                    📥 Télécharger PDF
                </button>
                <button onclick="shareSheet()" class="btn" style="background: #3b82f6;">
                    🔗 Partager
                </button>
            </div>
        </div>
    </div>
    
    <script>
        function printSheet() {
            window.print();
        }
        
        function downloadPDF() {
            alert("Fonctionnalité PDF en développement - Pour l'instant, utilisez 'Imprimer' puis 'Enregistrer au format PDF'");
        }
        
        function shareSheet() {
            if (navigator.share) {
                navigator.share({
                    title: 'Ma fiche de révision BAC Math',
                    text: 'Découvrez ma fiche de révision générée sur BAC Math Study Hub',
                    url: window.location.href
                });
            } else {
                alert("Copiez ce lien pour partager: " + window.location.href);
            }
        }
    </script>
    """
    
    return generate_header() + content + generate_footer()

@app.route('/exams')
def exams():
    content = """
    <div class="header">
        <h1>⏱️ Examens Blancs</h1>
        <p>Testez vos connaissances avec des examens chronométrés</p>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/topics">Thèmes</a>
            <a href="/exercises">Exercices</a>
            <a href="/exams">Examens</a>
        </div>
    </div>
    
    <div class="dashboard-grid" style="margin-top: 30px;">
    """
    
    for exam_id, exam in EXAM_TEMPLATES.items():
        hours = exam['duration'] // 60
        minutes = exam['duration'] % 60
        duration_str = f"{hours}h{minutes:02d}" if hours > 0 else f"{minutes}min"
        
        content += f"""
        <div class="card">
            <h3>{exam['name']}</h3>
            <p>Durée: {duration_str} • {len(exam['exercises'])} exercices</p>
            <div style="margin: 15px 0;">
                <strong>Exercices:</strong>
                <ul style="margin: 10px 0; padding-left: 20px;">
        """
        
        for i, exercise in enumerate(exam['exercises']):
            points = exam['points'][i] if i < len(exam['points']) else exam['points'][-1]
            content += f"<li>{exercise} ({points} points)</li>"
        
        content += f"""
                </ul>
                <strong>Total: {sum(exam['points'])} points</strong>
            </div>
            <button onclick="startExam('{exam_id}', {exam['duration']})" class="btn" style="width: 100%;">
                Commencer l'examen
            </button>
        </div>
        """
    
    content += """
    </div>
    
    <div id="exam-interface" style="display: none; margin-top: 40px; background: white; padding: 30px; border-radius: 16px;">
        <h2 id="exam-title"></h2>
        <div class="timer" id="timer-display">00:00:00</div>
        <div id="exam-questions"></div>
        <div style="margin-top: 30px; display: flex; gap: 15px;">
            <button onclick="submitExam()" class="btn" style="background: #10b981;">
                Soumettre l'examen
            </button>
            <button onclick="cancelExam()" class="btn" style="background: #ef4444;">
                Annuler
            </button>
        </div>
    </div>
    
    <script>
        let currentExam = null;
        
        function startExam(examId, durationMinutes) {
            currentExam = examId;
            document.getElementById('exam-interface').style.display = 'block';
            document.getElementById('exam-title').textContent = EXAM_TEMPLATES[examId].name;
            
            // Generate questions
            const questionsHtml = EXAM_TEMPLATES[examId].exercises.map((exercise, index) => `
                <div style="margin: 20px 0; padding: 20px; background: #f8fafc; border-radius: 12px;">
                    <h4>Exercice ${index + 1}: ${exercise}</h4>
                    <p><strong>Points: ${EXAM_TEMPLATES[examId].points[index]}</strong></p>
                    <textarea 
                        placeholder="Votre réponse ici..." 
                        style="width: 100%; height: 100px; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; margin-top: 10px;"
                        id="answer-${index}"
                    ></textarea>
                </div>
            `).join('');
            
            document.getElementById('exam-questions').innerHTML = questionsHtml;
            startTimer(durationMinutes);
            
            // Scroll to exam interface
            document.getElementById('exam-interface').scrollIntoView({ behavior: 'smooth' });
        }
        
        function submitExam() {
            if (confirm("Voulez-vous vraiment soumettre votre examen ?")) {
                clearInterval(examTimer);
                alert("Examen soumis ! Votre score sera calculé.");
                document.getElementById('exam-interface').style.display = 'none';
                fetch('/api/progress?action=exam_taken');
            }
        }
        
        function cancelExam() {
            if (confirm("Annuler l'examen en cours ?")) {
                clearInterval(examTimer);
                document.getElementById('exam-interface').style.display = 'none';
                examSeconds = 0;
            }
        }
        
        const EXAM_TEMPLATES = """ + json.dumps(EXAM_TEMPLATES, ensure_ascii=False) + """;
    </script>
    """
    
    return generate_header() + content + generate_footer()

@app.route('/progress')
def progress():
    user_progress = get_progress()
    total_exercises = sum(len(topic['exercises']) for topic in MATH_TOPICS.values())
    total_topics = len(MATH_TOPICS)
    
    progress_percentage = min(100, (user_progress['exercises_solved'] / total_exercises) * 100) if total_exercises > 0 else 0
    topics_percentage = min(100, (len(user_progress['topics_completed']) / total_topics) * 100) if total_topics > 0 else 0
    
    content = f"""
    <div class="header">
        <h1>📊 Votre Progression</h1>
        <p>Suivez votre avancement dans la préparation au BAC</p>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/progress">Progression</a>
        </div>
    </div>
    
    <div style="margin-top: 30px;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px;">
            <div style="background: white; padding: 25px; border-radius: 16px;">
                <h3>Exercices Complétés</h3>
                <div style="font-size: 2.5rem; font-weight: bold; color: #4f46e5; text-align: center;">
                    {user_progress['exercises_solved']}/{total_exercises}
                </div>
                <div class="progress-bar" style="margin: 20px 0;">
                    <div class="progress-fill" style="width: {progress_percentage}%"></div>
                </div>
                <p style="text-align: center;">{progress_percentage:.1f}% complété</p>
            </div>
            
            <div style="background: white; padding: 25px; border-radius: 16px;">
                <h3>Thèmes Maîtrisés</h3>
                <div style="font-size: 2.5rem; font-weight: bold; color: #10b981; text-align: center;">
                    {len(user_progress['topics_completed'])}/{total_topics}
                </div>
                <div class="progress-bar" style="margin: 20px 0;">
                    <div class="progress-fill" style="width: {topics_percentage}%"></div>
                </div>
                <p style="text-align: center;">{topics_percentage:.1f}% complété</p>
            </div>
            
            <div style="background: white; padding: 25px; border-radius: 16px;">
                <h3>Examens Passés</h3>
                <div style="font-size: 2.5rem; font-weight: bold; color: #f59e0b; text-align: center;">
                    {user_progress['exams_taken']}
                </div>
                <p style="text-align: center;">sur 3 types disponibles</p>
            </div>
            
            <div style="background: white; padding: 25px; border-radius: 16px;">
                <h3>Fiches Générées</h3>
                <div style="font-size: 2.5rem; font-weight: bold; color: #0ea5e9; text-align: center;">
                    {user_progress['formula_sheets_generated']}
                </div>
                <p style="text-align: center;">fiches personnalisées</p>
            </div>
        </div>
        
        <div style="margin-top: 40px; background: white; padding: 25px; border-radius: 16px;">
            <h3>Thèmes Complétés</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 20px;">
    """
    
    for topic_id, topic in MATH_TOPICS.items():
        completed = topic_id in user_progress['topics_completed']
        content += f"""
                <div style="padding: 15px; background: {'#f0fdf4' if completed else '#f8fafc'}; border-radius: 10px; min-width: 200px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>{topic['title']}</strong>
                        <span style="color: {'#10b981' if completed else '#6b7280'}">
                            {'✓' if completed else '○'}
                        </span>
                    </div>
                    <small>{len(topic['exercises'])} exercices</small>
                </div>
        """
    
    content += """
            </div>
        </div>
        
        <div style="margin-top: 30px; background: white; padding: 25px; border-radius: 16px;">
            <h3>Statistiques Détaillées</h3>
            <div style="margin-top: 20px;">
                <canvas id="progressChart" width="400" height="200"></canvas>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const ctx = document.getElementById('progressChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Exercices', 'Thèmes', 'Examens', 'Fiches'],
                datasets: [{
                    label: 'Progression',
                    data: [
                        """ + str(user_progress['exercises_solved']) + """,
                        """ + str(len(user_progress['topics_completed'])) + """,
                        """ + str(user_progress['exams_taken']) + """,
                        """ + str(user_progress['formula_sheets_generated']) + """
                    ],
                    backgroundColor: [
                        '#4f46e5',
                        '#10b981',
                        '#f59e0b',
                        '#0ea5e9'
                    ]
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    </script>
    """
    
    return generate_header() + content + generate_footer()

@app.route('/api/progress')
def api_progress():
    user_progress = get_progress()
    action = request.args.get('action')
    exercise_id = request.args.get('id')
    topic = request.args.get('topic')
    
    if action == 'exercise_completed' and exercise_id:
        user_progress['exercises_solved'] += 1
    elif action == 'topic_completed' and topic:
        if topic not in user_progress['topics_completed']:
            user_progress['topics_completed'].append(topic)
    elif action == 'exam_taken':
        user_progress['exams_taken'] += 1
    elif action == 'formula_generated':
        user_progress['formula_sheets_generated'] += 1
    
    save_progress(user_progress)
    return jsonify(user_progress)

@app.route('/api/reset')
def api_reset():
    save_progress(json.loads(json.dumps(DEFAULT_PROGRESS)))
    return jsonify({'status': 'reset', 'progress': get_progress()})

if __name__ == '__main__':
    # Local dev: `python app.py` still works exactly as before.
    # In production, gunicorn imports `app` directly and this block never runs.
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

