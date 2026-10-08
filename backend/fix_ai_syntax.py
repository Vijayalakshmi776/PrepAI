import os

# Create interview_ai.py cleanly
file_path = os.path.abspath("d:/PrepAi/backend/app/services/interview_ai.py")

with open(file_path, "w", encoding="utf-8") as f:
    f.write('''import json
import logging
import random
from typing import Any
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

# Curated company-specific and role-specific question banks for realistic PrepAI simulation
COMPANY_QUESTIONS: dict[str, dict[str, list[Any]]] = {
    "TCS": {
        "Aptitude": [
            {
                "prompt": "A train 240 meters in length crosses a telegraph post in 16 seconds. Calculate the speed of the train in kilometers per hour.",
                "options": ["54 km/h", "60 km/h", "45 km/h", "72 km/h"],
                "answer": "54 km/h"
            },
            {
                "prompt": "If 12 men or 18 women can complete a construction project in 14 days, how many days will 8 men and 16 women take to complete the same work?",
                "options": ["9 days", "10 days", "12 days", "8 days"],
                "answer": "9 days"
            },
            {
                "prompt": "In a code sequence, 'PREPARE' is coded as 'ERAPERP'. Using the identical permutation rule, how is 'SUCCESS' represented?",
                "options": ["SSECUS", "SSUCECS", "SSCUESC", "SUCCSEE"],
                "answer": "SSECUS"
            },
            {
                "prompt": "A jar contains 5 red marbles, 4 blue marbles, and 3 green marbles. If two marbles are drawn randomly without replacement, what is the probability that both are red?",
                "options": ["5/33", "1/6", "5/22", "1/11"],
                "answer": "5/33"
            },
            {
                "prompt": "A sum of money doubles itself at simple interest in 10 years. What is the rate of interest per annum?",
                "options": ["10%", "12%", "8%", "15%"],
                "answer": "10%"
            },
            {
                "prompt": "The average of 5 consecutive odd numbers is 27. What is the product of the lowest and highest number?",
                "options": ["713", "621", "759", "675"],
                "answer": "713"
            },
            {
                "prompt": "A vendor buys lemons at 6 for Rs 10 and sells them at 4 for Rs 10. Find his profit percentage.",
                "options": ["50%", "40%", "25%", "60%"],
                "answer": "50%"
            },
            {
                "prompt": "A train 150m long passes a bridge of length 250m in 20 seconds. What is the speed of the train in km/h?",
                "options": ["72 km/h", "54 km/h", "90 km/h", "60 km/h"],
                "answer": "72 km/h"
            },
            {
                "prompt": "The ratio of ages of A and B is 4:5. If the sum of their ages is 36 years, what will be the ratio of their ages after 4 years?",
                "options": ["5:6", "9:10", "4:5", "7:8"],
                "answer": "5:6"
            },
            {
                "prompt": "In how many different ways can the letters of the word 'TCS' be arranged?",
                "options": ["6", "3", "12", "9"],
                "answer": "6"
            },
            {
                "prompt": "A pipe can fill a tank in 15 hours. Due to a leak in the bottom, it is filled in 20 hours. If the tank is full, how much time will the leak take to empty it?",
                "options": ["60 hours", "45 hours", "30 hours", "50 hours"],
                "answer": "60 hours"
            },
            {
                "prompt": "If the radius of a circle is increased by 20%, by what percentage does its area increase?",
                "options": ["44%", "40%", "20%", "48%"],
                "answer": "44%"
            },
            {
                "prompt": "Find the missing number in the series: 3, 9, 27, 81, ?",
                "options": ["243", "162", "324", "216"],
                "answer": "243"
            },
            {
                "prompt": "Two cards are drawn from a standard deck of 52 cards. What is the probability that both are Kings?",
                "options": ["1/221", "1/169", "4/663", "1/13"],
                "answer": "1/221"
            },
            {
                "prompt": "A person covers a distance of 120 km at 40 km/h and returns at 60 km/h. What is his average speed for the whole journey?",
                "options": ["48 km/h", "50 km/h", "45 km/h", "52 km/h"],
                "answer": "48 km/h"
            }
        ],
        "Coding": [
            "Given an array of integers, find the contiguous subarray with the maximum sum (Kadane's Algorithm). Explain your approach and time/space complexity.",
            "Write a function to check if two strings are anagrams of each other in O(N) time complexity.",
            "Explain how a Hash Map handles collisions internally. Compare separate chaining versus open addressing.",
            "Given a singly linked list, write an algorithm to detect if a cycle exists and find the entry point of the cycle."
        ],
        "Technical": [
            "Explain the difference between call by value and call by reference in C/C++ or Java. How does stack versus heap memory allocation work?",
            "What are ACID properties in Database Management Systems? Explain each property using a real-world banking transaction.",
            "Explain the difference between WHERE and HAVING clauses in SQL with illustrative query examples.",
            "Explain the four fundamental principles of Object-Oriented Programming (OOP) and how polymorphism is achieved at runtime."
        ],
        "HR": [
            "Tell me about a challenging academic or team project. How did you resolve technical disagreements and align on decisions?",
            "Why do you want to join TCS, and how do you adapt to shifting project requirements and domain transitions?",
            "Describe a situation where you had to manage strict project deadlines while maintaining high engineering quality."
        ]
    },
    "Infosys": {
        "Aptitude": [
            {
                "prompt": "The average age of a team of 5 engineers increases by 2 years when a senior engineer replaces a member aged 24. What is the age of the new engineer?",
                "options": ["34", "32", "30", "36"],
                "answer": "34"
            },
            {
                "prompt": "A clock shows 3:40. What is the angle between the hour hand and the minute hand in degrees?",
                "options": ["130 degrees", "140 degrees", "120 degrees", "150 degrees"],
                "answer": "130 degrees"
            },
            {
                "prompt": "A shopkeeper marks goods 25% above cost price and allows a discount of 10% on the marked price. What is the net profit percentage?",
                "options": ["12.5%", "15%", "10%", "14%"],
                "answer": "12.5%"
            },
            {
                "prompt": "In Cryptarithmetic, if A + A + A = BA, what digit does A represent?",
                "options": ["5", "3", "7", "2"],
                "answer": "5"
            },
            {
                "prompt": "A boat goes 60 km downstream in 2 hours and 40 km upstream in 4 hours. What is the speed of the boat in still water?",
                "options": ["20 km/h", "15 km/h", "25 km/h", "18 km/h"],
                "answer": "20 km/h"
            },
            {
                "prompt": "A mixture of 40 liters contains 10% water. How many liters of water must be added to make the water content 20% in the new mixture?",
                "options": ["5 liters", "4 liters", "6 liters", "8 liters"],
                "answer": "5 liters"
            },
            {
                "prompt": "Three numbers are in the ratio 3:4:5. If the sum of their squares is 1250, what is the middle number?",
                "options": ["20", "15", "25", "30"],
                "answer": "20"
            },
            {
                "prompt": "If 15% of X is equal to 20% of Y, then what is the ratio X : Y?",
                "options": ["4:3", "3:4", "5:4", "2:3"],
                "answer": "4:3"
            },
            {
                "prompt": "Complete the logical series: 7, 10, 8, 11, 9, 12, ?",
                "options": ["10", "13", "11", "14"],
                "answer": "10"
            },
            {
                "prompt": "At what exact time between 4 and 5 o'clock will the hands of a clock coincide?",
                "options": ["21 9/11 min past 4", "20 min past 4", "22 min past 4", "21 5/11 min past 4"],
                "answer": "21 9/11 min past 4"
            },
            {
                "prompt": "What is the probability of drawing an Ace from a well-shuffled standard deck of 52 cards?",
                "options": ["1/13", "1/52", "4/13", "1/26"],
                "answer": "1/13"
            },
            {
                "prompt": "A is twice as efficient as B. If together they finish a job in 14 days, in how many days can A alone finish it?",
                "options": ["21 days", "28 days", "42 days", "35 days"],
                "answer": "21 days"
            },
            {
                "prompt": "A sum doubles itself at simple interest in 8 years. What is the annual interest rate?",
                "options": ["12.5%", "10%", "15%", "8%"],
                "answer": "12.5%"
            },
            {
                "prompt": "If 'INFOSYS' is coded as 'JOGPTZT' in a cipher, how is 'SYSTEM' coded under the same rule?",
                "options": ["TZTUEN", "TZTUFN", "UYTUEN", "SYTUEM"],
                "answer": "TZTUEN"
            },
            {
                "prompt": "The HCF of two numbers is 11 and their LCM is 693. If one of the numbers is 77, find the other number.",
                "options": ["99", "88", "121", "66"],
                "answer": "99"
            }
        ],
        "Coding": [
            "Implement an algorithm to find the first non-repeating character in a stream of characters in O(N) time.",
            "Explain Binary Search and how you would find the pivot element in a rotated sorted array.",
            "Write an efficient function to reverse words in a given sentence string without using auxiliary string arrays."
        ],
        "Technical": [
            "Explain the 4 fundamental pillars of Object-Oriented Programming (OOP) with real-world software examples.",
            "What is database indexing and how do B-Trees/B+ Trees improve query search performance?",
            "Explain the difference between synchronous and asynchronous operations in modern web applications."
        ],
        "HR": [
            "Describe a situation where you had to learn a new programming language or framework under a tight deadline.",
            "Where do you see yourself in 3 years in terms of technical growth and ownership at Infosys?"
        ]
    },
    "Zoho": {
        "Aptitude": [
            {
                "prompt": "Complete the logical series: 4, 18, 48, 100, 180, ?. Explain the underlying pattern.",
                "options": ["294", "252", "312", "216"],
                "answer": "294"
            },
            {
                "prompt": "Two pipes A and B can fill a tank in 20 and 30 minutes respectively. If both pipes are opened together, how long will it take to fill the tank?",
                "options": ["12 minutes", "15 minutes", "10 minutes", "25 minutes"],
                "answer": "12 minutes"
            },
            {
                "prompt": "If day before yesterday was Thursday, what day will it be 45 days from today?",
                "options": ["Tuesday", "Monday", "Wednesday", "Thursday"],
                "answer": "Tuesday"
            },
            {
                "prompt": "Find the greatest number that will divide 43, 91 and 183 so as to leave the same remainder in each case.",
                "options": ["4", "7", "9", "13"],
                "answer": "4"
            },
            {
                "prompt": "The population of a town increases by 5% annually. If the present population is 160,000, what will it be in 2 years?",
                "options": ["176,400", "175,000", "180,000", "172,000"],
                "answer": "176,400"
            },
            {
                "prompt": "How many unique permutations can be formed using all the letters of the word 'ZOHO'?",
                "options": ["12", "24", "6", "18"],
                "answer": "12"
            },
            {
                "prompt": "The cost price of 20 articles is the same as the selling price of x articles. If the profit is 25%, then the value of x is:",
                "options": ["16", "15", "18", "25"],
                "answer": "16"
            },
            {
                "prompt": "A train crosses a 120m long platform in 10 seconds and a telegraph post in 4 seconds. What is the speed of the train?",
                "options": ["72 km/h", "54 km/h", "60 km/h", "80 km/h"],
                "answer": "72 km/h"
            },
            {
                "prompt": "A clock strikes once at 1 o'clock, twice at 2 o'clock, thrice at 3 o'clock and so on. How many times will it strike in 24 hours?",
                "options": ["156", "78", "136", "196"],
                "answer": "156"
            },
            {
                "prompt": "Two numbers are respectively 20% and 50% more than a third number. The ratio of the two numbers is:",
                "options": ["4:5", "2:5", "3:5", "6:7"],
                "answer": "4:5"
            },
            {
                "prompt": "The sum of ages of 5 children born at intervals of 3 years each is 50 years. What is the age of the youngest child?",
                "options": ["4 years", "8 years", "10 years", "6 years"],
                "answer": "4 years"
            },
            {
                "prompt": "Walking at 3/4 of his usual speed, a person reaches his office 20 minutes late. What is his usual travel time?",
                "options": ["60 minutes", "45 minutes", "80 minutes", "30 minutes"],
                "answer": "60 minutes"
            },
            {
                "prompt": "Evaluate the mathematical expression: (256)^0.16 * (256)^0.09",
                "options": ["4", "16", "64", "2"],
                "answer": "4"
            },
            {
                "prompt": "How many 3-digit positive integers are completely divisible by 6?",
                "options": ["150", "149", "151", "160"],
                "answer": "150"
            },
            {
                "prompt": "A bag contains 6 red and 4 black balls. If 2 balls are drawn at random, what is the probability that both are red?",
                "options": ["1/3", "2/5", "1/2", "3/10"],
                "answer": "1/3"
            }
        ],
        "Coding": [
            "Write an algorithm to print a given N x M matrix in spiral order without using additional matrix memory.",
            "Given a string with nested parentheses and operators, evaluate if the expression is balanced and well-formed.",
            "Implement string multiplication for two arbitrarily large numerical strings without converting directly to standard integers."
        ],
        "Technical": [
            "Design the data models and core classes for a Call Taxi Booking application. What data structures would you use to assign nearest taxis?",
            "Explain how Garbage Collection works in memory management. What causes memory leaks in long-running applications?",
            "Explain the internal implementation of a Trie (Prefix Tree) and how it is used for auto-complete systems."
        ],
        "HR": [
            "Why do you prefer Zoho's engineering culture, and how do you approach self-directed problem solving without hand-holding?",
            "Describe a complex bug you solved independently. What debugging methodologies did you employ?"
        ]
    },
    "Google": {
        "Aptitude": [
            {
                "prompt": "You have 8 identical-looking balls where 1 is slightly heavier. Using a balance scale only 2 times, how do you find the heavier ball?",
                "options": ["Weigh 3 vs 3", "Weigh 4 vs 4", "Weigh 2 vs 2", "It's impossible"],
                "answer": "Weigh 3 vs 3"
            },
            {
                "prompt": "In a tournament with 64 teams playing single elimination, how many total matches are played to determine the champion?",
                "options": ["63 matches", "64 matches", "32 matches", "127 matches"],
                "answer": "63 matches"
            },
            {
                "prompt": "What is the expected number of fair coin tosses needed to get two consecutive heads?",
                "options": ["6", "4", "8", "5"],
                "answer": "6"
            },
            {
                "prompt": "In the Monty Hall problem with 3 doors, what is the probability of winning the prize if you switch your choice after a goat door is revealed?",
                "options": ["2/3", "1/2", "1/3", "3/4"],
                "answer": "2/3"
            },
            {
                "prompt": "In a room of 23 people, what is the approximate probability that at least two people share the same birthday?",
                "options": ["50.7%", "25.0%", "75.0%", "12.5%"],
                "answer": "50.7%"
            },
            {
                "prompt": "You have 1000 bottles of liquid and 1 is poisoned. What is the minimum number of test strips needed to identify the poisoned bottle in 1 test run?",
                "options": ["10", "100", "500", "50"],
                "answer": "10"
            },
            {
                "prompt": "Using two identical glass eggs on a 100-story building, what is the minimum number of drops needed in the worst case to find the highest safe floor?",
                "options": ["14 drops", "20 drops", "50 drops", "10 drops"],
                "answer": "14 drops"
            },
            {
                "prompt": "You have two ropes that each burn in exactly 60 minutes non-uniformly. How can you measure exactly 45 minutes?",
                "options": ["Light both ends of rope 1 and one end of rope 2", "Light one end of rope 1 only", "Cut rope 2 in half", "Light both ends of both ropes"],
                "answer": "Light both ends of rope 1 and one end of rope 2"
            },
            {
                "prompt": "An ant starts at a vertex of a 3D cube and moves along edges. How many distinct shortest paths of length 3 exist to the opposite vertex?",
                "options": ["6", "3", "12", "8"],
                "answer": "6"
            },
            {
                "prompt": "If 10 people in a room all shake hands with each other exactly once, how many handshakes occur in total?",
                "options": ["45", "90", "100", "50"],
                "answer": "45"
            },
            {
                "prompt": "What is the expected average score when rolling a single fair 6-sided die?",
                "options": ["3.5", "3.0", "4.0", "3.2"],
                "answer": "3.5"
            },
            {
                "prompt": "How many ways can a person climb a flight of 10 stairs taking either 1 or 2 steps at a time?",
                "options": ["89", "55", "144", "100"],
                "answer": "89"
            },
            {
                "prompt": "What is the acute angle between the hour hand and minute hand of a clock at 3:15?",
                "options": ["7.5 degrees", "0 degrees", "15 degrees", "11.25 degrees"],
                "answer": "7.5 degrees"
            },
            {
                "prompt": "In a binary search over 1,000,000 sorted elements, what is the maximum number of comparisons required?",
                "options": ["20", "10", "100", "1000"],
                "answer": "20"
            },
            {
                "prompt": "If a fair coin is flipped 4 times, what is the probability of getting exactly 2 heads?",
                "options": ["3/8", "1/2", "1/4", "5/8"],
                "answer": "3/8"
            }
        ],
        "Coding": [
            "Implement an algorithm to find the Median of Two Sorted Arrays in O(log(min(N,M))) time complexity.",
            "Given a stream of integers, design a data structure that efficiently retrieves the top K most frequent elements in O(1) or O(log K).",
            "Given a 2D grid representing a maze with obstacles, find the shortest path from start to target using BFS/A* search."
        ],
        "Technical": [
            "Given a large directed graph representing web page links, design an algorithm to find strongly connected components and detect cycles.",
            "Design a distributed rate limiter that supports millions of requests per second with low latency.",
            "Explain how you would optimize a dynamic programming solution from O(N^2) time or space to O(N)."
        ],
        "HR": [
            "Tell me about a time you identified an architectural flaw or performance bottleneck in a project and navigated the solution.",
            "How do you handle ambiguity when system requirements are incomplete or subject to rapid change?"
        ]
    },
    "Amazon": {
        "Aptitude": [
            {
                "prompt": "A warehouse processes 1,200 packages per hour with 8 robots. If 4 more robots of equal efficiency are added, how many packages are processed in 5 hours?",
                "options": ["9,000", "7,500", "8,400", "10,200"],
                "answer": "9,000"
            },
            {
                "prompt": "What is the probability of getting at least one 6 when rolling three fair 6-sided dice simultaneously?",
                "options": ["91/216", "1/2", "125/216", "1/6"],
                "answer": "91/216"
            },
            {
                "prompt": "A trader buys items at Rs 80 per dozen and sells them in packs of 8 for Rs 70. What is the percentage profit or loss?",
                "options": ["31.25% Profit", "25% Profit", "18.75% Loss", "42% Profit"],
                "answer": "31.25% Profit"
            },
            {
                "prompt": "Given 5 customer order delivery intervals, what is the minimum number of delivery trucks needed if max overlapping concurrent intervals is 3?",
                "options": ["3", "4", "2", "5"],
                "answer": "3"
            },
            {
                "prompt": "If 6 workers can pack 6 items in 6 hours, how many hours will 12 workers take to pack 12 items?",
                "options": ["6 hours", "12 hours", "3 hours", "1 hour"],
                "answer": "6 hours"
            },
            {
                "prompt": "An express shipping fee of $50 is discounted to $35 for Prime members. What is the percentage reduction?",
                "options": ["30%", "25%", "35%", "20%"],
                "answer": "30%"
            },
            {
                "prompt": "The average weight of 5 shipment boxes is 12 kg. If a 6th box weighing 18 kg is added, what is the new average weight?",
                "options": ["13 kg", "14 kg", "12.5 kg", "15 kg"],
                "answer": "13 kg"
            },
            {
                "prompt": "If the length of a storage container is doubled, width tripled, and height halved, by what factor does the volume change?",
                "options": ["3 times", "6 times", "2 times", "4 times"],
                "answer": "3 times"
            },
            {
                "prompt": "A fulfillment center has Cost of Goods Sold equal to $500,000 and average inventory of $100,000. Calculate the Inventory Turnover Ratio.",
                "options": ["5.0", "4.0", "6.0", "2.5"],
                "answer": "5.0"
            },
            {
                "prompt": "A robot battery depletes from 100% to 20% in 4 hours of continuous operation. What is the depletion rate per hour?",
                "options": ["20%", "25%", "15%", "18%"],
                "answer": "20%"
            },
            {
                "prompt": "A delivery vehicle drives 40 km at 40 km/h and returns along the same route at 60 km/h. What is its average speed for the round trip?",
                "options": ["48 km/h", "50 km/h", "45 km/h", "52 km/h"],
                "answer": "48 km/h"
            },
            {
                "prompt": "In a batch of 1,000 manufactured items, 2% are found defective. How many non-defective items are present?",
                "options": ["980", "950", "990", "970"],
                "answer": "980"
            },
            {
                "prompt": "An order processing center targets 95% SLA compliance. If 475 out of 500 orders are delivered on time, what is the achieved SLA percentage?",
                "options": ["95%", "90%", "96%", "92%"],
                "answer": "95%"
            },
            {
                "prompt": "Route A takes 30 minutes. Route B takes 25 minutes but incurs a $2 toll. What is the time saved per toll dollar using Route B?",
                "options": ["2.5 minutes/$", "5 minutes/$", "2 minutes/$", "3 minutes/$"],
                "answer": "2.5 minutes/$"
            },
            {
                "prompt": "Out of 200 customer returns, 10 items were damaged in transit. What percentage of returns were damaged?",
                "options": ["5%", "10%", "2.5%", "4%"],
                "answer": "5%"
            }
        ],
        "Coding": [
            "Given a list of customer orders with delivery deadlines, find the minimum number of delivery trucks needed (Interval Scheduling).",
            "Implement LRU (Least Recently Used) Cache with O(1) get and put operations.",
            "Given a binary tree, serialize and deserialize it efficiently into a compact string representation."
        ],
        "Technical": [
            "Design a URL shortening service (like TinyURL) that handles 100M new URLs per month with 99.99% availability.",
            "Explain how Amazon's DynamoDB achieves high availability and eventual consistency using vector clocks and consistent hashing.",
            "Design an inventory management service with idempotency to prevent overselling items during flash sales."
        ],
        "HR": [
            "Describe a situation where you had to demonstrate 'Customer Obsession' or 'Ownership' under tough constraints.",
            "Tell me about a time you made a decision with incomplete data (Bias for Action). What was the outcome?"
        ]
    },
    "Microsoft": {
        "Aptitude": [
            {
                "prompt": "A software build pipeline takes 45 minutes without caching. With caching, build time decreases by 60%. How much time is saved over 15 daily builds?",
                "options": ["405 minutes", "380 minutes", "450 minutes", "270 minutes"],
                "answer": "405 minutes"
            },
            {
                "prompt": "Find the missing number in the sequence: 2, 6, 12, 20, 30, 42, ?",
                "options": ["56", "54", "48", "60"],
                "answer": "56"
            },
            {
                "prompt": "If 5 servers can process 5,000 queries in 5 seconds, how many servers are needed to process 50,000 queries in 50 seconds?",
                "options": ["5", "10", "50", "25"],
                "answer": "5"
            },
            {
                "prompt": "The latencies of 5 network packets are 10ms, 12ms, 15ms, 8ms, and 15ms. What is the average packet latency?",
                "options": ["12 ms", "14 ms", "10 ms", "13 ms"],
                "answer": "12 ms"
            },
            {
                "prompt": "A 3 GHz processor completes an instruction in 6 clock cycles. What is the execution time of the instruction in nanoseconds?",
                "options": ["2 nanoseconds", "1 nanosecond", "3 nanoseconds", "0.5 nanoseconds"],
                "answer": "2 nanoseconds"
            },
            {
                "prompt": "In a virtual memory system with 4 KB page size, how many total pages exist in a 32-bit logical address space?",
                "options": ["1,048,576", "65,536", "512,000", "2,097,152"],
                "answer": "1,048,576"
            },
            {
                "prompt": "A thread queue has capacity 100. A producer adds 10 items/s and consumer removes 8 items/s. How long until the queue overflows?",
                "options": ["50 seconds", "40 seconds", "100 seconds", "25 seconds"],
                "answer": "50 seconds"
            },
            {
                "prompt": "What is the bitwise XOR result of the sequence: 1 ^ 2 ^ 3 ^ 4 ^ 5?",
                "options": ["1", "0", "7", "3"],
                "answer": "1"
            },
            {
                "prompt": "A CPU cache has 90% hit ratio with 2ns access time, and 10% miss ratio with 50ns RAM access time. Calculate the Average Memory Access Time (AMAT).",
                "options": ["6.8 ns", "5.0 ns", "7.2 ns", "10.0 ns"],
                "answer": "6.8 ns"
            },
            {
                "prompt": "How many total nodes are in a perfect binary tree of height 4 (root at height 0)?",
                "options": ["15", "16", "31", "7"],
                "answer": "15"
            },
            {
                "prompt": "If 2 cloud VMs handle 500 requests/sec, how many total VMs are required to scale to 2,000 requests/sec linearly?",
                "options": ["8", "6", "10", "4"],
                "answer": "8"
            },
            {
                "prompt": "A storage array achieves 5,000 IOPS with 4 KB block size per IO. What is the throughput in MB/s?",
                "options": ["20 MB/s", "25 MB/s", "10 MB/s", "40 MB/s"],
                "answer": "20 MB/s"
            },
            {
                "prompt": "What is the maximum recursion depth stack allocation for a balanced binary search tree with 65,535 nodes?",
                "options": ["16", "32", "64", "256"],
                "answer": "16"
            },
            {
                "prompt": "A file of size 100 MB is compressed to 25 MB. What is the compression ratio?",
                "options": ["4:1", "3:1", "2:1", "5:1"],
                "answer": "4:1"
            },
            {
                "prompt": "If 4 garbage collection pauses of 50ms occur during a 10-second server execution window, what is the GC overhead percentage?",
                "options": ["2%", "5%", "1%", "4%"],
                "answer": "2%"
            }
        ],
        "Coding": [
            "Find the lowest common ancestor (LCA) of two nodes in a binary search tree and in a general binary tree.",
            "Reverse nodes in k-group in a singly linked list in O(1) extra memory.",
            "Design an algorithm to find all unique triplets in an array that sum up to zero in O(N^2) time."
        ],
        "Technical": [
            "Explain how operating systems handle virtual memory, paging, and page fault resolution.",
            "Design a collaborative document editor like MS Word Online. How do you resolve concurrent conflicting edits (OT or CRDT)?",
            "What is the difference between monolithic, microservices, and serverless architectures in cloud design?"
        ],
        "HR": [
            "Tell me about a time you mentored a peer or led a complex technical initiative.",
            "How do you prioritize competing engineering tasks when everything is marked as high urgency?"
        ]
    },
    "Startup": {
        "Aptitude": [
            {
                "prompt": "A web service has a 99.9% uptime SLA. How many minutes of permissible downtime does this represent in a 30-day month?",
                "options": ["43.2", "45.0", "41.5", "50.4"],
                "answer": "43.2"
            },
            {
                "prompt": "If your server cost scales at $0.002 per API request and you expect 1.5M requests this month, calculate the estimated compute expense.",
                "options": ["$3,000", "$1,500", "$300", "$4,500"],
                "answer": "$3,000"
            },
            {
                "prompt": "A startup's user base grows 20% month-over-month. If current users are 10,000, what will be the count after 3 months?",
                "options": ["17,280", "16,000", "14,400", "18,500"],
                "answer": "17,280"
            },
            {
                "prompt": "If a startup spends $10,000 on marketing and acquires 200 new paying customers, what is the Customer Acquisition Cost (CAC)?",
                "options": ["$50", "$100", "$25", "$40"],
                "answer": "$50"
            },
            {
                "prompt": "A SaaS customer pays $20/month and stays subscribed for an average of 24 months. What is the Customer Lifetime Value (LTV)?",
                "options": ["$480", "$240", "$500", "$400"],
                "answer": "$480"
            },
            {
                "prompt": "What is the LTV : CAC ratio for a product with $480 LTV and $50 CAC?",
                "options": ["9.6:1", "4.8:1", "12.0:1", "5.0:1"],
                "answer": "9.6:1"
            },
            {
                "prompt": "A startup has $120,000 in bank balance and a net monthly burn rate of $15,000. How many months of runway remain?",
                "options": ["8 months", "10 months", "6 months", "12 months"],
                "answer": "8 months"
            },
            {
                "prompt": "A website receives 10,000 visitors, 500 sign up for a free trial, and 50 convert to paid plans. What is the overall visitor-to-paid conversion rate?",
                "options": ["0.5%", "5.0%", "1.0%", "2.0%"],
                "answer": "0.5%"
            },
            {
                "prompt": "An API rate limiter restricts requests to 100 per minute per IP address. What is the maximum allowed requests from an IP in 1 hour?",
                "options": ["6,000", "3,600", "1,000", "10,000"],
                "answer": "6,000"
            },
            {
                "prompt": "A database connection pool allows max 20 connections. If average query execution hold time is 50ms, what is the max theoretical QPS?",
                "options": ["400 QPS", "200 QPS", "500 QPS", "1000 QPS"],
                "answer": "400 QPS"
            },
            {
                "prompt": "If a microservice P50 response time is 20ms and P99 response time is 200ms, how many times slower is the P99 latency compared to P50?",
                "options": ["10x", "5x", "20x", "2x"],
                "answer": "10x"
            },
            {
                "prompt": "AWS S3 storage costs $0.023 per GB per month. What is the monthly storage cost for 500 GB of user uploads?",
                "options": ["$11.50", "$23.00", "$10.00", "$15.00"],
                "answer": "$11.50"
            },
            {
                "prompt": "Out of 2,000 active app users, 600 adopt a newly launched feature. What is the feature adoption rate?",
                "options": ["30%", "25%", "40%", "35%"],
                "answer": "30%"
            },
            {
                "prompt": "A startup begins a month with 1,000 active subscribers and loses 50 users by the end of the month. What is the monthly churn rate?",
                "options": ["5%", "10%", "2.5%", "4%"],
                "answer": "5%"
            },
            {
                "prompt": "An email campaign sends 5,000 emails, 1,000 are opened, and 200 links are clicked. What is the click-through rate (CTR) relative to total emails sent?",
                "options": ["4%", "20%", "10%", "2%"],
                "answer": "4%"
            }
        ],
        "Coding": [
            "Write a debouncing and throttling utility function and explain their differences in user interface event handling.",
            "Implement a function that deeply flattens a nested object / array structure with circular reference handling.",
            "Write a clean function to implement exponential backoff retry for network requests."
        ],
        "Technical": [
            "Design a RESTful / GraphQL API for an e-commerce checkout flow with idempotency keys to prevent double billing.",
            "How would you scale a web application backend from 1,000 to 100,000 active users? Where are the typical bottlenecks?",
            "Explain your testing strategy (Unit, Integration, End-to-End) and how CI/CD pipelines automate deployment."
        ],
        "HR": [
            "Why do you want to work in a high-velocity startup environment rather than an established enterprise?",
            "Tell me about a project where you took end-to-end ownership from design to deployment."
        ]
    }
}

GENERIC_QUESTIONS_BY_CATEGORY: dict[str, list[Any]] = {
    "Aptitude": [
        {
            "prompt": "A train 240 meters long passes a pole in 24 seconds. How long will it take to pass a platform 650 meters long?",
            "options": ["65 seconds", "89 seconds", "100 seconds", "120 seconds"],
            "answer": "89 seconds"
        },
        {
            "prompt": "If A can do a job in 10 days and B can do it in 15 days, in how many days will they finish working together?",
            "options": ["5 days", "6 days", "8 days", "9 days"],
            "answer": "6 days"
        },
        {
            "prompt": "Find the next number in the arithmetic-geometric progression: 3, 7, 15, 31, 63, ?",
            "options": ["115", "127", "131", "143"],
            "answer": "127"
        },
        {
            "prompt": "If 20% of a = b, then b% of 20 is the same as:",
            "options": ["4% of a", "5% of a", "20% of a", "None of the above"],
            "answer": "4% of a"
        },
        {
            "prompt": "Two numbers are respectively 20% and 50% more than a third number. The ratio of the two numbers is:",
            "options": ["2:5", "3:5", "4:5", "6:7"],
            "answer": "4:5"
        },
        {
            "prompt": "A clock strikes once at 1 o'clock, twice at 2 o'clock, thrice at 3 o'clock and so on. How many times will it strike in 24 hours?",
            "options": ["78", "136", "156", "196"],
            "answer": "156"
        },
        {
            "prompt": "The sum of ages of 5 children born at the intervals of 3 years each is 50 years. What is the age of the youngest child?",
            "options": ["4 years", "8 years", "10 years", "None of these"],
            "answer": "4 years"
        },
        {
            "prompt": "A person crosses a 600 m long street in 5 minutes. What is his speed in km per hour?",
            "options": ["3.6", "7.2", "8.4", "10"],
            "answer": "7.2"
        },
        {
            "prompt": "Find the greatest number that will divide 43, 91 and 183 so as to leave the same remainder in each case.",
            "options": ["4", "7", "9", "13"],
            "answer": "4"
        },
        {
            "prompt": "The cost price of 20 articles is the same as the selling price of x articles. If the profit is 25%, then the value of x is:",
            "options": ["15", "16", "18", "25"],
            "answer": "16"
        }
    ],
    "Coding": [
        "Given an array of integers, find two numbers such that they add up to a specific target sum in O(N) time.",
        "Implement a function to check if a binary tree is symmetric around its center.",
        "Write an algorithm to find the longest substring without repeating characters."
    ],
    "Technical": [
        "Explain the architectural components of your strongest technical project and the trade-offs you made.",
        "How do you approach debugging a high-latency issue in a database or API endpoint?",
        "Explain the difference between SQL (relational) and NoSQL databases, and when you would choose each."
    ],
    "HR": [
        "Tell me about a time you overcame a difficult technical hurdle under pressure.",
        "How do you prioritize multiple deadlines when collaborating with cross-functional teams?"
    ]
}

GENERIC_QUESTIONS = GENERIC_QUESTIONS_BY_CATEGORY["Technical"]


def resolve_round_category(round_title: str | None) -> str:
    """Categorizes a round title into Aptitude, Coding, Technical, or HR."""
    if not round_title:
        return "Aptitude"
    r_lower = round_title.lower()
    if r_lower.startswith("round 1") or "aptitude" in r_lower or "reasoning" in r_lower or "quantitative" in r_lower or "numerical" in r_lower:
        return "Aptitude"
    if "hr" in r_lower or "behavioral" in r_lower or "managerial" in r_lower or "culture" in r_lower or "leadership" in r_lower or "founder" in r_lower or "fit" in r_lower:
        return "HR"
    if "coding" in r_lower or "algorithm" in r_lower or "programming" in r_lower or "dsa" in r_lower:
        return "Coding"
    if "technical" in r_lower or "cs" in r_lower or "system" in r_lower or "design" in r_lower or "database" in r_lower:
        return "Technical"
    return "Technical"


def generate_interview_questions(
    company_name: str,
    role: str,
    difficulty: str,
    round_title: str | None = None,
    count: int = 3
) -> list[dict]:
    """Generates structured interview questions tailored for the specific company, role, round, and difficulty."""
    category = resolve_round_category(round_title)
    
    # Check if Gemini API is available for dynamic questions
    has_key = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "replace-with-gemini-key")
    logger.info(f"[GEMINI] API key configured: {has_key}")
    if has_key:

        model_name = "gemini-3.6-flash"
        logger.info(f"[GEMINI] model: {model_name}")
        logger.info(f"[GEMINI] {category.lower()} generation started")
        
        prompt = f"Generate {count} distinct interview questions for {company_name} {role} (Difficulty: {difficulty}). Round: {category}."
        if category == "Aptitude":
            prompt += " Output ONLY valid JSON containing an array of objects under the key 'questions'. Each question object must have exactly 4 keys: 'prompt' (the question text), 'question_type' (set to 'mcq'), 'options' (an array of exactly 4 strings), and 'correct_answer' (a string matching exactly one of the options). The questions must be mathematical or logical aptitude problems. ALL options must be completely distinct between different questions. Do NOT use generic placeholders like 'A', 'B', 'C', 'D'."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7, 
                "maxOutputTokens": 8192,
                "responseMimeType": "application/json"
            }
        }
        
        max_retries = 1
        
        for attempt in range(max_retries):
            try:
                res = httpx.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=12.0)
                logger.info(f"[GEMINI] HTTP status: {res.status_code}")
                
                if res.status_code == 503 or res.status_code == 429:
                    logger.warning(f"[GEMINI] Rate limited or unavailable (Status {res.status_code}). Using instant catalog fallback.")
                    break
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    logger.info(f"[GEMINI] raw output text: {text}")
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0].strip()
                    
                    try:
                        parsed = json.loads(text)
                    except json.JSONDecodeError as e:
                        logger.error(f"[GEMINI] JSON parsing failed. Text was: {text}")
                        raise e
                        
                    question_list = parsed.get("questions") if isinstance(parsed, dict) else parsed
                    
                    if isinstance(question_list, list) and len(question_list) >= count:
                        # Normalize output
                        normalized = []
                        seen_options_sets = []
                        for item in question_list[:count]:
                            if isinstance(item, str):
                                if not item.strip():
                                    raise ValueError("Empty prompt string")
                                normalized.append({"prompt": item, "question_type": "text", "options": None, "correct_answer": None})
                            elif isinstance(item, dict):
                                prompt_text = item.get("prompt", "").strip()
                                if not prompt_text:
                                    raise ValueError("Missing prompt in dictionary")
                                
                                if category == "Aptitude":
                                    options = item.get("options", [])
                                    correct_answer = str(item.get("correct_answer", item.get("answer", ""))).strip()
                                    
                                    if not isinstance(options, list) or len(options) != 4:
                                        raise ValueError("Options must be a list of exactly 4 items")
                                    
                                    cleaned_options = [str(opt).strip() for opt in options]
                                    if any(not opt for opt in cleaned_options):
                                        raise ValueError("Empty option string found")
                                    
                                    opts_set = frozenset(cleaned_options)
                                    if len(opts_set) != 4:
                                        raise ValueError("Options must be unique")
                                        
                                    if opts_set in seen_options_sets:
                                        raise ValueError("Options are being reused across multiple questions")
                                    seen_options_sets.append(opts_set)
                                    
                                    if not correct_answer:
                                        raise ValueError("Missing correct answer")
                                    if correct_answer not in cleaned_options:
                                        raise ValueError(f"Correct answer '{correct_answer}' does not match any option {cleaned_options}")
                                        
                                    if set(["a", "b", "c", "d"]).issubset(set([o.lower() for o in cleaned_options])):
                                        raise ValueError("Generic options [A, B, C, D] are not allowed")
                                        
                                    normalized.append({
                                        "prompt": prompt_text,
                                        "question_type": "mcq",
                                        "options": cleaned_options,
                                        "correct_answer": correct_answer
                                    })
                                else:
                                    normalized.append({
                                        "prompt": prompt_text,
                                        "question_type": "text",
                                        "options": None,
                                        "correct_answer": None
                                    })
                        logger.info("[GEMINI] generation succeeded")
                        logger.info(f"[GEMINI] generated questions: {json.dumps(normalized)}")
                        logger.info("[GEMINI] fallback used: false")
                        return normalized
                    else:
                        raise Exception(f"Gemini API Error {res.status_code}: {res.text}")
            except Exception as e:
                logger.warning(f"Gemini API dynamic generation fallback: {e}")
                logger.info("[GEMINI] generation failed")
        
    logger.info("[GEMINI] fallback used: true")
    # Heuristic & company pattern matching
    matched_company = None
    for name in COMPANY_QUESTIONS:
        if name.lower() in company_name.lower():
            matched_company = COMPANY_QUESTIONS[name]
            break

    if not matched_company:
        matched_company = COMPANY_QUESTIONS["Startup"]

    category_pool = list(matched_company.get(category, []))
    if not category_pool:
        category_pool = list(GENERIC_QUESTIONS_BY_CATEGORY.get(category, GENERIC_QUESTIONS))

    # Perform randomized sampling to guarantee fresh questions for every session
    # and prevent duplicate questions within the same session
    if len(category_pool) >= count:
        result = random.sample(category_pool, count)
    else:
        # Take all items in category_pool and complement from generic pool without duplicates
        result = list(category_pool)
        random.shuffle(result)
        fallback_pool = list(GENERIC_QUESTIONS_BY_CATEGORY.get(category, GENERIC_QUESTIONS))
        random.shuffle(fallback_pool)
        
        for item in fallback_pool:
            if len(result) >= count:
                break
            item_prompt = item if isinstance(item, str) else item.get("prompt")
            existing_prompts = [x if isinstance(x, str) else x.get("prompt") for x in result]
            if item_prompt not in existing_prompts:
                result.append(item)
                
    # Normalize fallback results
    normalized = []
    for item in result[:count]:
        if isinstance(item, str):
            normalized.append({"prompt": item, "question_type": "text", "options": None, "correct_answer": None})
        elif isinstance(item, dict):
            normalized.append({
                "prompt": item.get("prompt", ""),
                "question_type": item.get("question_type", "mcq").lower() if category == "Aptitude" else "text",
                "options": list(item.get("options")) if item.get("options") else None,
                "correct_answer": item.get("correct_answer", item.get("answer", None))
            })
    return normalized


def evaluate_answer(
    question_prompt: str,
    user_response: str,
    company_name: str,
    role: str,
    difficulty: str,
    round_title: str | None = None,
    question_type: str = "text",
    correct_answer: str | None = None
) -> tuple[int, str]:
    """
    Evaluates a single answer. Returns (score_0_to_100, feedback_text).
    """
    resp_text = user_response.strip()
    category = resolve_round_category(round_title)

    if question_type == "mcq":
        if correct_answer and resp_text.lower() == correct_answer.strip().lower():
            return (100, "Correct answer!")
        else:
            return (0, f"Incorrect. The correct answer was: {correct_answer}")

    word_count = len(resp_text.split())
    if word_count < 5:
        if category == "Coding":
            return (20, "Your response is too brief. Provide a structured explanation detailing your approach, implementation steps, and complexity analysis.")
        elif category == "Aptitude":
            return (20, "Your response is too brief. Provide the numerical answer and briefly explain your logic or formula.")
        elif category == "HR":
            return (20, "Your response is too brief. Provide a structured response highlighting your behavioral reasoning and communication.")
        else:
            return (20, "Your response is too brief. Provide a more detailed explanation covering technical accuracy and depth.")

    # Try Gemini if key is valid
    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "replace-with-gemini-key":
        try:
            eval_instructions = "Evaluate the answer."
            if category == "Aptitude":
                eval_instructions = "Evaluate based on correctness, logical reasoning, and numerical accuracy."
            elif category == "Coding":
                eval_instructions = "Evaluate based on correctness, logic, algorithm efficiency, and code quality."
            elif category == "Technical":
                eval_instructions = "Evaluate based on technical accuracy, depth, and clarity of explanation."
            elif category == "HR":
                eval_instructions = "Evaluate based on communication, clarity, relevance, and behavioral reasoning."

            prompt = (
                f"You are a hiring manager evaluating a mock interview answer for {company_name} ({role}, {difficulty} difficulty).\\n\\n"
                f"Question: {question_prompt}\\n"
                f"Candidate's Answer: {resp_text}\\n\\n"
                f"{eval_instructions} Return ONLY a JSON object in this format:\\n"
                f"{{\\"score\\": <integer 0-100>, \\"feedback\\": \\"<2-3 sentences of constructive critique highlighting strengths and missing key elements>\\"}}"
            )
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={settings.GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "maxOutputTokens": 400}
            }
            with httpx.Client(timeout=10.0) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0].strip()
                    parsed = json.loads(text)
                    return (int(parsed.get("score", 75)), str(parsed.get("feedback", "Good explanation with clear reasoning.")))
        except Exception as e:
            logger.warning(f"Gemini API answer evaluation fallback: {e}")

    # Robust reasoning evaluation
    score = 60
    feedback_parts = []

    # Depth scoring
    if word_count >= 50:
        score += 15
    elif word_count >= 25:
        score += 8

    # Category-specific keywords check
    if category == "Aptitude":
        keywords = ["calculate", "formula", "logic", "reasoning", "equation", "solve", "speed", "distance", "time", "rate", "probability", "ratio"]
        success_msg = "Solid reasoning and clear mathematical or logical approach."
        fail_msg = "Good start, but make sure to explicitly state your calculation steps or logical formula."
    elif category == "Coding":
        keywords = ["complexity", "time", "space", "o(", "algorithm", "trade-off", "example", "optimize", "structure", "scale", "handle", "memory", "database", "approach"]
        success_msg = "Solid technical explanation with awareness of core engineering principles and algorithmic trade-offs."
        fail_msg = "Good start, but make sure to explicitly state time/space complexity and trade-offs."
    elif category == "HR":
        keywords = ["experience", "team", "situation", "learned", "manager", "conflict", "collaborate", "impact", "result", "communication", "challenge"]
        success_msg = "Strong behavioral response with good examples of soft skills and impact."
        fail_msg = "Try to structure your answer using the STAR method (Situation, Task, Action, Result) to provide more concrete examples."
    else: # Technical
        keywords = ["architecture", "design", "pattern", "system", "component", "scalable", "database", "api", "flow", "integrate", "security", "framework"]
        success_msg = "Clear technical depth and good understanding of the subject matter."
        fail_msg = "Try to add more technical depth by mentioning specific patterns, frameworks, or architectural considerations."

    matched_kws = [kw for kw in keywords if kw in resp_text.lower()]
    score += min(20, len(matched_kws) * 4)

    if len(matched_kws) >= 3:
        feedback_parts.append(success_msg)
    else:
        feedback_parts.append(fail_msg)

    if word_count < 30:
        feedback_parts.append("Try expanding your answer to provide more detail.")
    else:
        feedback_parts.append("Clear structure and logical flow.")

    score = max(30, min(95, score))
    return (score, " ".join(feedback_parts))


def generate_session_summary(
    session_title: str,
    company_name: str,
    role: str,
    questions_and_answers: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Generates full session summary feedback.
    """
    total_answers = len(questions_and_answers)
    if total_answers == 0:
        return {
            "summary": f"Completed mock interview session for {company_name} as {role}.",
            "strengths": "Attempted the session setup.",
            "weaknesses": "No questions were answered during the interview.",
            "recommendations": "Complete all question prompts to get detailed AI feedback and score breakdown.",
            "overall_score": 0
        }

    # Calculate weighted categorical scores
    category_scores = {}
    category_counts = {}
    
    for qa in questions_and_answers:
        category = resolve_round_category(qa.get("round_title"))
        if category not in category_scores:
            category_scores[category] = 0
            category_counts[category] = 0
            
        category_counts[category] += 1
        category_scores[category] += qa.get("score", 0)

    categories_present = list(category_scores.keys())
    if categories_present:
        weight = 1.0 / len(categories_present)
        overall_score = 0
        for cat in categories_present:
            cat_avg = category_scores[cat] / category_counts[cat]
            overall_score += cat_avg * weight
        overall_score = int(round(overall_score))
    else:
        overall_score = 0

    summary = (
        f"You demonstrated promising readiness for {company_name}'s {role} interview round. "
        f"Overall evaluation score: {overall_score}%. Your answers exhibited good foundational skills."
    )

    categories_present = set()
    for qa in questions_and_answers:
        category = resolve_round_category(qa.get("round_title"))
        categories_present.add(category)

    strengths_list = ["• Structured thought process and clear conceptual clarity."]
    weaknesses_list = []
    recommendations_list = []

    if "Aptitude" in categories_present:
        strengths_list.append("• Good logic in quantitative reasoning.")
        weaknesses_list.append("• Ensure numerical calculations are explicitly stated.")
        recommendations_list.append("- Practice mathematical pacing and shortcut formulas.")
    if "Coding" in categories_present:
        strengths_list.append("• Good alignment with standard algorithmic practices.")
        weaknesses_list.append("• In-depth edge case analysis and asymptotic complexity optimization could be elaborated further.")
        recommendations_list.append("- State Time and Space complexity at the very beginning of your coding solutions.")
    if "Technical" in categories_present:
        strengths_list.append("• Effective communication of core engineering ideas and approaches.")
        weaknesses_list.append("• System trade-offs and alternative architectural designs can be compared more explicitly.")
        recommendations_list.append("- Compare different technical patterns directly when asked system design questions.")
    if "HR" in categories_present:
        strengths_list.append("• Strong behavioral communication and cultural alignment.")
        weaknesses_list.append("• Experiences could be tied more strongly to concrete outcomes.")
        recommendations_list.append("- Use the STAR method to structure your behavioral responses.")
        
    if not weaknesses_list:
        weaknesses_list.append("• Answers can generally be expanded for more depth.")
    if not recommendations_list:
        recommendations_list.append("- Continue practicing to improve detail and confidence.")

    strengths = "\\n".join(strengths_list)
    weaknesses = "\\n".join(weaknesses_list)
    recommendations = "\\n".join(recommendations_list)

    return {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "overall_score": overall_score
    }
''')

print("Successfully written interview_ai.py cleanly!")
