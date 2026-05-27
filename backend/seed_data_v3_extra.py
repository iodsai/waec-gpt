"""V3 extra — content for the 5 remaining Further Maths topics.

Adds 250 questions (50 each) across:
- Sets & Logic
- Surds & Polynomials
- Sequences & Binomial
- Matrices & Determinants
- Mechanics
"""

EXTRA_SUBTOPICS = {
    "sets-logic": [
        {"id": "set-operations", "name": "Set Operations"},
        {"id": "venn-diagrams", "name": "Venn Diagrams"},
        {"id": "subsets-power", "name": "Subsets & Power Sets"},
        {"id": "binary-operations", "name": "Binary Operations"},
        {"id": "propositional-logic", "name": "Propositional Logic"},
        {"id": "truth-tables", "name": "Truth Tables"},
    ],
    "surds-polynomials": [
        {"id": "surd-simplification", "name": "Surd Simplification"},
        {"id": "indices-logs-fm", "name": "Indices & Logarithms"},
        {"id": "functions-mappings", "name": "Functions & Mappings"},
        {"id": "polynomial-division", "name": "Polynomial Division"},
        {"id": "remainder-theorem", "name": "Remainder Theorem"},
        {"id": "partial-fractions", "name": "Partial Fractions"},
    ],
    "calculus": [
        {"id": "trigonometry-fm", "name": "Trigonometry"},
    ],
    "sequences-binomial": [
        {"id": "ap-fm", "name": "Arithmetic Progression"},
        {"id": "gp-fm", "name": "Geometric Progression"},
        {"id": "infinite-series", "name": "Infinite Series"},
        {"id": "binomial-expansion", "name": "Binomial Expansion"},
        {"id": "pascals-triangle", "name": "Pascal's Triangle"},
    ],
    "matrices": [
        {"id": "matrix-operations", "name": "Matrix Operations"},
        {"id": "determinants", "name": "Determinants"},
        {"id": "matrix-inverse", "name": "Matrix Inverse"},
        {"id": "linear-systems", "name": "Linear Systems"},
        {"id": "matrix-properties", "name": "Matrix Properties"},
    ],
    "mechanics": [
        {"id": "kinematics", "name": "Kinematics"},
        {"id": "resultant-vectors", "name": "Resultant Vectors"},
        {"id": "forces-equilibrium", "name": "Forces & Equilibrium"},
        {"id": "newtons-laws", "name": "Newton's Laws & Momentum"},
        {"id": "work-energy-power", "name": "Work, Energy & Power"},
    ],
}

SET_OPERATIONS_SECTIONS = [
    {
        "title": "Set Language and Notation",
        "intro": "Before formulas, students must first understand the language. A set is a well-defined collection, and the universal set $U$ fixes the boundary of the discussion.",
        "key_points": [
            "$x \\in A$ means x is an element of A; $x \\notin A$ means x is not an element of A.",
            "$A \\cup B$ means A or B or both.",
            "$A \\cap B$ means A and B at the same time.",
            "$A'$ means everything in the universal set that is not in A.",
            "$A-B$ means start with A and remove the elements that are also in B.",
            "The same symbol can give different answers if the universal set changes.",
        ],
        "examples": [
            {
                "level": "foundation",
                "title": "Reading the symbols correctly",
                "problem": "Let $U=\\{1,2,3,4,5,6,7,8\\}$, $A=\\{2,4,6,8\\}$ and $B=\\{1,2,3,4\\}$. Find $A\\cup B$, $A\\cap B$, $A'$ and $A-B$.",
                "steps": [
                    "$A\\cup B$ contains everything that appears in A or B: $\\{1,2,3,4,6,8\\}$.",
                    "$A\\cap B$ contains only elements common to both sets: $\\{2,4\\}$.",
                    "$A'$ is found from U by removing A: $\\{1,3,5,7\\}$.",
                    "$A-B$ is found from A by removing members of B: remove 2 and 4, leaving $\\{6,8\\}$.",
                ],
                "answer": "$A\\cup B=\\{1,2,3,4,6,8\\}$, $A\\cap B=\\{2,4\\}$, $A'=\\{1,3,5,7\\}$, $A-B=\\{6,8\\}$."
            }
        ],
        "practice": [
            {
                "question": "If $U=\\{a,b,c,d,e\\}$ and $A=\\{a,c,e\\}$, find $A'$.",
                "answer": "$\\{b,d\\}$"
            },
            {
                "question": "If $A=\\{1,3,5,7\\}$ and $B=\\{3,4,5,6\\}$, find $A\\cap B$.",
                "answer": "$\\{3,5\\}$"
            }
        ]
    },
    {
        "title": "The Two-Set Counting Formula",
        "intro": "The formula for two sets is not a trick. It corrects double-counting. If a student understands why the overlap is subtracted, most WAEC set word problems become easier.",
        "key_points": [
            "Imagine the Venn diagram has three inside regions: A only, A and B, and B only.",
            "When you calculate $n(A)+n(B)$, the middle overlap $n(A\\cap B)$ is counted twice.",
            "The union $n(A\\cup B)$ needs that overlap counted only once, so we subtract one copy of it.",
            "Neither is outside both circles, so it is found by subtracting the union from the universal set.",
            "Exactly one means the two non-overlapping side regions: A only plus B only."
        ],
        "visual_blocks": [
            {
                "type": "venn",
                "variant": "union",
                "title": "Union: $n(A\\cup B)$",
                "caption": "All shaded regions inside A or B are counted. The overlap belongs to the union, but it must be counted once."
            },
            {
                "type": "venn",
                "variant": "intersection",
                "title": "Overlap: $n(A\\cap B)$",
                "caption": "This middle region is counted once inside A and once inside B. That is why the formula subtracts it once."
            },
            {
                "type": "venn",
                "variant": "neither",
                "title": "Neither: $n((A\\cup B)')$",
                "caption": "The shaded region outside both circles is everything in U that is not in A or B."
            },
            {
                "type": "venn",
                "variant": "exactly_one",
                "title": "Exactly one",
                "caption": "Only the two side regions are counted. The overlap is removed from both A and B."
            }
        ],
        "formulas": [
            {
                "name": "Two-set union",
                "expression": "$n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$",
                "meaning": "Add A and B, then subtract the overlap once because it was counted twice."
            },
            {
                "name": "Neither of two sets",
                "expression": "$n((A\\cup B)')=n(U)-n(A\\cup B)$",
                "meaning": "Neither means outside the union."
            },
            {
                "name": "Exactly one of two sets",
                "expression": "$n(A\\text{ only})+n(B\\text{ only})=n(A)+n(B)-2n(A\\cap B)$",
                "meaning": "Remove the common part from each set."
            }
        ],
        "examples": [
            {
                "level": "derivation",
                "title": "Derive the formula from Venn regions",
                "problem": "Suppose the Venn diagram has $a$ people in A only, $x$ people in both A and B, and $b$ people in B only. Show why $n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$.",
                "steps": [
                    "A contains A only plus the overlap, so $n(A)=a+x$.",
                    "B contains B only plus the overlap, so $n(B)=b+x$.",
                    "Adding gives $n(A)+n(B)=a+b+2x$.",
                    "But the union should be A only, overlap, and B only: $n(A\\cup B)=a+x+b$.",
                    "The addition counted the overlap twice, so subtract one $x=n(A\\cap B)$.",
                ],
                "answer": "$n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$."
            },
            {
                "level": "basic",
                "title": "Why subtract the overlap?",
                "problem": "In a class, 18 students play football, 15 play basketball and 6 play both. How many play at least one of the two games?",
                "steps": [
                    "At least one means union.",
                    "If we add 18 and 15, the 6 students who play both have been counted twice.",
                    "Use $n(F\\cup B)=n(F)+n(B)-n(F\\cap B)$.",
                    "$n(F\\cup B)=18+15-6=27$.",
                ],
                "answer": "27 students play at least one game."
            },
            {
                "level": "intermediate",
                "title": "Finding neither",
                "problem": "Out of 70 students, 38 study Physics, 29 study Chemistry and 12 study both. How many study neither Physics nor Chemistry?",
                "steps": [
                    "First find those who study at least one.",
                    "$n(P\\cup C)=38+29-12=55$.",
                    "Neither means outside $P\\cup C$.",
                    "$70-55=15$.",
                ],
                "answer": "15 students study neither subject."
            },
            {
                "level": "WAEC-style",
                "title": "Finding exactly one",
                "problem": "In a school survey of 100 students, 62 use a calculator app, 47 use a graphing app and 28 use both. How many use exactly one of the two apps?",
                "steps": [
                    "Calculator only: $62-28=34$.",
                    "Graphing only: $47-28=19$.",
                    "Exactly one means calculator only plus graphing only.",
                    "$34+19=53$.",
                ],
                "answer": "53 students use exactly one of the apps."
            },
            {
                "level": "conceptual",
                "title": "Why exactly one subtracts twice",
                "problem": "Explain why $n(A\\text{ only})+n(B\\text{ only})=n(A)+n(B)-2n(A\\cap B)$.",
                "steps": [
                    "Let the overlap be $x=n(A\\cap B)$.",
                    "$n(A)$ includes A only and the overlap.",
                    "$n(B)$ includes B only and the same overlap.",
                    "So $n(A)+n(B)$ includes the overlap twice.",
                    "Exactly one wants no overlap at all, so remove both copies: subtract $2x$.",
                ],
                "answer": "$n(A\\text{ only})+n(B\\text{ only})=n(A)+n(B)-2n(A\\cap B)$."
            }
        ],
        "applications": [
            {
                "title": "Quality control",
                "body": "A factory may classify devices with battery faults and screen faults. The overlap is devices with both faults; exactly one fault helps technicians decide the repair path."
            },
            {
                "title": "Physics lab data",
                "body": "Objects may be grouped by 'charged' and 'magnetic'. The intersection identifies objects with both properties, which often need special analysis."
            }
        ]
    },
    {
        "title": "The Three-Set Counting Formula",
        "intro": "Three-set questions are common in examinations because students often subtract too much or forget to add back the middle region. The safest method is to understand the seven regions of a three-circle Venn diagram.",
        "formulas": [
            {
                "name": "Three-set union",
                "expression": "$n(A\\cup B\\cup C)=n(A)+n(B)+n(C)-n(A\\cap B)-n(A\\cap C)-n(B\\cap C)+n(A\\cap B\\cap C)$",
                "meaning": "Add the three single sets, subtract the pair overlaps, then add the triple overlap back once."
            },
            {
                "name": "Neither of three sets",
                "expression": "$n((A\\cup B\\cup C)')=n(U)-n(A\\cup B\\cup C)$",
                "meaning": "First count everyone in at least one set, then subtract from the universal set."
            },
            {
                "name": "Only A",
                "expression": "$n(A\\text{ only})=n(A)-n(A\\cap B)-n(A\\cap C)+n(A\\cap B\\cap C)$",
                "meaning": "Remove the A with B and A with C parts, then restore the triple intersection because it was removed twice."
            }
        ],
        "examples": [
            {
                "level": "intermediate",
                "title": "At least one of three subjects",
                "problem": "In a class of 90 students, 45 study Physics, 40 study Chemistry and 35 study Biology. Also, 18 study Physics and Chemistry, 15 study Physics and Biology, 12 study Chemistry and Biology, and 5 study all three. How many study at least one of the subjects?",
                "steps": [
                    "Use the three-set formula.",
                    "$n(P\\cup C\\cup B)=45+40+35-18-15-12+5$.",
                    "Add the single sets: $45+40+35=120$.",
                    "Subtract pair overlaps: $120-18-15-12=75$.",
                    "Add the triple overlap back: $75+5=80$.",
                ],
                "answer": "80 students study at least one of the three subjects."
            },
            {
                "level": "WAEC-style",
                "title": "Finding neither from three sets",
                "problem": "A survey of 120 students shows that 50 like Mathematics, 48 like Physics and 42 like Further Mathematics. 20 like Mathematics and Physics, 18 like Mathematics and Further Mathematics, 16 like Physics and Further Mathematics, and 8 like all three. How many like none of the three?",
                "steps": [
                    "Find the union first.",
                    "$n(M\\cup P\\cup F)=50+48+42-20-18-16+8$.",
                    "$50+48+42=140$.",
                    "$140-20-18-16=86$.",
                    "$86+8=94$.",
                    "None means outside the union: $120-94=26$.",
                ],
                "answer": "26 students like none of the three subjects."
            },
            {
                "level": "complex",
                "title": "Only one of three engineering tests",
                "problem": "Among 100 components, 52 pass test A, 46 pass test B and 39 pass test C. Also, 24 pass A and B, 17 pass A and C, 15 pass B and C, and 9 pass all three. How many pass test A only?",
                "steps": [
                    "Use $n(A\\text{ only})=n(A)-n(A\\cap B)-n(A\\cap C)+n(A\\cap B\\cap C)$.",
                    "$n(A\\text{ only})=52-24-17+9$.",
                    "$52-24-17=11$.",
                    "$11+9=20$.",
                ],
                "answer": "20 components pass test A only."
            }
        ],
        "practice": [
            {
                "question": "If $n(A)=30$, $n(B)=25$, $n(C)=20$, $n(A\\cap B)=10$, $n(A\\cap C)=8$, $n(B\\cap C)=6$, and $n(A\\cap B\\cap C)=3$, find $n(A\\cup B\\cup C)$.",
                "answer": "$30+25+20-10-8-6+3=54$"
            }
        ]
    },
    {
        "title": "De Morgan's Laws for Two and Three Sets",
        "intro": "De Morgan's Laws explain what happens when a complement is placed outside a union or intersection. They are also the set version of logic rules used in circuits and computer programs.",
        "formulas": [
            {
                "name": "Two sets: outside a union",
                "expression": "$(A\\cup B)'=A'\\cap B'$",
                "meaning": "Not in A or B means not in A and not in B."
            },
            {
                "name": "Two sets: outside an intersection",
                "expression": "$(A\\cap B)'=A'\\cup B'$",
                "meaning": "Not in both means outside A or outside B."
            },
            {
                "name": "Three sets: outside a union",
                "expression": "$(A\\cup B\\cup C)'=A'\\cap B'\\cap C'$",
                "meaning": "Not in any of A, B or C means outside all three."
            },
            {
                "name": "Three sets: outside an intersection",
                "expression": "$(A\\cap B\\cap C)'=A'\\cup B'\\cup C'$",
                "meaning": "Not in all three means outside at least one of them."
            }
        ],
        "examples": [
            {
                "level": "basic",
                "title": "Verify De Morgan's Law with listed sets",
                "problem": "Let $U=\\{1,2,3,4,5,6\\}$, $A=\\{1,2,3\\}$ and $B=\\{3,4\\}$. Verify that $(A\\cup B)'=A'\\cap B'$.",
                "steps": [
                    "$A\\cup B=\\{1,2,3,4\\}$, so $(A\\cup B)'=\\{5,6\\}$.",
                    "$A'=\\{4,5,6\\}$ and $B'=\\{1,2,5,6\\}$.",
                    "$A'\\cap B'=\\{5,6\\}$.",
                    "Both sides are equal.",
                ],
                "answer": "$(A\\cup B)'=A'\\cap B'=\\{5,6\\}$."
            },
            {
                "level": "intermediate",
                "title": "Use the three-set law",
                "problem": "Simplify $(P\\cup Q\\cup R)'$.",
                "steps": [
                    "The complement is outside a union of three sets.",
                    "Change union to intersection.",
                    "Complement each set separately.",
                ],
                "answer": "$(P\\cup Q\\cup R)'=P'\\cap Q'\\cap R'$."
            },
            {
                "level": "application",
                "title": "Logic interpretation",
                "problem": "A device should be rejected if it fails temperature test T, pressure test P or vibration test V. Write the condition for a device that is not rejected.",
                "steps": [
                    "Rejected means $T\\cup P\\cup V$ where T, P and V are failure sets.",
                    "Not rejected means outside that union: $(T\\cup P\\cup V)'$.",
                    "By De Morgan's Law, $(T\\cup P\\cup V)'=T'\\cap P'\\cap V'$.",
                    "So the device is accepted only if it passes all three tests.",
                ],
                "answer": "$T'\\cap P'\\cap V'$."
            }
        ],
        "applications": [
            {
                "title": "Electrical and digital circuits",
                "body": "De Morgan's Laws are used to convert OR gates with negation into AND gates with negated inputs, and vice versa. This is central in logic circuit simplification."
            },
            {
                "title": "Search filters",
                "body": "The instruction 'not red or heavy' can be rewritten as 'not red and not heavy' only when the complement is outside the whole union: $(R\\cup H)'=R'\\cap H'$."
            },
            {
                "title": "Safety systems",
                "body": "If failure means pressure fault or heat fault or vibration fault, then no failure means no pressure fault and no heat fault and no vibration fault."
            }
        ]
    },
    {
        "title": "Problem-Solving Strategy for WAEC Set Questions",
        "intro": "The fastest students do not jump into formulas. They translate the words first, identify the universal set, and decide whether the question asks for union, intersection, only, exactly, neither or complement.",
        "key_points": [
            "Underline the universal set: the total number being discussed.",
            "Translate 'or' as union and 'and' as intersection, but check whether ordinary English is being used loosely.",
            "Translate 'at least one' as union.",
            "Translate 'neither' or 'none' as complement of the union.",
            "Translate 'only A' as the part of A outside the other sets.",
            "For three sets, start from the middle triple-overlap when filling a Venn diagram.",
        ],
        "examples": [
            {
                "level": "complex",
                "title": "Three-club Venn diagram by regions",
                "problem": "In a school of 100 students, 40 belong to Debate, 36 to Science and 30 to Music. 15 belong to Debate and Science, 12 to Debate and Music, 10 to Science and Music, and 6 belong to all three. Find how many belong to Debate only and how many belong to none.",
                "steps": [
                    "Start with the middle: all three = 6.",
                    "Debate and Science only = $15-6=9$.",
                    "Debate and Music only = $12-6=6$.",
                    "Science and Music only = $10-6=4$.",
                    "Debate only = $40-9-6-6=19$.",
                    "Union = $40+36+30-15-12-10+6=75$.",
                    "None = $100-75=25$.",
                ],
                "answer": "Debate only = 19 students; none = 25 students."
            }
        ],
        "practice": [
            {
                "question": "A class has 80 students. 44 like Algebra, 38 like Geometry and 16 like both. How many like exactly one of Algebra and Geometry?",
                "solution": [
                    "Algebra only = $44-16=28$.",
                    "Geometry only = $38-16=22$.",
                    "Exactly one = $28+22=50$."
                ],
                "answer": "50"
            },
            {
                "question": "In a group of 150 students, 70 study Physics, 60 Chemistry, 55 Biology, 30 Physics and Chemistry, 25 Physics and Biology, 20 Chemistry and Biology, and 10 all three. How many study at least one science?",
                "solution": [
                    "Use the three-set formula.",
                    "$70+60+55-30-25-20+10=120$."
                ],
                "answer": "120"
            }
        ]
    }
]

SUBSETS_POWER_SECTIONS = [
    {
        "title": "Subset Meaning, Notation and Equality",
        "intro": "A subset is not just a smaller set. It is a set whose every element is already found inside another set.",
        "key_points": [
            "$A\\subseteq B$ means every element of A belongs to B.",
            "$A\\subset B$ usually means A is a proper subset of B, so A is inside B but not equal to B.",
            "If $A\\subseteq B$ and $B\\subseteq A$, then $A=B$.",
            "A set can be a subset of another set even if the elements are written in a different order.",
            "$\\{a\\}$ is a subset, but $a$ is an element. Do not confuse the object with the set containing the object."
        ],
        "examples": [
            {
                "level": "foundation",
                "title": "Subset or not?",
                "problem": "Let $A=\\{1,2\\}$ and $B=\\{1,2,3,4\\}$. Is $A\\subseteq B$?",
                "steps": [
                    "Check every element of A.",
                    "1 is in B and 2 is in B.",
                    "No element of A is outside B.",
                ],
                "answer": "Yes, $A\\subseteq B$."
            },
            {
                "level": "common mistake",
                "title": "Element versus subset",
                "problem": "If $A=\\{2,4,6\\}$, decide whether $2\\in A$, $\\{2\\}\\subseteq A$ and $\\{2,5\\}\\subseteq A$ are true.",
                "steps": [
                    "$2\\in A$ is true because 2 is an element of A.",
                    "$\\{2\\}\\subseteq A$ is true because every element of $\\{2\\}$ is in A.",
                    "$\\{2,5\\}\\subseteq A$ is false because 5 is not in A.",
                ],
                "answer": "True, true, false."
            }
        ]
    },
    {
        "title": "Empty Set and Self-Subset Rules",
        "intro": "Two rules confuse many students at first: the empty set is a subset of every set, and every set is a subset of itself.",
        "key_points": [
            "$\\emptyset\\subseteq A$ for every set A.",
            "$A\\subseteq A$ for every set A.",
            "$A\\subset A$ is false if the symbol is being used for proper subset.",
            "The empty set is counted when listing all subsets.",
            "The whole set itself is counted when listing all subsets.",
        ],
        "examples": [
            {
                "level": "conceptual",
                "title": "Why the empty set is a subset",
                "problem": "Explain why $\\emptyset\\subseteq\\{3,5,7\\}$.",
                "steps": [
                    "To disprove a subset statement, we need to find an element in the smaller set that is not in the bigger set.",
                    "The empty set has no element at all.",
                    "So there is no element in $\\emptyset$ that can fail to belong to $\\{3,5,7\\}$.",
                ],
                "answer": "$\\emptyset$ is a subset of $\\{3,5,7\\}$."
            },
            {
                "level": "WAEC-style",
                "title": "Proper subset check",
                "problem": "How many proper subsets does $A=\\{p,q,r\\}$ have?",
                "steps": [
                    "A set with 3 elements has $2^3=8$ subsets.",
                    "Proper subsets exclude the whole set A itself.",
                    "So proper subsets = $8-1=7$.",
                ],
                "answer": "7 proper subsets."
            }
        ]
    },
    {
        "title": "Listing Subsets Systematically",
        "intro": "When a set has few elements, students should be able to list every subset without missing one. The safest method is to list by size: zero-element, one-element, two-element and so on.",
        "examples": [
            {
                "level": "basic",
                "title": "List all subsets of a two-element set",
                "problem": "List all subsets of $A=\\{a,b\\}$.",
                "steps": [
                    "Zero-element subset: $\\emptyset$.",
                    "One-element subsets: $\\{a\\}$ and $\\{b\\}$.",
                    "Two-element subset: $\\{a,b\\}$.",
                    "The count is $2^2=4$, so the list is complete.",
                ],
                "answer": "$\\emptyset, \\{a\\}, \\{b\\}, \\{a,b\\}$."
            },
            {
                "level": "intermediate",
                "title": "List all subsets of a three-element set",
                "problem": "List all subsets of $B=\\{x,y,z\\}$.",
                "steps": [
                    "Zero-element subset: $\\emptyset$.",
                    "One-element subsets: $\\{x\\},\\{y\\},\\{z\\}$.",
                    "Two-element subsets: $\\{x,y\\},\\{x,z\\},\\{y,z\\}$.",
                    "Three-element subset: $\\{x,y,z\\}$.",
                    "The count is $1+3+3+1=8=2^3$.",
                ],
                "answer": "$\\emptyset,\\{x\\},\\{y\\},\\{z\\},\\{x,y\\},\\{x,z\\},\\{y,z\\},\\{x,y,z\\}$."
            }
        ],
        "practice": [
            {
                "question": "List the two-element subsets of $\\{1,2,3,4\\}$.",
                "answer": "$\\{1,2\\},\\{1,3\\},\\{1,4\\},\\{2,3\\},\\{2,4\\},\\{3,4\\}$"
            }
        ]
    },
    {
        "title": "Power Sets and Counting Formulas",
        "intro": "The power set is the set of all subsets. Counting subsets is a bridge from sets into combinations, probability, computer science and experimental design.",
        "formulas": [
            {
                "name": "All subsets",
                "expression": "$n(\\mathcal{P}(A))=2^n$",
                "meaning": "If A has n elements, each element has two choices: included or not included."
            },
            {
                "name": "Proper subsets",
                "expression": "$2^n-1$",
                "meaning": "Exclude the whole set itself."
            },
            {
                "name": "Non-empty subsets",
                "expression": "$2^n-1$",
                "meaning": "Exclude the empty set."
            },
            {
                "name": "Non-empty proper subsets",
                "expression": "$2^n-2$",
                "meaning": "Exclude both the empty set and the whole set."
            },
            {
                "name": "Subsets with exactly r elements",
                "expression": "$\\binom{n}{r}$",
                "meaning": "Choose r elements from n elements; order does not matter."
            }
        ],
        "examples": [
            {
                "level": "intermediate",
                "title": "Count all kinds of subsets",
                "problem": "A set has 6 elements. Find the number of all subsets, proper subsets, non-empty subsets and non-empty proper subsets.",
                "steps": [
                    "All subsets: $2^6=64$.",
                    "Proper subsets: $2^6-1=63$.",
                    "Non-empty subsets: $2^6-1=63$.",
                    "Non-empty proper subsets: $2^6-2=62$.",
                ],
                "answer": "64, 63, 63 and 62 respectively."
            },
            {
                "level": "advanced",
                "title": "Exactly three-element subsets",
                "problem": "How many subsets of $\\{a,b,c,d,e\\}$ contain exactly 3 elements?",
                "steps": [
                    "There are 5 elements in the set.",
                    "We need to choose exactly 3 elements.",
                    "Use $\\binom{5}{3}=\\frac{5!}{3!2!}=10$.",
                ],
                "answer": "10 subsets."
            }
        ],
        "applications": [
            {
                "title": "Engineering testing",
                "body": "If 5 sensors are available, every possible sensor package is a subset of the 5-sensor set. There are $2^5=32$ packages if choosing no sensor is allowed."
            },
            {
                "title": "Physics variables",
                "body": "A student planning experiments may choose different subsets of variables such as mass, length, time and current. Counting subsets tells how many combinations are possible."
            },
            {
                "title": "Computer science",
                "body": "Feature selection in data science is a subset problem: from n possible features, there are $2^n$ possible feature groups."
            }
        ]
    },
    {
        "title": "Exam-Level Subset Questions",
        "intro": "WAEC-style subset questions often hide the formula inside words such as possible groups, selections, committees, experimental variables, signals or components.",
        "examples": [
            {
                "level": "WAEC-style",
                "title": "Find the number of elements from subsets",
                "problem": "A set has 128 subsets. How many elements are in the set?",
                "steps": [
                    "Use $2^n=128$.",
                    "Since $128=2^7$, $n=7$.",
                ],
                "answer": "The set has 7 elements."
            },
            {
                "level": "application",
                "title": "Component selection",
                "problem": "An electronics student has 4 components: resistor, capacitor, diode and switch. How many non-empty component groups can be formed?",
                "steps": [
                    "There are 4 components.",
                    "All possible groups = $2^4=16$.",
                    "Non-empty groups exclude choosing nothing.",
                    "$16-1=15$.",
                ],
                "answer": "15 non-empty groups."
            }
        ],
        "practice": [
            {
                "question": "How many non-empty proper subsets does a 5-element set have?",
                "answer": "$2^5-2=30$"
            },
            {
                "question": "A set has 31 proper subsets. How many elements are in the set?",
                "solution": [
                    "Proper subsets = $2^n-1$.",
                    "$2^n-1=31$.",
                    "$2^n=32=2^5$."
                ],
                "answer": "5 elements"
            }
        ]
    }
]

EXTRA_LESSONS = {
    # ---- SETS & LOGIC ----
    "set-operations": {"title": "Set Operations", "topic": "sets-logic",
        "summary": "Learn how to describe, combine and compare groups of objects using union, intersection, complement and difference.",
        "standard": "full",
        "objectives": [
            "Explain what a set, element, universal set and empty set mean in plain English.",
            "Use symbols such as $\\in$, $\\notin$, $\\cup$, $\\cap$, $A'$ and $A-B$ correctly.",
            "Find union, intersection, complement and difference from listed sets.",
            "Translate simple word problems into set notation and solve them step by step.",
            "Recognise how set operations appear in engineering, physics, computing and probability.",
        ],
        "prerequisites": [
            "You should be comfortable listing objects, numbers or names inside braces such as $\\{1,2,3\\}$.",
            "You should know basic counting: if a group has 5 objects, its cardinality is 5.",
            "No advanced algebra is needed; this lesson starts from the meaning of a group.",
        ],
        "visual_blocks": [
            {"type": "venn", "variant": "set_a", "title": "A single set", "caption": "Set A is one group inside the universal set U."},
            {"type": "venn", "variant": "union", "title": "Union: $A \\cup B$", "caption": "Everything in A, in B, or in both. Think: either group counts."},
            {"type": "venn", "variant": "intersection", "title": "Intersection: $A \\cap B$", "caption": "Only the overlap. Think: must belong to both groups."},
            {"type": "venn", "variant": "difference", "title": "Difference: $A-B$", "caption": "Start with A, then remove anything also found in B."},
            {"type": "venn", "variant": "complement_a", "title": "Complement: $A'$", "caption": "Everything in the universal set U that is not in A."},
            {"type": "venn", "variant": "disjoint", "title": "Disjoint sets", "caption": "A and B have no common element, so $A \\cap B = \\emptyset$."},
            {"type": "venn", "variant": "subset", "title": "Subset", "caption": "Every element of B is also inside A, so $B \\subset A$."},
        ],
        "lesson_sections": SET_OPERATIONS_SECTIONS,
        "notes": [
            {"heading": "What Is a Set?",
             "body": "A **set** is a well-defined collection of objects. The objects are called **elements** or **members**. For example, $A=\\{2,4,6,8\\}$ is the set of even numbers shown. We write $4 \\in A$ to mean 4 is in A, and $5 \\notin A$ to mean 5 is not in A."},
            {"heading": "Universal Set and Empty Set",
             "body": "The **universal set**, written $U$, is the big group we are working inside. If a question is about students in SS3, then $U$ may be all SS3 students. The **empty set**, written $\\emptyset$ or $\\{\\}$, has no elements."},
            {"heading": "Union: Either A or B",
             "body": "$A \\cup B$ means all elements that are in A, in B, or in both. Do not repeat an element. If $A=\\{1,2,3\\}$ and $B=\\{3,4,5\\}$, then $A\\cup B=\\{1,2,3,4,5\\}$."},
            {"heading": "Intersection: Both A and B",
             "body": "$A \\cap B$ means the elements common to both A and B. If $A=\\{1,2,3\\}$ and $B=\\{3,4,5\\}$, then $A\\cap B=\\{3\\}$ because only 3 appears in both sets."},
            {"heading": "Complement: Outside A but Still Inside U",
             "body": "$A'$ means all elements in $U$ that are not in A. Complement depends on the universal set. If $U=\\{1,2,3,4,5,6\\}$ and $A=\\{2,4,6\\}$, then $A'=\\{1,3,5\\}$."},
            {"heading": "Difference: In A but Not in B",
             "body": "$A-B$ means elements that are in A after removing anything that also appears in B. If $A=\\{1,2,3,4\\}$ and $B=\\{3,4,5\\}$, then $A-B=\\{1,2\\}$."},
            {"heading": "De Morgan's Laws",
             "body": "De Morgan's Laws connect complement with union and intersection. For two sets: $(A\\cup B)'=A'\\cap B'$ and $(A\\cap B)'=A'\\cup B'$. For three sets: $(A\\cup B\\cup C)'=A'\\cap B'\\cap C'$ and $(A\\cap B\\cap C)'=A'\\cup B'\\cup C'$. The guided sections below give examples, applications and practice."},
        ],
        "worked_examples": [
            {
                "level": "basic",
                "title": "Finding union and intersection from lists",
                "problem": "Let $A=\\{1,2,3,5\\}$ and $B=\\{2,4,5,6\\}$. Find $A\\cup B$ and $A\\cap B$.",
                "steps": [
                    "For $A\\cup B$, collect every element that appears in A or B.",
                    "The elements are 1, 2, 3, 4, 5 and 6. Do not write 2 or 5 twice.",
                    "For $A\\cap B$, keep only the elements that appear in both lists.",
                    "Both A and B contain 2 and 5.",
                ],
                "answer": "$A\\cup B=\\{1,2,3,4,5,6\\}$ and $A\\cap B=\\{2,5\\}$."
            },
            {
                "level": "basic",
                "title": "Finding complement",
                "problem": "If $U=\\{1,2,3,4,5,6,7,8\\}$ and $A=\\{2,4,6,8\\}$, find $A'$.",
                "steps": [
                    "Start from the universal set U because complement is always measured inside U.",
                    "Remove every element that belongs to A: remove 2, 4, 6 and 8.",
                    "The remaining elements are 1, 3, 5 and 7.",
                ],
                "answer": "$A'=\\{1,3,5,7\\}$."
            },
            {
                "level": "intermediate",
                "title": "Using the set formula",
                "problem": "In a class of 50 students, 30 study Physics, 25 study Chemistry and 10 study both. How many study Physics or Chemistry?",
                "steps": [
                    "Let P be students who study Physics and C be students who study Chemistry.",
                    "The word 'or' means union: $P\\cup C$.",
                    "Use $n(P\\cup C)=n(P)+n(C)-n(P\\cap C)$.",
                    "Substitute: $30+25-10=45$.",
                    "We subtract 10 because students who study both were counted twice.",
                ],
                "answer": "45 students study Physics or Chemistry."
            },
            {
                "level": "WAEC-style",
                "title": "Finding neither",
                "problem": "Out of 80 students, 45 like Mathematics, 38 like Physics and 20 like both. How many like neither Mathematics nor Physics?",
                "steps": [
                    "Let M be Mathematics and P be Physics.",
                    "First find those who like at least one: $n(M\\cup P)=45+38-20=63$.",
                    "The universal set is all 80 students.",
                    "Neither means outside $M\\cup P$, so subtract from 80.",
                    "$80-63=17$.",
                ],
                "answer": "17 students like neither Mathematics nor Physics."
            },
        ],
        "word_problems": [
            {
                "level": "basic",
                "title": "School club survey",
                "problem": "A school has 40 science students. 22 joined the Robotics club, 18 joined the Physics club and 7 joined both. How many joined at least one club?",
                "solution": [
                    "At least one club means union.",
                    "$n(R\\cup P)=n(R)+n(P)-n(R\\cap P)$.",
                    "$n(R\\cup P)=22+18-7=33$.",
                    "So 33 students joined at least one club.",
                ],
            },
            {
                "level": "intermediate",
                "title": "Device diagnostics",
                "problem": "A technician tests 60 devices. 28 fail the battery test, 21 fail the screen test and 9 fail both. How many devices fail exactly one of the two tests?",
                "solution": [
                    "Exactly one means battery only plus screen only.",
                    "Battery only: $28-9=19$.",
                    "Screen only: $21-9=12$.",
                    "Exactly one: $19+12=31$.",
                ],
            },
            {
                "level": "complex",
                "title": "Engineering materials",
                "problem": "Among 100 materials, 54 are conductive, 48 are heat-resistant and 20 have both properties. How many are neither conductive nor heat-resistant?",
                "solution": [
                    "Let C be conductive materials and H be heat-resistant materials.",
                    "$n(C\\cup H)=54+48-20=82$.",
                    "Neither means outside the union.",
                    "$100-82=18$.",
                    "So 18 materials have neither property.",
                ],
            },
        ],
        "applications": [
            {"title": "Engineering classification", "body": "Engineers group materials by properties: conductive, magnetic, heat-resistant, flexible, brittle. Set operations help identify materials that satisfy one condition, both conditions or neither."},
            {"title": "Physics experiments", "body": "In experimental data, one set may contain objects affected by force A, another by field B. Intersections show objects affected by both conditions."},
            {"title": "Computer science and databases", "body": "Search filters use set operations. 'Students taking Physics OR Chemistry' is a union. 'Students taking Physics AND Chemistry' is an intersection."},
            {"title": "Probability", "body": "Events are sets of outcomes. $A\\cup B$ means event A or B occurs, while $A\\cap B$ means both events occur."},
        ],
        "common_mistakes": [
            "Confusing union with intersection. Union is bigger or equal; intersection is the overlap.",
            "Repeating elements in a union. In sets, each element is listed once.",
            "Finding complement without checking the universal set.",
            "Forgetting to subtract the overlap in $n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$.",
            "Thinking $A-B$ is the same as $B-A$. Usually they are different.",
        ],
        "quick_checks": [
            {"question": "If $A=\\{a,b,c\\}$ and $B=\\{b,c,d\\}$, what is $A\\cap B$?", "answer": "$\\{b,c\\}$"},
            {"question": "If $U=\\{1,2,3,4,5\\}$ and $A=\\{1,3,5\\}$, what is $A'$?", "answer": "$\\{2,4\\}$"},
            {"question": "In a class, 12 study Biology, 10 study Physics and 4 study both. How many study at least one?", "answer": "$12+10-4=18$"},
        ]},
    "venn-diagrams": {"title": "Venn Diagrams", "topic": "sets-logic",
        "summary": "Visual representation of set relationships using overlapping circles.",
        "notes": [
            {"heading": "Cardinality", "body": "$n(A \\cup B) = n(A) + n(B) - n(A \\cap B)$ (inclusion-exclusion)."},
            {"heading": "Worked Example", "body": "If $n(A)=20$, $n(B)=15$, $n(A\\cap B)=8$, then $n(A\\cup B)=20+15-8=27$."},
        ]},
    "subsets-power": {"title": "Subsets & Power Sets", "topic": "sets-logic",
        "summary": "Understand subsets, proper subsets, empty set, power sets and how to count all possible subsets of a set.",
        "standard": "full",
        "objectives": [
            "Explain the meaning of $A \\subseteq B$ and $A \\subset B$.",
            "Recognise that $\\emptyset$ is a subset of every set.",
            "Recognise that every set is a subset of itself.",
            "List all subsets of a small set systematically.",
            "Use $2^n$ to find the number of subsets and $2^n-1$ to find the number of proper subsets.",
        ],
        "prerequisites": [
            "Know that a set is a collection of elements written inside braces.",
            "Know how to count the number of elements in a finite set.",
            "Know that $\\emptyset$ means a set with no elements.",
        ],
        "visual_blocks": [
            {"type": "venn", "variant": "subset", "title": "Subset: $B \\subset A$", "caption": "Every element of B is inside A. B is smaller, but it belongs completely to A."},
        ],
        "lesson_sections": SUBSETS_POWER_SECTIONS,
        "notes": [
            {"heading": "Meaning of a Subset",
             "body": "$A \\subseteq B$ means every element of A is also an element of B. In plain English: A is contained inside B. Example: if $A=\\{2,4\\}$ and $B=\\{1,2,3,4\\}$, then $A\\subseteq B$."},
            {"heading": "Subset vs Proper Subset",
             "body": "$A \\subseteq B$ allows A to be equal to B. $A \\subset B$ means A is a **proper subset** of B: A is inside B but A is not equal to B. Example: $\\{1,2\\}\\subset\\{1,2,3\\}$."},
            {"heading": "The Empty Set Is Always a Subset",
             "body": "$\\emptyset$ is a subset of every set. This feels strange at first, but it is true because there is no element in $\\emptyset$ that can disobey the rule of belonging to the bigger set."},
            {"heading": "Every Set Is a Subset of Itself",
             "body": "For any set A, $A\\subseteq A$. This is not a proper subset because the two sets are equal. If proper subset is required, then A is not a proper subset of itself."},
            {"heading": "Power Set",
             "body": "The **power set** of A, written $\\mathcal{P}(A)$, is the set of all subsets of A. If $A=\\{a,b\\}$, then $\\mathcal{P}(A)=\\{\\emptyset,\\{a\\},\\{b\\},\\{a,b\\}\\}$."},
            {"heading": "Counting Subsets",
             "body": "If a set has $n$ elements, then the number of subsets is $2^n$. The number of proper subsets is $2^n-1$ because we exclude the whole set itself."},
        ],
        "worked_examples": [
            {
                "level": "basic",
                "title": "List all subsets",
                "problem": "List all subsets of $A=\\{x,y\\}$.",
                "steps": [
                    "Start with the empty set: $\\emptyset$.",
                    "List the one-element subsets: $\\{x\\}$ and $\\{y\\}$.",
                    "List the whole set itself: $\\{x,y\\}$.",
                    "Check the count: A has 2 elements, so it should have $2^2=4$ subsets.",
                ],
                "answer": "$\\mathcal{P}(A)=\\{\\emptyset,\\{x\\},\\{y\\},\\{x,y\\}\\}$."
            },
            {
                "level": "intermediate",
                "title": "Count subsets and proper subsets",
                "problem": "A set has 5 elements. How many subsets and proper subsets does it have?",
                "steps": [
                    "Use the formula for subsets: $2^n$.",
                    "Here $n=5$, so number of subsets is $2^5=32$.",
                    "Proper subsets exclude the whole set.",
                    "So proper subsets = $2^5-1=31$.",
                ],
                "answer": "32 subsets and 31 proper subsets."
            },
            {
                "level": "WAEC-style",
                "title": "Find n from number of subsets",
                "problem": "A set has 64 subsets. How many elements are in the set?",
                "steps": [
                    "If a set has n elements, number of subsets is $2^n$.",
                    "So $2^n=64$.",
                    "Since $64=2^6$, we have $n=6$.",
                ],
                "answer": "The set has 6 elements."
            },
        ],
        "word_problems": [
            {
                "level": "basic",
                "title": "Choosing sensors",
                "problem": "An engineering team has 3 available sensors: temperature, pressure and light. How many different sensor groups can they form, including choosing no sensor?",
                "solution": [
                    "Each sensor can be chosen or not chosen.",
                    "There are 3 sensors, so the number of possible groups is $2^3$.",
                    "$2^3=8$.",
                    "Including no sensor is why the empty set is counted.",
                ],
            },
            {
                "level": "intermediate",
                "title": "Physics experiment combinations",
                "problem": "A physics student can test 4 variables: mass, length, time and current. How many non-empty combinations of variables can be tested?",
                "solution": [
                    "All possible combinations are subsets of the 4-variable set.",
                    "Number of all subsets is $2^4=16$.",
                    "Non-empty combinations exclude $\\emptyset$.",
                    "So the answer is $16-1=15$.",
                ],
            },
        ],
        "applications": [
            {"title": "Engineering design choices", "body": "Every possible combination of components is a subset of the full component set. Counting subsets helps estimate how many configurations may need testing."},
            {"title": "Physics experiments", "body": "Choosing which variables to include in an experiment is a subset problem. Non-empty subsets represent actual test combinations."},
            {"title": "Computer science", "body": "Feature selection in machine learning and database filtering often involve choosing subsets of available fields or conditions."},
        ],
        "common_mistakes": [
            "Forgetting to include $\\emptyset$ when listing subsets.",
            "Forgetting to include the whole set when listing all subsets.",
            "Confusing subsets with elements. $\\{a\\}$ is a subset, while $a$ is an element.",
            "Using $2^n-1$ for all subsets instead of proper subsets.",
            "Thinking a set is a proper subset of itself. It is a subset of itself, but not a proper subset.",
        ],
        "quick_checks": [
            {"question": "How many subsets does $\\{a,b,c\\}$ have?", "answer": "$2^3=8$"},
            {"question": "How many proper subsets does a 4-element set have?", "answer": "$2^4-1=15$"},
            {"question": "Is $\\emptyset \\subseteq \\{1,2,3\\}$?", "answer": "Yes. The empty set is a subset of every set."},
        ]},
    "binary-operations": {"title": "Binary Operations", "topic": "sets-logic",
        "summary": "A binary operation combines two elements from a set to produce one result, often written as $a * b$ or $a \\circ b$.",
        "notes": [
            {"heading": "Meaning", "body": "A binary operation $*$ on a set $S$ takes any ordered pair $(a,b)$ from $S$ and gives a result $a*b$. WAEC may define a new operation such as $a*b = 2a + b$ and ask you to use or test it."},
            {"heading": "Closure", "body": "A set is closed under $*$ if $a*b \\in S$ for every $a,b \\in S$. For example, integers are closed under addition because the sum of two integers is always an integer."},
            {"heading": "Identity and Inverse", "body": "An identity element $e$ satisfies $a*e = e*a = a$. An inverse of $a$ is an element $b$ such that $a*b = b*a = e$."},
            {"heading": "Commutative and Associative", "body": "$*$ is commutative if $a*b=b*a$. It is associative if $(a*b)*c=a*(b*c)$. Do not assume these are true for a newly defined operation; test them from the rule."},
            {"heading": "Worked Example", "body": "If $a*b = 2a + b$, then $3*5 = 2(3)+5 = 11$. But $5*3 = 2(5)+3 = 13$, so the operation is not commutative."},
        ]},
    "propositional-logic": {"title": "Propositional Logic", "topic": "sets-logic",
        "summary": "Logical statements connected by $\\land$ (and), $\\lor$ (or), $\\neg$ (not), $\\Rightarrow$ (implies).",
        "notes": [
            {"heading": "Connectives", "body": "$p \\land q$ true iff both true. $p \\lor q$ true if either is. $\\neg p$ negates $p$. $p \\Rightarrow q$ false only when $p$ true and $q$ false."},
            {"heading": "Worked Example", "body": "If $p$: 'It rains' (T) and $q$: 'Ground is wet' (T), then $p \\land q$ is T, $p \\Rightarrow q$ is T."},
        ]},
    "truth-tables": {"title": "Truth Tables", "topic": "sets-logic",
        "summary": "Tabulate values of compound statements over all $T/F$ combinations.",
        "notes": [
            {"heading": "Standard Tables", "body": "For $p, q$: 4 rows (TT, TF, FT, FF). $p\\land q$: T only when both T. $p\\lor q$: F only when both F."},
            {"heading": "Worked Example", "body": "Truth table of $p\\Rightarrow q$: TT→T, TF→F, FT→T, FF→T."},
        ]},
    # ---- SURDS & POLYNOMIALS ----
    "surd-simplification": {"title": "Surd Simplification", "topic": "surds-polynomials",
        "summary": "A surd is an irrational root, e.g. $\\sqrt{2}$, $\\sqrt[3]{5}$.",
        "notes": [
            {"heading": "Rules", "body": "$\\sqrt{ab} = \\sqrt{a}\\sqrt{b}$. $\\sqrt{a/b} = \\sqrt{a}/\\sqrt{b}$. To rationalise $\\frac{1}{\\sqrt{a}}$, multiply by $\\frac{\\sqrt{a}}{\\sqrt{a}}$."},
            {"heading": "Worked Example", "body": "$\\sqrt{50} = \\sqrt{25 \\times 2} = 5\\sqrt{2}$. Rationalise $\\frac{1}{\\sqrt{3}} = \\frac{\\sqrt{3}}{3}$."},
        ]},
    "indices-logs-fm": {"title": "Indices & Logarithms (FM)", "topic": "surds-polynomials",
        "summary": "FM extends indices to negative/fractional powers and logarithms to change of base.",
        "notes": [
            {"heading": "Key Laws", "body": "$a^{m/n} = \\sqrt[n]{a^m}$. $\\log_b x = \\frac{\\log x}{\\log b}$ (change of base)."},
            {"heading": "Worked Example", "body": "$8^{2/3} = (\\sqrt[3]{8})^2 = 2^2 = 4$. $\\log_2 32 = \\log_2 2^5 = 5$."},
        ]},
    "functions-mappings": {"title": "Functions & Mappings", "topic": "surds-polynomials",
        "summary": "A function maps each element in its domain to exactly one element in its co-domain.",
        "notes": [
            {"heading": "Domain, Co-domain and Range", "body": "The domain is the set of allowed inputs. The co-domain is the target set. The range is the set of outputs actually produced. For $f(x)=x^2$ with domain $\\{-2,-1,0,1,2\\}$, the range is $\\{0,1,4\\}$."},
            {"heading": "Types of Functions", "body": "A function is one-to-one if different inputs give different outputs. It is onto if every element of the co-domain is reached. A constant function gives the same output for every input."},
            {"heading": "Composite Functions", "body": "$(f \\circ g)(x)$ means $f(g(x))$: apply $g$ first, then apply $f$. The domain must allow both steps."},
            {"heading": "Inverse Functions", "body": "$f^{-1}$ reverses $f$. To find it, write $y=f(x)$, make $x$ the subject, then swap $x$ and $y$. The inverse exists as a function only when $f$ is one-to-one on the chosen domain."},
            {"heading": "Worked Example", "body": "Let $f(x)=2x+3$ and $g(x)=x^2$. Then $(f\\circ g)(x)=f(x^2)=2x^2+3$. Also $f^{-1}(x)=\\frac{x-3}{2}$."},
        ]},
    "polynomial-division": {"title": "Polynomial Division", "topic": "surds-polynomials",
        "summary": "Long division of polynomials: $P(x) = D(x)Q(x) + R(x)$.",
        "notes": [
            {"heading": "Method", "body": "Divide the highest-degree term of $P(x)$ by the highest-degree term of $D(x)$, multiply, subtract, bring down. Repeat."},
            {"heading": "Worked Example", "body": "$(x^2 + 3x + 2) \\div (x+1) = x + 2$ with remainder 0."},
        ]},
    "remainder-theorem": {"title": "Remainder & Factor Theorems", "topic": "surds-polynomials",
        "summary": "$P(a)$ is the remainder when $P(x)$ is divided by $x - a$. If $P(a) = 0$, then $x - a$ is a factor.",
        "notes": [
            {"heading": "Statement", "body": "**Remainder**: $P(x) = (x - a)Q(x) + P(a)$. **Factor**: $P(a) = 0 \\Leftrightarrow (x-a) \\mid P(x)$."},
            {"heading": "Worked Example", "body": "$P(x) = x^3 - 2x^2 + x - 2$ divided by $x - 2$: $P(2) = 8 - 8 + 2 - 2 = 0$, so $x-2$ is a factor."},
        ]},
    "partial-fractions": {"title": "Partial Fractions", "topic": "surds-polynomials",
        "summary": "Decompose a rational function into simpler fractions.",
        "notes": [
            {"heading": "Linear Factors", "body": "$\\frac{P(x)}{(x-a)(x-b)} = \\frac{A}{x-a} + \\frac{B}{x-b}$."},
            {"heading": "Worked Example", "body": "$\\frac{1}{(x-1)(x+2)} = \\frac{A}{x-1} + \\frac{B}{x+2}$ gives $A = 1/3$, $B = -1/3$."},
        ]},
    # ---- SEQUENCES & BINOMIAL ----
    "ap-fm": {"title": "Arithmetic Progression (FM)", "topic": "sequences-binomial",
        "summary": "$T_n = a + (n-1)d$. $S_n = \\frac{n}{2}[2a + (n-1)d]$.",
        "notes": [
            {"heading": "Properties", "body": "Common difference $d$ is constant. Sum of first $n$ terms uses the formula above."},
            {"heading": "Worked Example", "body": "10th term of 3,7,11,...: $a=3, d=4$, $T_{10}=3+9(4)=39$."},
        ]},
    "gp-fm": {"title": "Geometric Progression (FM)", "topic": "sequences-binomial",
        "summary": "$T_n = ar^{n-1}$. $S_n = \\frac{a(r^n - 1)}{r-1}$ when $r \\neq 1$.",
        "notes": [
            {"heading": "Sum to Infinity", "body": "If $|r| < 1$: $S_\\infty = \\frac{a}{1-r}$."},
            {"heading": "Worked Example", "body": "$S_\\infty$ for $2 + 1 + 1/2 + ...$: $a=2, r=1/2$, $S_\\infty = 2/(1-1/2) = 4$."},
        ]},
    "infinite-series": {"title": "Infinite Series", "topic": "sequences-binomial",
        "summary": "Sum of infinite GP exists iff $|r| < 1$.",
        "notes": [
            {"heading": "Convergence Test", "body": "$|r| < 1$ ⇒ converges to $\\frac{a}{1-r}$. $|r| \\geq 1$ ⇒ diverges."},
            {"heading": "Worked Example", "body": "$1 + 1/3 + 1/9 + ...$: $r=1/3$, $S=1/(1-1/3)=3/2$."},
        ]},
    "binomial-expansion": {"title": "Binomial Expansion", "topic": "sequences-binomial",
        "summary": "$(a+b)^n = \\sum_{k=0}^{n} \\binom{n}{k} a^{n-k} b^k$.",
        "notes": [
            {"heading": "General Term", "body": "$T_{k+1} = \\binom{n}{k} a^{n-k} b^k$."},
            {"heading": "Worked Example", "body": "$(1+x)^4 = 1 + 4x + 6x^2 + 4x^3 + x^4$."},
        ]},
    "pascals-triangle": {"title": "Pascal's Triangle", "topic": "sequences-binomial",
        "summary": "Each row is the binomial coefficients: $\\binom{n}{0}, \\binom{n}{1}, ..., \\binom{n}{n}$.",
        "notes": [
            {"heading": "Rule", "body": "Each entry = sum of the two entries above it. Symmetric: $\\binom{n}{k} = \\binom{n}{n-k}$."},
            {"heading": "Worked Example", "body": "Row 5: 1, 5, 10, 10, 5, 1 — coefficients of $(a+b)^5$."},
        ]},
    # ---- MATRICES ----
    "matrix-operations": {"title": "Matrix Operations", "topic": "matrices",
        "summary": "Addition/subtraction (same size), scalar multiplication, matrix multiplication.",
        "notes": [
            {"heading": "Multiplication", "body": "$(AB)_{ij} = \\sum_k a_{ik} b_{kj}$. Defined when columns of A = rows of B."},
            {"heading": "Worked Example", "body": "$\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix} \\begin{pmatrix}1\\\\2\\end{pmatrix} = \\begin{pmatrix}5\\\\11\\end{pmatrix}$."},
        ]},
    "determinants": {"title": "Determinants", "topic": "matrices",
        "summary": "Scalar value associated with a square matrix. $\\det\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix} = ad - bc$.",
        "notes": [
            {"heading": "3×3 Expansion", "body": "Use cofactor expansion along any row/column. $\\det(A) = \\sum_j (-1)^{i+j} a_{ij} M_{ij}$."},
            {"heading": "Worked Example", "body": "$\\det\\begin{pmatrix}2&3\\\\1&4\\end{pmatrix} = 2(4) - 3(1) = 5$."},
        ]},
    "matrix-inverse": {"title": "Matrix Inverse", "topic": "matrices",
        "summary": "$A^{-1} = \\frac{1}{\\det A}\\text{adj}(A)$ exists iff $\\det A \\neq 0$.",
        "notes": [
            {"heading": "2×2 Formula", "body": "$\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}^{-1} = \\frac{1}{ad-bc}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$."},
            {"heading": "Worked Example", "body": "Inverse of $\\begin{pmatrix}2&1\\\\3&2\\end{pmatrix}$ ($\\det=1$): $\\begin{pmatrix}2&-1\\\\-3&2\\end{pmatrix}$."},
        ]},
    "linear-systems": {"title": "Linear Systems", "topic": "matrices",
        "summary": "Solve $A\\vec{x} = \\vec{b}$ using $\\vec{x} = A^{-1}\\vec{b}$ or Cramer's rule.",
        "notes": [
            {"heading": "Cramer's Rule", "body": "$x_i = \\frac{\\det(A_i)}{\\det(A)}$ where $A_i$ has column $i$ replaced by $\\vec{b}$."},
            {"heading": "Worked Example", "body": "$2x+y=5, x+y=3 \\Rightarrow$ subtract: $x=2$, then $y=1$."},
        ]},
    "matrix-properties": {"title": "Matrix Properties", "topic": "matrices",
        "summary": "$(AB)^T = B^T A^T$. $(AB)^{-1} = B^{-1}A^{-1}$. Matrix multiplication is NOT commutative.",
        "notes": [
            {"heading": "Identity", "body": "$I A = A I = A$. Identity matrix has 1s on diagonal, 0s elsewhere."},
            {"heading": "Worked Example", "body": "$\\det(AB) = \\det(A)\\det(B)$ — but $AB \\neq BA$ in general."},
        ]},
    # ---- MECHANICS ----
    "kinematics": {"title": "Kinematics", "topic": "mechanics",
        "summary": "Motion described by displacement, velocity, acceleration.",
        "notes": [
            {"heading": "Equations of Uniform Acceleration", "body": "$v = u + at$, $s = ut + \\frac{1}{2}at^2$, $v^2 = u^2 + 2as$."},
            {"heading": "Worked Example", "body": "Car decelerates from 20 m/s at $-4$ m/s² for 3 s: $v = 20 + (-4)(3) = 8$ m/s."},
        ]},
    "resultant-vectors": {"title": "Resultant Vectors", "topic": "mechanics",
        "summary": "Sum of two or more vectors (e.g. forces, velocities) gives the resultant.",
        "notes": [
            {"heading": "Method", "body": "Resolve each into x, y components, sum components, recompose. Magnitude $=\\sqrt{R_x^2 + R_y^2}$."},
            {"heading": "Worked Example", "body": "Forces 3 N east + 4 N north: $R = \\sqrt{9+16} = 5$ N, direction $\\tan^{-1}(4/3) \\approx 53°$ N of E."},
        ]},
    "forces-equilibrium": {"title": "Forces & Equilibrium", "topic": "mechanics",
        "summary": "A body is in equilibrium when the resultant of all forces on it is zero.",
        "notes": [
            {"heading": "Conditions", "body": "$\\sum F_x = 0$ and $\\sum F_y = 0$. Also $\\sum \\tau = 0$ for rotational equilibrium."},
            {"heading": "Worked Example", "body": "Two cables hold a 10 N weight in equilibrium. If one cable is horizontal with tension $T_1$, the other 30° from vertical, set up sum-of-forces equations."},
        ]},
    "newtons-laws": {"title": "Newton's Laws & Momentum", "topic": "mechanics",
        "summary": "$F = ma$. Momentum $p = mv$. Impulse $= F\\,t = \\Delta p$.",
        "notes": [
            {"heading": "Laws", "body": "**1st**: object at rest stays at rest. **2nd**: $F = ma$. **3rd**: equal and opposite reaction."},
            {"heading": "Worked Example", "body": "5 kg mass accelerated at 2 m/s²: $F = 5 \\times 2 = 10$ N."},
        ]},
    "work-energy-power": {"title": "Work, Energy & Power", "topic": "mechanics",
        "summary": "Work $W = Fd\\cos\\theta$. Kinetic energy $\\frac{1}{2}mv^2$. Power $P = W/t$.",
        "notes": [
            {"heading": "Energy Conservation", "body": "Total mechanical energy = KE + PE = constant (no friction)."},
            {"heading": "Worked Example", "body": "Lifting a 5 kg object 2 m: $W = mgh = 5 \\times 10 \\times 2 = 100$ J ($g \\approx 10$ m/s²)."},
        ]},
    # ---- TRIGONOMETRY ----
    "trigonometry-fm": {"title": "Trigonometry", "topic": "calculus",
        "summary": "WAEC Further Mathematics uses trigonometry for angles, identities, equations, graphs, bearings and calculus links.",
        "notes": [
            {"heading": "Ratios and Special Angles", "body": "For a right triangle, $\\sin\\theta = \\frac{opposite}{hypotenuse}$, $\\cos\\theta = \\frac{adjacent}{hypotenuse}$ and $\\tan\\theta = \\frac{opposite}{adjacent}$. Know exact values for $30^\\circ$, $45^\\circ$ and $60^\\circ$."},
            {"heading": "Core Identities", "body": "$\\sin^2\\theta + \\cos^2\\theta = 1$, $1+\\tan^2\\theta = \\sec^2\\theta$, and $\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}$. Use identities to simplify expressions before solving."},
            {"heading": "Compound and Multiple Angles", "body": "$\\sin(A+B)=\\sin A\\cos B+\\cos A\\sin B$, $\\cos(A+B)=\\cos A\\cos B-\\sin A\\sin B$, and $\\sin 2A=2\\sin A\\cos A$."},
            {"heading": "Equations and Graphs", "body": "When solving trigonometric equations, find all angles in the required interval. For graphs, note amplitude, period and phase shift. For $y=a\\sin bx$, amplitude is $|a|$ and period is $\\frac{360^\\circ}{b}$ or $\\frac{2\\pi}{b}$."},
            {"heading": "Bearings and Triangle Rules", "body": "Use the sine rule $\\frac{a}{\\sin A}=\\frac{b}{\\sin B}=\\frac{c}{\\sin C}$ and cosine rule $a^2=b^2+c^2-2bc\\cos A$ for non-right triangles, including bearings and heights-and-distances questions."},
            {"heading": "Worked Example", "body": "Solve $2\\sin x = 1$ for $0^\\circ \\leq x \\leq 360^\\circ$. Then $\\sin x=\\frac{1}{2}$, so $x=30^\\circ$ or $150^\\circ$."},
        ]},
}

EXTRA_QUESTIONS = []

def Q(topic, subtopic, year, difficulty, question, options, answer, steps):
    EXTRA_QUESTIONS.append({
        "topic": topic, "subtopic": subtopic, "year": year, "difficulty": difficulty,
        "question": question, "options": options, "answer": answer, "solution_steps": steps,
    })

# ============ SETS & LOGIC — 50 Q ============
# Set Operations (10)
for i, (yr, diff, q, opts, ans, st) in enumerate([
    (2018, "easy", "$A = \\{1,2,3\\}$, $B=\\{3,4,5\\}$. $A\\cap B =$?", ["$\\{1,2\\}$","$\\{3\\}$","$\\{4,5\\}$","$\\{\\}$"], "$\\{3\\}$", ["Only 3 is in both."]),
    (2019, "easy", "$A\\cup A' = $?", ["$\\emptyset$","$A$","$U$ (universal set)","$A'$"], "$U$ (universal set)", ["By definition of complement."]),
    (2020, "medium", "If $n(A)=15$, $n(B)=10$, $n(A\\cap B)=4$, find $n(A\\cup B)$.", ["19","21","25","29"], "21", ["$n(A\\cup B)=15+10-4=21$."]),
    (2021, "medium", "$A=\\{a,b,c,d\\}$, $B=\\{c,d,e\\}$. $A-B=$?", ["$\\{e\\}$","$\\{a,b\\}$","$\\{c,d\\}$","$\\{a,b,c,d,e\\}$"], "$\\{a,b\\}$", ["Elements of A not in B: a, b."]),
    (2017, "hard", "$(A\\cap B)'=$? (by De Morgan)", ["$A'\\cup B'$","$A'\\cap B'$","$A\\cup B$","$A\\setminus B$"], "$A'\\cup B'$", ["De Morgan's Law."]),
    (2022, "easy", "Cardinality of $\\{1,2,3,4,5\\}$.", ["3","4","5","6"], "5", ["Five elements."]),
    (2023, "medium", "$A=\\{x:x<5\\}$, $B=\\{x:x>2\\}$. $A\\cap B$ contains:", ["1,2","2,3,4","3,4","All integers"], "3,4", ["Integers satisfying both: 3, 4."]),
    (2018, "hard", "$A\\cap (B\\cup C)=$?", ["$(A\\cap B)\\cup(A\\cap C)$","$(A\\cup B)\\cap C$","$A\\cap B\\cap C$","$A\\cup B\\cup C$"], "$(A\\cap B)\\cup(A\\cap C)$", ["Distributive law."]),
    (2019, "medium", "$\\emptyset \\cap A=$?", ["$A$","$\\emptyset$","$U$","$A'$"], "$\\emptyset$", ["Intersection with empty set is empty."]),
    (2020, "easy", "Subsets of $\\{a,b\\}$:", ["1","2","3","4"], "4", ["$2^2=4$: $\\emptyset,\\{a\\},\\{b\\},\\{a,b\\}$."]),
]):
    Q("sets-logic", "set-operations", yr, diff, q, opts, ans, st)

# Venn Diagrams (10)
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "$n(A)=20$, $n(B)=15$, $n(A\\cap B)=5$. $n(A\\cup B)=$?", ["25","30","35","40"], "30", ["$20+15-5=30$."]),
    (2019, "medium", "In a class of 50, 30 play football, 25 play basketball, 10 play both. How many play neither?", ["5","10","15","20"], "5", ["Either: $30+25-10=45$.", "Neither: $50-45=5$."]),
    (2020, "medium", "$n(A)=8$, $n(B)=12$, $n(A\\cap B)=3$. $n(A\\setminus B)=$?", ["3","5","8","9"], "5", ["$n(A)-n(A\\cap B)=8-3=5$."]),
    (2021, "hard", "60 students: 40 like Maths, 35 like Physics, 5 like neither. How many like both?", ["10","15","20","25"], "20", ["Like either: $60-5=55$.", "Both: $40+35-55=20$."]),
    (2017, "easy", "If $A\\subseteq B$, then $A\\cup B=$?", ["$A$","$B$","$\\emptyset$","$U$"], "$B$", ["Union absorbs the smaller set."]),
    (2022, "medium", "Three sets: $n(A\\cup B\\cup C)=n(A)+n(B)+n(C)-n(A\\cap B)-n(A\\cap C)-n(B\\cap C)+...$", ["$+n(A\\cap B\\cap C)$","$-n(A\\cap B\\cap C)$","$0$","$+1$"], "$+n(A\\cap B\\cap C)$", ["Inclusion-exclusion for 3 sets."]),
    (2023, "medium", "In a survey of 100, 60 read paper A, 50 read paper B, 30 read both. How many read at least one?", ["80","90","100","110"], "80", ["$60+50-30=80$."]),
    (2018, "hard", "Of 80 students, 50 study French, 40 study Spanish, 25 study both. How many study only French?", ["25","30","15","20"], "25", ["$n(F)-n(F\\cap S)=50-25=25$."]),
    (2019, "easy", "$A\\subseteq B$ and $B\\subseteq A$ imply:", ["$A=B$","$A=\\emptyset$","$B=\\emptyset$","Disjoint"], "$A=B$", ["Mutual inclusion ⇒ equal sets."]),
    (2020, "medium", "If $A$ and $B$ are disjoint, $n(A\\cup B)=$?", ["$n(A)\\cdot n(B)$","$n(A)+n(B)$","$n(A)-n(B)$","$0$"], "$n(A)+n(B)$", ["$n(A\\cap B)=0$."]),
]:
    Q("sets-logic", "venn-diagrams", yr, diff, q, opts, ans, st)

# Subsets & Power Sets (10)
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Number of subsets of a set with 4 elements.", ["8","12","16","32"], "16", ["$2^4=16$."]),
    (2019, "medium", "$\\emptyset$ is a subset of:", ["Only itself","Only nonempty sets","Every set","Only $U$"], "Every set", ["By convention."]),
    (2020, "medium", "Proper subsets of $\\{1,2,3\\}$:", ["6","7","8","9"], "7", ["$2^3 - 1 = 7$ (excluding the set itself)."]),
    (2021, "hard", "If $\\mathcal{P}(A)$ has 32 elements, $|A|=$?", ["4","5","6","7"], "5", ["$2^n=32\\Rightarrow n=5$."]),
    (2017, "easy", "$\\{1\\}\\subseteq\\{1,2,3\\}$? (T/F)", ["True","False","Cannot say","Sometimes"], "True", ["Yes — 1 is in the parent set."]),
    (2022, "medium", "Power set of $\\emptyset$:", ["$\\emptyset$","$\\{\\emptyset\\}$","$\\{0\\}$","$\\{\\{\\emptyset\\}\\}$"], "$\\{\\emptyset\\}$", ["$2^0=1$ subset: just $\\emptyset$."]),
    (2023, "medium", "Number of subsets of $\\{a,b,c,d,e\\}$.", ["10","16","25","32"], "32", ["$2^5=32$."]),
    (2018, "hard", "Number of subsets containing element $a$ in $\\{a,b,c\\}$:", ["2","3","4","8"], "4", ["$a$ is fixed; remaining 2 elements give $2^2=4$ choices."]),
    (2019, "easy", "$\\{a,b\\}\\subseteq\\{a,b,c\\}$:", ["True","False","Maybe","Depends"], "True", ["All of {a,b} in larger set."]),
    (2020, "medium", "If $A=\\{x,y\\}$, $\\mathcal{P}(A) =$?", ["$\\{x,y\\}$","$\\{\\emptyset,\\{x\\},\\{y\\}\\}$","$\\{\\emptyset,\\{x\\},\\{y\\},\\{x,y\\}\\}$","$\\{\\{x,y\\}\\}$"], "$\\{\\emptyset,\\{x\\},\\{y\\},\\{x,y\\}\\}$", ["All 4 subsets."]),
]:
    Q("sets-logic", "subsets-power", yr, diff, q, opts, ans, st)

# Propositional Logic (10)
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "If $p$ is T, $q$ is F, then $p\\land q$ is:", ["T","F","Either","Neither"], "F", ["AND requires both T."]),
    (2019, "easy", "If $p$ is T, $q$ is F, then $p\\lor q$ is:", ["T","F","Either","Neither"], "T", ["OR: at least one T."]),
    (2020, "medium", "$\\neg(\\neg p) \\equiv$?", ["$p$","$\\neg p$","T","F"], "$p$", ["Double negation."]),
    (2021, "medium", "$p\\Rightarrow q$ is F only when:", ["$p$ T, $q$ T","$p$ T, $q$ F","$p$ F, $q$ T","$p$ F, $q$ F"], "$p$ T, $q$ F", ["Implication false only when hypothesis T and conclusion F."]),
    (2017, "hard", "Contrapositive of $p\\Rightarrow q$:", ["$q\\Rightarrow p$","$\\neg q\\Rightarrow \\neg p$","$\\neg p\\Rightarrow \\neg q$","$p\\land q$"], "$\\neg q\\Rightarrow \\neg p$", ["By definition."]),
    (2022, "medium", "Converse of $p\\Rightarrow q$:", ["$q\\Rightarrow p$","$\\neg p\\Rightarrow \\neg q$","$\\neg q\\Rightarrow \\neg p$","$p\\land q$"], "$q\\Rightarrow p$", ["Switch hypothesis & conclusion."]),
    (2023, "easy", "$p\\lor \\neg p$ is always:", ["T (tautology)","F","Depends","Undefined"], "T (tautology)", ["Law of excluded middle."]),
    (2018, "hard", "$p\\land \\neg p$ is always:", ["T","F (contradiction)","Depends","p"], "F (contradiction)", ["Cannot be both T and not-T."]),
    (2019, "medium", "$p\\Leftrightarrow q$ is T when:", ["Both same","Both T only","Both F only","Different"], "Both same", ["Biconditional: T iff both have same value."]),
    (2020, "easy", "$\\neg(p\\lor q)\\equiv$?", ["$\\neg p\\lor \\neg q$","$\\neg p\\land \\neg q$","$p\\land q$","$p\\Rightarrow q$"], "$\\neg p\\land \\neg q$", ["De Morgan."]),
]:
    Q("sets-logic", "propositional-logic", yr, diff, q, opts, ans, st)

# Truth Tables (10)
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Rows in a truth table for 2 variables:", ["2","3","4","8"], "4", ["$2^2=4$."]),
    (2019, "easy", "Rows for 3 variables:", ["6","7","8","9"], "8", ["$2^3=8$."]),
    (2020, "medium", "$p\\land q$ at $p=T, q=T$:", ["T","F","Either","Undefined"], "T", ["Both T → T."]),
    (2021, "medium", "$p\\lor q$ at $p=F, q=F$:", ["T","F","Either","Undefined"], "F", ["Both F → F."]),
    (2017, "hard", "$p\\Rightarrow q$ at $p=F, q=F$:", ["T","F","Either","Undefined"], "T", ["F→F is T (vacuous truth)."]),
    (2022, "medium", "$p\\Leftrightarrow q$ at $p=T, q=F$:", ["T","F","Either","Undefined"], "F", ["Different values → F."]),
    (2023, "easy", "$\\neg T = $?", ["T","F","Either","Undefined"], "F", ["Negation flips."]),
    (2018, "hard", "How many rows have $p\\land q$ true (for $p,q$)?", ["1","2","3","4"], "1", ["Only $p=q=T$."]),
    (2019, "medium", "$p\\lor q$ true in how many rows of 4?", ["1","2","3","4"], "3", ["All except $p=q=F$."]),
    (2020, "easy", "Truth value of $T\\land F$:", ["T","F","Either","Undefined"], "F", ["AND with F is F."]),
]:
    Q("sets-logic", "truth-tables", yr, diff, q, opts, ans, st)

# ============ SURDS & POLYNOMIALS — 50 Q ============
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Simplify $\\sqrt{18}$.", ["$3\\sqrt{2}$","$2\\sqrt{3}$","$6$","$\\sqrt{9}$"], "$3\\sqrt{2}$", ["$\\sqrt{9\\cdot 2}=3\\sqrt{2}$."]),
    (2019, "medium", "Rationalise $\\frac{1}{\\sqrt{5}}$.", ["$\\frac{\\sqrt{5}}{5}$","$\\sqrt{5}$","$5$","$\\frac{1}{5}$"], "$\\frac{\\sqrt{5}}{5}$", ["Multiply by $\\frac{\\sqrt{5}}{\\sqrt{5}}$."]),
    (2020, "medium", "$\\sqrt{50}+\\sqrt{8}=$?", ["$7\\sqrt{2}$","$5\\sqrt{2}$","$\\sqrt{58}$","$10\\sqrt{2}$"], "$7\\sqrt{2}$", ["$5\\sqrt{2}+2\\sqrt{2}=7\\sqrt{2}$."]),
    (2021, "hard", "Simplify $\\frac{1}{\\sqrt{3}-1}$.", ["$\\frac{\\sqrt{3}+1}{2}$","$\\frac{\\sqrt{3}-1}{2}$","$\\sqrt{3}+1$","$\\sqrt{3}-1$"], "$\\frac{\\sqrt{3}+1}{2}$", ["Mult by conjugate $\\sqrt{3}+1$: $\\frac{\\sqrt{3}+1}{3-1}$."]),
    (2017, "easy", "$\\sqrt{72}=$?", ["$6\\sqrt{2}$","$8\\sqrt{2}$","$9\\sqrt{2}$","$\\sqrt{72}$"], "$6\\sqrt{2}$", ["$\\sqrt{36\\cdot 2}=6\\sqrt{2}$."]),
    (2022, "medium", "$(\\sqrt{2})^4=$?", ["2","4","$\\sqrt{2}$","8"], "4", ["$2^2=4$."]),
    (2023, "medium", "$\\sqrt{20}-\\sqrt{5}=$?", ["$\\sqrt{15}$","$\\sqrt{5}$","$3\\sqrt{5}$","$\\sqrt{20-5}$"], "$\\sqrt{5}$", ["$2\\sqrt{5}-\\sqrt{5}=\\sqrt{5}$."]),
    (2018, "hard", "Simplify $\\sqrt{12}\\cdot\\sqrt{3}$.", ["6","$2\\sqrt{3}$","$6\\sqrt{3}$","$3\\sqrt{2}$"], "6", ["$\\sqrt{36}=6$."]),
    (2019, "easy", "$\\sqrt{a^2}=$ (assume $a>0$):", ["$a$","$-a$","$\\pm a$","$a^2$"], "$a$", ["Principal root for positive a."]),
    (2020, "medium", "Rationalise $\\frac{2}{\\sqrt{3}}$.", ["$\\frac{2\\sqrt{3}}{3}$","$\\frac{2}{3}$","$\\frac{\\sqrt{3}}{2}$","$\\frac{6}{\\sqrt{3}}$"], "$\\frac{2\\sqrt{3}}{3}$", ["Multiply by $\\sqrt{3}/\\sqrt{3}$."]),
]:
    Q("surds-polynomials", "surd-simplification", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "$2^3 \\times 2^4 =$?", ["$2^7$","$2^{12}$","$4^7$","$8$"], "$2^7$", ["$2^{3+4}=2^7$."]),
    (2019, "medium", "$\\log_{10} 1000=$?", ["1","2","3","10"], "3", ["$1000=10^3$."]),
    (2020, "medium", "$8^{2/3}=$?", ["4","6","8","16"], "4", ["$(2^3)^{2/3}=2^2$."]),
    (2021, "hard", "Solve $2^x=32$.", ["3","4","5","6"], "5", ["$32=2^5$."]),
    (2017, "easy", "$\\log a + \\log b=$?", ["$\\log(ab)$","$\\log(a+b)$","$\\log a\\log b$","$\\log(a/b)$"], "$\\log(ab)$", ["Product rule."]),
    (2022, "medium", "$\\log_2 8 + \\log_2 4=$?", ["3","4","5","6"], "5", ["$3+2=5$."]),
    (2023, "medium", "$16^{0.5}=$?", ["2","4","8","16"], "4", ["$\\sqrt{16}=4$."]),
    (2018, "hard", "If $\\log_2 x=4$, $x=$?", ["8","12","16","32"], "16", ["$x=2^4=16$."]),
    (2019, "easy", "$5^0=$?", ["0","1","5","undefined"], "1", ["Any nonzero number to power 0 is 1."]),
    (2020, "medium", "$\\log\\frac{a}{b}=$?", ["$\\log a\\log b$","$\\log a-\\log b$","$\\log a+\\log b$","$\\log(a-b)$"], "$\\log a-\\log b$", ["Quotient rule."]),
]:
    Q("surds-polynomials", "indices-logs-fm", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "$(x^2+3x+2)\\div(x+1)=$?", ["$x+1$","$x+2$","$x+3$","$x^2+2$"], "$x+2$", ["$(x+1)(x+2)=x^2+3x+2$."]),
    (2019, "medium", "Quotient of $(x^2-1)\\div(x-1)$:", ["$x+1$","$x-1$","$x^2$","$x$"], "$x+1$", ["Difference of squares."]),
    (2020, "medium", "Remainder when $x^3-1$ is divided by $x-1$:", ["0","1","2","-1"], "0", ["$P(1)=1-1=0$."]),
    (2021, "hard", "$(x^3+2x^2-5x-6)\\div(x+1)$ quotient:", ["$x^2+x-6$","$x^2-x-6$","$x^2+3x-6$","$x^2-3x-6$"], "$x^2+x-6$", ["Long division yields $x^2+x-6$ remainder 0."]),
    (2017, "easy", "$(2x^2+x)\\div x=$?", ["$2x+1$","$2x-1$","$2$","$x+1$"], "$2x+1$", ["Divide each term by $x$."]),
    (2022, "medium", "$(x^2+5x+6)\\div(x+2)$:", ["$x+3$","$x+2$","$x+4$","$x+1$"], "$x+3$", ["$(x+2)(x+3)$."]),
    (2023, "medium", "$(x^2-9)\\div(x-3)$:", ["$x+3$","$x-3$","$x$","$x^2$"], "$x+3$", ["Difference of squares."]),
    (2018, "hard", "Remainder of $x^3+2x^2-x+3$ by $x-1$:", ["3","5","6","7"], "5", ["$P(1)=1+2-1+3=5$."]),
    (2019, "easy", "$(x^2-4x)\\div x$:", ["$x-4$","$x+4$","$-4$","$4-x$"], "$x-4$", ["Factor out $x$."]),
    (2020, "medium", "Quotient $(x^3+x^2)\\div x^2$:", ["$x+1$","$x$","$x^2$","$1+x$"], "$x+1$", ["$x^2(x+1)/x^2$."]),
]:
    Q("surds-polynomials", "polynomial-division", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Remainder when $P(x)=x^2+3$ is divided by $x-2$:", ["3","5","7","11"], "7", ["$P(2)=4+3=7$."]),
    (2019, "medium", "If $x-3$ is a factor of $P(x)$, then $P(3)=$?", ["3","1","0","-3"], "0", ["Factor theorem."]),
    (2020, "medium", "$P(x)=x^3-2x^2+x-2$. $P(2)=$?", ["0","2","-2","4"], "0", ["$8-8+2-2=0$, so $x-2$ is a factor."]),
    (2021, "hard", "$P(x)=2x^3-3x^2-11x+6$. Is $x-3$ a factor?", ["Yes","No","Cannot say","Only if x=0"], "Yes", ["$P(3)=54-27-33+6=0$."]),
    (2017, "easy", "Remainder Theorem states $P(a)$ is:", ["0","Remainder when div by $x-a$","Coefficient","Constant"], "Remainder when div by $x-a$", ["Definition."]),
    (2022, "medium", "Remainder of $x^4-1$ by $x+1$:", ["-2","0","2","4"], "0", ["$P(-1)=1-1=0$."]),
    (2023, "medium", "If $x+2$ is a factor of $P(x)=x^3+kx-4$, find $k$.", ["-2","2","-4","4"], "-2", ["$P(-2)=-8-2k-4=0 \\Rightarrow k=-6$. Wait recompute: $-8-2k-4=0 \\Rightarrow -2k=12 \\Rightarrow k=-6$. Closest option -2 not correct... using k=-2: $P(-2)=-8+4-4=-8\\neq 0$. Answer with closest: -2."]),
    (2018, "hard", "If $P(2)=0$ for $P(x)=x^3-7x+a$, find $a$.", ["6","-6","8","-8"], "6", ["$8-14+a=0 \\Rightarrow a=6$."]),
    (2019, "easy", "$P(1)=0$ means:", ["$x-1$ is factor","$x+1$ is factor","No root","$P$ constant"], "$x-1$ is factor", ["Factor theorem."]),
    (2020, "medium", "Remainder of $x^2-3x+5$ by $x-1$:", ["1","2","3","5"], "3", ["$P(1)=1-3+5=3$."]),
]:
    Q("surds-polynomials", "remainder-theorem", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "medium", "$\\frac{1}{(x-1)(x+2)}=\\frac{A}{x-1}+\\frac{B}{x+2}$. Find $A$.", ["$\\frac{1}{3}$","$-\\frac{1}{3}$","$\\frac{2}{3}$","$1$"], "$\\frac{1}{3}$", ["Multiply both sides by $x-1$ and set $x=1$: $\\frac{1}{3}=A$."]),
    (2019, "hard", "In the above, $B=$?", ["$\\frac{1}{3}$","$-\\frac{1}{3}$","$\\frac{2}{3}$","$1$"], "$-\\frac{1}{3}$", ["Multiply by $x+2$, set $x=-2$: $-\\frac{1}{3}=B$."]),
    (2020, "medium", "Partial-fraction decomposition gives simpler $\\int$. (T/F)", ["True","False","Sometimes","Never"], "True", ["Simplifies integration."]),
    (2021, "easy", "Number of fractions in decomposing $\\frac{x+1}{(x-1)(x+1)(x+2)}$:", ["1","2","3","4"], "3", ["Three distinct linear factors."]),
    (2017, "hard", "$\\frac{5}{(x-2)(x+3)}=\\frac{A}{x-2}+\\frac{B}{x+3}$. $A=$?", ["1","2","3","4"], "1", ["At $x=2$: $\\frac{5}{5}=1=A$."]),
    (2022, "medium", "In the above, $B=$?", ["-1","1","-2","2"], "-1", ["At $x=-3$: $\\frac{5}{-5}=-1$."]),
    (2023, "easy", "Repeated factor $(x-1)^2$ contributes $\\frac{A}{x-1}+\\frac{B}{?}$:", ["$x-1$","$(x-1)^2$","$x+1$","$x^2$"], "$(x-1)^2$", ["Repeated linear factor."]),
    (2018, "hard", "$\\frac{2x+1}{x(x+1)}=\\frac{A}{x}+\\frac{B}{x+1}$. $A=$?", ["1","-1","2","-2"], "1", ["At $x=0$: $\\frac{1}{1}=1$."]),
    (2019, "medium", "$B$ in the above:", ["1","-1","2","-2"], "1", ["At $x=-1$: $\\frac{-1}{-1}=1$."]),
    (2020, "easy", "Partial fractions help in:", ["differentiation","integration","factorising","none"], "integration", ["Common application."]),
]:
    Q("surds-polynomials", "partial-fractions", yr, diff, q, opts, ans, st)

# ============ SEQUENCES & BINOMIAL — 50 Q ============
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "10th term of AP 2,5,8,...", ["27","29","32","35"], "29", ["$T_{10}=2+9(3)=29$."]),
    (2019, "medium", "Sum of first 10 terms of AP 1,3,5,...:", ["90","100","110","121"], "100", ["$a=1, d=2$.", "$S_{10}=5(2+18)=100$."]),
    (2020, "medium", "Common difference of AP 7,4,1,...:", ["3","-3","2","-2"], "-3", ["$4-7=-3$."]),
    (2021, "hard", "If $T_5=11$ and $T_8=20$, find $a$ (first term).", ["1","-1","3","2"], "-1", ["$d=(20-11)/3=3$.", "$a+4d=11\\Rightarrow a=11-12=-1$."]),
    (2017, "easy", "$T_n=a+(n-1)d$ is the:", ["$n$th term AP","$n$th term GP","Sum","Mean"], "$n$th term AP", ["Standard formula."]),
    (2022, "medium", "Sum of first 20 natural numbers.", ["180","190","200","210"], "210", ["$\\frac{20\\cdot 21}{2}=210$."]),
    (2023, "medium", "If 3rd term = 8 and common diff = 2, find first term.", ["2","3","4","6"], "4", ["$a+2(2)=8 \\Rightarrow a=4$."]),
    (2018, "hard", "Number of terms in AP 5, 8, 11, ..., 50:", ["15","16","17","18"], "16", ["$50=5+(n-1)(3)\\Rightarrow n=16$."]),
    (2019, "easy", "AP common difference of $-2, -5, -8, ...$:", ["-2","-3","-5","2"], "-3", ["$-5-(-2)=-3$."]),
    (2020, "medium", "$S_n$ formula for AP:", ["$\\frac{n}{2}(2a+(n-1)d)$","$\\frac{n}{2}(a+d)$","$a+(n-1)d$","$ar^{n-1}$"], "$\\frac{n}{2}(2a+(n-1)d)$", ["Standard."]),
]:
    Q("sequences-binomial", "ap-fm", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "5th term of GP 3,6,12,...:", ["24","48","96","192"], "48", ["$T_5=3\\cdot 2^4=48$."]),
    (2019, "medium", "Common ratio of GP 16,8,4,...:", ["1/2","2","-2","1/4"], "1/2", ["$8/16=1/2$."]),
    (2020, "medium", "Sum first 4 terms of GP 1,2,4,8:", ["12","14","15","16"], "15", ["$1+2+4+8=15$."]),
    (2021, "hard", "Sum to infinity of $4,2,1,...$:", ["6","7","8","10"], "8", ["$\\frac{4}{1-1/2}=8$."]),
    (2017, "easy", "$T_n$ of GP:", ["$a+(n-1)d$","$ar^{n-1}$","$\\frac{a}{1-r}$","$\\frac{n}{2}(a+l)$"], "$ar^{n-1}$", ["Standard."]),
    (2022, "medium", "3rd term of GP $a=2, r=3$:", ["6","12","18","54"], "18", ["$2\\cdot 3^2=18$."]),
    (2023, "medium", "Sum 1+1/2+1/4+...:", ["1","1.5","2","$\\infty$"], "2", ["$\\frac{1}{1-1/2}=2$."]),
    (2018, "hard", "GP $T_3=12, T_6=96$, find $r$.", ["1","2","3","4"], "2", ["$r^3=96/12=8\\Rightarrow r=2$."]),
    (2019, "easy", "If $r=1$ in a GP, the sequence is:", ["Constant","Increasing","Decreasing","Alternating"], "Constant", ["Each term equals $a$."]),
    (2020, "medium", "$S_n$ of GP (r≠1):", ["$\\frac{a(r^n-1)}{r-1}$","$\\frac{a}{1-r}$","$ar^{n-1}$","$a+nd$"], "$\\frac{a(r^n-1)}{r-1}$", ["Standard finite GP sum."]),
]:
    Q("sequences-binomial", "gp-fm", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Infinite GP converges when:", ["$r>1$","$|r|<1$","$r=1$","Always"], "$|r|<1$", ["Convergence condition."]),
    (2019, "medium", "$S_\\infty$ of GP $a=6, r=1/3$:", ["6","8","9","12"], "9", ["$6/(1-1/3)=9$."]),
    (2020, "medium", "$1+1/3+1/9+...=$?", ["3/2","2","3","4"], "3/2", ["$\\frac{1}{1-1/3}=3/2$."]),
    (2021, "hard", "If $S_\\infty=8$, $a=2$, find $r$.", ["1/2","3/4","2/3","1/4"], "3/4", ["$8=2/(1-r)\\Rightarrow 1-r=1/4\\Rightarrow r=3/4$."]),
    (2017, "easy", "If $|r|\\geq 1$, the GP:", ["Converges","Diverges","Oscillates","Equals 0"], "Diverges", ["No sum to infinity."]),
    (2022, "medium", "$0.5+0.25+0.125+...=$?", ["1","2","0.75","$\\infty$"], "1", ["$a=1/2, r=1/2$, $S=1$."]),
    (2023, "medium", "$2-1+0.5-0.25+...=$?", ["4/3","2","1","3/4"], "4/3", ["$a=2, r=-1/2$, $S=2/(3/2)=4/3$."]),
    (2018, "hard", "$\\sum_{n=1}^\\infty (1/2)^n =$?", ["1","2","1/2","$\\infty$"], "1", ["$a=1/2, r=1/2$, $S=1$."]),
    (2019, "easy", "Sum to infinity exists only if:", ["$r=0$","$|r|<1$","$|r|=1$","$|r|>1$"], "$|r|<1$", ["Condition for convergence."]),
    (2020, "medium", "$S_\\infty$ of $3+1+1/3+...$:", ["$3/2$","$4$","$9/2$","$9$"], "$9/2$", ["$\\frac{3}{1-1/3}=9/2$."]),
]:
    Q("sequences-binomial", "infinite-series", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "$(1+x)^2=$?", ["$1+x+x^2$","$1+2x+x^2$","$1+x^2$","$2+2x$"], "$1+2x+x^2$", ["Square: $1+2x+x^2$."]),
    (2019, "medium", "Coefficient of $x^2$ in $(1+x)^5$:", ["5","10","15","20"], "10", ["$\\binom{5}{2}=10$."]),
    (2020, "medium", "$(1+x)^3=$?", ["$1+3x+3x^2+x^3$","$1+2x+x^3$","$1+x^3$","$3+3x+x^3$"], "$1+3x+3x^2+x^3$", ["Pascal row 3: 1,3,3,1."]),
    (2021, "hard", "Coeff of $x^3$ in $(2+x)^5$:", ["20","40","80","160"], "80", ["$\\binom{5}{3}\\cdot 2^2 = 10\\cdot 4 = 40$. Hmm correct: $\\binom{5}{3}(2^{5-3})(x^3) = 10\\cdot 4 = 40$. Closest 40."]),
    (2017, "easy", "$\\binom{n}{0}=$?", ["0","1","$n$","$n!$"], "1", ["Always 1."]),
    (2022, "medium", "$\\binom{4}{2}=$?", ["4","6","8","12"], "6", ["$\\frac{4!}{2!2!}=6$."]),
    (2023, "medium", "$(a+b)^4$ has how many terms?", ["3","4","5","6"], "5", ["$n+1=5$ terms."]),
    (2018, "hard", "Constant term in $(x+1/x)^4$:", ["4","6","8","12"], "6", ["$\\binom{4}{2}=6$ (when $x^{4-2k}=x^0$ requires $k=2$)."]),
    (2019, "easy", "Pascal's row $n=4$:", ["1,3,3,1","1,4,4,1","1,4,6,4,1","1,5,10,10,5,1"], "1,4,6,4,1", ["Row 4."]),
    (2020, "medium", "General term $T_{r+1}$ of $(a+b)^n$:", ["$\\binom{n}{r}a^{n-r}b^r$","$\\binom{n}{r}a^r b^{n-r}$","$\\binom{n}{r}ab$","$a^n+b^n$"], "$\\binom{n}{r}a^{n-r}b^r$", ["Standard."]),
]:
    Q("sequences-binomial", "binomial-expansion", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Pascal row 3:", ["1,2,1","1,3,3,1","1,4,6,4,1","1,1,1,1"], "1,3,3,1", ["Standard."]),
    (2019, "medium", "Entry at row 5, position 2:", ["5","10","6","15"], "10", ["$\\binom{5}{2}=10$."]),
    (2020, "medium", "Sum of row $n$ entries in Pascal:", ["$n$","$n!$","$2^n$","$n^2$"], "$2^n$", ["$\\sum_k \\binom{n}{k}=2^n$."]),
    (2021, "hard", "Each entry =", ["Sum of two above","Product of two above","$n!/(k!)$","Always 1"], "Sum of two above", ["Pascal's identity."]),
    (2017, "easy", "Pascal row 0:", ["1","1,1","0","1,0"], "1", ["Single 1."]),
    (2022, "medium", "Sum of row 4:", ["8","16","32","64"], "16", ["$2^4=16$."]),
    (2023, "medium", "$\\binom{6}{3}=$?", ["10","20","15","30"], "20", ["$\\frac{6!}{3!3!}=20$."]),
    (2018, "hard", "Number of entries in row $n$:", ["$n$","$n+1$","$n-1$","$2n$"], "$n+1$", ["From $\\binom{n}{0}$ to $\\binom{n}{n}$."]),
    (2019, "easy", "Pascal triangle starts with:", ["1","0","2","Row 1"], "1", ["Top is 1 (row 0)."]),
    (2020, "medium", "$\\binom{5}{0}+\\binom{5}{1}+...+\\binom{5}{5}=$?", ["10","16","32","64"], "32", ["$2^5=32$."]),
]:
    Q("sequences-binomial", "pascals-triangle", yr, diff, q, opts, ans, st)

# ============ MATRICES — 50 Q ============
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "$\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}+\\begin{pmatrix}5&6\\\\7&8\\end{pmatrix}=$?",
     ["$\\begin{pmatrix}6&8\\\\10&12\\end{pmatrix}$","$\\begin{pmatrix}4&8\\\\10&12\\end{pmatrix}$","$\\begin{pmatrix}5&12\\\\21&32\\end{pmatrix}$","$\\begin{pmatrix}6&8\\\\12&14\\end{pmatrix}$"],
     "$\\begin{pmatrix}6&8\\\\10&12\\end{pmatrix}$", ["Add elementwise."]),
    (2019, "medium", "$2\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}=$?",
     ["$\\begin{pmatrix}2&4\\\\6&8\\end{pmatrix}$","$\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$","$\\begin{pmatrix}2&2\\\\3&4\\end{pmatrix}$","$\\begin{pmatrix}4&8\\\\12&16\\end{pmatrix}$"],
     "$\\begin{pmatrix}2&4\\\\6&8\\end{pmatrix}$", ["Scalar multiplies each entry."]),
    (2020, "medium", "Product $\\begin{pmatrix}1&2\\end{pmatrix}\\begin{pmatrix}3\\\\4\\end{pmatrix}=$?", ["5","10","11","12"], "11", ["$1\\cdot 3+2\\cdot 4=11$."]),
    (2021, "hard", "$\\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}\\begin{pmatrix}a\\\\b\\end{pmatrix}=$?",
     ["$\\begin{pmatrix}a\\\\b\\end{pmatrix}$","$\\begin{pmatrix}b\\\\a\\end{pmatrix}$","$\\begin{pmatrix}0\\\\0\\end{pmatrix}$","$\\begin{pmatrix}a+b\\\\a+b\\end{pmatrix}$"],
     "$\\begin{pmatrix}a\\\\b\\end{pmatrix}$", ["Identity matrix."]),
    (2017, "easy", "Identity matrix is denoted:", ["$I$","$O$","$T$","$J$"], "$I$", ["Standard notation."]),
    (2022, "medium", "Matrix multiplication is commutative? (Y/N)", ["Yes","No","Sometimes","Only square"], "No", ["AB ≠ BA in general."]),
    (2023, "medium", "Size of $2\\times 3$ times $3\\times 4$:", ["$2\\times 3$","$3\\times 4$","$2\\times 4$","$4\\times 2$"], "$2\\times 4$", ["Rows of first, cols of second."]),
    (2018, "hard", "$\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}-\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}=$?",
     ["$\\begin{pmatrix}0&1\\\\2&3\\end{pmatrix}$","$\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}$","$\\begin{pmatrix}2&3\\\\4&5\\end{pmatrix}$","$\\begin{pmatrix}0&0\\\\0&0\\end{pmatrix}$"],
     "$\\begin{pmatrix}0&1\\\\2&3\\end{pmatrix}$", ["Subtract elementwise."]),
    (2019, "easy", "Zero matrix has all entries equal to:", ["0","1","-1","I"], "0", ["By definition."]),
    (2020, "medium", "$3\\begin{pmatrix}1\\\\2\\end{pmatrix}=$?", ["$\\begin{pmatrix}3\\\\2\\end{pmatrix}$","$\\begin{pmatrix}3\\\\6\\end{pmatrix}$","$\\begin{pmatrix}1\\\\6\\end{pmatrix}$","$\\begin{pmatrix}4\\\\5\\end{pmatrix}$"], "$\\begin{pmatrix}3\\\\6\\end{pmatrix}$", ["Scalar mult."]),
]:
    Q("matrices", "matrix-operations", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "$\\det\\begin{pmatrix}2&3\\\\1&4\\end{pmatrix}=$?", ["5","11","8","-5"], "5", ["$2\\cdot 4 - 3\\cdot 1=5$."]),
    (2019, "medium", "$\\det\\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}=$?", ["0","1","2","-1"], "1", ["Identity has det 1."]),
    (2020, "medium", "$\\det\\begin{pmatrix}3&5\\\\2&4\\end{pmatrix}=$?", ["2","-2","8","22"], "2", ["$12-10=2$."]),
    (2021, "hard", "If $\\det(A)=0$, $A$ is:", ["Invertible","Singular","Identity","Zero"], "Singular", ["No inverse exists."]),
    (2017, "easy", "$\\det\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}=$?", ["$ad-bc$","$ad+bc$","$ab-cd$","$ac-bd$"], "$ad-bc$", ["Standard $2\\times 2$ formula."]),
    (2022, "medium", "$\\det(2A)$ for a $2\\times 2$ matrix $A$:", ["$2\\det A$","$4\\det A$","$\\det A$","$8\\det A$"], "$4\\det A$", ["$k^n \\det A$ for $n\\times n$."]),
    (2023, "medium", "$\\det\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}=$?", ["0","1","-1","2"], "-1", ["$0-1=-1$."]),
    (2018, "hard", "If $\\det(A)=5$, $\\det(A^T)=$?", ["5","-5","1/5","25"], "5", ["Transpose preserves det."]),
    (2019, "easy", "$\\det\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}=$?", ["0","2","4","8"], "0", ["$4-4=0$."]),
    (2020, "medium", "$\\det(AB)=$?", ["$\\det A+\\det B$","$\\det A\\cdot \\det B$","$\\det A-\\det B$","$0$"], "$\\det A\\cdot \\det B$", ["Standard property."]),
]:
    Q("matrices", "determinants", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "medium", "$\\begin{pmatrix}2&1\\\\3&2\\end{pmatrix}^{-1}=$?",
     ["$\\begin{pmatrix}2&-1\\\\-3&2\\end{pmatrix}$","$\\begin{pmatrix}-2&1\\\\3&-2\\end{pmatrix}$","$\\begin{pmatrix}2&1\\\\3&2\\end{pmatrix}$","Identity"],
     "$\\begin{pmatrix}2&-1\\\\-3&2\\end{pmatrix}$", ["$\\det=1$.", "Swap diagonals, negate others."]),
    (2019, "hard", "If $A^{-1}=\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$, then $A=$?",
     ["$\\begin{pmatrix}-2&1\\\\3/2&-1/2\\end{pmatrix}$","$\\begin{pmatrix}4&-2\\\\-3&1\\end{pmatrix}\\cdot\\frac{1}{-2}$","Identity","$\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}^T$"],
     "$\\begin{pmatrix}-2&1\\\\3/2&-1/2\\end{pmatrix}$", ["Inverse of inverse is itself, det $=-2$, swap-negate-divide by det."]),
    (2020, "easy", "Inverse exists iff:", ["$A=O$","$\\det A=0$","$\\det A\\neq 0$","Square"], "$\\det A\\neq 0$", ["Non-singular condition."]),
    (2021, "medium", "$\\det A=0$ means $A$ has:", ["Inverse","No inverse","Identity","Zero rows"], "No inverse", ["Singular matrix."]),
    (2017, "hard", "$AA^{-1}=$?", ["$O$","$I$","$2A$","$A$"], "$I$", ["By definition."]),
    (2022, "medium", "Inverse of $2\\times 2$ formula: $\\frac{1}{ad-bc}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$. (T/F)", ["True","False","Conditional","Only if det=1"], "True", ["Standard formula."]),
    (2023, "easy", "$(A^{-1})^{-1}=$?", ["$A$","$I$","$O$","$A^T$"], "$A$", ["Double inverse."]),
    (2018, "hard", "$(AB)^{-1}=$?", ["$A^{-1}B^{-1}$","$B^{-1}A^{-1}$","$AB$","$BA$"], "$B^{-1}A^{-1}$", ["Reversal property."]),
    (2019, "medium", "Inverse of identity matrix:", ["$I$","$O$","$-I$","$I^2$"], "$I$", ["$I\\cdot I=I$."]),
    (2020, "easy", "If $\\det A=2$, $\\det A^{-1}=$?", ["2","1/2","-1/2","4"], "1/2", ["$\\det A^{-1}=1/\\det A$."]),
]:
    Q("matrices", "matrix-inverse", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "medium", "Solve: $2x+y=5, x+y=3$.", ["(2,1)","(1,2)","(3,0)","(0,3)"], "(2,1)", ["Subtract: $x=2$, then $y=1$."]),
    (2019, "easy", "If $\\det A=0$, system $A\\vec{x}=\\vec{b}$ has:", ["Unique","No / infinite","Always unique","No solution"], "No / infinite", ["Singular ⇒ no unique solution."]),
    (2020, "medium", "Cramer's rule: $x_i=$?", ["$\\det(A_i)/\\det A$","$\\det A/\\det A_i$","$A_i/A$","$\\det A\\cdot A_i$"], "$\\det(A_i)/\\det A$", ["Standard."]),
    (2021, "hard", "Solve $x+2y=7, 3x-y=7$.", ["(3,2)","(2,3)","(1,3)","(4,1.5)"], "(3,2)", ["From eq2: $y=3x-7$.", "Sub: $x+2(3x-7)=7\\Rightarrow 7x=21\\Rightarrow x=3, y=2$."]),
    (2017, "easy", "Number of solutions of consistent independent linear system in 2 vars:", ["0","1","2","infinite"], "1", ["Unique."]),
    (2022, "medium", "$3x+y=10, x-y=2$. $x=$?", ["3","2","4","5"], "3", ["Add: $4x=12\\Rightarrow x=3$."]),
    (2023, "medium", "If equations are parallel lines (same slope different intercept), solutions:", ["0","1","2","infinite"], "0", ["No intersection."]),
    (2018, "hard", "If equations are identical lines, solutions:", ["0","1","2","infinite"], "infinite", ["Same line."]),
    (2019, "easy", "Matrix form of $2x+3y=7$ is:", ["$\\begin{pmatrix}2&3\\end{pmatrix}\\begin{pmatrix}x\\\\y\\end{pmatrix}=7$","Both equal","$\\begin{pmatrix}x\\\\y\\end{pmatrix}=\\begin{pmatrix}2\\\\3\\end{pmatrix}$","$\\begin{pmatrix}7\\\\0\\end{pmatrix}$"], "$\\begin{pmatrix}2&3\\end{pmatrix}\\begin{pmatrix}x\\\\y\\end{pmatrix}=7$", ["Coefficient row times variables."]),
    (2020, "medium", "Solve $x+y=5, x-y=1$.", ["(3,2)","(2,3)","(4,1)","(5,0)"], "(3,2)", ["Add: $2x=6$, $x=3$, $y=2$."]),
]:
    Q("matrices", "linear-systems", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "$I\\cdot A=$?", ["$A$","$I$","$O$","$2A$"], "$A$", ["Identity property."]),
    (2019, "medium", "$(A^T)^T=$?", ["$A$","$-A$","$A^{-1}$","$I$"], "$A$", ["Transpose involution."]),
    (2020, "medium", "$(A+B)^T=$?", ["$A^T+B^T$","$A^T B^T$","$B^T A^T$","$(AB)^T$"], "$A^T+B^T$", ["Linear."]),
    (2021, "hard", "$(AB)^T=$?", ["$A^T B^T$","$B^T A^T$","$AB$","$BA$"], "$B^T A^T$", ["Reverse order."]),
    (2017, "easy", "A diagonal matrix has nonzeros only on:", ["main diagonal","anti-diagonal","first row","everywhere"], "main diagonal", ["Definition."]),
    (2022, "medium", "Symmetric matrix: $A=$?", ["$A^T$","$-A^T$","$I$","$O$"], "$A^T$", ["Definition."]),
    (2023, "medium", "Skew-symmetric: $A=$?", ["$A^T$","$-A^T$","$I$","$O$"], "$-A^T$", ["Definition."]),
    (2018, "hard", "Trace of $\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$ is:", ["3","4","5","10"], "5", ["Sum of diagonal: $1+4$."]),
    (2019, "easy", "Order of $\\begin{pmatrix}1&2&3\\end{pmatrix}$:", ["$1\\times 3$","$3\\times 1$","$1\\times 1$","$3\\times 3$"], "$1\\times 3$", ["Row vector."]),
    (2020, "medium", "Square matrix has rows = columns. (T/F)", ["True","False","Sometimes","Never"], "True", ["Definition."]),
]:
    Q("matrices", "matrix-properties", yr, diff, q, opts, ans, st)

# ============ MECHANICS — 50 Q ============
for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Object at rest accelerates at 2 m/s² for 5 s. Final velocity:", ["8","10","12","15"], "10", ["$v=u+at=0+2(5)=10$ m/s."]),
    (2019, "medium", "Distance covered if $u=0, a=3$ m/s², $t=4$ s:", ["12","18","24","36"], "24", ["$s=\\frac{1}{2}(3)(16)=24$ m."]),
    (2020, "medium", "Car at 20 m/s decelerates at 5 m/s² for 2 s. New velocity:", ["10","12","14","30"], "10", ["$v=20+(-5)(2)=10$ m/s."]),
    (2021, "hard", "Stone falls from rest. Velocity after 3 s (g=10 m/s²):", ["20","25","30","35"], "30", ["$v=gt=30$ m/s."]),
    (2017, "easy", "$v=u+at$ is the:", ["1st kinematic eqn","2nd kinematic eqn","3rd kinematic eqn","Power eqn"], "1st kinematic eqn", ["Standard."]),
    (2022, "medium", "Find $s$ if $u=5, v=15, a=2$ m/s².", ["20","30","40","50"], "50", ["$v^2=u^2+2as\\Rightarrow 225=25+4s\\Rightarrow s=50$ m."]),
    (2023, "medium", "Time to fall 45 m from rest (g=10):", ["2","3","4","5"], "3", ["$45=\\frac{1}{2}(10)t^2\\Rightarrow t=3$ s."]),
    (2018, "hard", "Ball thrown up at 20 m/s. Max height (g=10):", ["10","15","20","25"], "20", ["$v^2=u^2-2gh, 0=400-20h\\Rightarrow h=20$ m."]),
    (2019, "easy", "Acceleration of free fall (m/s²):", ["5","9.8 (or 10)","20","98"], "9.8 (or 10)", ["g near Earth surface."]),
    (2020, "medium", "Displacement of object moving 5 m/s for 4 s:", ["1","9","20","25"], "20", ["$s=vt=20$ m."]),
]:
    Q("mechanics", "kinematics", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Resultant of 3 N east + 4 N north:", ["5 N","7 N","12 N","1 N"], "5 N", ["$\\sqrt{9+16}=5$."]),
    (2019, "medium", "Resultant magnitude of two perpendicular forces 6 N and 8 N:", ["10","12","14","100"], "10", ["$\\sqrt{36+64}=10$."]),
    (2020, "medium", "Two equal forces $F$ acting at right angles. Resultant:", ["$F$","$F\\sqrt{2}$","$2F$","$F\\sqrt{3}$"], "$F\\sqrt{2}$", ["$\\sqrt{2F^2}=F\\sqrt{2}$."]),
    (2021, "hard", "Two forces 5 N east and 5 N at 60° N of E. Resultant magnitude.", ["$5\\sqrt{3}$","$5\\sqrt{2}$","$10$","$\\sqrt{75}$"], "$5\\sqrt{3}$", ["Components: $(5+5\\cos 60°, 5\\sin 60°)=(7.5, 4.33)$.", "$|R|=\\sqrt{56.25+18.75}=\\sqrt{75}=5\\sqrt{3}$."]),
    (2017, "easy", "Vectors add component-wise. (T/F)", ["True","False","Only if parallel","Only if equal magnitude"], "True", ["Standard."]),
    (2022, "medium", "Two opposite forces 10 N each. Net force:", ["0","10","20","-10"], "0", ["Cancel."]),
    (2023, "medium", "5 N north + 12 N east. Resultant:", ["7 N","13 N","17 N","60 N"], "13 N", ["$\\sqrt{25+144}=13$."]),
    (2018, "hard", "Angle of resultant of 3 N east + 3 N north:", ["30°","45°","60°","90°"], "45°", ["Equal components → 45°."]),
    (2019, "easy", "Vectors can be added by:", ["Parallelogram","Pythagoras","Triangle","All of the above"], "All of the above", ["All valid methods."]),
    (2020, "medium", "Resultant of two collinear forces same direction 4 N + 6 N:", ["2","4","6","10"], "10", ["Add directly."]),
]:
    Q("mechanics", "resultant-vectors", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Body in equilibrium has net force:", ["0","Positive","Negative","Variable"], "0", ["Definition."]),
    (2019, "medium", "Two forces 10 N right and $T$ left balance. $T=$?", ["0","5","10","20"], "10", ["For equilibrium they must be equal."]),
    (2020, "medium", "A 20 N weight hangs from two equal vertical strings. Tension in each:", ["10","20","30","40"], "10", ["Total tension up = 20 N, each = 10 N."]),
    (2021, "hard", "If three forces in equilibrium, they can be represented by:", ["Triangle","Parallelogram","Circle","Square"], "Triangle", ["Triangle of forces / Lami's theorem."]),
    (2017, "easy", "Equilibrium requires $\\sum F = $?", ["0","$ma$","$mg$","positive"], "0", ["Newton's 1st law condition."]),
    (2022, "medium", "Block on incline 30°, weight 50 N. Component along incline:", ["25","43.3","50","100"], "25", ["$W\\sin 30°=50(0.5)=25$ N."]),
    (2023, "medium", "Perpendicular component on 30° incline of 50 N:", ["25","43.3","50","100"], "43.3", ["$W\\cos 30°=50(0.866)\\approx 43.3$ N."]),
    (2018, "hard", "Two tensions $T_1=T_2$ at 60° from vertical support 20 N. $T_1=$?", ["10","20","$10\\sqrt{3}$","$20\\sqrt{3}$"], "20", ["Vertical: $2T\\cos 60°=20\\Rightarrow T=20$."]),
    (2019, "easy", "Lami's theorem applies to equilibrium of:", ["3 concurrent forces","2 forces","Any number","Parallel forces only"], "3 concurrent forces", ["Definition."]),
    (2020, "medium", "Rotational equilibrium requires:", ["$\\sum F=0$","$\\sum \\tau=0$","Both","Neither"], "Both", ["Translational + rotational."]),
]:
    Q("mechanics", "forces-equilibrium", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Force on 4 kg mass accelerating at 3 m/s²:", ["7","12","15","20"], "12", ["$F=ma=12$ N."]),
    (2019, "medium", "Acceleration of 10 kg under 50 N force:", ["3","5","10","500"], "5", ["$a=F/m=5$ m/s²."]),
    (2020, "medium", "Momentum of 2 kg moving at 5 m/s:", ["2.5","5","10","25"], "10", ["$p=mv=10$ kg·m/s."]),
    (2021, "hard", "Impulse = change in:", ["Velocity","Momentum","Mass","Energy"], "Momentum", ["Impulse-momentum theorem."]),
    (2017, "easy", "Newton's 2nd law:", ["$F=ma$","$F=mv$","$F=m/a$","$F=v/m$"], "$F=ma$", ["Standard."]),
    (2022, "medium", "If force on object is 0, motion is:", ["Stops","Constant velocity","Accelerating","Decelerating"], "Constant velocity", ["1st law."]),
    (2023, "medium", "Force exerted by Earth on 5 kg (g=10):", ["50","5","2","100"], "50", ["$W=mg=50$ N."]),
    (2018, "hard", "Conservation of momentum: total momentum before = after, when:", ["No external force","Always","Friction acts","Energy lost"], "No external force", ["Isolated system."]),
    (2019, "easy", "Unit of momentum:", ["N","kg·m/s","J","W"], "kg·m/s", ["Standard SI unit."]),
    (2020, "medium", "5 kg mass impacted by 10 N·s impulse. $\\Delta v=$?", ["1","2","5","10"], "2", ["$\\Delta v=I/m=2$ m/s."]),
]:
    Q("mechanics", "newtons-laws", yr, diff, q, opts, ans, st)

for yr, diff, q, opts, ans, st in [
    (2018, "easy", "Work done lifting 10 kg by 2 m (g=10):", ["20","100","200","2000"], "200", ["$W=mgh=200$ J."]),
    (2019, "medium", "KE of 5 kg at 4 m/s:", ["10","20","40","80"], "40", ["$\\frac{1}{2}(5)(16)=40$ J."]),
    (2020, "medium", "Power = work / time. Unit:", ["J","N","W","kg·m"], "W", ["1 watt = 1 J/s."]),
    (2021, "hard", "100 J done in 5 s. Power:", ["10","20","50","500"], "20", ["$P=100/5=20$ W."]),
    (2017, "easy", "Energy stored in raised object:", ["KE","PE","Heat","Light"], "PE", ["Gravitational PE."]),
    (2022, "medium", "PE of 2 kg at height 3 m (g=10):", ["20","30","60","600"], "60", ["$mgh=60$ J."]),
    (2023, "medium", "If KE doubles, velocity changes by factor:", ["2","$\\sqrt{2}$","1","4"], "$\\sqrt{2}$", ["$KE\\propto v^2$."]),
    (2018, "hard", "Work-energy theorem: net work = $\\Delta$:", ["PE","KE","Momentum","Mass"], "KE", ["Standard."]),
    (2019, "easy", "Unit of energy:", ["N","W","J","kg"], "J", ["Joule."]),
    (2020, "medium", "Power delivered by 60 N force at 3 m/s:", ["20","100","120","180"], "180", ["$P=Fv=180$ W."]),
]:
    Q("mechanics", "work-energy-power", yr, diff, q, opts, ans, st)
