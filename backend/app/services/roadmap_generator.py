import logging
import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.interview_feedback import InterviewFeedback
from app.models.interview_session import InterviewSession
from app.models.progress import Progress
from app.models.roadmap import Roadmap
from app.models.roadmap_task import RoadmapTask
from app.models.skill import Skill
from app.models.skill_gap import SkillGap
from app.models.student_profile import StudentProfile
from app.models.student_skill import StudentSkill
from app.models.interview_answer import InterviewAnswer
from sqlalchemy import func

logger = logging.getLogger(__name__)

# Company specific preparation templates and learning tracks
COMPANY_ROADMAP_TEMPLATES: dict[str, dict[str, Any]] = {
    "Google": {
        "title": "Google SWE Placement Mastery Roadmap",
        "summary": "Tailored 8-week intensive roadmap focused on Graph Algorithms, Dynamic Programming, Scalable System Design, and Googleyness behavioral leadership.",
        "company_type": "Product-based",
        "recommendations": [
            "Practice graph algorithms (Topological Sort, Dijkstra, Tarjan's SCC) on LeetCode Medium/Hard.",
            "Master Dynamic Programming state transitions and space-optimization techniques.",
            "Study distributed caching, load balancing, and rate limiting for architectural rounds.",
            "Prepare STAR format stories reflecting Google values: navigating ambiguity, collaborative leadership, and technical ownership."
        ],
        "skill_gaps": [
            {"skill": "Graph Algorithms & Trees", "gap": "Google technical loops heavily test complex graph traversals, shortest path, and tree optimizations.", "priority": 1},
            {"skill": "Dynamic Programming", "gap": "High probability of 2D/3D DP and state machine questions requiring sub-quadratic time optimization.", "priority": 1},
            {"skill": "System Scalability & Concurrency", "gap": "Expectation to discuss concurrency models, locking strategies, and scalable distributed architectures.", "priority": 2},
            {"skill": "Googleyness & Behavioral Leadership", "gap": "Behavioral round focuses on navigating ambiguous scenarios and constructive peer collaboration.", "priority": 2},
        ],
        "phases": [
            {
                "phase_name": "Phase 1: Core Algorithms & Advanced Data Structures",
                "weeks": "Weeks 1-2",
                "tasks": [
                    {"title": "Trees & Graph Traversals", "description": "Implement BFS, DFS, Dijkstra, and Topological Sort. Solve 10 LeetCode graph problems.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Heaps, Tries & Custom Hash Tables", "description": "Build a Trie from scratch and solve Top-K frequent elements problems.", "priority": 2, "due_date": "Week 1"},
                    {"title": "Bit Manipulation & Binary Search Variants", "description": "Master search in rotated sorted arrays, lower/upper bounds, and bitwise arithmetic.", "priority": 2, "due_date": "Week 2"},
                ]
            },
            {
                "phase_name": "Phase 2: Dynamic Programming & Optimization",
                "weeks": "Weeks 3-4",
                "tasks": [
                    {"title": "1D & 2D Dynamic Programming", "description": "Solve classic DP problems: Longest Common Subsequence, Knapsack, and Edit Distance.", "priority": 1, "due_date": "Week 3"},
                    {"title": "State Compression & Tree DP", "description": "Practice advanced DP on trees and bitmask representations.", "priority": 2, "due_date": "Week 4"},
                    {"title": "Sliding Window & Two Pointers Drills", "description": "Solve 8 medium/hard problems on variable-length sliding window and monotonically increasing queues.", "priority": 2, "due_date": "Week 4"},
                ]
            },
            {
                "phase_name": "Phase 3: System Design & Object Modeling",
                "weeks": "Weeks 5-6",
                "tasks": [
                    {"title": "Distributed Rate Limiter Design", "description": "Design a scalable rate limiter using Token Bucket and Redis distributed keys.", "priority": 1, "due_date": "Week 5"},
                    {"title": "Scalable URL Shortener / Pastebin", "description": "Architect database partitioning, caching layers, and unique ID generation (Snowflake).", "priority": 2, "due_date": "Week 6"},
                    {"title": "Concurrency & Thread Safety", "description": "Deep dive into mutexes, race conditions, atomic variables, and deadlock avoidance.", "priority": 2, "due_date": "Week 6"},
                ]
            },
            {
                "phase_name": "Phase 4: Full Loop Mock Interviews & Behavioral",
                "weeks": "Weeks 7-8",
                "tasks": [
                    {"title": "Timed Mock Interview: DSA Hard Loop", "description": "Complete a 45-minute timed mock interview under strict asymptotic constraints.", "priority": 1, "due_date": "Week 7"},
                    {"title": "Googleyness & Conflict Resolution Practice", "description": "Draft and rehearse 5 behavioral stories demonstrating resilience, empathy, and intellectual humility.", "priority": 2, "due_date": "Week 8"},
                    {"title": "Final Placement Readiness Audit", "description": "Review all past interview weaknesses, cheat sheets, and time-management strategies.", "priority": 1, "due_date": "Week 8"},
                ]
            }
        ]
    },
    "Amazon": {
        "title": "Amazon SDE Placement Mastery Roadmap",
        "summary": "Structured 8-week roadmap emphasizing Tree/Heap problem solving, Low/High-Level System Design, and the 16 Amazon Leadership Principles.",
        "company_type": "Product-based",
        "recommendations": [
            "Focus on Trees, Heaps, Hash Tables, and String Parsing.",
            "Tie all project experiences to Amazon Leadership Principles (Customer Obsession, Ownership, Bias for Action, Dive Deep).",
            "Prepare LLD (Low-Level Design) class diagrams for modular software components.",
            "Practice explaining time/space complexity before writing any code."
        ],
        "skill_gaps": [
            {"skill": "Trees, Heaps & Priority Queues", "gap": "Amazon technical rounds frequently feature BSTs, lowest common ancestor, and priority queue streaming.", "priority": 1},
            {"skill": "Low-Level System Design (LLD)", "gap": "Expectation to produce clean OOP class hierarchies and design patterns for real-world services.", "priority": 1},
            {"skill": "Amazon Leadership Principles", "gap": "Every interview round evaluates behavioral fit using specific leadership competencies.", "priority": 1},
            {"skill": "Database Schema & Indexing", "gap": "Need deep knowledge of relational vs NoSQL trade-offs for high-throughput ecommerce use cases.", "priority": 2},
        ],
        "phases": [
            {
                "phase_name": "Phase 1: Core DSA & Amazon Frequent Patterns",
                "weeks": "Weeks 1-2",
                "tasks": [
                    {"title": "Binary Trees, BST & Serialization", "description": "Practice lowest common ancestor, tree serialization/deserialization, and boundary views.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Heaps & Top-K Streaming", "description": "Implement median finder in a data stream using two heaps (min-heap and max-heap).", "priority": 1, "due_date": "Week 1"},
                    {"title": "Graphs & BFS Grid Exploration", "description": "Solve rotting oranges, number of islands, and word ladder problems.", "priority": 2, "due_date": "Week 2"},
                ]
            },
            {
                "phase_name": "Phase 2: Low-Level Design & Clean Architecture",
                "weeks": "Weeks 3-4",
                "tasks": [
                    {"title": "Design Locker / Amazon Delivery Hub", "description": "Create modular OOP models and state machine for automated package lockers.", "priority": 1, "due_date": "Week 3"},
                    {"title": "Design Parking Lot & Design Patterns", "description": "Apply Factory, Singleton, and Strategy design patterns in clean, extensible code.", "priority": 2, "due_date": "Week 4"},
                    {"title": "Dynamic Programming Fundamentals", "description": "Master Coin Change, Word Break, and Longest Increasing Subsequence.", "priority": 2, "due_date": "Week 4"},
                ]
            },
            {
                "phase_name": "Phase 3: High-Level Architecture & Leadership Principles",
                "weeks": "Weeks 5-6",
                "tasks": [
                    {"title": "Leadership Principles STAR Stories", "description": "Formulate 2 concrete STAR examples for each of the top 8 Amazon Leadership Principles.", "priority": 1, "due_date": "Week 5"},
                    {"title": "High-Level Design: Shopping Cart & Checkout", "description": "Architect transactional inventory reservation, payment idempotency, and asynchronous notifications.", "priority": 1, "due_date": "Week 6"},
                    {"title": "NoSQL vs Relational Storage Trade-offs", "description": "Analyze DynamoDB single-table design vs PostgreSQL ACID transactions.", "priority": 2, "due_date": "Week 6"},
                ]
            },
            {
                "phase_name": "Phase 4: Bar Raiser & Full Mock Loops",
                "weeks": "Weeks 7-8",
                "tasks": [
                    {"title": "Bar Raiser Mock Interview", "description": "Simulate deep-dive behavioral drill challenging past trade-offs, failures, and ownership.", "priority": 1, "due_date": "Week 7"},
                    {"title": "Live Coding Speed & Edge Case Drills", "description": "Complete 5 medium problems with 100% test case coverage in under 25 minutes each.", "priority": 2, "due_date": "Week 8"},
                    {"title": "Final Placement Readiness Audit", "description": "Complete self-assessment checklist across all rounds.", "priority": 1, "due_date": "Week 8"},
                ]
            }
        ]
    },
    "Microsoft": {
        "title": "Microsoft SDE Placement Mastery Roadmap",
        "summary": "Targeted 8-week preparation plan covering Core CS fundamentals, Linked Lists, Trees, Clean Code refactoring, and Azure cloud/distributed basics.",
        "company_type": "Product-based",
        "recommendations": [
            "Focus on clean code readability, edge cases, and modular functions.",
            "Master Linked Lists, Trees, String Parsing, and OS/Threading fundamentals.",
            "Demonstrate a growth mindset and ability to receive feedback during technical discussions.",
            "Review RESTful API design, database normalization, and asynchronous design patterns."
        ],
        "skill_gaps": [
            {"skill": "Data Structures & Clean Code", "gap": "Microsoft prioritizes readable, production-grade code with zero memory leaks and proper naming.", "priority": 1},
            {"skill": "Operating Systems & Memory Management", "gap": "Technical interviewers frequently probe memory paging, virtual memory, threads, and concurrency.", "priority": 2},
            {"skill": "Object-Oriented System Modeling", "gap": "Ability to design maintainable enterprise modules with clear interfaces and separation of concerns.", "priority": 1},
            {"skill": "Growth Mindset & Collaboration", "gap": "Evaluated on how candidate responds to hints and approaches constructive critique.", "priority": 2},
        ],
        "phases": [
            {
                "phase_name": "Phase 1: Core Data Structures & String Drills",
                "weeks": "Weeks 1-2",
                "tasks": [
                    {"title": "Linked Lists & Pointer Manipulation", "description": "Implement reverse in K-groups, detect cycles, and merge K sorted lists.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Trees & Level-Order Traversals", "description": "Solve zig-zag level order, diameter of binary tree, and vertical order traversal.", "priority": 1, "due_date": "Week 1"},
                    {"title": "String Parsing & Recursion", "description": "Implement custom string atoi, evaluate mathematical expressions, and anagram grouping.", "priority": 2, "due_date": "Week 2"},
                ]
            },
            {
                "phase_name": "Phase 2: OS Fundamentals & Algorithmic Optimization",
                "weeks": "Weeks 3-4",
                "tasks": [
                    {"title": "OS Memory, Processes & Threads", "description": "Revise paging, thrashing, context switching, semaphores, and reader-writer problems.", "priority": 1, "due_date": "Week 3"},
                    {"title": "Dynamic Programming & Backtracking", "description": "Solve N-Queens, Sudoku Solver, and subset sum partitions.", "priority": 2, "due_date": "Week 4"},
                    {"title": "DBMS Normalization & Indexing Internals", "description": "Deep dive into B-Trees, 1NF to BCNF normalization, and query explain plans.", "priority": 2, "due_date": "Week 4"},
                ]
            },
            {
                "phase_name": "Phase 3: System Modeling & API Design",
                "weeks": "Weeks 5-6",
                "tasks": [
                    {"title": "Design a Distributed File Storage / OneDrive", "description": "Architect metadata service, chunk upload, deduplication, and synchronization.", "priority": 1, "due_date": "Week 5"},
                    {"title": "Clean Code & Refactoring Practices", "description": "Study SOLID principles and refactor complex legacy functions into clean modules.", "priority": 2, "due_date": "Week 6"},
                    {"title": "REST API & Microservice Integration", "description": "Design resilient REST endpoints with proper error schemas, idempotency, and telemetry.", "priority": 2, "due_date": "Week 6"},
                ]
            },
            {
                "phase_name": "Phase 4: Hiring Manager Simulation & Culture Fit",
                "weeks": "Weeks 7-8",
                "tasks": [
                    {"title": "Technical Loop Simulation", "description": "Conduct 2 mock technical interviews with interactive whiteboard problem solving.", "priority": 1, "due_date": "Week 7"},
                    {"title": "Growth Mindset & Project Deep-Dive", "description": "Prepare detailed explanations of past technical architecture and continuous learning.", "priority": 2, "due_date": "Week 8"},
                    {"title": "Final Placement Readiness Audit", "description": "Review all key topics and ensure peak readiness.", "priority": 1, "due_date": "Week 8"},
                ]
            }
        ]
    },
    "Zoho": {
        "title": "Zoho Software Developer Placement Roadmap",
        "summary": "Specialized 8-week preparation focusing on pure coding without libraries, Low-Level System Design (LLD), Object-Oriented modeling, and core problem solving.",
        "company_type": "Product-based",
        "recommendations": [
            "Practice solving complex matrix and string problems without using standard library shortcuts.",
            "Master Low-Level Design (LLD): Call Taxi, Train Ticket Reservation, Splitwise, Bowling Alley.",
            "Write clean, modular code with classes, methods, and minimal global state.",
            "Strengthen OOP principles, Garbage Collection mechanics, and database relationship modeling."
        ],
        "skill_gaps": [
            {"skill": "Low-Level System Design (LLD)", "gap": "Zoho Round 2 exclusively tests building a fully functioning command-line application (e.g. Taxi Booking, Splitwise).", "priority": 1},
            {"skill": "Core Programming Without Libraries", "gap": "Round 1 requires manual string parsing, pattern printing, and array manipulation from scratch.", "priority": 1},
            {"skill": "OOP Design & Modular Code Structure", "gap": "Strong emphasis on class segregation, encapsulation, and exception handling.", "priority": 1},
            {"skill": "Database Schema & Relationships", "gap": "Round 3 technical interviews evaluate entity-relationship design and relational modeling.", "priority": 2},
        ],
        "phases": [
            {
                "phase_name": "Phase 1: Basic & Advanced Programming Drills",
                "weeks": "Weeks 1-2",
                "tasks": [
                    {"title": "Matrix & Spiral Manipulations", "description": "Write algorithms to rotate matrices, print spirals, and find path coordinates without built-in libraries.", "priority": 1, "due_date": "Week 1"},
                    {"title": "String Parsing & Pattern Printing", "description": "Implement substring search (KMP), Roman to Integer, and diamond/pyramid character patterns.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Array Rearrangement & Math Logic", "description": "Solve sliding max sum, merge overlapping intervals, and prime factorization.", "priority": 2, "due_date": "Week 2"},
                ]
            },
            {
                "phase_name": "Phase 2: Low-Level Design (LLD) Applications - Part 1",
                "weeks": "Weeks 3-4",
                "tasks": [
                    {"title": "LLD Project: Call Taxi Booking Application", "description": "Design classes for Customer, Taxi, Booking, and calculate pickup location nearest to customer.", "priority": 1, "due_date": "Week 3"},
                    {"title": "LLD Project: Railway Ticket Reservation System", "description": "Model Berths (Lower, Middle, Upper, RAC, Waiting List) with booking, cancellation, and chart display.", "priority": 1, "due_date": "Week 4"},
                    {"title": "OOP Refactoring & Class Responsibility", "description": "Refactor LLD code into clear Model-View-Controller or Service-Repository layers.", "priority": 2, "due_date": "Week 4"},
                ]
            },
            {
                "phase_name": "Phase 3: Low-Level Design (LLD) Applications - Part 2 & DB",
                "weeks": "Weeks 5-6",
                "tasks": [
                    {"title": "LLD Project: Expense Sharing / Splitwise", "description": "Implement exact, equal, and percentage splits with simplified balance debt settlement.", "priority": 1, "due_date": "Week 5"},
                    {"title": "LLD Project: Snake and Ladder / Board Game", "description": "Design modular board, player turns, dice roll, and game state management.", "priority": 2, "due_date": "Week 6"},
                    {"title": "Relational DB Schema for LLD Projects", "description": "Design SQL schemas with primary keys, foreign keys, and indexes for your LLD apps.", "priority": 2, "due_date": "Week 6"},
                ]
            },
            {
                "phase_name": "Phase 4: Advanced Technical HR & Logic Round",
                "weeks": "Weeks 7-8",
                "tasks": [
                    {"title": "Live 3-Hour LLD Coding Simulation", "description": "Build an end-to-end CLI booking application in 3 hours with 100% working test cases.", "priority": 1, "due_date": "Week 7"},
                    {"title": "Zoho Technical Culture & Problem Defense", "description": "Practice explaining your data structure choices and memory footprint to senior architects.", "priority": 2, "due_date": "Week 8"},
                    {"title": "Final Placement Readiness Audit", "description": "Complete full review of all LLD problem templates.", "priority": 1, "due_date": "Week 8"},
                ]
            }
        ]
    },
    "TCS": {
        "title": "TCS National Qualifier & Technical Flow Roadmap",
        "summary": "Comprehensive 8-week preparation focusing on Aptitude, Logical Reasoning, Core Computer Science (DBMS/SQL, OOPs), and Technical Interview rounds.",
        "company_type": "Service-based",
        "recommendations": [
            "Practice quantitative aptitude and logical reasoning daily (speed and accuracy).",
            "Master SQL queries: Joins, Aggregate functions, Subqueries, and GROUP BY/HAVING.",
            "Be prepared to explain your final year and academic projects thoroughly.",
            "Practice speaking English confidently during technical and HR interviews."
        ],
        "skill_gaps": [
            {"skill": "Quantitative Aptitude & Logic", "gap": "TCS NQT cutoff requires high accuracy in numerical ability, reasoning, and verbal logic.", "priority": 1},
            {"skill": "SQL & Relational Databases", "gap": "Technical interviewers consistently ask to write live SQL queries with Joins and GROUP BY.", "priority": 1},
            {"skill": "Core CS Fundamentals (OOP/OS)", "gap": "Must explain OOP 4 pillars, process vs thread, and memory management with clear examples.", "priority": 2},
            {"skill": "Project Walkthrough & Communication", "gap": "Crucial to explain project architecture, role, and troubleshooting steps smoothly.", "priority": 2},
        ],
        "phases": [
            {
                "phase_name": "Phase 1: Aptitude, Numerical Ability & Reasoning",
                "weeks": "Weeks 1-2",
                "tasks": [
                    {"title": "Quantitative Aptitude Speed Drills", "description": "Practice Time & Work, Speed Distance, Percentages, and Probability formulas.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Logical Reasoning & Series Patterns", "description": "Solve blood relations, coding-decoding, syllogisms, and seating arrangement puzzles.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Verbal Ability & Grammar Drills", "description": "Practice reading comprehension, error spotting, and sentence completion.", "priority": 2, "due_date": "Week 2"},
                ]
            },
            {
                "phase_name": "Phase 2: Foundational Coding & Array/String Logic",
                "weeks": "Weeks 2-4",
                "tasks": [
                    {"title": "TCS NQT Coding Questions (Part 1)", "description": "Solve palindrome, prime check, Armstrong numbers, matrix rotations, and GCD/LCM.", "priority": 1, "due_date": "Week 3"},
                    {"title": "TCS NQT Coding Questions (Part 2)", "description": "Solve Kadane's algorithm, find subarray with given sum, and remove duplicate elements.", "priority": 1, "due_date": "Week 4"},
                    {"title": "Basic Sorting & Searching", "description": "Implement Binary Search, Bubble Sort, Merge Sort, and analyze time complexities.", "priority": 2, "due_date": "Week 4"},
                ]
            },
            {
                "phase_name": "Phase 3: Core CS & SQL Query Mastery",
                "weeks": "Weeks 5-6",
                "tasks": [
                    {"title": "SQL Queries, Joins & Aggregations", "description": "Write queries for 2nd highest salary, Inner/Left/Right joins, and GROUP BY with HAVING.", "priority": 1, "due_date": "Week 5"},
                    {"title": "OOPs Concepts with Code Examples", "description": "Explain Abstraction, Encapsulation, Polymorphism, and Inheritance in Java/Python.", "priority": 1, "due_date": "Week 6"},
                    {"title": "Operating Systems & Networking Basics", "description": "Revise Deadlock conditions, Paging, OSI model 7 layers, and TCP vs UDP.", "priority": 2, "due_date": "Week 6"},
                ]
            },
            {
                "phase_name": "Phase 4: Mock Technical & HR Interview Rounds",
                "weeks": "Weeks 7-8",
                "tasks": [
                    {"title": "Project Explanation & Architecture Defense", "description": "Prepare a 3-minute pitch and deep-dive answers for your academic/portfolio project.", "priority": 1, "due_date": "Week 7"},
                    {"title": "HR & Managerial Scenario Handling", "description": "Practice answering 'Why TCS?', relocation preferences, and team conflict questions.", "priority": 2, "due_date": "Week 8"},
                    {"title": "Final Placement Readiness Audit", "description": "Take full NQT mock test and technical interview drill.", "priority": 1, "due_date": "Week 8"},
                ]
            }
        ]
    },
    "Infosys": {
        "title": "Infosys Specialist Programmer & SE Placement Roadmap",
        "summary": "8-week curriculum targeting algorithmic problem solving, Web & Database fundamentals, and behavioral presentation.",
        "company_type": "Service-based",
        "recommendations": [
            "Practice dynamic programming and greedy algorithms for Specialist Programmer (SP) roles.",
            "Thoroughly prepare web architecture, REST APIs, and database indexing fundamentals.",
            "Refine verbal communication and problem-solving explanation skills.",
            "Know your resume line by line, especially technologies mentioned in projects."
        ],
        "skill_gaps": [
            {"skill": "Algorithmic Problem Solving", "gap": "Infosys SP tests dynamic programming, graph coloring, and greedy heuristics.", "priority": 1},
            {"skill": "Database Indexing & SQL", "gap": "Understanding query execution plans and relational database optimization.", "priority": 1},
            {"skill": "Web Architecture & Protocols", "gap": "HTTP methods, status codes, RESTful API design, and client-server paradigm.", "priority": 2},
            {"skill": "Technical Communication", "gap": "Articulating logic clearly during technical explanation rounds.", "priority": 2},
        ],
        "phases": [
            {
                "phase_name": "Phase 1: Reasoning, Aptitude & Pseudocode Logic",
                "weeks": "Weeks 1-2",
                "tasks": [
                    {"title": "Infosys Pseudocode & Logic Puzzles", "description": "Practice predicting output for bitwise operations, recursion, and nested loops.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Numerical & Data Interpretation Drills", "description": "Solve charts, tables, speed math, and profit-loss aptitude problems.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Verbal Reasoning & Critical Thinking", "description": "Practice critical reasoning, paragraph summary, and grammar.", "priority": 2, "due_date": "Week 2"},
                ]
            },
            {
                "phase_name": "Phase 2: Data Structures & Algorithmic Drills",
                "weeks": "Weeks 3-4",
                "tasks": [
                    {"title": "Arrays, Strings & Sliding Window", "description": "Solve longest substring without repeating characters, trapping rain water, and 2-sum.", "priority": 1, "due_date": "Week 3"},
                    {"title": "Trees & Binary Search Trees", "description": "Practice binary tree paths, validation of BST, and tree depth calculations.", "priority": 1, "due_date": "Week 4"},
                    {"title": "Greedy Algorithms & Recursion", "description": "Solve Activity Selection, Fractional Knapsack, and subset generation.", "priority": 2, "due_date": "Week 4"},
                ]
            },
            {
                "phase_name": "Phase 3: Web, Database & OOP Architecture",
                "weeks": "Weeks 5-6",
                "tasks": [
                    {"title": "Relational Databases & SQL Queries", "description": "Practice complex joins, views, stored procedures, and index optimizations.", "priority": 1, "due_date": "Week 5"},
                    {"title": "Web Fundamentals & REST APIs", "description": "Revise HTTP vs HTTPS, REST design principles, JSON serialization, and status codes.", "priority": 2, "due_date": "Week 6"},
                    {"title": "Object-Oriented Design in Java/Python", "description": "Implement clean interfaces, abstract classes, and exception handling hierarchies.", "priority": 2, "due_date": "Week 6"},
                ]
            },
            {
                "phase_name": "Phase 4: Mock Technical & HR Rounds",
                "weeks": "Weeks 7-8",
                "tasks": [
                    {"title": "Live Mock Technical Interview", "description": "Conduct 45-minute technical session covering DSA, project questions, and SQL.", "priority": 1, "due_date": "Week 7"},
                    {"title": "HR & Fitment Interview Prep", "description": "Prepare responses for career goals, willingness to learn new tech stacks, and team collaboration.", "priority": 2, "due_date": "Week 8"},
                    {"title": "Final Placement Readiness Audit", "description": "Review cheat sheets, formula sheets, and top 50 Infosys interview questions.", "priority": 1, "due_date": "Week 8"},
                ]
            }
        ]
    },
    "Default": {
        "title": "Software Engineering Placement Mastery Roadmap",
        "summary": "Comprehensive 8-week placement preparation plan tailored to your target role, core data structures, system design, and placement interviews.",
        "company_type": "Product & Service",
        "recommendations": [
            "Strengthen Data Structures and Algorithms with daily coding practice.",
            "Master database modeling, SQL queries, and backend API concepts.",
            "Build and thoroughly document 2 impactful software projects on GitHub.",
            "Participate in mock interviews to build technical communication confidence."
        ],
        "skill_gaps": [
            {"skill": "Data Structures & Algorithms", "gap": "Core problem-solving foundation across arrays, strings, trees, and graphs.", "priority": 1},
            {"skill": "Database & SQL Mastery", "gap": "Writing optimal SQL queries and designing normalized relational databases.", "priority": 1},
            {"skill": "System Design & Architecture", "gap": "Structuring scalable, maintainable software systems with clean design patterns.", "priority": 2},
            {"skill": "Technical Interview Communication", "gap": "Explaining algorithmic approaches and architectural decisions clearly to interviewers.", "priority": 2},
        ],
        "phases": [
            {
                "phase_name": "Phase 1: Language Mastery & Core Data Structures",
                "weeks": "Weeks 1-2",
                "tasks": [
                    {"title": "Language Fundamentals & Standard Libraries", "description": "Master memory management, collections, and idiomatic patterns in your primary programming language.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Arrays, Strings & Hash Tables", "description": "Solve 15 essential problems on two pointers, frequency counting, and string manipulation.", "priority": 1, "due_date": "Week 1"},
                    {"title": "Linked Lists, Stacks & Queues", "description": "Implement custom stack, queue, and solve linked list reversal and cycle detection.", "priority": 2, "due_date": "Week 2"},
                ]
            },
            {
                "phase_name": "Phase 2: Trees, Graphs & Dynamic Programming",
                "weeks": "Weeks 3-4",
                "tasks": [
                    {"title": "Binary Trees & BST Traversals", "description": "Implement in-order, pre-order, post-order, and level-order traversals; solve tree validation.", "priority": 1, "due_date": "Week 3"},
                    {"title": "Graph Traversals (BFS & DFS)", "description": "Implement connected components, cycle detection, and shortest path in unweighted graphs.", "priority": 1, "due_date": "Week 4"},
                    {"title": "Dynamic Programming Fundamentals", "description": "Master memoization vs tabulation with classic 1D DP problems (Fibonacci, Climbing Stairs, House Robber).", "priority": 2, "due_date": "Week 4"},
                ]
            },
            {
                "phase_name": "Phase 3: Database, API Architecture & Design",
                "weeks": "Weeks 5-6",
                "tasks": [
                    {"title": "Relational Database Design & SQL Drills", "description": "Design normalized database tables, write complex multi-table joins, and study indexing.", "priority": 1, "due_date": "Week 5"},
                    {"title": "REST API Architecture & Web Concepts", "description": "Understand REST endpoints, authentication (JWT), error handling, and CORS.", "priority": 2, "due_date": "Week 6"},
                    {"title": "Object-Oriented Design & Design Patterns", "description": "Apply Factory, Singleton, and Observer design patterns to modular project components.", "priority": 2, "due_date": "Week 6"},
                ]
            },
            {
                "phase_name": "Phase 4: Mock Interviews, Projects & Placement Readiness",
                "weeks": "Weeks 7-8",
                "tasks": [
                    {"title": "Project Architecture & Resume Defense", "description": "Prepare detailed technical explanations for all projects listed on your resume.", "priority": 1, "due_date": "Week 7"},
                    {"title": "Full Loop Mock Technical Interview", "description": "Conduct timed mock interviews covering coding, CS fundamentals, and scenario handling.", "priority": 1, "due_date": "Week 8"},
                    {"title": "HR & Behavioral Story Crafting", "description": "Formulate STAR responses for leadership, conflict resolution, and career aspirations.", "priority": 2, "due_date": "Week 8"},
                ]
            }
        ]
    }
}


def get_or_create_skill(db: Session, skill_name: str) -> Skill:
    """Retrieve an existing Skill or create a new one."""
    skill = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill:
        skill = Skill(
            id=uuid.uuid4(),
            name=skill_name,
            description=f"Core competency in {skill_name}"
        )
        db.add(skill)
        db.flush()
    return skill


def generate_personalized_roadmap(
    db: Session,
    user_id: str,
    profile: StudentProfile | None
) -> dict[str, Any]:
    """
    Generate or regenerate a personalized roadmap, roadmap tasks, skill gaps,
    and progress tracking based on student profile, target company, role, skills,
    and past interview performance.
    """
    # 1. Determine Target Company and Template
    target_company = profile.target_company if profile and profile.target_company else "Default"
    target_role = profile.target_role if profile and profile.target_role else "Software Engineer"
    current_level = profile.current_level if profile and profile.current_level else "Intermediate"
    career_goal = profile.career_goal if profile and profile.career_goal else "Placement"

    # Find matching template
    template_key = "Default"
    for key in COMPANY_ROADMAP_TEMPLATES:
        if key.lower() == target_company.lower():
            template_key = key
            break

    template = COMPANY_ROADMAP_TEMPLATES[template_key]

    # 2. Check Interview Performance if available
    recent_sessions = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == user_id, InterviewSession.completed == True)
        .order_by(InterviewSession.created_at.desc())
        .limit(3)
        .all()
    )

    interview_weaknesses: list[str] = []
    avg_interview_score: float | None = None
    if recent_sessions:
        session_ids = [s.id for s in recent_sessions]
        feedbacks = db.query(InterviewFeedback).filter(InterviewFeedback.session_id.in_(session_ids)).all()
        for f in feedbacks:
            if f.weaknesses:
                interview_weaknesses.append(f.weaknesses)

    # 3. Create or Update Roadmap Entity
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == user_id).first()
    roadmap_title = f"{target_company} {target_role} Placement Roadmap" if target_company != "Default" else f"{target_role} Placement Roadmap"
    roadmap_summary = f"Personalized 8-week roadmap tailored for {target_company} ({target_role}) focusing on your target goal: '{career_goal}' at {current_level} proficiency."

    if roadmap:
        roadmap.title = roadmap_title
        roadmap.summary = roadmap_summary
        roadmap.profile_id = profile.id if profile else None
    else:
        roadmap = Roadmap(
            id=uuid.uuid4(),
            user_id=user_id,
            profile_id=profile.id if profile else None,
            title=roadmap_title,
            summary=roadmap_summary,
        )
        db.add(roadmap)
        db.flush()

    # 4. Clean existing tasks and recreate them based on personalized template
    db.query(RoadmapTask).filter(RoadmapTask.roadmap_id == roadmap.id).delete()

    created_tasks: list[RoadmapTask] = []
    task_order = 0
    for phase_idx, phase in enumerate(template["phases"]):
        for t in phase["tasks"]:
            task_order += 1
            task = RoadmapTask(
                id=uuid.uuid4(),
                roadmap_id=roadmap.id,
                title=t["title"],
                description=t["description"],
                completed=False,
                priority=t.get("priority", 1),
                due_date=t.get("due_date", f"Week {phase_idx * 2 + 1}"),
            )
            db.add(task)
            created_tasks.append(task)

    # If interview feedback identified specific weaknesses, add a targeted booster task
    if interview_weaknesses:
        booster_task = RoadmapTask(
            id=uuid.uuid4(),
            roadmap_id=roadmap.id,
            title="Post-Interview Weak Area Drill",
            description=f"Targeted review based on recent mock interview feedback: {interview_weaknesses[0][:120]}...",
            completed=False,
            priority=1,
            due_date="Week 8 (Booster)",
        )
        db.add(booster_task)
        created_tasks.append(booster_task)

    # 5. Populate Skill Gaps
    # Clear existing skill gaps for user to refresh with latest alignment
    db.query(SkillGap).filter(SkillGap.user_id == user_id).delete()

    created_skill_gaps: list[dict[str, Any]] = []
    for sg_data in template.get("skill_gaps", []):
        skill_obj = get_or_create_skill(db, sg_data["skill"])
        skill_gap = SkillGap(
            id=uuid.uuid4(),
            user_id=user_id,
            skill_id=skill_obj.id,
            gap_description=sg_data["gap"],
            priority=sg_data["priority"],
        )
        db.add(skill_gap)
        created_skill_gaps.append({
            "id": str(skill_gap.id),
            "skill_name": sg_data["skill"],
            "gap_description": sg_data["gap"],
            "priority": sg_data["priority"]
        })

    # 6. Initialize / Update Progress Entry
    progress = db.query(Progress).filter(Progress.user_id == user_id, Progress.category == "Roadmap").first()
    total_tasks = len(created_tasks)
    completed_count = 0
    score_percentage = 0.0
    xp_points = 0

    if not progress:
        progress = Progress(
            id=uuid.uuid4(),
            user_id=user_id,
            category="Roadmap",
            completed_count=completed_count,
            score=score_percentage,
            xp_points=xp_points,
            streak_days=1,
            last_activity=datetime.now(timezone.utc)
        )
        db.add(progress)
    else:
        progress.completed_count = completed_count
        progress.score = score_percentage
        progress.last_activity = datetime.now(timezone.utc)

    db.commit()
    db.refresh(roadmap)
    if progress:
        db.refresh(progress)

    return {
        "roadmap_id": str(roadmap.id),
        "title": roadmap.title,
        "summary": roadmap.summary,
        "target_company": target_company,
        "target_role": target_role,
        "current_phase": template["phases"][0]["phase_name"] if template["phases"] else "Phase 1",
        "company_recommendations": template.get("recommendations", []),
        "tasks": [
            {
                "id": str(t.id),
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "priority": t.priority,
                "due_date": t.due_date,
            }
            for t in created_tasks
        ],
        "skill_gaps": created_skill_gaps,
        "progress": {
            "completed_count": completed_count,
            "total_tasks": total_tasks,
            "completion_percentage": score_percentage,
            "xp_points": xp_points,
            "streak_days": progress.streak_days if progress else 1,
        }
    }


def get_user_roadmap_data(db: Session, user_id: str) -> dict[str, Any] | None:
    """Retrieve full roadmap, tasks, skill gaps, progress, and recommendations for a user."""
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == user_id).first()
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()

    if not roadmap:
        if not profile:
            return None
        # User has profile but roadmap not generated yet -> generate it!
        return generate_personalized_roadmap(db, user_id, profile)

    tasks = db.query(RoadmapTask).filter(RoadmapTask.roadmap_id == roadmap.id).order_by(RoadmapTask.created_at.asc()).all()
    skill_gaps_rows = db.query(SkillGap, Skill).join(Skill, SkillGap.skill_id == Skill.id).filter(SkillGap.user_id == user_id).all()
    progress = db.query(Progress).filter(Progress.user_id == user_id, Progress.category == "Roadmap").first()

    total_tasks = len(tasks)
    completed_count = sum(1 for t in tasks if t.completed)
    completion_percentage = round((completed_count / total_tasks * 100), 1) if total_tasks > 0 else 0.0
    xp_points = completed_count * 50

    target_company = profile.target_company if profile and profile.target_company else "Default"
    target_role = profile.target_role if profile and profile.target_role else "Software Engineer"

    # Match template recommendations
    template_key = "Default"
    for key in COMPANY_ROADMAP_TEMPLATES:
        if key.lower() == target_company.lower():
            template_key = key
            break
    template = COMPANY_ROADMAP_TEMPLATES[template_key]

    # Calculate current phase based on first uncompleted task
    first_uncompleted = next((t for t in tasks if not t.completed), None)
    current_phase = "Phase 1: Foundation"
    if first_uncompleted and first_uncompleted.due_date:
        dd = first_uncompleted.due_date
        if "Week 1" in dd or "Week 2" in dd:
            current_phase = template["phases"][0]["phase_name"] if len(template["phases"]) > 0 else "Phase 1"
        elif "Week 3" in dd or "Week 4" in dd:
            current_phase = template["phases"][1]["phase_name"] if len(template["phases"]) > 1 else "Phase 2"
        elif "Week 5" in dd or "Week 6" in dd:
            current_phase = template["phases"][2]["phase_name"] if len(template["phases"]) > 2 else "Phase 3"
        elif "Week 7" in dd or "Week 8" in dd:
            current_phase = template["phases"][3]["phase_name"] if len(template["phases"]) > 3 else "Phase 4"
        elif template["phases"]:
            current_phase = template["phases"][0]["phase_name"]
    elif template["phases"]:
        current_phase = "All Phases Completed!"

    # Calculate overall readiness score
    avg_score = db.query(func.avg(InterviewAnswer.score)).filter(
        InterviewAnswer.user_id == user_id, 
        InterviewAnswer.score.isnot(None)
    ).scalar()
    readiness_score = round(float(avg_score), 1) if avg_score else 0.0

    return {
        "roadmap_id": str(roadmap.id),
        "title": roadmap.title,
        "summary": roadmap.summary,
        "target_company": target_company,
        "target_role": target_role,
        "current_phase": current_phase,
        "company_recommendations": template.get("recommendations", []),
        "tasks": [
            {
                "id": str(t.id),
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "priority": t.priority,
                "due_date": t.due_date,
            }
            for t in tasks
        ],
        "skill_gaps": [
            {
                "id": str(gap.id),
                "skill_name": skill.name,
                "gap_description": gap.gap_description,
                "priority": gap.priority,
            }
            for gap, skill in skill_gaps_rows
        ],
        "progress": {
            "completed_count": completed_count,
            "total_tasks": total_tasks,
            "completion_percentage": completion_percentage,
            "xp_points": xp_points,
            "streak_days": progress.streak_days if progress else 1,
            "readiness_score": readiness_score,
        }
    }


def toggle_roadmap_task(db: Session, user_id: str, task_id: str) -> dict[str, Any]:
    """Toggle task completed status and update progress metrics."""
    task = db.query(RoadmapTask).filter(RoadmapTask.id == task_id).first()
    if not task:
        raise ValueError("Task not found")

    # Authorization check: verify task belongs to this user's roadmap
    roadmap = db.query(Roadmap).filter(Roadmap.id == task.roadmap_id, Roadmap.user_id == user_id).first()
    if not roadmap:
        raise PermissionError("Unauthorized to modify this task")

    # Toggle task status
    task.completed = not task.completed

    # Recalculate progress for the user
    all_tasks = db.query(RoadmapTask).filter(RoadmapTask.roadmap_id == roadmap.id).all()
    total_tasks = len(all_tasks)
    completed_count = sum(1 for t in all_tasks if t.completed)
    completion_percentage = round((completed_count / total_tasks * 100), 1) if total_tasks > 0 else 0.0
    xp_points = completed_count * 50

    progress = db.query(Progress).filter(Progress.user_id == user_id, Progress.category == "Roadmap").first()
    if not progress:
        progress = Progress(
            id=uuid.uuid4(),
            user_id=user_id,
            category="Roadmap",
            completed_count=completed_count,
            score=completion_percentage,
            xp_points=xp_points,
            streak_days=1,
            last_activity=datetime.now(timezone.utc)
        )
        db.add(progress)
    else:
        progress.completed_count = completed_count
        progress.score = completion_percentage
        progress.xp_points = xp_points
        progress.last_activity = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)
    db.refresh(progress)

    return {
        "task_id": str(task.id),
        "title": task.title,
        "completed": task.completed,
        "progress": {
            "completed_count": completed_count,
            "total_tasks": total_tasks,
            "completion_percentage": completion_percentage,
            "xp_points": xp_points,
            "streak_days": progress.streak_days,
            "readiness_score": 0.0,
        }
    }
