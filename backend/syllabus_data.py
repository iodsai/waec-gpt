"""WAEC Further Mathematics / Mathematics (Elective) syllabus map.

This file keeps the official syllabus structure separate from the seeded
lesson/question bank. Items can point to existing lessons where available while
still exposing the full syllabus for planning and country-specific guidance.
"""

SYLLABUS_SOURCE = {
    "name": "WAEC Further Mathematics / Mathematics (Elective) syllabus",
    "url": "https://waecgh.org/wp-content/uploads/2024/07/FURTHER-MATHEMATICS.pdf",
    "note": "Topics marked Ghana-only or Nigeria-only follow the asterisk notes in the WAEC syllabus.",
}

COUNTRY_FILTERS = [
    {"id": "all", "name": "All WAEC candidates"},
    {"id": "nigeria", "name": "Nigeria"},
    {"id": "ghana", "name": "Ghana"},
]


def item(
    item_id,
    title,
    summary,
    contents,
    course_topic=None,
    course_subtopic=None,
    related_subtopics=None,
    country_details=None,
):
    return {
        "id": item_id,
        "title": title,
        "summary": summary,
        "scope": "general",
        "contents": contents,
        "course_topic": course_topic,
        "course_subtopic": course_subtopic,
        "related_subtopics": related_subtopics or [],
        "country_details": country_details or [],
    }


SYLLABUS_SECTIONS = [
    {
        "id": "pure-mathematics",
        "name": "Pure Mathematics",
        "paper_weight": "Paper 1: 30 of 40 objective questions. Paper 2: main Part I coverage.",
        "description": "Algebra, functions, matrices, trigonometry, coordinate geometry, differentiation and integration.",
        "items": [
            item(
                "sets",
                "Sets",
                "Set notation, operations, Venn diagrams and De Morgan's laws.",
                [
                    "Idea of a set defined by a property and set notation.",
                    "Disjoint sets, universal set, complement, subset and power set ideas.",
                    "Venn diagrams, including three-set problems.",
                    "Commutative, associative and distributive laws over union and intersection.",
                    "De Morgan's laws for related set problems.",
                ],
                "sets-logic",
                "set-operations",
                ["set-operations", "venn-diagrams", "subsets-power"],
            ),
            item(
                "surds",
                "Surds",
                "Operations on surds and rationalising denominators.",
                [
                    "Surds of the form a/sqrt(b), a sqrt(b), and a + b sqrt(n).",
                    "Addition, subtraction, multiplication and division of surds.",
                    "Rationalising denominators involving one or two surd terms.",
                ],
                "surds-polynomials",
                "surd-simplification",
                ["surd-simplification"],
            ),
            item(
                "binary-operations",
                "Binary Operations",
                "Closure, identity, inverse and structural properties of operations.",
                [
                    "Closure, commutativity, associativity and distributivity.",
                    "Identity elements and inverses.",
                    "Use of operation tables or defined operations to solve problems.",
                ],
                "sets-logic",
                "binary-operations",
                ["binary-operations", "set-operations", "propositional-logic"],
            ),
            item(
                "logical-reasoning",
                "Logical Reasoning",
                "Truth values, connectives, implications and truth tables.",
                [
                    "True and false statements.",
                    "Rules of logic applied to arguments, implications and deductions.",
                    "Connectives including not, or, and, implies.",
                    "Truth tables and negation of compound statements.",
                ],
                "sets-logic",
                "propositional-logic",
                ["propositional-logic", "truth-tables"],
            ),
            item(
                "functions",
                "Functions",
                "Domain, range, inverse functions and composite functions.",
                [
                    "Domain and co-domain.",
                    "One-to-one, onto, identity and constant mappings.",
                    "Inverse of a function.",
                    "Composite functions and notation such as fog(x).",
                    "Graphical representation, image and range.",
                ],
                "surds-polynomials",
                "functions-mappings",
                ["functions-mappings", "polynomial-division", "remainder-theorem"],
            ),
            item(
                "polynomial-functions",
                "Polynomial Functions",
                "Linear, quadratic and cubic functions, equations, inequalities and graphs.",
                [
                    "Linear functions, equations, inequalities and linear programming.",
                    "Quadratic functions, equations, inequalities and graph features.",
                    "Completing the square, discriminant, roots, sum and product of roots.",
                    "Cubic functions, factorisation and solution of cubic equations.",
                    "Basic operations on polynomials, remainder theorem and factor theorem.",
                ],
                "surds-polynomials",
                "polynomial-division",
                ["polynomial-division", "remainder-theorem"],
            ),
            item(
                "rational-functions",
                "Rational Functions",
                "Rational functions, domain/range and partial fractions.",
                [
                    "Rational functions of the form f(x)/g(x), where g(x) is not zero.",
                    "Zeros, domain and range.",
                    "Resolution of rational functions into partial fractions.",
                ],
                "surds-polynomials",
                "partial-fractions",
                ["partial-fractions"],
            ),
            item(
                "indices-logarithms",
                "Indices and Logarithmic Functions",
                "Laws of indices, logarithms and related equations.",
                [
                    "Laws of indices and application to products, quotients, powers and roots.",
                    "Equations involving indices.",
                    "Laws of logarithms and logarithmic calculations.",
                    "Equations involving logarithms.",
                ],
                "surds-polynomials",
                "indices-logs-fm",
                ["indices-logs-fm"],
                [
                    {
                        "country": "ghana",
                        "title": "Logarithmic graph work",
                        "details": "Drawing and interpreting logarithmic graphs and estimating constants from the graph.",
                    }
                ],
            ),
            item(
                "permutation-combination",
                "Permutations and Combinations",
                "Arrangement and selection problems.",
                [
                    "Simple cases of arrangements.",
                    "Simple cases of selection of objects.",
                    "Use of nPr and nCr notation and formulae.",
                    "Examples such as arranging students or drawing balls with or without replacement.",
                ],
                "statistics",
                "perms-combinations",
                ["perms-combinations"],
            ),
            item(
                "binomial-theorem",
                "Binomial Theorem",
                "Expansion of (a + b)^n and simple approximations.",
                [
                    "Expansion of (a + b)^n for positive integral index.",
                    "Use of (1 + x)^n approximations for small x.",
                    "General term and binomial coefficients.",
                ],
                "sequences-binomial",
                "binomial-expansion",
                ["binomial-expansion", "pascals-triangle"],
            ),
            item(
                "sequences-series",
                "Sequences and Series",
                "Finite and infinite sequences, AP, GP and sum formulae.",
                [
                    "Recognising patterns in finite and infinite sequences.",
                    "Arithmetic progression nth term and sum.",
                    "Geometric progression nth term, finite sum and sum to infinity.",
                ],
                "sequences-binomial",
                "ap-fm",
                ["ap-fm", "gp-fm", "infinite-series"],
                [
                    {
                        "country": "ghana",
                        "title": "Recurrence series",
                        "details": "Generating terms of a recurrence series and finding an explicit formula for the sequence.",
                    }
                ],
            ),
            item(
                "matrices-linear-transformation",
                "Matrices and Linear Transformation",
                "Matrix operations, determinants, inverses and transformations.",
                [
                    "Order, type and equality of matrices.",
                    "Addition, subtraction and multiplication of matrices up to 3 by 3.",
                    "Determinants and inverse of 2 by 2 matrices.",
                    "Use of determinants to solve simultaneous linear equations.",
                    "Finding images of points under a linear transformation.",
                    "Reflection, rotation, identity and composition of transformations.",
                ],
                "matrices",
                "matrix-operations",
                ["matrix-operations", "determinants", "matrix-inverse", "linear-systems", "matrix-properties"],
                [
                    {
                        "country": "nigeria",
                        "title": "3 by 3 determinants",
                        "details": "Evaluation of determinants of 3 by 3 matrices.",
                    },
                    {
                        "country": "ghana",
                        "title": "Image of a line",
                        "details": "Finding the equation of the image of a line under a given linear transformation.",
                    },
                ],
            ),
            item(
                "trigonometry",
                "Trigonometry",
                "Ratios, identities, compound angles, equations and graphs.",
                [
                    "Sine, cosine and tangent of general angles.",
                    "Ratios for 30, 45 and 60 degrees without tables.",
                    "Basic identities, negative angles, radians and degrees.",
                    "Heights and distances, bearings, sine rule and cosine rule.",
                    "Compound and multiple angles.",
                    "Trigonometric functions, graphs and equations.",
                ],
                "calculus",
                "trigonometry-fm",
                ["trigonometry-fm", "differentiation", "integration"],
                country_details=[
                    {
                        "country": "ghana",
                        "title": "R sin/cos transformation",
                        "details": "Expressing a sin x + b cos x in R cos(x +/- alpha) or R sin(x +/- alpha) form.",
                    }
                ],
            ),
            item(
                "coordinate-geometry",
                "Coordinate Geometry",
                "Straight lines, circles, loci and conic sections.",
                [
                    "Midpoint, section formula and distance between two points.",
                    "Gradient, equation of a line and intercept forms.",
                    "Parallel and perpendicular lines and angle between intersecting lines.",
                    "Loci, equations of circles and tangents/normals to circles.",
                    "Parabola equations and tangent/normal to a parabola.",
                ],
                "vectors",
                "vectors-applications",
                ["vectors-applications"],
                [
                    {
                        "country": "ghana",
                        "title": "Advanced coordinate geometry",
                        "details": "Distance from a point to a line and sketching parabolas with axis of symmetry.",
                    }
                ],
            ),
            item(
                "differentiation",
                "Differentiation",
                "Limits, derivatives, rules and applications.",
                [
                    "Intuitive treatment of limits.",
                    "Derivative from first principles in simple cases.",
                    "Differentiation of polynomials and trigonometric functions.",
                    "Product, quotient and implicit differentiation.",
                    "Second derivatives, rates of change, small changes, maxima and minima.",
                    "Tangents, normals and curve sketching up to cubic functions.",
                ],
                "calculus",
                "differentiation",
                ["limits", "differentiation", "applications-differentiation"],
                [
                    {
                        "country": "nigeria",
                        "title": "Transcendental functions",
                        "details": "Differentiation of functions such as exponential and logarithmic functions.",
                    }
                ],
            ),
            item(
                "integration",
                "Integration",
                "Indefinite, definite and applied integration.",
                [
                    "Integration of polynomial expressions.",
                    "Definite integrals.",
                    "Simple substitution and simple trigonometric integrals.",
                    "Plane areas, rate of change and linear kinematics.",
                    "Volume of revolution and trapezium rule approximation.",
                ],
                "calculus",
                "integration",
                ["integration", "applications-integration"],
                [
                    {
                        "country": "nigeria",
                        "title": "Integral of x^-1",
                        "details": "Integration of x^-1 giving ln x.",
                    }
                ],
            ),
        ],
    },
    {
        "id": "statistics-probability",
        "name": "Statistics and Probability",
        "paper_weight": "Paper 1: 4 of 40 objective questions. Paper 2: Part II coverage.",
        "description": "Data representation, measures, correlation, probability and probability distributions.",
        "items": [
            item(
                "statistics",
                "Statistics",
                "Data representation, location, dispersion and correlation.",
                [
                    "Frequency tables and cumulative frequency tables.",
                    "Histograms, including unequal class intervals.",
                    "Cumulative frequency curve or ogive.",
                    "Mean, median, mode, quartiles and percentiles.",
                    "Range, interquartile range, mean deviation, variance and standard deviation.",
                    "Scatter diagrams, correlation and Spearman's rank coefficient.",
                ],
                "statistics",
                "measures-of-location",
                ["measures-of-location", "measures-of-spread", "correlation"],
                [
                    {
                        "country": "ghana",
                        "title": "Least-squares regression",
                        "details": "Equation of line of best fit by least-square method.",
                    }
                ],
            ),
            item(
                "probability",
                "Probability",
                "Probability rules, events and distributions.",
                [
                    "Meaning of probability and relative frequency.",
                    "Calculation of probability using simple sample spaces.",
                    "Addition and multiplication rules.",
                    "Equally likely, mutually exclusive, independent and conditional events.",
                    "Probability of an event as probability of a set.",
                    "Binomial distribution for simple problems.",
                ],
                "statistics",
                "probability",
                ["probability", "perms-combinations"],
                [
                    {
                        "country": "nigeria",
                        "title": "Poisson distribution",
                        "details": "Poisson distribution where n is large and p is small.",
                    }
                ],
            ),
        ],
    },
    {
        "id": "vectors-mechanics",
        "name": "Vectors and Mechanics",
        "paper_weight": "Paper 1: 6 of 40 objective questions. Paper 2: Part III coverage.",
        "description": "Vectors, statics and dynamics.",
        "items": [
            item(
                "vectors",
                "Vectors",
                "Vector algebra, position vectors, resolution and products.",
                [
                    "Definitions of scalar and vector quantities.",
                    "Representation of vectors in ai + bj form.",
                    "Addition, subtraction and multiplication by scalars.",
                    "Triangle, parallelogram and polygon laws.",
                    "Unit vectors, position vectors and midpoint of a line segment.",
                    "Resolution and composition of vectors.",
                    "Scalar product and angle between two vectors.",
                ],
                "vectors",
                "vector-algebra-2d",
                ["vector-algebra-2d", "vectors-3d", "magnitude-direction", "scalar-product", "vectors-applications"],
                [
                    {
                        "country": "ghana",
                        "title": "Vector ratio and scale drawing",
                        "details": "Internal division of a line segment in a ratio and resultant by scale drawing.",
                    },
                    {
                        "country": "nigeria",
                        "title": "Vector cross product",
                        "details": "Vector cross product and its application.",
                    },
                ],
            ),
            item(
                "statics",
                "Statics",
                "Forces, equilibrium, moments and friction.",
                [
                    "Definition and representation of forces.",
                    "Composition and resolution of coplanar forces.",
                    "Equilibrium of bodies and determination of resultant.",
                    "Moments of forces and application to related problems.",
                    "Friction, smooth and rough planes, coefficient of friction.",
                    "Lami's theorem and suspended particles.",
                ],
                "mechanics",
                "forces-equilibrium",
                ["resultant-vectors", "forces-equilibrium"],
            ),
            item(
                "dynamics",
                "Dynamics",
                "Motion, Newton's laws, momentum and projectiles.",
                [
                    "Displacement, speed, velocity and acceleration.",
                    "Composition of velocities and accelerations.",
                    "Rectilinear motion and motion under gravity.",
                    "Newton's laws and motion along inclined planes.",
                    "Equations of motion.",
                    "Impulse, momentum and conservation of linear momentum.",
                ],
                "mechanics",
                "kinematics",
                ["kinematics", "newtons-laws", "work-energy-power"],
                [
                    {
                        "country": "nigeria",
                        "title": "Projectiles",
                        "details": "Objects projected at an angle to the horizontal.",
                    }
                ],
            ),
        ],
    },
]
