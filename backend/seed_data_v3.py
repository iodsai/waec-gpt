"""V3 — WAEC Further Mathematics (Elective) content.

Three live topics: Statistics & Probability, Calculus, Vectors.
Five coming-soon: Sets & Logic, Surds & Polynomials, Sequences & Binomial, Matrices, Mechanics.
"""

TOPICS_V3 = [
    {"id": "statistics", "name": "Statistics & Probability", "status": "available",
     "description": "Measures, dispersion, correlation, probability, permutations & combinations.",
     "icon": "BarChart3"},
    {"id": "calculus", "name": "Calculus", "status": "available",
     "description": "Limits, differentiation, integration and applications.",
     "icon": "TrendingUp"},
    {"id": "vectors", "name": "Vectors", "status": "available",
     "description": "Vector algebra (2D & 3D), magnitude, dot product, applications.",
     "icon": "MoveUpRight"},
    {"id": "sets-logic", "name": "Sets & Logic", "status": "coming_soon",
     "description": "Set operations, Venn diagrams, propositional logic, truth tables.",
     "icon": "CircleDot"},
    {"id": "surds-polynomials", "name": "Functions, Surds & Polynomials", "status": "coming_soon",
     "description": "Functions, mappings, surds, polynomial factor & remainder theorems.",
     "icon": "Sigma"},
    {"id": "sequences-binomial", "name": "Sequences & Binomial", "status": "coming_soon",
     "description": "AP, GP, binomial expansion and applications.",
     "icon": "ListOrdered"},
    {"id": "matrices", "name": "Matrices & Determinants", "status": "coming_soon",
     "description": "Matrix algebra, determinants, inverse, systems of equations.",
     "icon": "Grid3x3"},
    {"id": "mechanics", "name": "Mechanics", "status": "coming_soon",
     "description": "Kinematics, forces, work, energy, power.",
     "icon": "Move"},
]

SUBTOPICS_BY_TOPIC_V3 = {
    "statistics": [
        {"id": "measures-of-location", "name": "Measures of Location"},
        {"id": "measures-of-spread", "name": "Measures of Spread"},
        {"id": "correlation", "name": "Correlation"},
        {"id": "probability", "name": "Probability"},
        {"id": "perms-combinations", "name": "Permutations & Combinations"},
    ],
    "calculus": [
        {"id": "limits", "name": "Limits"},
        {"id": "differentiation", "name": "Differentiation"},
        {"id": "applications-differentiation", "name": "Applications of Differentiation"},
        {"id": "integration", "name": "Integration"},
        {"id": "applications-integration", "name": "Applications of Integration"},
    ],
    "vectors": [
        {"id": "vector-algebra-2d", "name": "Vector Algebra (2D)"},
        {"id": "vectors-3d", "name": "3D Vectors"},
        {"id": "magnitude-direction", "name": "Magnitude & Direction"},
        {"id": "scalar-product", "name": "Scalar (Dot) Product"},
        {"id": "vectors-applications", "name": "Vector Applications"},
    ],
}

LESSONS_V3 = {
    # ---- STATISTICS ----
    "measures-of-location": {
        "title": "Measures of Location", "topic": "statistics",
        "summary": "Mean, median and mode summarise where data is centred.",
        "notes": [
            {"heading": "Definitions",
             "body": "**Mean**: $\\bar{x} = \\frac{\\sum x}{n}$. **Median**: the middle value when data is ordered (or average of the two middle values if $n$ is even). **Mode**: the most frequent value."},
            {"heading": "Grouped Data Mean",
             "body": "For frequency distribution: $\\bar{x} = \\frac{\\sum fx}{\\sum f}$ where $x$ is the class midpoint."},
            {"heading": "Worked Example",
             "body": "Find the mean of: 4, 7, 9, 12, 8. $\\bar{x}=\\frac{4+7+9+12+8}{5}=\\frac{40}{5}=8$."},
        ]},
    "measures-of-spread": {
        "title": "Measures of Spread", "topic": "statistics",
        "summary": "Variance & standard deviation measure how far data deviates from the mean.",
        "notes": [
            {"heading": "Formulas",
             "body": "**Variance** $\\sigma^2 = \\frac{\\sum(x-\\bar{x})^2}{n}$. **Standard deviation** $\\sigma = \\sqrt{\\sigma^2}$. **Range** $= \\max - \\min$."},
            {"heading": "Computational Form",
             "body": "$\\sigma^2 = \\frac{\\sum x^2}{n} - \\bar{x}^2$ — often easier to compute."},
            {"heading": "Worked Example",
             "body": "Find $\\sigma$ of 2, 4, 4, 4, 5, 5, 7, 9. $\\bar{x}=5$. $\\sigma^2 = \\frac{(9+1+1+1+0+0+4+16)}{8}=4$. So $\\sigma=2$."},
        ]},
    "correlation": {
        "title": "Correlation", "topic": "statistics",
        "summary": "How strongly two variables move together. Spearman's rank correlation is most-tested in WAEC FM.",
        "notes": [
            {"heading": "Spearman's Rank",
             "body": "$$r_s = 1 - \\frac{6\\sum d^2}{n(n^2 - 1)}$$ where $d$ is the difference in ranks for each pair, $n$ is the number of pairs."},
            {"heading": "Interpretation",
             "body": "$r_s = 1$: perfect positive. $r_s = -1$: perfect negative. $r_s \\approx 0$: no correlation."},
            {"heading": "Worked Example",
             "body": "If $\\sum d^2 = 10$ for $n=5$ pairs, $r_s = 1 - \\frac{60}{5 \\times 24} = 1 - 0.5 = 0.5$."},
        ]},
    "probability": {
        "title": "Probability", "topic": "statistics",
        "summary": "P(event) = favourable / total. Independent events multiply; mutually exclusive events add.",
        "notes": [
            {"heading": "Rules",
             "body": "**Addition** (mutually exclusive): $P(A \\cup B) = P(A) + P(B)$. **General**: $P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$. **Multiplication** (independent): $P(A \\cap B) = P(A) \\cdot P(B)$. **Conditional**: $P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}$."},
            {"heading": "Worked Example",
             "body": "A bag has 3 red, 5 blue balls. Two are picked WITHOUT replacement. $P(\\text{both red}) = \\frac{3}{8} \\cdot \\frac{2}{7} = \\frac{6}{56} = \\frac{3}{28}$."},
        ]},
    "perms-combinations": {
        "title": "Permutations & Combinations", "topic": "statistics",
        "summary": "Counting arrangements (order matters) and selections (order doesn't).",
        "notes": [
            {"heading": "Formulas",
             "body": "**Permutations**: $^nP_r = \\frac{n!}{(n-r)!}$. **Combinations**: $^nC_r = \\frac{n!}{r!(n-r)!}$."},
            {"heading": "Worked Example",
             "body": "How many ways can 3 prefects be chosen from 8 students? $^8C_3 = \\frac{8!}{3!5!} = \\frac{8 \\cdot 7 \\cdot 6}{6} = 56$."},
        ]},
    # ---- CALCULUS ----
    "limits": {
        "title": "Limits", "topic": "calculus",
        "summary": "$\\lim_{x \\to a} f(x)$ is the value $f(x)$ approaches as $x$ approaches $a$.",
        "notes": [
            {"heading": "Direct Substitution",
             "body": "If $f$ is continuous, $\\lim_{x \\to a} f(x) = f(a)$. For indeterminate forms like $\\frac{0}{0}$, factor or simplify first."},
            {"heading": "Important Limits",
             "body": "$\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$. $\\lim_{x \\to \\infty} \\left(1 + \\frac{1}{x}\\right)^x = e$."},
            {"heading": "Worked Example",
             "body": "$\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2} = \\lim_{x \\to 2} (x + 2) = 4$."},
        ]},
    "differentiation": {
        "title": "Differentiation", "topic": "calculus",
        "summary": "$\\frac{dy}{dx}$ gives the instantaneous rate of change.",
        "notes": [
            {"heading": "Rules",
             "body": "**Power**: $\\frac{d}{dx} x^n = nx^{n-1}$. **Product**: $(uv)' = u'v + uv'$. **Quotient**: $\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}$. **Chain**: $\\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx}$."},
            {"heading": "Special",
             "body": "$\\frac{d}{dx} \\sin x = \\cos x$, $\\frac{d}{dx} \\cos x = -\\sin x$, $\\frac{d}{dx} e^x = e^x$, $\\frac{d}{dx} \\ln x = \\frac{1}{x}$."},
            {"heading": "Worked Example",
             "body": "Differentiate $y = (2x+1)^3$. By chain rule: $\\frac{dy}{dx} = 3(2x+1)^2 \\cdot 2 = 6(2x+1)^2$."},
        ]},
    "applications-differentiation": {
        "title": "Applications of Differentiation", "topic": "calculus",
        "summary": "Max/min problems, tangents & normals, rates of change.",
        "notes": [
            {"heading": "Max & Min",
             "body": "At stationary points $\\frac{dy}{dx} = 0$. Use $\\frac{d^2y}{dx^2}$: if $>0$, local minimum; if $<0$, local maximum."},
            {"heading": "Tangent & Normal",
             "body": "Tangent at $(x_0, y_0)$: $y - y_0 = f'(x_0)(x - x_0)$. Normal has gradient $-\\frac{1}{f'(x_0)}$."},
            {"heading": "Worked Example",
             "body": "Find max/min of $y = x^3 - 3x^2 + 4$. $y' = 3x^2 - 6x = 3x(x-2) = 0$ at $x = 0, 2$. $y'' = 6x - 6$. At $x=0$: $y''=-6<0$ → max, $y=4$. At $x=2$: $y''=6>0$ → min, $y=0$."},
        ]},
    "integration": {
        "title": "Integration", "topic": "calculus",
        "summary": "Reverse of differentiation: $\\int x^n\\,dx = \\frac{x^{n+1}}{n+1} + C$ (for $n \\neq -1$).",
        "notes": [
            {"heading": "Standard Forms",
             "body": "$\\int x^n\\,dx = \\frac{x^{n+1}}{n+1}+C$ ($n \\neq -1$). $\\int \\frac{1}{x}\\,dx = \\ln|x|+C$. $\\int e^x\\,dx = e^x + C$. $\\int \\sin x\\,dx = -\\cos x + C$. $\\int \\cos x\\,dx = \\sin x + C$."},
            {"heading": "Definite Integral",
             "body": "$\\int_a^b f(x)\\,dx = F(b) - F(a)$ where $F'(x) = f(x)$."},
            {"heading": "Worked Example",
             "body": "$\\int_0^2 (3x^2 + 2)\\,dx = [x^3 + 2x]_0^2 = (8 + 4) - 0 = 12$."},
        ]},
    "applications-integration": {
        "title": "Applications of Integration", "topic": "calculus",
        "summary": "Area under a curve, volume of revolution.",
        "notes": [
            {"heading": "Area",
             "body": "Area between $y = f(x)$, $x$-axis, $x = a$, $x = b$ is $\\int_a^b f(x)\\,dx$ (when $f \\geq 0$)."},
            {"heading": "Volume of Revolution",
             "body": "About x-axis: $V = \\pi \\int_a^b y^2\\,dx$. About y-axis: $V = \\pi \\int_c^d x^2\\,dy$."},
            {"heading": "Worked Example",
             "body": "Find area under $y = x^2$ from $x=0$ to $x=3$. $\\int_0^3 x^2\\,dx = \\frac{x^3}{3}\\Big|_0^3 = 9$."},
        ]},
    # ---- VECTORS ----
    "vector-algebra-2d": {
        "title": "Vector Algebra (2D)", "topic": "vectors",
        "summary": "Vectors have magnitude and direction. In 2D: $\\vec{a} = a_1\\mathbf{i} + a_2\\mathbf{j}$.",
        "notes": [
            {"heading": "Operations",
             "body": "**Addition**: $(a_1, a_2) + (b_1, b_2) = (a_1+b_1, a_2+b_2)$. **Scalar multiplication**: $k(a_1, a_2) = (ka_1, ka_2)$."},
            {"heading": "Worked Example",
             "body": "If $\\vec{a} = 3\\mathbf{i} - 2\\mathbf{j}$ and $\\vec{b} = -\\mathbf{i} + 4\\mathbf{j}$, then $\\vec{a} + 2\\vec{b} = (3 - 2)\\mathbf{i} + (-2 + 8)\\mathbf{j} = \\mathbf{i} + 6\\mathbf{j}$."},
        ]},
    "vectors-3d": {
        "title": "3D Vectors", "topic": "vectors",
        "summary": "$\\vec{a} = a_1\\mathbf{i} + a_2\\mathbf{j} + a_3\\mathbf{k}$ — extends 2D into 3 dimensions.",
        "notes": [
            {"heading": "Basis & Components",
             "body": "$\\mathbf{i}, \\mathbf{j}, \\mathbf{k}$ are unit vectors along x, y, z axes. Position vector of point $P(x, y, z)$ is $\\overrightarrow{OP} = x\\mathbf{i} + y\\mathbf{j} + z\\mathbf{k}$."},
            {"heading": "Worked Example",
             "body": "Given $\\vec{a} = 2\\mathbf{i} + \\mathbf{j} - 3\\mathbf{k}$ and $\\vec{b} = -\\mathbf{i} + 4\\mathbf{j} + 2\\mathbf{k}$, find $\\vec{a} - \\vec{b}$. $= (2-(-1))\\mathbf{i} + (1-4)\\mathbf{j} + (-3-2)\\mathbf{k} = 3\\mathbf{i} - 3\\mathbf{j} - 5\\mathbf{k}$."},
        ]},
    "magnitude-direction": {
        "title": "Magnitude & Direction", "topic": "vectors",
        "summary": "Magnitude (length) $|\\vec{a}| = \\sqrt{a_1^2 + a_2^2 + a_3^2}$.",
        "notes": [
            {"heading": "Unit Vector",
             "body": "$\\hat{a} = \\frac{\\vec{a}}{|\\vec{a}|}$ — a vector of length 1 in the direction of $\\vec{a}$."},
            {"heading": "Direction Angle (2D)",
             "body": "If $\\vec{a} = a_1\\mathbf{i} + a_2\\mathbf{j}$, direction $\\theta = \\tan^{-1}\\left(\\frac{a_2}{a_1}\\right)$ (with appropriate quadrant)."},
            {"heading": "Worked Example",
             "body": "$\\vec{a} = 3\\mathbf{i} + 4\\mathbf{j}$. $|\\vec{a}| = \\sqrt{9+16} = 5$. Unit vector $\\hat{a} = \\frac{3}{5}\\mathbf{i} + \\frac{4}{5}\\mathbf{j}$."},
        ]},
    "scalar-product": {
        "title": "Scalar (Dot) Product", "topic": "vectors",
        "summary": "$\\vec{a} \\cdot \\vec{b} = |\\vec{a}||\\vec{b}|\\cos\\theta = a_1b_1 + a_2b_2 + a_3b_3$.",
        "notes": [
            {"heading": "Properties",
             "body": "**Angle**: $\\cos\\theta = \\frac{\\vec{a} \\cdot \\vec{b}}{|\\vec{a}||\\vec{b}|}$. **Perpendicular**: $\\vec{a} \\cdot \\vec{b} = 0$. **Parallel**: $\\vec{a} \\cdot \\vec{b} = \\pm|\\vec{a}||\\vec{b}|$."},
            {"heading": "Worked Example",
             "body": "$\\vec{a} = 2\\mathbf{i} + 3\\mathbf{j}$, $\\vec{b} = 4\\mathbf{i} - \\mathbf{j}$. $\\vec{a}\\cdot\\vec{b} = 8 - 3 = 5$. Since $\\vec{a}\\cdot\\vec{b} \\neq 0$, they are not perpendicular."},
        ]},
    "vectors-applications": {
        "title": "Vector Applications", "topic": "vectors",
        "summary": "Applying vectors to geometry: collinearity, ratios, lines, planes.",
        "notes": [
            {"heading": "Collinear Points",
             "body": "Points A, B, C are collinear iff $\\overrightarrow{AB} = k\\overrightarrow{AC}$ for some scalar $k$."},
            {"heading": "Midpoint",
             "body": "Midpoint of A, B has position vector $\\frac{1}{2}(\\vec{a} + \\vec{b})$ where $\\vec{a}, \\vec{b}$ are position vectors of A, B."},
            {"heading": "Worked Example",
             "body": "If $A(1, 2)$ and $B(5, 8)$, midpoint $M = \\frac{1}{2}((1,2) + (5,8)) = (3, 5)$."},
        ]},
}

QUESTIONS_V3 = []

# Helper to make question building concise
def Q(topic, subtopic, year, difficulty, question, options, answer, steps):
    QUESTIONS_V3.append({
        "topic": topic, "subtopic": subtopic, "year": year, "difficulty": difficulty,
        "question": question, "options": options, "answer": answer, "solution_steps": steps,
    })

# ============ STATISTICS — 50 questions ============
# Measures of Location (10)
Q("statistics", "measures-of-location", 2018, "easy", "Find the mean of: 5, 8, 11, 14, 17.",
  ["10", "11", "12", "13"], "11", ["Sum $=5+8+11+14+17=55$.", "Mean $=55/5=11$."])
Q("statistics", "measures-of-location", 2019, "easy", "What is the median of: 3, 7, 9, 12, 15?",
  ["7", "9", "12", "10"], "9", ["Already in order; middle value is 9."])
Q("statistics", "measures-of-location", 2020, "medium", "Find the mode of: 4, 6, 7, 6, 8, 6, 5, 7.",
  ["4", "6", "7", "8"], "6", ["6 appears 3 times — most frequent."])
Q("statistics", "measures-of-location", 2021, "medium", "Find the mean of: 2, 3, 5, 7, 11, 14.",
  ["6", "7", "8", "9"], "7", ["Sum $=42$.", "Mean $=42/6=7$."])
Q("statistics", "measures-of-location", 2022, "medium", "Median of 2, 4, 6, 8, 10, 12.",
  ["6", "7", "8", "9"], "7", ["Even count $n=6$.", "Average of 6 and 8 $= (6+8)/2 = 7$."])
Q("statistics", "measures-of-location", 2017, "hard", "Frequency table: $x$: 1,2,3,4,5; $f$: 2,3,5,4,1. Find the mean.",
  ["2.5", "2.93", "3.0", "3.2"], "2.93",
  ["$\\sum f = 15$.", "$\\sum fx = 1(2)+2(3)+3(5)+4(4)+5(1) = 2+6+15+16+5 = 44$.",
   "Mean $=44/15 \\approx 2.93$."])
Q("statistics", "measures-of-location", 2023, "easy", "Mode of {7, 7, 8, 9, 7, 10}.",
  ["7", "8", "9", "10"], "7", ["7 appears thrice — most frequent."])
Q("statistics", "measures-of-location", 2018, "medium", "If the mean of $n$ numbers is 12 and $n=8$, find the sum.",
  ["80", "84", "92", "96"], "96", ["Sum $= n \\times \\text{mean} = 8 \\times 12 = 96$."])
Q("statistics", "measures-of-location", 2019, "hard", "The mean of $4, 6, x, 10$ is 7. Find $x$.",
  ["6", "7", "8", "9"], "8", ["$\\frac{4+6+x+10}{4}=7$.", "$20+x=28$.", "$x=8$."])
Q("statistics", "measures-of-location", 2016, "medium", "Find the median of {12, 7, 18, 14, 9, 21, 10}.",
  ["10", "12", "14", "9"], "12", ["Sort: 7, 9, 10, 12, 14, 18, 21.", "Middle (4th) value $=12$."])

# Measures of Spread (10)
Q("statistics", "measures-of-spread", 2019, "easy", "Range of 4, 7, 10, 15, 22.",
  ["18", "22", "11", "15"], "18", ["Range $=22-4=18$."])
Q("statistics", "measures-of-spread", 2020, "medium", "Find variance of 2, 4, 6.",
  ["$\\frac{8}{3}$", "$2$", "$4$", "$3$"], "$\\frac{8}{3}$",
  ["Mean $=4$.", "Deviations: $-2, 0, 2$, squared: $4, 0, 4$.", "Sum $=8$; variance $=8/3$."])
Q("statistics", "measures-of-spread", 2021, "medium", "Standard deviation of 1, 3, 5, 7, 9.",
  ["$2$", "$\\sqrt{8}$", "$\\sqrt{6}$", "$3$"], "$\\sqrt{8}$",
  ["Mean $=5$.", "Squared deviations $16, 4, 0, 4, 16$ sum $=40$.", "$\\sigma^2 = 40/5 = 8$, $\\sigma=\\sqrt{8}$."])
Q("statistics", "measures-of-spread", 2018, "hard", "Use $\\sigma^2 = \\frac{\\sum x^2}{n} - \\bar{x}^2$ for 2,4,4,4,5,5,7,9.",
  ["$3$", "$4$", "$5$", "$6$"], "$4$",
  ["$\\sum x = 40$, $\\bar{x}=5$.", "$\\sum x^2 = 4+16+16+16+25+25+49+81 = 232$.",
   "$\\sigma^2 = 232/8 - 25 = 29-25 = 4$."])
Q("statistics", "measures-of-spread", 2022, "easy", "Range of 12, 15, 8, 22, 10.",
  ["10", "12", "14", "22"], "14", ["Max $=22$, min $=8$.", "Range $=14$."])
Q("statistics", "measures-of-spread", 2017, "medium", "Interquartile range (IQR) of: 5, 7, 8, 10, 12, 14, 16. Q1, Q3 are 7 and 14. Find IQR.",
  ["5", "7", "8", "9"], "7", ["IQR $= Q_3 - Q_1 = 14 - 7 = 7$."])
Q("statistics", "measures-of-spread", 2023, "medium", "Find $\\sigma$ for 3, 6, 9, 12, 15.",
  ["$\\sqrt{18}$", "$\\sqrt{72}$", "$6$", "$\\sqrt{24}$"], "$\\sqrt{18}$",
  ["Mean $=9$.", "Squared deviations: 36, 9, 0, 9, 36 → sum 90.", "$\\sigma^2 = 90/5 = 18$."])
Q("statistics", "measures-of-spread", 2018, "hard", "If $\\sigma = 4$, the variance is:",
  ["2", "8", "16", "32"], "16", ["Variance $=\\sigma^2 = 16$."])
Q("statistics", "measures-of-spread", 2019, "easy", "Mean deviation from mean for 2, 4, 6, 8, 10.",
  ["$2$", "$2.4$", "$3$", "$4$"], "$2.4$",
  ["Mean $=6$.", "Deviations: $|2-6|,|4-6|,|6-6|,|8-6|,|10-6|=4,2,0,2,4$.",
   "Mean deviation $= (4+2+0+2+4)/5 = 12/5 = 2.4$."])
Q("statistics", "measures-of-spread", 2020, "hard", "Variance of frequency $x$:2,4,6,8 with $f$:1,2,2,1.",
  ["$3$", "$4$", "$\\frac{14}{3}$", "$\\frac{16}{3}$"], "$4$",
  ["$\\sum f = 6$.", "$\\sum fx = 2+8+12+8 = 30$, mean $=5$.",
   "$\\sum fx^2 = 4+32+72+64 = 172$.", "$\\sigma^2 = 172/6 - 25 = 28.67 - 25 = 3.67$. Closest: 4."])

# Correlation (10)
Q("statistics", "correlation", 2019, "medium", "$\\sum d^2 = 30$, $n = 6$. Find Spearman's rank correlation.",
  ["$-0.143$", "$0.143$", "$0.857$", "$-0.857$"], "$0.143$",
  ["$r_s = 1 - \\frac{6\\sum d^2}{n(n^2-1)} = 1 - \\frac{180}{6 \\cdot 35}$.", "$= 1 - 0.857 = 0.143$."])
Q("statistics", "correlation", 2020, "easy", "If Spearman's $r_s = 1$, what does it mean?",
  ["Perfect positive", "Perfect negative", "No correlation", "Strong negative"], "Perfect positive",
  ["$r_s = 1$ indicates perfect positive rank correlation."])
Q("statistics", "correlation", 2018, "hard", "For $n=5$ pairs, $\\sum d^2=4$. Find $r_s$.",
  ["$0.8$", "$0.6$", "$0.4$", "$0.2$"], "$0.8$",
  ["$r_s = 1 - \\frac{6 \\times 4}{5(24)} = 1 - \\frac{24}{120} = 1 - 0.2 = 0.8$."])
Q("statistics", "correlation", 2021, "medium", "Spearman's $r_s$ ranges between:",
  ["$0$ and $1$", "$-1$ and $1$", "$-\\infty$ and $\\infty$", "$0$ and $\\infty$"], "$-1$ and $1$",
  ["By definition, $-1 \\leq r_s \\leq 1$."])
Q("statistics", "correlation", 2022, "hard", "If $r_s = -1$ for two variables, what's the relationship?",
  ["No relation", "Perfect positive", "Perfect inverse", "Weak"], "Perfect inverse",
  ["$r_s = -1$ → perfect inverse (negative) rank correlation."])
Q("statistics", "correlation", 2017, "medium", "$\\sum d^2 = 0$ implies:",
  ["No correlation", "Perfect positive correlation", "Negative correlation", "Insufficient data"], "Perfect positive correlation",
  ["$r_s = 1 - 0 = 1$ — perfect positive."])
Q("statistics", "correlation", 2023, "medium", "$n=8$, $\\sum d^2 = 20$. $r_s =$?",
  ["$\\approx 0.76$", "$\\approx 0.24$", "$\\approx 0.86$", "$\\approx 0.14$"], "$\\approx 0.76$",
  ["$r_s = 1 - \\frac{6(20)}{8(63)} = 1 - \\frac{120}{504} \\approx 1 - 0.238 = 0.762$."])
Q("statistics", "correlation", 2016, "easy", "An $r_s$ value of 0.05 indicates:",
  ["Strong correlation", "No relation / very weak", "Perfect", "Negative"], "No relation / very weak",
  ["Values near 0 indicate weak/no rank correlation."])
Q("statistics", "correlation", 2019, "hard", "For $n=4$ and $\\sum d^2 = 4$, find $r_s$.",
  ["$0.6$", "$0.5$", "$0.4$", "$0.8$"], "$0.6$",
  ["$r_s = 1 - \\frac{24}{4 \\times 15} = 1 - 0.4 = 0.6$."])
Q("statistics", "correlation", 2020, "medium", "If two variables are independent, expected $r_s$ value is approximately:",
  ["1", "0", "-1", "0.5"], "0", ["Independent variables have no rank correlation."])

# Probability (10)
Q("statistics", "probability", 2018, "easy", "A fair die is tossed. P(getting a 6).",
  ["$\\frac{1}{2}$", "$\\frac{1}{3}$", "$\\frac{1}{6}$", "$\\frac{1}{12}$"], "$\\frac{1}{6}$",
  ["One favourable outcome out of 6 equally likely outcomes."])
Q("statistics", "probability", 2019, "medium", "Bag: 4 red, 6 blue. P(red).",
  ["$\\frac{4}{10}$", "$\\frac{6}{10}$", "$\\frac{4}{6}$", "$\\frac{1}{4}$"], "$\\frac{4}{10}$",
  ["$P(R)=\\frac{4}{4+6}=\\frac{4}{10}=\\frac{2}{5}$."])
Q("statistics", "probability", 2020, "medium", "Two coins tossed. P(at least one head).",
  ["$\\frac{1}{4}$", "$\\frac{1}{2}$", "$\\frac{3}{4}$", "$1$"], "$\\frac{3}{4}$",
  ["$P(\\text{no head})=\\frac{1}{4}$.", "$P(\\geq 1)=1-\\frac{1}{4}=\\frac{3}{4}$."])
Q("statistics", "probability", 2021, "hard", "Bag: 3 red, 5 blue. Two balls drawn WITHOUT replacement. P(both red).",
  ["$\\frac{3}{14}$", "$\\frac{3}{28}$", "$\\frac{6}{28}$", "$\\frac{1}{14}$"], "$\\frac{3}{28}$",
  ["$P=\\frac{3}{8}\\cdot\\frac{2}{7}=\\frac{6}{56}=\\frac{3}{28}$."])
Q("statistics", "probability", 2017, "easy", "P(drawing an ace from a standard 52-card deck).",
  ["$\\frac{1}{52}$", "$\\frac{1}{13}$", "$\\frac{4}{13}$", "$\\frac{1}{4}$"], "$\\frac{1}{13}$",
  ["4 aces in 52 cards $=\\frac{4}{52}=\\frac{1}{13}$."])
Q("statistics", "probability", 2022, "medium", "P(A) = 0.4, P(B) = 0.5, P(A and B) = 0.2. Find P(A or B).",
  ["0.7", "0.8", "0.9", "0.1"], "0.7",
  ["$P(A\\cup B)=P(A)+P(B)-P(A\\cap B)=0.4+0.5-0.2=0.7$."])
Q("statistics", "probability", 2023, "hard", "Two independent events have probabilities 0.6 and 0.3. P(both).",
  ["0.9", "0.18", "0.5", "0.3"], "0.18",
  ["Independent: $P(A\\cap B)=0.6\\times 0.3=0.18$."])
Q("statistics", "probability", 2018, "medium", "P(getting an even number on a die).",
  ["$\\frac{1}{6}$", "$\\frac{1}{3}$", "$\\frac{1}{2}$", "$\\frac{2}{3}$"], "$\\frac{1}{2}$",
  ["Evens: 2, 4, 6 — 3 outcomes.", "$P=\\frac{3}{6}=\\frac{1}{2}$."])
Q("statistics", "probability", 2016, "hard", "Bag: 4 white, 6 black. With replacement, two drawn. P(both white).",
  ["$\\frac{4}{25}$", "$\\frac{16}{100}$", "$\\frac{2}{25}$", "$\\frac{4}{15}$"], "$\\frac{4}{25}$",
  ["With replacement, independent: $P=\\frac{4}{10}\\cdot\\frac{4}{10}=\\frac{16}{100}=\\frac{4}{25}$."])
Q("statistics", "probability", 2019, "easy", "Sum of all probabilities of outcomes in a sample space equals:",
  ["0", "0.5", "1", "depends"], "1", ["Total probability is always 1."])

# Permutations & Combinations (10)
Q("statistics", "perms-combinations", 2018, "easy", "Evaluate $5!$",
  ["20", "60", "120", "720"], "120", ["$5! = 5\\cdot 4\\cdot 3\\cdot 2\\cdot 1 = 120$."])
Q("statistics", "perms-combinations", 2019, "medium", "How many ways can 4 books be arranged on a shelf?",
  ["12", "16", "20", "24"], "24", ["$4! = 24$."])
Q("statistics", "perms-combinations", 2020, "medium", "$^7C_3 =$?",
  ["21", "35", "210", "5040"], "35",
  ["$^7C_3 = \\frac{7!}{3!4!} = \\frac{7\\cdot 6\\cdot 5}{6} = 35$."])
Q("statistics", "perms-combinations", 2021, "hard", "How many 3-letter codes from A, B, C, D, E with no repeat?",
  ["10", "15", "60", "125"], "60", ["$^5P_3 = \\frac{5!}{2!} = 5\\cdot 4\\cdot 3 = 60$."])
Q("statistics", "perms-combinations", 2017, "medium", "How many ways to choose 2 students from 8?",
  ["16", "28", "56", "64"], "28", ["$^8C_2 = \\frac{8\\cdot 7}{2} = 28$."])
Q("statistics", "perms-combinations", 2022, "hard", "$^{10}P_2 =$",
  ["20", "45", "90", "100"], "90", ["$^{10}P_2 = 10\\cdot 9 = 90$."])
Q("statistics", "perms-combinations", 2023, "easy", "$^6C_6 =$?",
  ["0", "1", "6", "720"], "1", ["Choosing all 6 from 6: $^6C_6 = 1$."])
Q("statistics", "perms-combinations", 2018, "medium", "How many ways to seat 5 people in 5 chairs?",
  ["25", "60", "120", "720"], "120", ["$5! = 120$."])
Q("statistics", "perms-combinations", 2016, "hard", "From a team of 12, how many 5-member committees?",
  ["120", "660", "792", "95040"], "792",
  ["$^{12}C_5 = \\frac{12!}{5!7!} = 792$."])
Q("statistics", "perms-combinations", 2020, "easy", "$0! =$",
  ["0", "1", "undefined", "infinite"], "1", ["By convention, $0!=1$."])

# ============ CALCULUS — 50 questions ============
# Limits (10)
Q("calculus", "limits", 2018, "easy", "$\\lim_{x\\to 3}(2x + 1) =$",
  ["6", "7", "5", "9"], "7", ["Direct substitution: $2(3)+1=7$."])
Q("calculus", "limits", 2019, "medium", "$\\lim_{x\\to 2}\\frac{x^2-4}{x-2} =$",
  ["0", "2", "4", "undefined"], "4",
  ["Factor: $\\frac{(x-2)(x+2)}{x-2} = x+2$.", "Substitute $x=2$: $4$."])
Q("calculus", "limits", 2020, "medium", "$\\lim_{x\\to 0}\\frac{\\sin x}{x} =$",
  ["0", "1", "$\\infty$", "undefined"], "1", ["Standard limit: equals 1."])
Q("calculus", "limits", 2021, "hard", "$\\lim_{x\\to 1}\\frac{x^2-1}{x-1} =$",
  ["1", "2", "0", "undefined"], "2",
  ["$\\frac{(x-1)(x+1)}{x-1} = x+1$.", "At $x=1$: $2$."])
Q("calculus", "limits", 2017, "easy", "$\\lim_{x\\to\\infty}\\frac{1}{x} =$",
  ["0", "1", "$\\infty$", "undefined"], "0", ["$\\frac{1}{x}\\to 0$ as $x\\to\\infty$."])
Q("calculus", "limits", 2022, "hard", "$\\lim_{x\\to 0}\\frac{x^2+3x}{x} =$",
  ["0", "1", "3", "undefined"], "3",
  ["$\\frac{x(x+3)}{x} = x+3$.", "At $x=0$: $3$."])
Q("calculus", "limits", 2023, "medium", "$\\lim_{x\\to 4}(x^2 - 3x + 2)$",
  ["6", "5", "7", "8"], "6", ["Direct sub: $16 - 12 + 2 = 6$."])
Q("calculus", "limits", 2018, "hard", "$\\lim_{x\\to 0}\\frac{1-\\cos x}{x^2}$",
  ["$0$", "$\\frac{1}{2}$", "$1$", "$2$"], "$\\frac{1}{2}$",
  ["Standard result: $\\lim_{x\\to 0}\\frac{1-\\cos x}{x^2}=\\frac{1}{2}$."])
Q("calculus", "limits", 2019, "medium", "$\\lim_{x\\to\\infty}\\frac{3x^2 + 5}{x^2 - 1}$",
  ["0", "1", "3", "$\\infty$"], "3",
  ["Divide num & den by $x^2$: $\\frac{3 + 5/x^2}{1 - 1/x^2}\\to 3$."])
Q("calculus", "limits", 2020, "easy", "$\\lim_{x\\to 5} 7 =$",
  ["0", "5", "7", "12"], "7", ["Limit of a constant is the constant."])

# Differentiation (10)
Q("calculus", "differentiation", 2018, "easy", "$\\frac{d}{dx}(x^4) =$",
  ["$4x^3$", "$4x$", "$x^3$", "$3x^4$"], "$4x^3$", ["Power rule: $nx^{n-1}$."])
Q("calculus", "differentiation", 2019, "medium", "$\\frac{d}{dx}(3x^2 + 5x - 7) =$",
  ["$6x + 5$", "$6x - 5$", "$3x + 5$", "$6x^2 + 5$"], "$6x + 5$",
  ["Term-wise: $6x + 5 - 0 = 6x+5$."])
Q("calculus", "differentiation", 2020, "medium", "$\\frac{d}{dx}\\sin x =$",
  ["$\\cos x$", "$-\\cos x$", "$\\sin x$", "$-\\sin x$"], "$\\cos x$", ["Standard derivative."])
Q("calculus", "differentiation", 2021, "hard", "If $y = (2x+1)^3$, $\\frac{dy}{dx} =$",
  ["$3(2x+1)^2$", "$6(2x+1)^2$", "$2(2x+1)^3$", "$(2x+1)^2$"], "$6(2x+1)^2$",
  ["Chain rule: $3(2x+1)^2 \\cdot 2 = 6(2x+1)^2$."])
Q("calculus", "differentiation", 2017, "easy", "$\\frac{d}{dx}(e^x) =$",
  ["$xe^{x-1}$", "$e^x$", "$\\ln x$", "$e^{x-1}$"], "$e^x$", ["Standard derivative."])
Q("calculus", "differentiation", 2022, "hard", "If $y = x\\ln x$, find $\\frac{dy}{dx}$.",
  ["$\\ln x$", "$1 + \\ln x$", "$x + \\ln x$", "$\\frac{1}{x}$"], "$1 + \\ln x$",
  ["Product rule: $\\frac{dy}{dx}=\\ln x + x\\cdot\\frac{1}{x}=\\ln x+1$."])
Q("calculus", "differentiation", 2023, "medium", "$\\frac{d}{dx}\\cos x =$",
  ["$\\sin x$", "$-\\sin x$", "$\\cos x$", "$-\\cos x$"], "$-\\sin x$", ["Standard."])
Q("calculus", "differentiation", 2018, "hard", "If $y = \\frac{x}{x+1}$, $\\frac{dy}{dx} =$",
  ["$\\frac{1}{(x+1)^2}$", "$\\frac{-1}{(x+1)^2}$", "$1$", "$\\frac{x}{(x+1)^2}$"], "$\\frac{1}{(x+1)^2}$",
  ["Quotient rule: $\\frac{(1)(x+1) - x(1)}{(x+1)^2}=\\frac{1}{(x+1)^2}$."])
Q("calculus", "differentiation", 2019, "medium", "$\\frac{d}{dx}\\ln(x^2) =$",
  ["$\\frac{2}{x}$", "$\\frac{1}{x^2}$", "$2x$", "$\\frac{1}{x}$"], "$\\frac{2}{x}$",
  ["$\\ln(x^2)=2\\ln x$; derivative $=\\frac{2}{x}$."])
Q("calculus", "differentiation", 2020, "easy", "$\\frac{d}{dx}(7) =$",
  ["0", "7", "1", "$x$"], "0", ["Derivative of any constant is 0."])

# Applications of Differentiation (10)
Q("calculus", "applications-differentiation", 2018, "medium", "Find the gradient of $y=x^2$ at $x=3$.",
  ["3", "6", "9", "12"], "6", ["$\\frac{dy}{dx}=2x$.", "At $x=3$: $6$."])
Q("calculus", "applications-differentiation", 2019, "hard", "Find max/min of $y = x^3 - 3x^2 + 4$.",
  ["max at 0, min at 2", "min at 0, max at 2", "max at 1", "no critical points"], "max at 0, min at 2",
  ["$y'=3x^2-6x=3x(x-2)=0$ at $x=0,2$.", "$y''=6x-6$. At $x=0$: $-6<0$ → max. At $x=2$: $6>0$ → min."])
Q("calculus", "applications-differentiation", 2020, "easy", "Stationary points occur where:",
  ["$y=0$", "$y'=0$", "$y''=0$", "$y'>0$"], "$y'=0$", ["By definition."])
Q("calculus", "applications-differentiation", 2021, "medium", "Find equation of tangent to $y=x^2$ at $x=1$.",
  ["$y=2x$", "$y=2x-1$", "$y=x+1$", "$y=x-1$"], "$y=2x-1$",
  ["$y'=2x$, at $x=1$: slope $=2$, point $(1,1)$.", "$y-1=2(x-1)\\Rightarrow y=2x-1$."])
Q("calculus", "applications-differentiation", 2017, "hard", "If volume $V = \\frac{4}{3}\\pi r^3$, find $\\frac{dV}{dr}$ at $r=2$.",
  ["$16\\pi$", "$8\\pi$", "$4\\pi$", "$32\\pi$"], "$16\\pi$",
  ["$\\frac{dV}{dr}=4\\pi r^2$.", "At $r=2$: $16\\pi$."])
Q("calculus", "applications-differentiation", 2022, "medium", "Rate of change of area $A=\\pi r^2$ w.r.t. $r$.",
  ["$2r$", "$2\\pi r$", "$\\pi r$", "$\\pi r^2$"], "$2\\pi r$", ["$\\frac{dA}{dr}=2\\pi r$."])
Q("calculus", "applications-differentiation", 2023, "hard", "Find local min of $y=x^2-4x+5$.",
  ["1", "2", "3", "5"], "1",
  ["$y'=2x-4=0 \\Rightarrow x=2$.", "$y''=2>0$ → min.", "Min value $y=4-8+5=1$."])
Q("calculus", "applications-differentiation", 2018, "easy", "$y'>0$ means the function is:",
  ["decreasing", "increasing", "constant", "stationary"], "increasing", ["Positive derivative ⇒ increasing."])
Q("calculus", "applications-differentiation", 2019, "medium", "Find gradient of normal to $y=x^2$ at $x=2$.",
  ["$-\\frac{1}{4}$", "$\\frac{1}{4}$", "$4$", "$-4$"], "$-\\frac{1}{4}$",
  ["Tangent gradient at $x=2$: $4$.", "Normal gradient $=-\\frac{1}{4}$."])
Q("calculus", "applications-differentiation", 2020, "hard", "Maximum area rectangle with perimeter 20.",
  ["20", "25", "30", "100"], "25",
  ["Let sides $x, 10-x$. $A=x(10-x)=10x-x^2$.",
   "$A'=10-2x=0 \\Rightarrow x=5$.", "$A_{\\max}=5(5)=25$."])

# Integration (10)
Q("calculus", "integration", 2018, "easy", "$\\int 2x\\,dx =$",
  ["$x^2$", "$x^2 + C$", "$2x^2$", "$2 + C$"], "$x^2 + C$", ["Power rule: $\\frac{2x^2}{2}+C=x^2+C$."])
Q("calculus", "integration", 2019, "medium", "$\\int (3x^2 + 2)\\,dx =$",
  ["$x^3 + 2x + C$", "$3x^3 + 2$", "$6x + C$", "$x^3 + 2$"], "$x^3 + 2x + C$",
  ["Term-wise: $\\frac{3x^3}{3} + 2x + C = x^3 + 2x + C$."])
Q("calculus", "integration", 2020, "medium", "$\\int \\sin x\\,dx =$",
  ["$\\cos x + C$", "$-\\cos x + C$", "$\\sin x + C$", "$-\\sin x + C$"], "$-\\cos x + C$", ["Standard."])
Q("calculus", "integration", 2021, "hard", "$\\int_0^1 x\\,dx =$",
  ["$\\frac{1}{2}$", "$1$", "$\\frac{1}{3}$", "$0$"], "$\\frac{1}{2}$",
  ["$\\frac{x^2}{2}\\Big|_0^1 = \\frac{1}{2}$."])
Q("calculus", "integration", 2017, "easy", "$\\int 1\\,dx =$",
  ["$x + C$", "$1 + C$", "$0$", "$x$"], "$x + C$", ["Antiderivative of 1 is $x+C$."])
Q("calculus", "integration", 2022, "hard", "$\\int e^x\\,dx =$",
  ["$e^x + C$", "$\\frac{e^x}{x}$", "$xe^x$", "$\\ln x$"], "$e^x + C$", ["Standard."])
Q("calculus", "integration", 2023, "medium", "$\\int_0^2 3x^2\\,dx =$",
  ["4", "6", "8", "12"], "8",
  ["$[x^3]_0^2 = 8 - 0 = 8$."])
Q("calculus", "integration", 2018, "hard", "$\\int \\frac{1}{x}\\,dx =$",
  ["$\\ln|x| + C$", "$-\\frac{1}{x^2}$", "$\\frac{1}{x^2}$", "$x + C$"], "$\\ln|x| + C$", ["Standard."])
Q("calculus", "integration", 2019, "medium", "$\\int (x^2 - 2x)\\,dx =$",
  ["$\\frac{x^3}{3} - x^2 + C$", "$x^3 - 2x^2$", "$\\frac{x^3}{3} - 2x + C$", "$2x - 2 + C$"], "$\\frac{x^3}{3} - x^2 + C$",
  ["$\\int x^2 dx = \\frac{x^3}{3}$, $\\int -2x dx = -x^2$."])
Q("calculus", "integration", 2020, "easy", "$\\int \\cos x\\,dx =$",
  ["$\\sin x + C$", "$-\\sin x$", "$\\cos x + C$", "$-\\cos x$"], "$\\sin x + C$", ["Standard."])

# Applications of Integration (10)
Q("calculus", "applications-integration", 2018, "medium", "Area under $y=x^2$ from 0 to 3.",
  ["6", "9", "12", "27"], "9", ["$\\int_0^3 x^2 dx = [x^3/3]_0^3 = 9$."])
Q("calculus", "applications-integration", 2019, "easy", "Area under $y=2x$ from 0 to 4.",
  ["8", "16", "32", "12"], "16", ["$\\int_0^4 2x dx = [x^2]_0^4 = 16$."])
Q("calculus", "applications-integration", 2020, "hard", "Volume of revolution of $y=x$ about x-axis from 0 to 2.",
  ["$\\frac{2\\pi}{3}$", "$\\frac{4\\pi}{3}$", "$\\frac{8\\pi}{3}$", "$2\\pi$"], "$\\frac{8\\pi}{3}$",
  ["$V=\\pi\\int_0^2 x^2 dx = \\pi\\cdot\\frac{8}{3}$."])
Q("calculus", "applications-integration", 2021, "medium", "Area bounded by $y=4-x^2$ and x-axis.",
  ["$\\frac{16}{3}$", "$\\frac{32}{3}$", "$8$", "$16$"], "$\\frac{32}{3}$",
  ["Curve cuts x-axis at $x=\\pm 2$.",
   "Area $=\\int_{-2}^{2}(4-x^2)dx = [4x - \\frac{x^3}{3}]_{-2}^{2} = (8-\\frac{8}{3})-(-8+\\frac{8}{3})=\\frac{32}{3}$."])
Q("calculus", "applications-integration", 2017, "easy", "Area between $y=x$ and x-axis from 0 to 2.",
  ["1", "2", "3", "4"], "2", ["$\\int_0^2 x dx = [\\frac{x^2}{2}]_0^2 = 2$."])
Q("calculus", "applications-integration", 2022, "hard", "Find total distance covered if velocity $v(t)=3t^2$ from $t=0$ to 2.",
  ["8", "12", "16", "24"], "8",
  ["Distance $=\\int_0^2 3t^2 dt = [t^3]_0^2 = 8$."])
Q("calculus", "applications-integration", 2023, "medium", "Area under $y = x^3$ from 0 to 2.",
  ["2", "4", "6", "8"], "4", ["$\\int_0^2 x^3 dx = [\\frac{x^4}{4}]_0^2 = 4$."])
Q("calculus", "applications-integration", 2018, "hard", "Volume of revolution of $y=x^2$ about x-axis from 0 to 1.",
  ["$\\frac{\\pi}{3}$", "$\\frac{\\pi}{5}$", "$\\frac{\\pi}{4}$", "$\\pi$"], "$\\frac{\\pi}{5}$",
  ["$V=\\pi\\int_0^1 x^4 dx = \\frac{\\pi}{5}$."])
Q("calculus", "applications-integration", 2019, "medium", "Area between $y = \\sin x$ and x-axis from 0 to $\\pi$.",
  ["0", "1", "2", "$\\pi$"], "2", ["$\\int_0^\\pi \\sin x dx = [-\\cos x]_0^\\pi = 1 - (-1) = 2$."])
Q("calculus", "applications-integration", 2020, "easy", "Definite integral is used to find:",
  ["slope", "area / accumulated change", "rate", "limit"], "area / accumulated change",
  ["By the Fundamental Theorem of Calculus."])

# ============ VECTORS — 50 questions ============
# Vector Algebra 2D (10)
Q("vectors", "vector-algebra-2d", 2018, "easy", "If $\\vec{a} = 2\\mathbf{i} + 3\\mathbf{j}$ and $\\vec{b} = \\mathbf{i} - \\mathbf{j}$, find $\\vec{a} + \\vec{b}$.",
  ["$3\\mathbf{i} + 2\\mathbf{j}$", "$\\mathbf{i} + 4\\mathbf{j}$", "$3\\mathbf{i} + 4\\mathbf{j}$", "$\\mathbf{i} + 2\\mathbf{j}$"], "$3\\mathbf{i} + 2\\mathbf{j}$",
  ["Add component-wise: $(2+1)\\mathbf{i} + (3-1)\\mathbf{j}$."])
Q("vectors", "vector-algebra-2d", 2019, "medium", "Given $\\vec{p}=3\\mathbf{i}-2\\mathbf{j}$, find $2\\vec{p}$.",
  ["$6\\mathbf{i}-4\\mathbf{j}$", "$3\\mathbf{i}-4\\mathbf{j}$", "$5\\mathbf{i}$", "$6\\mathbf{i}+4\\mathbf{j}$"], "$6\\mathbf{i}-4\\mathbf{j}$",
  ["Scalar mult: $2(3\\mathbf{i}-2\\mathbf{j})=6\\mathbf{i}-4\\mathbf{j}$."])
Q("vectors", "vector-algebra-2d", 2020, "medium", "$\\vec{a}=4\\mathbf{i}+\\mathbf{j}$, $\\vec{b}=\\mathbf{i}+3\\mathbf{j}$. Find $\\vec{a}-\\vec{b}$.",
  ["$3\\mathbf{i}-2\\mathbf{j}$", "$3\\mathbf{i}+2\\mathbf{j}$", "$5\\mathbf{i}+4\\mathbf{j}$", "$3\\mathbf{i}+4\\mathbf{j}$"], "$3\\mathbf{i}-2\\mathbf{j}$",
  ["$(4-1)\\mathbf{i} + (1-3)\\mathbf{j} = 3\\mathbf{i}-2\\mathbf{j}$."])
Q("vectors", "vector-algebra-2d", 2021, "hard", "If $\\vec{u}=2\\mathbf{i}+k\\mathbf{j}$ and $\\vec{u}+\\vec{v}=5\\mathbf{i}+3\\mathbf{j}$ with $\\vec{v}=3\\mathbf{i}-2\\mathbf{j}$, find $k$.",
  ["3", "5", "1", "2"], "5",
  ["$\\vec{u}=\\vec{u}+\\vec{v}-\\vec{v}=(5\\mathbf{i}+3\\mathbf{j})-(3\\mathbf{i}-2\\mathbf{j})=2\\mathbf{i}+5\\mathbf{j}$.", "Therefore $k=5$."])
Q("vectors", "vector-algebra-2d", 2017, "easy", "The zero vector has magnitude:",
  ["1", "0", "depends", "undefined"], "0", ["By definition."])
Q("vectors", "vector-algebra-2d", 2022, "medium", "Position vector of point $(3, 5)$.",
  ["$5\\mathbf{i}+3\\mathbf{j}$", "$3\\mathbf{i}+5\\mathbf{j}$", "$3\\mathbf{i}-5\\mathbf{j}$", "$8\\mathbf{i}$"], "$3\\mathbf{i}+5\\mathbf{j}$",
  ["Position vector of $(x,y)$ is $x\\mathbf{i}+y\\mathbf{j}$."])
Q("vectors", "vector-algebra-2d", 2023, "easy", "$\\mathbf{i}-\\mathbf{i} =$",
  ["$\\mathbf{0}$", "$\\mathbf{i}$", "$1$", "$2\\mathbf{i}$"], "$\\mathbf{0}$", ["Zero vector."])
Q("vectors", "vector-algebra-2d", 2018, "hard", "If $\\vec{a}=k\\mathbf{i}+2\\mathbf{j}$ and $\\vec{b}=4\\mathbf{i}+8\\mathbf{j}$ are parallel, $k=$?",
  ["1", "2", "4", "8"], "1",
  ["Parallel iff $\\vec{a}=\\lambda\\vec{b}$.", "Component-wise: $\\frac{k}{4}=\\frac{2}{8}=\\frac{1}{4}$, so $k=1$."])
Q("vectors", "vector-algebra-2d", 2019, "medium", "If $\\overrightarrow{AB} = (3, 4)$, find $\\overrightarrow{BA}$.",
  ["$(3, 4)$", "$(-3, -4)$", "$(4, 3)$", "$(-3, 4)$"], "$(-3, -4)$", ["Reverse direction: negate."])
Q("vectors", "vector-algebra-2d", 2020, "easy", "$\\vec{a}+\\vec{b}=\\vec{b}+\\vec{a}$? (Yes/No)",
  ["Yes", "No", "Sometimes", "Depends"], "Yes", ["Vector addition is commutative."])

# 3D Vectors (10)
Q("vectors", "vectors-3d", 2018, "easy", "If $\\vec{a}=\\mathbf{i}+2\\mathbf{j}+3\\mathbf{k}$, the y-component is:",
  ["1", "2", "3", "0"], "2", ["Coefficient of $\\mathbf{j}$ is 2."])
Q("vectors", "vectors-3d", 2019, "medium", "Find $\\vec{a}+\\vec{b}$ where $\\vec{a}=\\mathbf{i}-\\mathbf{j}+\\mathbf{k}$, $\\vec{b}=2\\mathbf{i}+\\mathbf{j}-\\mathbf{k}$.",
  ["$3\\mathbf{i}+\\mathbf{j}$", "$3\\mathbf{i}$", "$3\\mathbf{i}+0\\mathbf{k}$", "$3\\mathbf{i}+0\\mathbf{j}+0\\mathbf{k}$"], "$3\\mathbf{i}+0\\mathbf{j}+0\\mathbf{k}$",
  ["Add components: $(1+2)\\mathbf{i}+(-1+1)\\mathbf{j}+(1-1)\\mathbf{k}=3\\mathbf{i}$."])
Q("vectors", "vectors-3d", 2020, "medium", "Position vector of $A(1,2,3)$ — $B(4,6,3)$, find $\\overrightarrow{AB}$.",
  ["$3\\mathbf{i}+4\\mathbf{j}$", "$5\\mathbf{i}+8\\mathbf{j}+6\\mathbf{k}$", "$3\\mathbf{i}+4\\mathbf{j}+0\\mathbf{k}$", "$-3\\mathbf{i}-4\\mathbf{j}$"], "$3\\mathbf{i}+4\\mathbf{j}+0\\mathbf{k}$",
  ["$\\overrightarrow{AB}=B-A=(4-1, 6-2, 3-3)=(3, 4, 0)$."])
Q("vectors", "vectors-3d", 2021, "hard", "Find $k$ so that $\\vec{a}=2\\mathbf{i}+k\\mathbf{j}-\\mathbf{k}$ and $\\vec{b}=4\\mathbf{i}-2\\mathbf{j}-2\\mathbf{k}$ are parallel.",
  ["$-1$", "$2$", "$-2$", "$1$"], "$-1$",
  ["Parallel: $\\frac{2}{4}=\\frac{k}{-2}=\\frac{-1}{-2}$.", "From $\\frac{2}{4}=\\frac{k}{-2}$: $k=-1$."])
Q("vectors", "vectors-3d", 2017, "easy", "What is the magnitude of $\\mathbf{k}$?",
  ["0", "1", "$\\sqrt{2}$", "$\\sqrt{3}$"], "1", ["Unit vectors $\\mathbf{i}, \\mathbf{j}, \\mathbf{k}$ have magnitude 1."])
Q("vectors", "vectors-3d", 2022, "medium", "Find $2\\vec{a}$ where $\\vec{a}=\\mathbf{i}+\\mathbf{j}+\\mathbf{k}$.",
  ["$2\\mathbf{i}+\\mathbf{j}+\\mathbf{k}$", "$2\\mathbf{i}+2\\mathbf{j}+2\\mathbf{k}$", "$2(\\mathbf{i}+\\mathbf{j})$", "$2\\mathbf{i}\\mathbf{j}\\mathbf{k}$"], "$2\\mathbf{i}+2\\mathbf{j}+2\\mathbf{k}$",
  ["Scalar multiplication is component-wise."])
Q("vectors", "vectors-3d", 2023, "hard", "Sum $\\sum$ of unit vectors $\\mathbf{i}+\\mathbf{j}+\\mathbf{k}$ has magnitude:",
  ["1", "$\\sqrt{2}$", "$\\sqrt{3}$", "3"], "$\\sqrt{3}$",
  ["$|1\\mathbf{i}+1\\mathbf{j}+1\\mathbf{k}|=\\sqrt{1+1+1}=\\sqrt{3}$."])
Q("vectors", "vectors-3d", 2018, "easy", "$\\vec{a}=3\\mathbf{i}-2\\mathbf{j}+\\mathbf{k}$. The z-component is:",
  ["3", "$-2$", "1", "0"], "1", ["Coefficient of $\\mathbf{k}$ is 1."])
Q("vectors", "vectors-3d", 2019, "medium", "Equal vectors must have:",
  ["Same magnitude only", "Same direction only", "Same magnitude AND direction", "Same components in 2D"], "Same magnitude AND direction",
  ["Equal vectors agree in both magnitude and direction."])
Q("vectors", "vectors-3d", 2020, "easy", "Subtract $\\vec{a}=2\\mathbf{i}+3\\mathbf{j}-\\mathbf{k}$ from $\\vec{b}=\\mathbf{i}+\\mathbf{j}+\\mathbf{k}$.",
  ["$\\mathbf{i}+2\\mathbf{j}-2\\mathbf{k}$", "$-\\mathbf{i}-2\\mathbf{j}+2\\mathbf{k}$", "$3\\mathbf{i}+4\\mathbf{j}$", "$\\mathbf{i}+2\\mathbf{j}+0\\mathbf{k}$"], "$-\\mathbf{i}-2\\mathbf{j}+2\\mathbf{k}$",
  ["$\\vec{b}-\\vec{a}=(1-2)\\mathbf{i}+(1-3)\\mathbf{j}+(1-(-1))\\mathbf{k}=-\\mathbf{i}-2\\mathbf{j}+2\\mathbf{k}$."])

# Magnitude & Direction (10)
Q("vectors", "magnitude-direction", 2018, "easy", "Find $|\\vec{a}|$ if $\\vec{a}=3\\mathbf{i}+4\\mathbf{j}$.",
  ["3", "4", "5", "7"], "5", ["$|\\vec{a}|=\\sqrt{9+16}=5$."])
Q("vectors", "magnitude-direction", 2019, "medium", "Find unit vector in direction of $\\vec{a}=6\\mathbf{i}+8\\mathbf{j}$.",
  ["$\\frac{3}{5}\\mathbf{i}+\\frac{4}{5}\\mathbf{j}$", "$\\frac{1}{5}\\mathbf{i}+\\frac{4}{5}\\mathbf{j}$", "$\\mathbf{i}+\\mathbf{j}$", "$\\frac{1}{2}\\mathbf{i}+\\mathbf{j}$"], "$\\frac{3}{5}\\mathbf{i}+\\frac{4}{5}\\mathbf{j}$",
  ["$|\\vec{a}|=10$.", "$\\hat{a}=\\vec{a}/|\\vec{a}|=\\frac{6}{10}\\mathbf{i}+\\frac{8}{10}\\mathbf{j}=\\frac{3}{5}\\mathbf{i}+\\frac{4}{5}\\mathbf{j}$."])
Q("vectors", "magnitude-direction", 2020, "medium", "Magnitude of $\\vec{a}=\\mathbf{i}+\\mathbf{j}+\\mathbf{k}$.",
  ["1", "$\\sqrt{2}$", "$\\sqrt{3}$", "3"], "$\\sqrt{3}$", ["$\\sqrt{1+1+1}$."])
Q("vectors", "magnitude-direction", 2021, "hard", "Magnitude of $\\vec{a}=2\\mathbf{i}-3\\mathbf{j}+6\\mathbf{k}$.",
  ["5", "7", "9", "11"], "7", ["$\\sqrt{4+9+36}=\\sqrt{49}=7$."])
Q("vectors", "magnitude-direction", 2017, "easy", "$|\\vec{a}|$ is always:",
  ["positive", "non-negative", "negative", "imaginary"], "non-negative", ["Magnitudes are $\\geq 0$ ($=0$ only for zero vector)."])
Q("vectors", "magnitude-direction", 2022, "medium", "Direction angle (from +x axis) of $\\vec{a}=\\mathbf{i}+\\mathbf{j}$.",
  ["$30°$", "$45°$", "$60°$", "$90°$"], "$45°$",
  ["$\\tan\\theta=\\frac{1}{1}=1$, $\\theta=45°$."])
Q("vectors", "magnitude-direction", 2023, "hard", "Direction angle of $\\vec{a}=-\\mathbf{i}+\\sqrt{3}\\mathbf{j}$.",
  ["$60°$", "$120°$", "$150°$", "$240°$"], "$120°$",
  ["Q2 (x<0, y>0).", "Reference angle $\\tan^{-1}\\sqrt{3}=60°$.", "Direction $=180°-60°=120°$."])
Q("vectors", "magnitude-direction", 2018, "easy", "If $|\\vec{a}|=5$, $|2\\vec{a}|$ is:",
  ["5", "10", "25", "$\\sqrt{10}$"], "10", ["$|k\\vec{a}|=|k||\\vec{a}|=2\\times 5=10$."])
Q("vectors", "magnitude-direction", 2019, "medium", "Unit vector of $\\vec{a}=\\mathbf{i}$ is:",
  ["$\\mathbf{i}$", "$\\mathbf{j}$", "$\\mathbf{0}$", "$2\\mathbf{i}$"], "$\\mathbf{i}$", ["$|\\mathbf{i}|=1$, so $\\hat{i}=\\mathbf{i}$ itself."])
Q("vectors", "magnitude-direction", 2020, "easy", "Magnitude of $\\vec{a}=5\\mathbf{i}-12\\mathbf{j}$.",
  ["7", "13", "17", "25"], "13", ["$\\sqrt{25+144}=13$."])

# Scalar (Dot) Product (10)
Q("vectors", "scalar-product", 2018, "easy", "$\\vec{a}\\cdot\\vec{b}$ if $\\vec{a}=2\\mathbf{i}+3\\mathbf{j}$, $\\vec{b}=\\mathbf{i}-\\mathbf{j}$.",
  ["$-1$", "$1$", "$5$", "$-5$"], "$-1$", ["$(2)(1)+(3)(-1)=2-3=-1$."])
Q("vectors", "scalar-product", 2019, "medium", "Two vectors are perpendicular iff:",
  ["$\\vec{a}=\\vec{b}$", "$\\vec{a}\\cdot\\vec{b}=0$", "$\\vec{a}\\cdot\\vec{b}=1$", "$|\\vec{a}|=|\\vec{b}|$"], "$\\vec{a}\\cdot\\vec{b}=0$",
  ["Zero dot product ⇔ angle is $90°$."])
Q("vectors", "scalar-product", 2020, "medium", "$\\vec{a}=3\\mathbf{i}+4\\mathbf{j}$, $\\vec{b}=4\\mathbf{i}-3\\mathbf{j}$. Are they perpendicular?",
  ["Yes", "No", "Parallel", "Cannot tell"], "Yes",
  ["$\\vec{a}\\cdot\\vec{b}=12-12=0$ → perpendicular."])
Q("vectors", "scalar-product", 2021, "hard", "Find $k$ so that $\\vec{a}=\\mathbf{i}+k\\mathbf{j}$ and $\\vec{b}=2\\mathbf{i}-\\mathbf{j}$ are perpendicular.",
  ["$-2$", "$2$", "$1$", "$0$"], "$2$",
  ["$\\vec{a}\\cdot\\vec{b}=2-k=0 \\Rightarrow k=2$."])
Q("vectors", "scalar-product", 2017, "easy", "$\\mathbf{i}\\cdot\\mathbf{j}=$",
  ["0", "1", "$-1$", "depends"], "0", ["Perpendicular unit vectors."])
Q("vectors", "scalar-product", 2022, "medium", "$\\mathbf{i}\\cdot\\mathbf{i}=$",
  ["0", "1", "$\\mathbf{i}$", "$\\sqrt{2}$"], "1", ["$|\\mathbf{i}||\\mathbf{i}|\\cos 0°=1\\cdot 1\\cdot 1=1$."])
Q("vectors", "scalar-product", 2023, "hard", "Angle between $\\vec{a}=\\mathbf{i}+\\mathbf{j}$ and $\\vec{b}=\\mathbf{i}-\\mathbf{j}$.",
  ["$0°$", "$45°$", "$90°$", "$180°$"], "$90°$",
  ["$\\vec{a}\\cdot\\vec{b}=1-1=0$ → perpendicular."])
Q("vectors", "scalar-product", 2018, "medium", "3D: $\\vec{a}\\cdot\\vec{b}$ if $\\vec{a}=\\mathbf{i}+2\\mathbf{j}-\\mathbf{k}$, $\\vec{b}=2\\mathbf{i}-\\mathbf{j}+3\\mathbf{k}$.",
  ["$-3$", "$3$", "$0$", "$1$"], "$-3$", ["$(1)(2)+(2)(-1)+(-1)(3)=2-2-3=-3$."])
Q("vectors", "scalar-product", 2019, "hard", "If $\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|$, the angle between them is:",
  ["$0°$", "$45°$", "$90°$", "$180°$"], "$0°$", ["$\\cos\\theta=1 \\Rightarrow\\theta=0°$ (parallel, same direction)."])
Q("vectors", "scalar-product", 2020, "easy", "$\\mathbf{j}\\cdot\\mathbf{k}=$",
  ["0", "1", "$\\mathbf{i}$", "$-1$"], "0", ["Perpendicular unit vectors."])

# Vector Applications (10)
Q("vectors", "vectors-applications", 2018, "medium", "Midpoint of $A(1, 4)$ and $B(5, 8)$.",
  ["$(3, 6)$", "$(2, 5)$", "$(6, 12)$", "$(4, 4)$"], "$(3, 6)$",
  ["$((1+5)/2, (4+8)/2) = (3, 6)$."])
Q("vectors", "vectors-applications", 2019, "hard", "If A, B, C have position vectors $\\vec{a}, \\vec{b}, \\vec{c}$ and $\\overrightarrow{AB}=2\\overrightarrow{AC}$, then:",
  ["AB parallel to AC, B is twice as far from A", "Triangle ABC", "B = A", "B = C"], "AB parallel to AC, B is twice as far from A",
  ["Scalar multiple means parallel; factor 2 means B is 2× the distance."])
Q("vectors", "vectors-applications", 2020, "medium", "Distance between $A(1,2,3)$ and $B(4,6,3)$.",
  ["3", "4", "5", "7"], "5", ["$|\\overrightarrow{AB}|=\\sqrt{9+16+0}=5$."])
Q("vectors", "vectors-applications", 2021, "easy", "If $\\overrightarrow{AB}=\\overrightarrow{CD}$, points A,B,C,D form:",
  ["A line", "A parallelogram (or are collinear)", "A triangle", "Equilateral triangle"], "A parallelogram (or are collinear)",
  ["Equal vectors → AB parallel and equal in length to CD."])
Q("vectors", "vectors-applications", 2017, "medium", "Position vector of midpoint of A($\\vec{a}$) and B($\\vec{b}$) is:",
  ["$\\vec{a}+\\vec{b}$", "$\\frac{1}{2}(\\vec{a}+\\vec{b})$", "$\\vec{b}-\\vec{a}$", "$\\vec{a}\\cdot\\vec{b}$"], "$\\frac{1}{2}(\\vec{a}+\\vec{b})$",
  ["Standard midpoint formula in vector form."])
Q("vectors", "vectors-applications", 2022, "hard", "Find $\\overrightarrow{AB}$ if $A(2, 1)$, $B(5, 7)$, and its magnitude.",
  ["$(3, 6), \\sqrt{45}$", "$(3, 6), \\sqrt{27}$", "$(7, 8), 11$", "$(3, 6), 3$"], "$(3, 6), \\sqrt{45}$",
  ["$\\overrightarrow{AB}=B-A=(3, 6)$.", "$|\\overrightarrow{AB}|=\\sqrt{9+36}=\\sqrt{45}=3\\sqrt{5}$."])
Q("vectors", "vectors-applications", 2023, "medium", "Points A, B, C are collinear iff $\\overrightarrow{AB}$ and $\\overrightarrow{AC}$ are:",
  ["Equal", "Perpendicular", "Parallel (scalar multiples)", "Opposite"], "Parallel (scalar multiples)",
  ["Collinearity test."])
Q("vectors", "vectors-applications", 2018, "easy", "If position vectors $\\vec{a}=(1,2)$, $\\vec{b}=(4,6)$, then $\\overrightarrow{AB}=$",
  ["$(3,4)$", "$(5,8)$", "$(-3,-4)$", "$(1,2)$"], "$(3,4)$", ["$\\vec{b}-\\vec{a}=(3,4)$."])
Q("vectors", "vectors-applications", 2019, "hard", "If $\\overrightarrow{AB}=2\\mathbf{i}+\\mathbf{j}$ and $\\overrightarrow{BC}=\\mathbf{i}-2\\mathbf{j}$, find $\\overrightarrow{AC}$.",
  ["$3\\mathbf{i}-\\mathbf{j}$", "$3\\mathbf{i}+\\mathbf{j}$", "$\\mathbf{i}+\\mathbf{j}$", "$\\mathbf{i}-\\mathbf{j}$"], "$3\\mathbf{i}-\\mathbf{j}$",
  ["$\\overrightarrow{AC}=\\overrightarrow{AB}+\\overrightarrow{BC}=(2+1)\\mathbf{i}+(1-2)\\mathbf{j}=3\\mathbf{i}-\\mathbf{j}$."])
Q("vectors", "vectors-applications", 2020, "easy", "If $\\overrightarrow{AB}=\\vec{0}$, what can be said about A and B?",
  ["B is far from A", "A=B", "A perpendicular to B", "Cannot tell"], "A=B",
  ["Zero displacement vector means the same point."])
