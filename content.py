"""Course content for Hermes — Maths Première (spécialité).

Math is written in LaTeX with \\( ... \\) delimiters and rendered by KaTeX in the
browser. Videos are Yvan Monka's "LE COURS" lessons; PDFs are the matching course
sheets on his site maths-et-tiques.fr.
"""

PDF_BASE = 'https://www.maths-et-tiques.fr/telech/'
MONKA_SITE = 'https://www.maths-et-tiques.fr/index.php/cours-maths/niveau-premiere'
MONKA_SEARCH = 'https://www.youtube.com/results?search_query=Yvan+Monka+'


def E(i, level, question, solution, hint=''):
    """One exercise. level: 1 = application directe, 2 = standard, 3 = approfondissement."""
    return {'id': i, 'level': level, 'question': question, 'solution': solution, 'hint': hint}


def pdf(label, name):
    return {'label': label, 'url': PDF_BASE + name}


DOMAINS = [
    ('algebre', 'Algèbre', '🧮'),
    ('analyse', 'Analyse', '📈'),
    ('geometrie', 'Géométrie', '📐'),
    ('probas', 'Probabilités', '🎲'),
]

CHAPTERS = [
    # ------------------------------------------------------------------ 1
    {
        'id': 'second-degre', 'num': 1, 'domain': 'algebre', 'icon': '🧮',
        'title': 'Second degré',
        'tagline': 'Forme canonique, discriminant, racines, signe d\'un trinôme.',
        'video': {'id': 'WVYWdN13kPE', 'title': 'LE COURS : Fonctions du second degré - Première'},
        'pdfs': [pdf('Cours 1 — Fonction polynôme du second degré', '19SecdegP1M.pdf'),
                 pdf('Cours 2 — Équations et inéquations', '19SecdegP2M.pdf')],
        'cours': [
            ('Forme canonique', r"Tout trinôme \(f(x)=ax^2+bx+c\) (avec \(a\neq 0\)) s'écrit \(f(x)=a(x-\alpha)^2+\beta\) avec \(\alpha=-\dfrac{b}{2a}\) et \(\beta=f(\alpha)\). La parabole a pour sommet \(S(\alpha\,;\,\beta)\) : c'est un minimum si \(a>0\), un maximum si \(a<0\)."),
            ('Discriminant et racines', r"On pose \(\Delta=b^2-4ac\). Si \(\Delta>0\) : deux racines \(x_{1,2}=\dfrac{-b\pm\sqrt{\Delta}}{2a}\). Si \(\Delta=0\) : une racine double \(x_0=-\dfrac{b}{2a}\). Si \(\Delta<0\) : aucune racine réelle."),
            ('Factorisation', r"Si \(\Delta>0\) : \(f(x)=a(x-x_1)(x-x_2)\). Si \(\Delta=0\) : \(f(x)=a(x-x_0)^2\). Si \(\Delta<0\) : pas de factorisation dans \(\mathbb{R}\)."),
            ('Signe du trinôme', r"Le trinôme est du signe de \(a\) à l'extérieur des racines et du signe opposé à celui de \(a\) entre les racines. Si \(\Delta\leq 0\), il est du signe de \(a\) partout (nul seulement en \(x_0\) si \(\Delta=0\))."),
            ('Somme et produit des racines', r"Si \(x_1\) et \(x_2\) sont les racines : \(x_1+x_2=-\dfrac{b}{a}\) et \(x_1x_2=\dfrac{c}{a}\)."),
        ],
        'formulas': [
            r"\(\Delta=b^2-4ac\)",
            r"\(x_{1,2}=\dfrac{-b\pm\sqrt{\Delta}}{2a}\)",
            r"\(f(x)=a(x-\alpha)^2+\beta\;,\quad \alpha=-\dfrac{b}{2a}\;,\;\beta=f(\alpha)\)",
            r"\(x_1+x_2=-\dfrac{b}{a}\;,\qquad x_1x_2=\dfrac{c}{a}\)",
        ],
        'pitfalls': [
            r"Oublier le facteur \(a\) en factorisant : \(3x^2-12x+9=3(x-1)(x-3)\), pas \((x-1)(x-3)\).",
            r"Oublier de diviser par \(2a\) (et pas seulement par \(a\)) dans la formule des racines.",
            r"Pour une inéquation, toujours faire un tableau de signes : le signe de \(a\) décide.",
        ],
        'exercises': [
            E('sd1', 1, r"Mettre sous forme canonique \(f(x)=x^2-6x+5\).", r"\(\alpha=-\dfrac{-6}{2}=3\) et \(\beta=f(3)=9-18+5=-4\).\nDonc \(f(x)=(x-3)^2-4\)."),
            E('sd2', 1, r"Résoudre \(x^2-5x+6=0\).", r"\(\Delta=25-24=1>0\), donc \(x=\dfrac{5-1}{2}=2\) ou \(x=\dfrac{5+1}{2}=3\).\n\(S=\{2\,;\,3\}\)."),
            E('sd3', 1, r"Résoudre \(2x^2+3x-5=0\).", r"\(\Delta=9+40=49>0\) donc \(x=\dfrac{-3-7}{4}=-\dfrac{5}{2}\) ou \(x=\dfrac{-3+7}{4}=1\).", r"Vérifie avec la somme des racines : \(-b/a\)."),
            E('sd4', 2, r"Résoudre \(x^2-4x+4=0\).", r"\(\Delta=16-16=0\) : racine double \(x_0=\dfrac{4}{2}=2\).\n(On reconnaît aussi \((x-2)^2=0\).)"),
            E('sd5', 2, r"Résoudre l'inéquation \(x^2-2x-3>0\).", r"\(\Delta=4+12=16\), racines \(x_1=-1\) et \(x_2=3\). Comme \(a=1>0\), le trinôme est positif à l'extérieur des racines.\n\(S=]-\infty\,;\,-1[\,\cup\,]3\,;\,+\infty[\)."),
            E('sd6', 2, r"Pour quelles valeurs du réel \(m\) l'équation \(x^2+mx+9=0\) admet-elle une unique solution ?", r"Une unique solution \(\iff \Delta=0\). Ici \(\Delta=m^2-36\), donc \(m^2=36\) et \(m=6\) ou \(m=-6\).", r"Unique solution = racine double."),
            E('sd7', 2, r"Factoriser \(3x^2-12x+9\).", r"\(\Delta=144-108=36\), racines \(\dfrac{12-6}{6}=1\) et \(\dfrac{12+6}{6}=3\).\nDonc \(3x^2-12x+9=3(x-1)(x-3)\)."),
            E('sd8', 3, r"Un rectangle a pour périmètre \(20\) m et pour aire \(21\) m\(^2\). Déterminer ses dimensions.", r"Soient \(x\) et \(y\) les dimensions : \(x+y=10\) et \(xy=21\). Donc \(y=10-x\) et \(x(10-x)=21\), soit \(x^2-10x+21=0\).\n\(\Delta=100-84=16\), \(x=3\) ou \(x=7\). Le rectangle mesure \(3\) m sur \(7\) m.", r"Exprime \(y\) en fonction de \(x\) avec le périmètre."),
            E('sd9', 3, r"Résoudre dans \(\mathbb{R}\) : \(x^4-5x^2+4=0\).", r"On pose \(X=x^2\) (avec \(X\geq 0\)) : \(X^2-5X+4=0\), \(\Delta=9\), \(X=1\) ou \(X=4\), tous deux positifs.\nDonc \(x^2=1\) ou \(x^2=4\) : \(S=\{-2\,;\,-1\,;\,1\,;\,2\}\).", r"Change de variable \(X=x^2\)."),
            E('sd10', 3, r"Déterminer l'extremum de \(f(x)=-2x^2+8x-3\) et préciser où il est atteint.", r"\(a=-2<0\) : la parabole est tournée vers le bas, donc \(f\) admet un maximum atteint en \(\alpha=-\dfrac{8}{2\times(-2)}=2\).\n\(f(2)=-8+16-3=5\). Le maximum vaut \(5\), atteint en \(x=2\)."),
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        'id': 'suites-generalites', 'num': 2, 'domain': 'algebre', 'icon': '🔢',
        'title': 'Suites : généralités',
        'tagline': 'Définition, sens de variation, raisonnement par récurrence, seuils.',
        'video': {'id': '8I6dotcdW3I', 'title': 'LE COURS : Les suites - Première'},
        'pdfs': [pdf('Cours — Généralités sur les suites', '19SuitesP1M.pdf')],
        'cours': [
            ('Deux façons de définir une suite', r"Explicite : \(u_n=f(n)\) (on calcule directement chaque terme). Par récurrence : on donne \(u_0\) et une relation \(u_{n+1}=f(u_n)\) (il faut calculer les termes un par un)."),
            ('Sens de variation', r"\((u_n)\) est croissante si \(u_{n+1}-u_n\geq 0\) pour tout \(n\), décroissante si \(u_{n+1}-u_n\leq 0\). Si tous les termes sont strictement positifs, on peut comparer \(\dfrac{u_{n+1}}{u_n}\) à \(1\)."),
            ('Lien avec les fonctions', r"Si \(u_n=f(n)\) et que \(f\) est croissante sur \([0\,;+\infty[\), alors \((u_n)\) est croissante. Attention : cette méthode ne marche pas pour une suite définie par récurrence."),
            ('Raisonnement par récurrence', r"Pour prouver une propriété \(P(n)\) pour tout \(n\geq n_0\) : <b>initialisation</b> (\(P(n_0)\) est vraie), <b>hérédité</b> (si \(P(n)\) est vraie alors \(P(n+1)\) est vraie), <b>conclusion</b>."),
            ('Algorithme de seuil', r"Pour trouver le plus petit \(n\) tel que \(u_n>S\), on utilise une boucle <i>while</i> qui calcule les termes tant que le seuil n'est pas dépassé."),
        ],
        'formulas': [
            r"\(u_{n+1}-u_n\geq 0\;\Rightarrow\;(u_n)\text{ croissante}\)",
            r"\(u_n>0\text{ et }\dfrac{u_{n+1}}{u_n}\geq 1\;\Rightarrow\;(u_n)\text{ croissante}\)",
            r"Récurrence : initialisation \(\to\) hérédité \(\to\) conclusion",
        ],
        'code': ('Seuil en Python', "def seuil(S):\n    n = 0\n    u = 2 * 0**2 - 3      # u_0\n    while u <= S:\n        n = n + 1\n        u = 2 * n**2 - 3\n    return n\n\nprint(seuil(1000))   # affiche 23"),
        'pitfalls': [
            r"Confondre \(u_{n+1}\) (terme suivant) et \(u_n+1\) (terme plus 1).",
            r"Dans l'hérédité, on <b>suppose</b> \(P(n)\) vraie : on ne la démontre pas.",
            r"Pour une suite définie par récurrence, étudier \(f\) ne suffit pas : calcule \(u_{n+1}-u_n\).",
        ],
        'exercises': [
            E('sg1', 1, r"Soit \(u_n=2n^2-3\). Calculer \(u_0\), \(u_1\) et \(u_2\).", r"\(u_0=-3\), \(u_1=2-3=-1\), \(u_2=8-3=5\)."),
            E('sg2', 1, r"Soit \((u_n)\) définie par \(u_0=1\) et \(u_{n+1}=2u_n+3\). Calculer \(u_1\), \(u_2\), \(u_3\).", r"\(u_1=2\times1+3=5\), \(u_2=2\times5+3=13\), \(u_3=2\times13+3=29\)."),
            E('sg3', 2, r"Étudier le sens de variation de \(u_n=\dfrac{3n+1}{n+1}\) pour \(n\geq 0\).", r"\(u_{n+1}-u_n=\dfrac{3n+4}{n+2}-\dfrac{3n+1}{n+1}=\dfrac{(3n+4)(n+1)-(3n+1)(n+2)}{(n+1)(n+2)}=\dfrac{2}{(n+1)(n+2)}>0\).\nLa suite est strictement croissante.", r"Mets au même dénominateur."),
            E('sg4', 2, r"Soit \(u_n=n^2-4n\). Montrer que \(u_{n+1}-u_n=2n-3\), puis étudier les variations de \((u_n)\).", r"\(u_{n+1}-u_n=(n+1)^2-4(n+1)-n^2+4n=2n+1-4=2n-3\).\nCette différence est strictement positive si et seulement si \(n\geq 2\). Donc \(u_3>u_2\), \(u_4>u_3\), … : la suite est croissante à partir du rang 2 (alors que \(u_0=0>u_1=-3>u_2=-4\))."),
            E('sg5', 2, r"Soit \(u_0=2\) et \(u_{n+1}=u_n-n\). Calculer \(u_1\), \(u_2\), \(u_3\), \(u_4\).", r"\(u_1=2-0=2\), \(u_2=2-1=1\), \(u_3=1-2=-1\), \(u_4=-1-3=-4\)."),
            E('sg6', 2, r"Soit \(u_0=0\) et \(u_{n+1}=\sqrt{u_n+2}\). Donner des valeurs approchées de \(u_1\) et \(u_2\) à \(10^{-3}\) près.", r"\(u_1=\sqrt{2}\approx 1{,}414\) et \(u_2=\sqrt{2+\sqrt2}\approx 1{,}848\)."),
            E('sg7', 3, r"Démontrer par récurrence que pour tout entier \(n\geq 0\) : \(2^n\geq n+1\).", r"<b>Initialisation</b> : pour \(n=0\), \(2^0=1\geq 1\) : vrai.\n<b>Hérédité</b> : on suppose \(2^n\geq n+1\) pour un certain \(n\). Alors \(2^{n+1}=2\times 2^n\geq 2n+2\geq n+2\) (car \(n\geq 0\)). Donc la propriété est vraie au rang \(n+1\).\n<b>Conclusion</b> : elle est vraie pour tout \(n\geq 0\).", r"Multiplie l'inégalité de l'hypothèse par 2."),
            E('sg8', 3, r"Soit \(u_n=2n^2-3\). Déterminer le plus petit entier \(n\) tel que \(u_n>1000\) (algorithme de seuil).", r"On teste : \(u_{22}=2\times484-3=965\leq 1000\) et \(u_{23}=2\times529-3=1055>1000\).\nLe plus petit entier est \(n=23\) (c'est ce que renvoie la fonction Python ci-dessus)."),
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        'id': 'suites-arith-geo', 'num': 3, 'domain': 'algebre', 'icon': '🧱',
        'title': 'Suites arithmétiques et géométriques',
        'tagline': 'Termes, sommes, variations et problèmes d\'intérêts composés.',
        'video': {'id': '05UHsy9G4M4', 'title': 'LE COURS : Suites arithmétiques, suites géométriques - Première'},
        'pdfs': [pdf('Cours — Suites arithmétiques et géométriques', '19SuitesP2M.pdf')],
        'cours': [
            ('Suite arithmétique', r"On passe d'un terme au suivant en <b>ajoutant</b> la raison \(r\) : \(u_{n+1}=u_n+r\). Terme général : \(u_n=u_0+nr=u_p+(n-p)r\). Elle est croissante si \(r>0\), décroissante si \(r<0\)."),
            ('Suite géométrique', r"On passe d'un terme au suivant en <b>multipliant</b> par la raison \(q\) : \(v_{n+1}=q\,v_n\). Terme général : \(v_n=v_0\,q^n=v_p\,q^{n-p}\). Pour \(v_0>0\) : croissante si \(q>1\), décroissante si \(0<q<1\)."),
            ('Sommes de termes consécutifs', r"Arithmétique : \(S=\text{(nombre de termes)}\times\dfrac{\text{premier}+\text{dernier}}{2}\). Géométrique (\(q\neq1\)) : \(1+q+\dots+q^n=\dfrac{1-q^{n+1}}{1-q}\)."),
            ('Cas particulier à connaître', r"\(1+2+3+\dots+n=\dfrac{n(n+1)}{2}\)."),
        ],
        'formulas': [
            r"\(u_n=u_0+nr\)",
            r"\(v_n=v_0\,q^n\)",
            r"\(S=(\text{nb de termes})\times\dfrac{\text{premier}+\text{dernier}}{2}\)",
            r"\(1+q+\dots+q^n=\dfrac{1-q^{n+1}}{1-q}\quad(q\neq1)\)",
            r"\(1+2+\dots+n=\dfrac{n(n+1)}{2}\)",
        ],
        'pitfalls': [
            r"De \(u_0\) à \(u_n\), il y a \(n+1\) termes (pas \(n\)).",
            r"Ne pas confondre raison arithmétique \(r\) (on additionne) et raison géométrique \(q\) (on multiplie).",
            r"Augmenter de \(3\,\%\) revient à multiplier par \(1{,}03\), pas par \(3\).",
        ],
        'exercises': [
            E('ag1', 1, r"Suite arithmétique avec \(u_0=3\) et \(r=5\). Calculer \(u_{10}\).", r"\(u_{10}=3+10\times5=53\)."),
            E('ag2', 1, r"Suite géométrique avec \(v_0=2\) et \(q=3\). Calculer \(v_5\).", r"\(v_5=2\times3^5=2\times243=486\)."),
            E('ag3', 1, r"Suite arithmétique avec \(u_5=17\) et \(u_9=29\). Déterminer \(r\) et \(u_0\).", r"\(r=\dfrac{29-17}{9-5}=3\) puis \(u_0=u_5-5r=17-15=2\)."),
            E('ag4', 2, r"Calculer \(1+2+3+\dots+100\).", r"Somme arithmétique de \(100\) termes : \(S=100\times\dfrac{1+100}{2}=5050\)."),
            E('ag5', 2, r"Calculer \(S=5+10+20+\dots+5\times2^9\).", r"Suite géométrique de premier terme \(5\), de raison \(2\), avec \(10\) termes : \(S=5\times\dfrac{1-2^{10}}{1-2}=5\times1023=5115\)."),
            E('ag6', 2, r"Une suite géométrique <b>positive</b> vérifie \(v_2=12\) et \(v_4=48\). Déterminer \(q\) et \(v_0\).", r"\(v_4=v_2\times q^2\) donc \(q^2=\dfrac{48}{12}=4\) et \(q=2\) (la suite est positive).\nPuis \(v_0=\dfrac{v_2}{q^2}=\dfrac{12}{4}=3\)."),
            E('ag7', 2, r"On place \(1000\) € à intérêts composés au taux de \(3\,\%\) par an. Quel capital après \(10\) ans ?", r"Le capital est multiplié par \(1{,}03\) chaque année : suite géométrique de raison \(1{,}03\).\n\(C_{10}=1000\times1{,}03^{10}\approx 1343{,}92\) €."),
            E('ag8', 3, r"Soit \((u_n)\) définie par \(u_0=3\) et \(u_{n+1}=0{,}5\,u_n+1\). On pose \(v_n=u_n-2\). Montrer que \((v_n)\) est géométrique, puis exprimer \(u_n\) en fonction de \(n\).", r"\(v_{n+1}=u_{n+1}-2=0{,}5u_n+1-2=0{,}5u_n-1=0{,}5(u_n-2)=0{,}5\,v_n\).\n\((v_n)\) est géométrique de raison \(0{,}5\) et de premier terme \(v_0=1\). Donc \(v_n=0{,}5^n\) et \(u_n=2+0{,}5^n\).", r"Calcule \(v_{n+1}\) et fais apparaître \(v_n\)."),
            E('ag9', 3, r"Un loyer est de \(600\) € la 1<sup>re</sup> année, puis augmente de \(20\) € chaque année. Quelle somme totale aura-t-on versée au bout de \(10\) ans ?", r"Suite arithmétique : \(u_1=600\), \(r=20\), donc \(u_{10}=600+9\times20=780\).\n\(S=10\times\dfrac{600+780}{2}=6900\) €."),
            E('ag10', 3, r"Avec \(1000\) € placés à \(3\,\%\) par an, au bout de combien d'années le capital aura-t-il doublé ?", r"On cherche le plus petit \(n\) tel que \(1000\times1{,}03^n\geq 2000\), soit \(1{,}03^n\geq2\).\n\(1{,}03^{23}\approx1{,}974<2\) et \(1{,}03^{24}\approx2{,}033>2\). Il faut <b>24 ans</b>."),
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        'id': 'derivation', 'num': 4, 'domain': 'analyse', 'icon': '📉',
        'title': 'Dérivation et variations',
        'tagline': 'Nombre dérivé, tangente, fonction dérivée, étude des variations.',
        'video': {'id': 'uMSNllPBFhQ', 'title': 'LE COURS : La dérivation - Première'},
        'pdfs': [pdf('Cours 1 — Nombre dérivé, tangente', '19DeriP1M.pdf'),
                 pdf('Cours 2 — Fonction dérivée', '19DeriP2M.pdf'),
                 pdf('Cours 3 — Variations et extremums', '19DeriP3M.pdf')],
        'cours': [
            ('Nombre dérivé et tangente', r"Le nombre dérivé de \(f\) en \(a\) est \(f'(a)=\lim\limits_{h\to0}\dfrac{f(a+h)-f(a)}{h}\) : c'est la pente de la tangente en \(a\). Équation de la tangente : \(y=f'(a)(x-a)+f(a)\)."),
            ('Dérivées usuelles', r"\((k)'=0\), \((x)'=1\), \((x^n)'=nx^{n-1}\), \(\left(\dfrac1x\right)'=-\dfrac{1}{x^2}\), \((\sqrt{x})'=\dfrac{1}{2\sqrt{x}}\)."),
            ('Opérations', r"\((u+v)'=u'+v'\), \((ku)'=ku'\), \((uv)'=u'v+uv'\), \(\left(\dfrac uv\right)'=\dfrac{u'v-uv'}{v^2}\). Fonction composée avec une fonction affine : \(\big(g(ax+b)\big)'=a\,g'(ax+b)\)."),
            ('Variations', r"Si \(f'\geq0\) sur un intervalle, \(f\) y est croissante ; si \(f'\leq0\), elle est décroissante. Si \(f'\) s'annule <b>en changeant de signe</b> en \(a\), alors \(f(a)\) est un extremum local."),
            ('Méthode d\'étude', r"1) domaine ; 2) calcul de \(f'\) ; 3) signe de \(f'\) (souvent un trinôme ou un produit) ; 4) tableau de variations avec les valeurs aux bornes et aux extremums."),
        ],
        'formulas': [
            r"\(f'(a)=\lim\limits_{h\to0}\dfrac{f(a+h)-f(a)}{h}\)",
            r"\(y=f'(a)(x-a)+f(a)\)",
            r"\((uv)'=u'v+uv'\)",
            r"\(\left(\dfrac uv\right)'=\dfrac{u'v-uv'}{v^2}\)",
            r"\((x^n)'=nx^{n-1}\;;\;(\sqrt x)'=\dfrac1{2\sqrt x}\;;\;\left(\dfrac1x\right)'=-\dfrac1{x^2}\)",
        ],
        'pitfalls': [
            r"\((uv)'\neq u'v'\) : c'est \(u'v+uv'\).",
            r"Un point où \(f'(a)=0\) n'est un extremum que si \(f'\) <b>change de signe</b> (contre-exemple : \(x^3\) en \(0\)).",
            r"\(\sqrt{x}\) et \(\dfrac1x\) ne sont pas dérivables en \(0\).",
        ],
        'exercises': [
            E('de1', 1, r"Dériver \(f(x)=3x^2+2x-5\).", r"\(f'(x)=6x+2\)."),
            E('de2', 1, r"Dériver \(f(x)=x^3-3x\).", r"\(f'(x)=3x^2-3=3(x-1)(x+1)\)."),
            E('de3', 1, r"Déterminer la pente de la tangente à la courbe de \(f(x)=x^2\) au point d'abscisse \(3\).", r"\(f'(x)=2x\), donc la pente est \(f'(3)=6\)."),
            E('de4', 2, r"Déterminer l'équation de la tangente à la courbe de \(f(x)=x^2\) au point d'abscisse \(3\).", r"\(f(3)=9\) et \(f'(3)=6\).\n\(y=6(x-3)+9=6x-9\)."),
            E('de5', 2, r"Dériver \(f(x)=\dfrac{2x+1}{x-3}\) sur \(]3\,;+\infty[\).", r"\(u=2x+1\), \(v=x-3\) : \(f'(x)=\dfrac{2(x-3)-(2x+1)}{(x-3)^2}=\dfrac{-7}{(x-3)^2}\)."),
            E('de6', 2, r"Dériver \(f(x)=(x^2+1)(3x-2)\).", r"\(f'(x)=2x(3x-2)+3(x^2+1)=6x^2-4x+3x^2+3=9x^2-4x+3\)."),
            E('de7', 2, r"Dériver \(f(x)=x\sqrt{x}\) sur \(]0\,;+\infty[\).", r"\(f'(x)=1\times\sqrt x+x\times\dfrac{1}{2\sqrt x}=\sqrt x+\dfrac{\sqrt x}{2}=\dfrac{3}{2}\sqrt{x}\)."),
            E('de8', 2, r"Dériver \(f(x)=(3x-1)^4\).", r"On applique \(\big(g(ax+b)\big)'=a\,g'(ax+b)\) avec \(g(t)=t^4\), \(a=3\) :\n\(f'(x)=3\times4(3x-1)^3=12(3x-1)^3\)."),
            E('de9', 3, r"Retrouver, avec la définition du nombre dérivé, la valeur de \(f'(1)\) pour \(f(x)=x^2\).", r"Le taux d'accroissement est \(\dfrac{(1+h)^2-1}{h}=\dfrac{2h+h^2}{h}=2+h\). Quand \(h\to0\), il tend vers \(2\). Donc \(f'(1)=2\)."),
            E('de10', 3, r"Déterminer l'équation de la tangente à la courbe de \(f(x)=\dfrac1x\) au point d'abscisse \(2\).", r"\(f'(x)=-\dfrac1{x^2}\) donc \(f'(2)=-\dfrac14\) et \(f(2)=\dfrac12\).\n\(y=-\dfrac14(x-2)+\dfrac12=-\dfrac14x+1\)."),
            E('de11', 2, r"Dresser le tableau de variations de \(f(x)=x^3-3x\) sur \(\mathbb{R}\).", r"\(f'(x)=3(x-1)(x+1)\) est positif pour \(x\leq-1\), négatif sur \([-1\,;1]\), positif pour \(x\geq1\).\n\(f\) est donc croissante sur \(]-\infty\,;-1]\), décroissante sur \([-1\,;1]\), croissante sur \([1\,;+\infty[\).\nMaximum local \(f(-1)=2\), minimum local \(f(1)=-2\)."),
            E('de12', 3, r"Le bénéfice (en milliers d'euros) d'une entreprise est \(B(x)=-x^2+8x-7\) pour \(x\in[0\,;8]\) centaines d'objets produits. Pour quelle production le bénéfice est-il maximal ?", r"\(B'(x)=-2x+8\), qui s'annule en \(x=4\), positif avant et négatif après : \(B\) est maximale en \(x=4\).\n\(B(4)=-16+32-7=9\) : bénéfice maximal de \(9\) milliers d'euros pour \(400\) objets."),
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        'id': 'exponentielle', 'num': 5, 'domain': 'analyse', 'icon': '🚀',
        'title': 'Fonction exponentielle',
        'tagline': 'Définition, propriétés algébriques, dérivée et variations.',
        'video': {'id': 'aD03wqgxexk', 'title': 'LE COURS : La fonction exponentielle - Première'},
        'pdfs': [pdf('Cours — Fonction exponentielle', '19ExpoPM.pdf')],
        'cours': [
            ('Définition', r"La fonction exponentielle est l'unique fonction dérivable sur \(\mathbb{R}\) telle que \(f'=f\) et \(f(0)=1\). On la note \(x\mapsto e^x\) avec \(e=e^1\approx2{,}718\)."),
            ('Propriétés algébriques', r"Pour tous réels \(x,y\) et entier \(n\) : \(e^{x+y}=e^x\,e^y\), \(e^{-x}=\dfrac1{e^x}\), \(e^{x-y}=\dfrac{e^x}{e^y}\), \((e^x)^n=e^{nx}\). De plus \(e^x>0\) pour tout \(x\)."),
            ('Équations et inéquations', r"La fonction est strictement croissante : \(e^x=e^y\iff x=y\) et \(e^x<e^y\iff x<y\)."),
            ('Dérivées', r"\((e^x)'=e^x\) ; \((e^{u})'=u'e^{u}\) ; en particulier \((e^{ax+b})'=a\,e^{ax+b}\)."),
            ('Lien avec les suites', r"La suite \((e^{na})_n\) est géométrique de raison \(e^a\)."),
        ],
        'formulas': [
            r"\(e^0=1\;;\;e^1=e\approx2{,}718\;;\;e^x>0\)",
            r"\(e^{a+b}=e^a\,e^b\;;\;e^{a-b}=\dfrac{e^a}{e^b}\;;\;(e^a)^n=e^{na}\)",
            r"\((e^x)'=e^x\;;\;(e^{ax+b})'=a\,e^{ax+b}\)",
            r"\(e^a=e^b\iff a=b\;;\;e^a<e^b\iff a<b\)",
        ],
        'pitfalls': [
            r"\(e^{x+y}\neq e^x+e^y\) : la somme devient un <b>produit</b>.",
            r"\(e^x\) n'est jamais nulle : une équation du type \(e^x=0\) n'a pas de solution.",
            r"Pour résoudre \(e^{A}=e^{B}\), on ne \"simplifie\" pas les \(e\) : on utilise \(A=B\).",
        ],
        'exercises': [
            E('ex1', 1, r"Simplifier \(\dfrac{e^3\times e^{-1}}{e^2}\).", r"\(\dfrac{e^{3-1}}{e^2}=\dfrac{e^2}{e^2}=e^0=1\)."),
            E('ex2', 1, r"Dériver \(f(x)=e^x+x^2\).", r"\(f'(x)=e^x+2x\)."),
            E('ex3', 1, r"Dériver \(f(x)=(x+1)e^x\).", r"\(f'(x)=1\times e^x+(x+1)e^x=(x+2)e^x\)."),
            E('ex4', 2, r"Résoudre \(e^{2x-1}=e^{x+3}\).", r"\(2x-1=x+3\iff x=4\)."),
            E('ex5', 2, r"Résoudre \(e^{2x}-e^x=0\).", r"\(e^x(e^x-1)=0\). Comme \(e^x>0\), on a \(e^x=1=e^0\), donc \(x=0\).", r"Factorise par \(e^x\)."),
            E('ex6', 2, r"Dériver \(f(x)=e^{-2x+1}\).", r"\(f'(x)=-2\,e^{-2x+1}\)."),
            E('ex7', 2, r"Étudier les variations de \(f(x)=(x-1)e^x\).", r"\(f'(x)=e^x+(x-1)e^x=x\,e^x\). Comme \(e^x>0\), \(f'(x)\) est du signe de \(x\).\n\(f\) est décroissante sur \(]-\infty\,;0]\), croissante sur \([0\,;+\infty[\), avec un minimum \(f(0)=-1\)."),
            E('ex8', 2, r"Déterminer l'équation de la tangente à la courbe de \(\exp\) au point d'abscisse \(0\).", r"\(f(0)=1\) et \(f'(0)=e^0=1\). \(y=1\times(x-0)+1=x+1\)."),
            E('ex9', 3, r"Montrer que \(f(x)=\dfrac{e^x}{x^2+1}\) est croissante sur \(\mathbb{R}\).", r"\(f'(x)=\dfrac{e^x(x^2+1)-e^x\times2x}{(x^2+1)^2}=\dfrac{e^x(x^2-2x+1)}{(x^2+1)^2}=\dfrac{e^x(x-1)^2}{(x^2+1)^2}\geq0\).\nDonc \(f\) est croissante sur \(\mathbb{R}\).", r"Quotient : \((u/v)'\) avec \(u=e^x\), \(v=x^2+1\)."),
            E('ex10', 3, r"Montrer que la suite \(u_n=e^{2n}\) est géométrique et préciser sa raison.", r"\(u_{n+1}=e^{2(n+1)}=e^{2n+2}=e^{2n}\times e^2=e^2\,u_n\).\nC'est une suite géométrique de raison \(e^2\) et de premier terme \(u_0=1\)."),
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        'id': 'trigonometrie', 'num': 6, 'domain': 'analyse', 'icon': '🎡',
        'title': 'Trigonométrie',
        'tagline': 'Radians, cercle trigonométrique, cosinus et sinus, équations.',
        'video': {'id': 'wJjb3CSS3cg', 'title': 'LE COURS : Trigonométrie - Première'},
        'pdfs': [pdf('Cours 1 — Cercle trigonométrique', '19TrigoP1M.pdf'),
                 pdf('Cours 2 — Fonctions cosinus et sinus', '19TrigoP2M.pdf')],
        'cours': [
            ('Radians', r"\(\pi\) radians \(=180^\circ\). La longueur d'un arc de cercle de rayon \(R\) et d'angle \(x\) (en rad) est \(R\,x\). Un angle se repère modulo \(2\pi\) ; sa <b>mesure principale</b> est celle de \(]-\pi\,;\pi]\)."),
            ('Cosinus et sinus', r"Sur le cercle trigonométrique, le point \(M\) associé au réel \(x\) a pour coordonnées \((\cos x\,;\sin x)\). Donc \(-1\leq\cos x\leq1\), \(-1\leq\sin x\leq1\) et \(\cos^2x+\sin^2x=1\)."),
            ('Valeurs remarquables', r"\(\cos0=1\), \(\cos\frac\pi6=\frac{\sqrt3}{2}\), \(\cos\frac\pi4=\frac{\sqrt2}{2}\), \(\cos\frac\pi3=\frac12\), \(\cos\frac\pi2=0\). Pour le sinus, on lit la liste à l'envers : \(\sin0=0\), \(\sin\frac\pi6=\frac12\), \(\sin\frac\pi4=\frac{\sqrt2}2\), \(\sin\frac\pi3=\frac{\sqrt3}2\), \(\sin\frac\pi2=1\)."),
            ('Symétries', r"\(\cos(-x)=\cos x\), \(\sin(-x)=-\sin x\), \(\cos(\pi-x)=-\cos x\), \(\sin(\pi-x)=\sin x\), \(\cos(\tfrac\pi2-x)=\sin x\), \(\sin(\tfrac\pi2-x)=\cos x\)."),
            ('Périodicité et dérivées', r"\(\cos\) et \(\sin\) sont \(2\pi\)-périodiques. \(\cos'=-\sin\) et \(\sin'=\cos\)."),
        ],
        'formulas': [
            r"\(\cos^2x+\sin^2x=1\)",
            r"\(\cos(\pi-x)=-\cos x\;;\;\sin(\pi-x)=\sin x\)",
            r"\(\cos\!\left(\tfrac\pi2-x\right)=\sin x\;;\;\sin\!\left(\tfrac\pi2-x\right)=\cos x\)",
            r"\(\cos'=-\sin\;;\;\sin'=\cos\)",
            r"\(\cos(x+2\pi)=\cos x\;;\;\sin(x+2\pi)=\sin x\)",
        ],
        'pitfalls': [
            r"Régler la calculatrice en <b>radians</b> (et pas en degrés).",
            r"\(\cos x=a\) a en général <b>deux</b> solutions dans \(]-\pi\,;\pi]\) : \(x\) et \(-x\).",
            r"\(\sin(2x)\neq2\sin x\).",
        ],
        'exercises': [
            E('tr1', 1, r"Convertir \(60^\circ\) en radians et \(\dfrac{3\pi}{4}\) en degrés.", r"\(60^\circ=60\times\dfrac{\pi}{180}=\dfrac\pi3\) rad.\n\(\dfrac{3\pi}4\) rad \(=\dfrac{3\times180}{4}=135^\circ\)."),
            E('tr2', 1, r"Calculer \(\cos\dfrac\pi6+\sin\dfrac\pi3\).", r"\(\dfrac{\sqrt3}{2}+\dfrac{\sqrt3}{2}=\sqrt3\)."),
            E('tr3', 2, r"Déterminer la mesure principale de \(\dfrac{13\pi}{3}\).", r"\(\dfrac{13\pi}{3}-4\pi=\dfrac{13\pi-12\pi}{3}=\dfrac\pi3\in]-\pi\,;\pi]\). La mesure principale est \(\dfrac\pi3\)."),
            E('tr4', 2, r"Déterminer la mesure principale de \(-\dfrac{17\pi}{4}\).", r"\(-\dfrac{17\pi}{4}+4\pi=\dfrac{-17\pi+16\pi}{4}=-\dfrac\pi4\). La mesure principale est \(-\dfrac\pi4\)."),
            E('tr5', 2, r"Calculer \(\cos\dfrac{2\pi}{3}\) et \(\sin\dfrac{2\pi}{3}\).", r"\(\dfrac{2\pi}3=\pi-\dfrac\pi3\) donc \(\cos\dfrac{2\pi}3=-\cos\dfrac\pi3=-\dfrac12\) et \(\sin\dfrac{2\pi}3=\sin\dfrac\pi3=\dfrac{\sqrt3}2\).", r"Écris \(\frac{2\pi}{3}=\pi-\frac\pi3\)."),
            E('tr6', 2, r"Résoudre \(\cos x=\dfrac12\) sur \(]-\pi\,;\pi]\).", r"\(\cos\dfrac\pi3=\dfrac12\), et \(\cos\) est paire : \(S=\left\{-\dfrac\pi3\,;\,\dfrac\pi3\right\}\)."),
            E('tr7', 2, r"Résoudre \(\sin x=-\dfrac{\sqrt2}{2}\) sur \(]-\pi\,;\pi]\).", r"\(\sin\dfrac\pi4=\dfrac{\sqrt2}{2}\). Les solutions sont les points d'ordonnée négative : \(x=-\dfrac\pi4\) et \(x=-\pi+\dfrac\pi4=-\dfrac{3\pi}4\).\n\(S=\left\{-\dfrac{3\pi}4\,;\,-\dfrac\pi4\right\}\)."),
            E('tr8', 3, r"Sachant que \(\cos x=\dfrac35\) et \(x\in[0\,;\pi]\), calculer \(\sin x\).", r"\(\sin^2x=1-\cos^2x=1-\dfrac9{25}=\dfrac{16}{25}\). Sur \([0\,;\pi]\), \(\sin x\geq0\), donc \(\sin x=\dfrac45\)."),
            E('tr9', 3, r"Simplifier \(\cos(\pi-x)+\sin\left(\dfrac\pi2-x\right)\).", r"\(\cos(\pi-x)=-\cos x\) et \(\sin\left(\dfrac\pi2-x\right)=\cos x\).\nLa somme vaut \(0\)."),
            E('tr10', 3, r"Résoudre \(2\sin^2x-\sin x-1=0\) sur \([0\,;2\pi[\).", r"On pose \(X=\sin x\) : \(2X^2-X-1=0\), \(\Delta=9\), \(X=1\) ou \(X=-\dfrac12\).\n\(\sin x=1\iff x=\dfrac\pi2\). \(\sin x=-\dfrac12\iff x=\dfrac{7\pi}6\) ou \(x=\dfrac{11\pi}6\).\n\(S=\left\{\dfrac\pi2\,;\,\dfrac{7\pi}6\,;\,\dfrac{11\pi}6\right\}\).", r"Change de variable \(X=\sin x\)."),
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        'id': 'produit-scalaire', 'num': 7, 'domain': 'geometrie', 'icon': '✖️',
        'title': 'Produit scalaire',
        'tagline': 'Définitions, orthogonalité, angles, Al-Kashi.',
        'video': {'id': 'dII7myZuLvo', 'title': 'LE COURS : Produit scalaire - Première'},
        'pdfs': [pdf('Cours 1 — Produit scalaire : définitions', '19Prodscal1M.pdf'),
                 pdf('Cours 2 — Applications', '19Prodscal2M.pdf')],
        'cours': [
            ('Trois expressions', r"\(\vec u\cdot\vec v=\|\vec u\|\,\|\vec v\|\cos(\vec u,\vec v)\) ; avec les coordonnées \(\vec u\cdot\vec v=xx'+yy'\) ; et \(\vec u\cdot\vec v=\dfrac12\left(\|\vec u+\vec v\|^2-\|\vec u\|^2-\|\vec v\|^2\right)\)."),
            ('Propriétés', r"Le produit scalaire est symétrique et bilinéaire. On a \(\vec u\cdot\vec u=\|\vec u\|^2\) et \(\|\vec u\|=\sqrt{x^2+y^2}\)."),
            ('Orthogonalité', r"\(\vec u\perp\vec v\iff\vec u\cdot\vec v=0\)."),
            ('Calcul d\'un angle', r"\(\cos(\vec u,\vec v)=\dfrac{\vec u\cdot\vec v}{\|\vec u\|\,\|\vec v\|}\)."),
            ('Al-Kashi', r"Dans un triangle \(ABC\) avec \(a=BC\), \(b=AC\), \(c=AB\) : \(a^2=b^2+c^2-2bc\cos\widehat{A}\)."),
            ('Cercle de diamètre [AB]', r"L'ensemble des points \(M\) tels que \(\overrightarrow{MA}\cdot\overrightarrow{MB}=0\) est le cercle de diamètre \([AB]\)."),
        ],
        'formulas': [
            r"\(\vec u\cdot\vec v=\|\vec u\|\|\vec v\|\cos(\vec u,\vec v)\)",
            r"\(\vec u\cdot\vec v=xx'+yy'\)",
            r"\(\vec u\perp\vec v\iff\vec u\cdot\vec v=0\)",
            r"\(a^2=b^2+c^2-2bc\cos\widehat A\)",
            r"\(MA^2+MB^2=2MI^2+\dfrac{AB^2}{2}\) (où \(I\) est le milieu de \([AB]\))",
        ],
        'pitfalls': [
            r"Le produit scalaire est un <b>nombre</b>, pas un vecteur.",
            r"\(\vec u\cdot\vec v=0\) n'implique pas \(\vec u=\vec 0\) ou \(\vec v=\vec 0\) : il peut s'agir de vecteurs orthogonaux.",
            r"Pour un angle, vérifier que \(\cos\) donne bien un angle de \([0\,;\pi]\) avec la calculatrice en degrés ou en radians selon la demande.",
        ],
        'exercises': [
            E('ps1', 1, r"Calculer \(\vec u\cdot\vec v\) pour \(\vec u(2\,;3)\) et \(\vec v(4\,;-1)\).", r"\(2\times4+3\times(-1)=8-3=5\)."),
            E('ps2', 1, r"Calculer la norme de \(\vec u(3\,;4)\).", r"\(\|\vec u\|=\sqrt{9+16}=5\)."),
            E('ps3', 2, r"Calculer \(\overrightarrow{AB}\cdot\overrightarrow{AC}\) avec \(A(1\,;1)\), \(B(4\,;2)\), \(C(2\,;5)\).", r"\(\overrightarrow{AB}(3\,;1)\) et \(\overrightarrow{AC}(1\,;4)\) donc \(\overrightarrow{AB}\cdot\overrightarrow{AC}=3\times1+1\times4=7\)."),
            E('ps4', 2, r"Dans un triangle \(ABC\), \(AB=5\), \(AC=4\) et \(\widehat{BAC}=60^\circ\). Calculer \(\overrightarrow{AB}\cdot\overrightarrow{AC}\).", r"\(\overrightarrow{AB}\cdot\overrightarrow{AC}=5\times4\times\cos60^\circ=20\times\dfrac12=10\)."),
            E('ps5', 2, r"Les vecteurs \(\vec u(1\,;2)\) et \(\vec v(4\,;-2)\) sont-ils orthogonaux ?", r"\(\vec u\cdot\vec v=1\times4+2\times(-2)=0\) : oui, ils sont orthogonaux."),
            E('ps6', 2, r"Déterminer \(k\) pour que \(\vec u(k\,;3)\) et \(\vec v(2\,;-1)\) soient orthogonaux.", r"\(\vec u\cdot\vec v=2k-3=0\iff k=\dfrac32\)."),
            E('ps7', 2, r"Déterminer l'angle entre \(\vec u(1\,;0)\) et \(\vec v(1\,;1)\).", r"\(\cos\theta=\dfrac{1}{1\times\sqrt2}=\dfrac{\sqrt2}{2}\), donc \(\theta=45^\circ\)."),
            E('ps8', 3, r"Un triangle a pour côtés \(a=5\), \(b=7\), \(c=8\). Calculer l'angle \(\widehat{C}\) (opposé au côté \(c\)).", r"Al-Kashi : \(c^2=a^2+b^2-2ab\cos C\), soit \(64=25+49-70\cos C\).\n\(\cos C=\dfrac{10}{70}=\dfrac17\) donc \(C\approx81{,}8^\circ\).", r"Isole \(\cos C\)."),
            E('ps9', 3, r"Avec \(A(0\,;0)\), \(B(4\,;0)\), \(C(1\,;3)\), calculer l'angle \(\widehat{BAC}\) à \(0{,}1^\circ\) près.", r"\(\overrightarrow{AB}(4\,;0)\), \(\overrightarrow{AC}(1\,;3)\) : \(\overrightarrow{AB}\cdot\overrightarrow{AC}=4\), \(AB=4\), \(AC=\sqrt{10}\).\n\(\cos\widehat A=\dfrac{4}{4\sqrt{10}}=\dfrac1{\sqrt{10}}\approx0{,}316\) donc \(\widehat A\approx71{,}6^\circ\)."),
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        'id': 'geometrie-repere', 'num': 8, 'domain': 'geometrie', 'icon': '🧭',
        'title': 'Géométrie repérée',
        'tagline': 'Équations de droites, vecteur normal, cercles.',
        'video': {'id': 'EehP4SFpo5c', 'title': 'LE COURS : Géométrie repérée - Première'},
        'pdfs': [pdf('Cours — Géométrie repérée', '19RepM.pdf')],
        'cours': [
            ('Équation cartésienne d\'une droite', r"Toute droite a une équation \(ax+by+c=0\) avec \((a\,;b)\neq(0\,;0)\). Le vecteur \(\vec n(a\,;b)\) est <b>normal</b> à la droite et \(\vec u(-b\,;a)\) en est un vecteur <b>directeur</b>."),
            ('Droite définie par un point et un vecteur normal', r"Si \(A(x_A\,;y_A)\) et \(\vec n(a\,;b)\) : \(M\in d\iff a(x-x_A)+b(y-y_A)=0\)."),
            ('Parallélisme et perpendicularité', r"Deux droites sont parallèles si leurs vecteurs normaux sont colinéaires : \(ab'-a'b=0\). Elles sont perpendiculaires si \(aa'+bb'=0\)."),
            ('Équation de cercle', r"Le cercle de centre \(\Omega(a\,;b)\) et de rayon \(R\) a pour équation \((x-a)^2+(y-b)^2=R^2\). Pour le cercle de diamètre \([AB]\) : \(\overrightarrow{MA}\cdot\overrightarrow{MB}=0\)."),
            ('Rappels', r"Distance \(AB=\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}\) ; milieu \(\left(\dfrac{x_A+x_B}2\,;\dfrac{y_A+y_B}2\right)\) ; pente \(m=\dfrac{y_B-y_A}{x_B-x_A}\)."),
        ],
        'formulas': [
            r"\(d : ax+by+c=0\;,\quad\vec n(a\,;b)\text{ normal},\;\vec u(-b\,;a)\text{ directeur}\)",
            r"\(a(x-x_A)+b(y-y_A)=0\)",
            r"\((x-a)^2+(y-b)^2=R^2\)",
            r"\(AB=\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}\)",
        ],
        'pitfalls': [
            r"Le vecteur directeur est \((-b\,;a)\) et non \((a\,;b)\) (qui est le vecteur normal).",
            r"Dans \((x-a)^2+(y-b)^2=R^2\), les coordonnées du centre ont le signe <b>opposé</b> à celui qui apparaît.",
            r"Pour trouver centre et rayon à partir de \(x^2+y^2+\dots=0\), il faut compléter les carrés.",
        ],
        'exercises': [
            E('gr1', 1, r"Déterminer l'équation réduite de la droite passant par \(A(1\,;2)\) et \(B(3\,;8)\).", r"Pente \(m=\dfrac{8-2}{3-1}=3\), puis \(p=2-3\times1=-1\). \(y=3x-1\)."),
            E('gr2', 1, r"Déterminer le milieu de \([AB]\) avec \(A(1\,;2)\) et \(B(5\,;8)\).", r"\(M\left(\dfrac{1+5}2\,;\dfrac{2+8}2\right)=(3\,;5)\)."),
            E('gr3', 1, r"Calculer la distance entre \(A(1\,;2)\) et \(B(4\,;6)\).", r"\(AB=\sqrt{3^2+4^2}=5\)."),
            E('gr4', 2, r"Donner un vecteur directeur de la droite \(d : 2x-3y+6=0\).", r"Un vecteur directeur est \((-b\,;a)=(3\,;2)\)."),
            E('gr5', 2, r"Déterminer une équation de la droite passant par \(A(1\,;2)\) et de vecteur normal \(\vec n(3\,;-1)\).", r"\(3(x-1)-(y-2)=0\iff3x-y-1=0\)."),
            E('gr6', 2, r"Les droites \(d_1 : 2x+y-3=0\) et \(d_2 : 4x+2y+1=0\) sont-elles parallèles ?", r"Normaux \((2\,;1)\) et \((4\,;2)\) : colinéaires (\(2\times2-4\times1=0\)). Elles sont parallèles, et distinctes car \((0\,;3)\in d_1\) mais \(0+6+1\neq0\)."),
            E('gr7', 2, r"Montrer que \(d : x+2y-1=0\) et \(d' : 2x-y+5=0\) sont perpendiculaires.", r"Normaux \((1\,;2)\) et \((2\,;-1)\) : \(1\times2+2\times(-1)=0\). Elles sont perpendiculaires."),
            E('gr8', 1, r"Écrire l'équation du cercle de centre \(\Omega(2\,;-1)\) et de rayon \(3\).", r"\((x-2)^2+(y+1)^2=9\)."),
            E('gr9', 3, r"Déterminer le centre et le rayon du cercle d'équation \(x^2+y^2-4x+6y-3=0\).", r"On complète les carrés : \((x-2)^2-4+(y+3)^2-9-3=0\), soit \((x-2)^2+(y+3)^2=16\).\nCentre \((2\,;-3)\), rayon \(4\)."),
            E('gr10', 3, r"Déterminer les points d'intersection de la droite \(y=x+1\) et du cercle \(x^2+y^2=5\).", r"\(x^2+(x+1)^2=5\iff2x^2+2x-4=0\iff x^2+x-2=0\). \(\Delta=9\), \(x=1\) ou \(x=-2\).\nPoints : \((1\,;2)\) et \((-2\,;-1)\)."),
            E('gr11', 3, r"Déterminer l'équation du cercle de diamètre \([AB]\) avec \(A(1\,;2)\) et \(B(5\,;4)\).", r"Centre \(I(3\,;3)\), rayon \(\dfrac{AB}{2}=\dfrac{\sqrt{16+4}}2=\sqrt5\).\n\((x-3)^2+(y-3)^2=5\).", r"Centre = milieu de \([AB]\)."),
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        'id': 'probas-conditionnelles', 'num': 9, 'domain': 'probas', 'icon': '🌳',
        'title': 'Probabilités conditionnelles',
        'tagline': 'Arbres pondérés, probabilités totales, indépendance.',
        'video': {'id': '5oBnmZVrOXE', 'title': 'LE COURS : Probabilités conditionnelles - Première/Terminale'},
        'pdfs': [pdf('Cours — Probabilités conditionnelles et indépendance', '19CondPM.pdf')],
        'cours': [
            ('Probabilité conditionnelle', r"Si \(P(A)\neq0\) : \(P_A(B)=\dfrac{P(A\cap B)}{P(A)}\), donc \(P(A\cap B)=P(A)\times P_A(B)\)."),
            ('Arbre pondéré', r"La somme des probabilités des branches issues d'un même nœud vaut \(1\). La probabilité d'un chemin est le <b>produit</b> des probabilités de ses branches."),
            ('Probabilités totales', r"Si \(A_1,\dots,A_n\) forment une partition de l'univers : \(P(B)=P(A_1\cap B)+\dots+P(A_n\cap B)\)."),
            ('Indépendance', r"\(A\) et \(B\) sont indépendants si \(P(A\cap B)=P(A)P(B)\), ce qui équivaut à \(P_A(B)=P(B)\)."),
            ('Inverser un conditionnement', r"\(P_B(A)=\dfrac{P(A\cap B)}{P(B)}=\dfrac{P(A)\,P_A(B)}{P(B)}\)."),
            ('Événement « au moins un »', r"\(P(\text{au moins un})=1-P(\text{aucun})\)."),
        ],
        'formulas': [
            r"\(P_A(B)=\dfrac{P(A\cap B)}{P(A)}\)",
            r"\(P(A\cap B)=P(A)\,P_A(B)\)",
            r"\(P(B)=P(A\cap B)+P(\overline{A}\cap B)\)",
            r"\(A,B\text{ indépendants}\iff P(A\cap B)=P(A)P(B)\)",
            r"\(P(A\cup B)=P(A)+P(B)-P(A\cap B)\)",
        ],
        'pitfalls': [
            r"\(P_A(B)\neq P_B(A)\) en général : attention au sens du conditionnement.",
            r"\(A\) et \(B\) <b>incompatibles</b> (\(A\cap B=\emptyset\)) n'est pas la même chose qu'<b>indépendants</b>.",
            r"Sur un arbre, ne pas oublier de multiplier le long d'un chemin puis d'<b>additionner</b> les chemins qui mènent à l'événement.",
        ],
        'exercises': [
            E('pc1', 1, r"On donne \(P(A)=0{,}3\), \(P(B)=0{,}4\) et \(P(A\cap B)=0{,}1\). Calculer \(P(A\cup B)\).", r"\(P(A\cup B)=0{,}3+0{,}4-0{,}1=0{,}6\)."),
            E('pc2', 1, r"Avec les mêmes données, calculer \(P_B(A)\).", r"\(P_B(A)=\dfrac{P(A\cap B)}{P(B)}=\dfrac{0{,}1}{0{,}4}=0{,}25\)."),
            E('pc3', 1, r"On sait que \(P_B(A)=0{,}7\) et \(P(B)=0{,}5\). Calculer \(P(A\cap B)\).", r"\(P(A\cap B)=P(B)\times P_B(A)=0{,}5\times0{,}7=0{,}35\)."),
            E('pc4', 2, r"Une usine a deux machines : \(A\) produit \(60\,\%\) des pièces avec \(2\,\%\) de défauts, \(B\) produit \(40\,\%\) avec \(5\,\%\) de défauts. Quelle est la probabilité qu'une pièce prise au hasard soit défectueuse ?", r"Avec l'arbre et la formule des probabilités totales :\n\(P(D)=0{,}6\times0{,}02+0{,}4\times0{,}05=0{,}012+0{,}020=0{,}032\).", r"Fais un arbre : machine puis défaut."),
            E('pc5', 2, r"Dans l'exercice précédent, sachant qu'une pièce est défectueuse, quelle est la probabilité qu'elle vienne de la machine \(B\) ?", r"\(P_D(B)=\dfrac{P(B\cap D)}{P(D)}=\dfrac{0{,}02}{0{,}032}=0{,}625\)."),
            E('pc6', 2, r"On a \(P(A)=0{,}5\), \(P(B)=0{,}4\) et \(P(A\cap B)=0{,}2\). \(A\) et \(B\) sont-ils indépendants ?", r"\(P(A)\times P(B)=0{,}5\times0{,}4=0{,}2=P(A\cap B)\) : oui, ils sont indépendants."),
            E('pc7', 2, r"On lance un dé équilibré \(5\) fois. Quelle est la probabilité d'obtenir au moins un \(6\) ?", r"\(1-P(\text{aucun }6)=1-\left(\dfrac56\right)^5\approx0{,}598\)."),
            E('pc8', 3, r"Une maladie touche \(1\,\%\) de la population. Un test est positif pour \(95\,\%\) des malades et pour \(4\,\%\) des personnes saines. Une personne a un test positif : quelle est la probabilité qu'elle soit malade ?", r"\(P(T)=0{,}01\times0{,}95+0{,}99\times0{,}04=0{,}0095+0{,}0396=0{,}0491\).\n\(P_T(M)=\dfrac{0{,}0095}{0{,}0491}\approx0{,}193\), soit environ <b>19 %</b> seulement (la maladie est rare !).", r"Construis l'arbre : malade ou non, puis test."),
            E('pc9', 3, r"Une urne contient \(3\) boules rouges et \(2\) bleues. On tire deux boules successivement sans remise. Calculer la probabilité de tirer deux boules rouges, puis deux boules de la même couleur.", r"\(P(RR)=\dfrac35\times\dfrac24=\dfrac3{10}\) et \(P(BB)=\dfrac25\times\dfrac14=\dfrac1{10}\).\nMême couleur : \(\dfrac3{10}+\dfrac1{10}=\dfrac25\)."),
            E('pc10', 2, r"On tire une carte dans un jeu de \(32\) cartes. Probabilité d'obtenir un cœur ou un roi ?", r"\(P(C\cup R)=\dfrac8{32}+\dfrac4{32}-\dfrac1{32}=\dfrac{11}{32}\approx0{,}344\)."),
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        'id': 'variables-aleatoires', 'num': 10, 'domain': 'probas', 'icon': '🎰',
        'title': 'Variables aléatoires et loi binomiale',
        'tagline': 'Loi, espérance, variance, schéma de Bernoulli.',
        'video': {'id': 'krbtyBDeRqQ', 'title': 'LE COURS : Variables aléatoires - Première'},
        'pdfs': [pdf('Cours — Variables aléatoires', '19vaPM.pdf')],
        'cours': [
            ('Loi, espérance, variance', r"Pour \(X\) prenant les valeurs \(x_i\) avec les probabilités \(p_i\) : \(E(X)=\sum p_ix_i\), \(V(X)=\sum p_i(x_i-E(X))^2=E(X^2)-E(X)^2\) et \(\sigma(X)=\sqrt{V(X)}\)."),
            ('Transformation affine', r"\(E(aX+b)=aE(X)+b\), \(V(aX+b)=a^2V(X)\), \(\sigma(aX+b)=|a|\sigma(X)\)."),
            ('Schéma de Bernoulli', r"Une épreuve de Bernoulli a deux issues (succès de probabilité \(p\), échec). Un schéma de Bernoulli répète \(n\) fois, de façon <b>identique et indépendante</b>, une épreuve de Bernoulli."),
            ('Loi binomiale \\(\\mathcal B(n\\,;p)\\)', r"Si \(X\) compte les succès : \(P(X=k)=\dbinom nk p^k(1-p)^{n-k}\), avec \(E(X)=np\) et \(V(X)=np(1-p)\)."),
            ('Coefficients binomiaux', r"\(\dbinom n0=1\), \(\dbinom n1=n\), \(\dbinom nk=\dbinom n{n-k}\) ; on les lit dans le triangle de Pascal ou à la calculatrice (touche nCr)."),
        ],
        'formulas': [
            r"\(E(X)=\sum p_ix_i\;;\;V(X)=E(X^2)-E(X)^2\)",
            r"\(E(aX+b)=aE(X)+b\;;\;V(aX+b)=a^2V(X)\)",
            r"\(P(X=k)=\dbinom nk p^k(1-p)^{n-k}\)",
            r"\(E(X)=np\;;\;V(X)=np(1-p)\)",
        ],
        'pitfalls': [
            r"Pour utiliser la loi binomiale : vérifier <b>répétitions identiques et indépendantes</b> (un tirage sans remise ne convient pas).",
            r"La somme de toutes les probabilités d'une loi vaut \(1\) : vérifie-le !",
            r"\(V(aX+b)=a^2V(X)\) : le \(b\) disparaît et \(a\) passe au carré.",
        ],
        'exercises': [
            E('va1', 1, r"\(X\) prend les valeurs \(0\), \(1\), \(2\) avec les probabilités \(0{,}2\), \(0{,}5\), \(0{,}3\). Calculer \(E(X)\), \(V(X)\) et \(\sigma(X)\).", r"\(E(X)=0+0{,}5+0{,}6=1{,}1\).\n\(E(X^2)=0+0{,}5+1{,}2=1{,}7\) donc \(V(X)=1{,}7-1{,}21=0{,}49\) et \(\sigma(X)=0{,}7\)."),
            E('va2', 1, r"\(X\) suit la loi binomiale \(\mathcal B(4\,;0{,}5)\). Calculer \(P(X=2)\).", r"\(\dbinom42\times0{,}5^2\times0{,}5^2=6\times0{,}0625=0{,}375\)."),
            E('va3', 2, r"On mise \(2\) € puis on lance un dé : si on obtient \(6\), on reçoit \(9\) €, sinon rien. Soit \(G\) le gain algébrique. Calculer \(E(G)\). Le jeu est-il équitable ?", r"Gain \(+7\) avec la probabilité \(\dfrac16\), gain \(-2\) avec la probabilité \(\dfrac56\).\n\(E(G)=\dfrac76-\dfrac{10}6=-0{,}5\) €. Le jeu est défavorable au joueur (non équitable)."),
            E('va4', 2, r"\(X\) suit \(\mathcal B(10\,;0{,}3)\). Calculer \(E(X)\) et \(V(X)\).", r"\(E(X)=10\times0{,}3=3\) et \(V(X)=10\times0{,}3\times0{,}7=2{,}1\)."),
            E('va5', 2, r"\(X\) suit \(\mathcal B(5\,;0{,}2)\). Calculer \(P(X=0)\) puis \(P(X\geq1)\).", r"\(P(X=0)=0{,}8^5=0{,}32768\).\n\(P(X\geq1)=1-0{,}32768=0{,}67232\)."),
            E('va6', 2, r"On lance \(3\) fois une pièce équilibrée ; \(X\) est le nombre de « pile ». Donner la loi de \(X\).", r"\(X\sim\mathcal B(3\,;0{,}5)\) : \(P(X=0)=\dfrac18\), \(P(X=1)=\dfrac38\), \(P(X=2)=\dfrac38\), \(P(X=3)=\dfrac18\)."),
            E('va7', 3, r"\(X\) suit \(\mathcal B(6\,;0{,}4)\). Calculer \(P(X=3)\).", r"\(\dbinom63\times0{,}4^3\times0{,}6^3=20\times0{,}064\times0{,}216=0{,}27648\)."),
            E('va8', 3, r"\(X\) suit \(\mathcal B(8\,;0{,}5)\). Calculer \(P(X\geq7)\).", r"\(P(X=7)+P(X=8)=\dfrac{8+1}{2^8}=\dfrac9{256}\approx0{,}035\)."),
            E('va9', 3, r"Un QCM comporte \(10\) questions à \(4\) choix dont une seule bonne réponse. Un élève répond au hasard. Quelle est la probabilité d'avoir au moins une bonne réponse ?", r"\(X\sim\mathcal B(10\,;0{,}25)\). \(P(X\geq1)=1-0{,}75^{10}\approx1-0{,}0563=0{,}944\)."),
            E('va10', 3, r"\(E(X)=1\) et \(V(X)=4\). On pose \(Y=2X+3\). Calculer \(E(Y)\), \(V(Y)\), \(\sigma(Y)\).", r"\(E(Y)=2\times1+3=5\), \(V(Y)=2^2\times4=16\), \(\sigma(Y)=4\)."),
        ],
    },
]
