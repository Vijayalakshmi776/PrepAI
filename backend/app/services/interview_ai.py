import json
import logging
import random
from typing import Any
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

# Curated company-specific and role-specific question banks for realistic PrepAI simulation
# Structured by Company -> Category (Aptitude, Coding, Technical, HR) -> Difficulty (Easy, Medium, Hard)
COMPANY_QUESTIONS: dict[str, dict[str, dict[str, list[Any]] | list[Any]]] = {
    "TCS": {
        "Aptitude": {
            "Easy": [
                {
                    "prompt": "Find the missing number in the sequence: 3, 9, 27, 81, ?",
                    "options": ["243", "162", "324", "216"],
                    "answer": "243"
                },
                {
                    "prompt": "In how many different ways can the letters of the word 'TCS' be arranged?",
                    "options": ["6", "3", "12", "9"],
                    "answer": "6"
                },
                {
                    "prompt": "A sum of money doubles itself at simple interest in 10 years. What is the rate of interest per annum?",
                    "options": ["10%", "12%", "8%", "15%"],
                    "answer": "10%"
                },
                {
                    "prompt": "A vendor buys lemons at 6 for Rs 10 and sells them at 4 for Rs 10. Find his profit percentage.",
                    "options": ["50%", "40%", "25%", "60%"],
                    "answer": "50%"
                },
                {
                    "prompt": "The ratio of ages of A and B is 4:5. If the sum of their ages is 36 years, what will be the ratio of their ages after 4 years?",
                    "options": ["5:6", "9:10", "4:5", "7:8"],
                    "answer": "5:6"
                },
                {
                    "prompt": "A person crosses a 600 m long street in 5 minutes. What is his speed in kilometers per hour?",
                    "options": ["7.2 km/h", "8.4 km/h", "6.0 km/h", "9.6 km/h"],
                    "answer": "7.2 km/h"
                },
                {
                    "prompt": "If 20% of a number is 50, what is 50% of that number?",
                    "options": ["125", "100", "150", "200"],
                    "answer": "125"
                },
                {
                    "prompt": "What is the average of the first 5 prime numbers?",
                    "options": ["5.6", "5.0", "5.4", "6.2"],
                    "answer": "5.6"
                },
                {
                    "prompt": "If the cost price of an article is Rs 200 and selling price is Rs 250, find the profit percentage.",
                    "options": ["25%", "20%", "30%", "15%"],
                    "answer": "25%"
                },
                {
                    "prompt": "If a day before yesterday was Tuesday, what day will it be tomorrow?",
                    "options": ["Friday", "Thursday", "Saturday", "Wednesday"],
                    "answer": "Friday"
                }
            ],
            "Medium": [
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
                    "prompt": "The average of 5 consecutive odd numbers is 27. What is the product of the lowest and highest number?",
                    "options": ["713", "621", "759", "675"],
                    "answer": "713"
                },
                {
                    "prompt": "A train 150m long passes a bridge of length 250m in 20 seconds. What is the speed of the train in km/h?",
                    "options": ["72 km/h", "54 km/h", "90 km/h", "60 km/h"],
                    "answer": "72 km/h"
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
            "Hard": [
                {
                    "prompt": "A sum of money invested at compound interest amounts to Rs 4,608 in 2 years and Rs 5,529.60 in 3 years. Find the rate of interest per annum.",
                    "options": ["20%", "15%", "18%", "25%"],
                    "answer": "20%"
                },
                {
                    "prompt": "In how many ways can 5 men and 4 women be seated in a row so that the women always occupy the even places?",
                    "options": ["2880", "1440", "5760", "720"],
                    "answer": "2880"
                },
                {
                    "prompt": "A vessel is full of 80 liters of milk. 8 liters of milk is taken out and replaced by water. This process is repeated 2 more times. How much milk is now in the vessel?",
                    "options": ["58.32 liters", "60.40 liters", "55.80 liters", "62.10 liters"],
                    "answer": "58.32 liters"
                },
                {
                    "prompt": "A and B start a business with investments of Rs 50,000 and Rs 70,000 respectively. After 6 months, C joins with Rs 80,000. What is C's share in an annual profit of Rs 36,000?",
                    "options": ["Rs 8,000", "Rs 10,000", "Rs 12,000", "Rs 9,000"],
                    "answer": "Rs 8,000"
                },
                {
                    "prompt": "Two trains moving in opposite directions at 60 km/h and 90 km/h cross each other in 12 seconds. If the length of one train is 250 meters, what is the length of the other train?",
                    "options": ["250 meters", "300 meters", "200 meters", "350 meters"],
                    "answer": "250 meters"
                },
                {
                    "prompt": "Three pipes A, B and C can fill a reservoir in 6 hours together. After working together for 2 hours, C is closed and A and B can fill it in 7 hours. How long will C alone take to fill it?",
                    "options": ["14 hours", "12 hours", "16 hours", "10 hours"],
                    "answer": "14 hours"
                },
                {
                    "prompt": "Find the compound interest on Rs 10,000 at 10% per annum for 2.5 years, compounded annually.",
                    "options": ["Rs 2,705", "Rs 2,500", "Rs 2,850", "Rs 2,625"],
                    "answer": "Rs 2,705"
                },
                {
                    "prompt": "From a box containing 6 red balls and 4 green balls, 3 balls are drawn at random. What is the probability that at least 1 green ball is drawn?",
                    "options": ["5/6", "4/5", "3/4", "7/8"],
                    "answer": "5/6"
                },
                {
                    "prompt": "A work can be completed by 10 men in 12 days. They worked together for 4 days, then 2 more men joined. In how many days will the remaining work be finished?",
                    "options": ["6.67 days", "7 days", "5 days", "8 days"],
                    "answer": "6.67 days"
                },
                {
                    "prompt": "A trader marks his goods 40% above the cost price and allows a discount of 15% to retail customers and an additional 5% to wholesale buyers. What is the profit percentage on wholesale sales?",
                    "options": ["12.86%", "15.00%", "10.50%", "14.20%"],
                    "answer": "12.86%"
                }
            ]
        },
        "Coding": {
            "Easy": [
                "Write a function to check if a given string is a palindrome ignoring spaces and case.",
                "Given an array of integers, write a program to find the second largest element.",
                "Implement a program to count the number of vowels and consonants in a string."
            ],
            "Medium": [
                "Given an array of integers, find the contiguous subarray with the maximum sum (Kadane's Algorithm). Explain your approach and time/space complexity.",
                "Write a function to check if two strings are anagrams of each other in O(N) time complexity.",
                "Given a singly linked list, write an algorithm to detect if a cycle exists and find the entry point of the cycle."
            ],
            "Hard": [
                "Design and implement an LRU Cache with O(1) time complexity for get and put operations.",
                "Given a binary tree, write an algorithm to serialize and deserialize the tree structure efficiently.",
                "Solve the N-Queens problem and return all distinct solutions for an N x N chessboard."
            ]
        },
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
        "Aptitude": {
            "Easy": [
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
                    "prompt": "What is the probability of drawing an Ace from a well-shuffled standard deck of 52 cards?",
                    "options": ["1/13", "1/52", "4/13", "1/26"],
                    "answer": "1/13"
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
                },
                {
                    "prompt": "What is 25% of 80% of 500?",
                    "options": ["100", "80", "120", "150"],
                    "answer": "100"
                },
                {
                    "prompt": "A car travels 180 km in 3 hours. What is its speed in m/s?",
                    "options": ["16.67 m/s", "15 m/s", "20 m/s", "18 m/s"],
                    "answer": "16.67 m/s"
                },
                {
                    "prompt": "The average of 4 numbers is 20. If one number is removed, the average becomes 18. What was the removed number?",
                    "options": ["26", "24", "22", "28"],
                    "answer": "26"
                },
                {
                    "prompt": "A seller gains 20% by selling an item for Rs 600. What was its cost price?",
                    "options": ["Rs 500", "Rs 480", "Rs 520", "Rs 450"],
                    "answer": "Rs 500"
                }
            ],
            "Medium": [
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
                    "prompt": "At what exact time between 4 and 5 o'clock will the hands of a clock coincide?",
                    "options": ["21 9/11 min past 4", "20 min past 4", "22 min past 4", "21 5/11 min past 4"],
                    "answer": "21 9/11 min past 4"
                },
                {
                    "prompt": "A is twice as efficient as B. If together they finish a job in 14 days, in how many days can A alone finish it?",
                    "options": ["21 days", "28 days", "42 days", "35 days"],
                    "answer": "21 days"
                },
                {
                    "prompt": "A train 120 meters long passes a platform 180 meters long in 15 seconds. Find the speed of the train in km/h.",
                    "options": ["72 km/h", "60 km/h", "54 km/h", "80 km/h"],
                    "answer": "72 km/h"
                }
            ],
            "Hard": [
                {
                    "prompt": "A man can row 6 km/h in still water. If the river flows at 2 km/h, it takes him 3 hours to row to a place and back. How far is the place?",
                    "options": ["8 km", "6 km", "9 km", "7.5 km"],
                    "answer": "8 km"
                },
                {
                    "prompt": "How many 4-digit numbers can be formed using digits 1, 2, 3, 4, 5, 6 without repetition such that the number is divisible by 4?",
                    "options": ["96", "72", "120", "84"],
                    "answer": "96"
                },
                {
                    "prompt": "A bag contains 5 red, 6 yellow, and 4 green balls. 3 balls are drawn at random. What is the probability that all 3 are of different colors?",
                    "options": ["24/91", "12/91", "30/91", "18/91"],
                    "answer": "24/91"
                },
                {
                    "prompt": "The simple interest on a sum of money for 3 years at 12% per annum is Rs 3,600. What will be the compound interest on the same sum for 2 years at 10% per annum?",
                    "options": ["Rs 2,100", "Rs 2,000", "Rs 2,200", "Rs 1,950"],
                    "answer": "Rs 2,100"
                },
                {
                    "prompt": "A, B and C enter into a partnership. A invests 3 times as much as B, and B invests 2/3 of what C invests. Find the ratio of their profits.",
                    "options": ["6:2:3", "3:2:3", "2:1:3", "4:2:3"],
                    "answer": "6:2:3"
                },
                {
                    "prompt": "A clock gains 5 minutes every 3 hours. If it was set correctly at 8:00 AM, what will be the true time when the clock shows 6:00 PM on the same day?",
                    "options": ["5:45 PM", "5:30 PM", "5:50 PM", "5:40 PM"],
                    "answer": "5:45 PM"
                },
                {
                    "prompt": "Two workers A and B are paid Rs 1,120 per week in total. If A is paid 180% of what B is paid, how much is B paid per week?",
                    "options": ["Rs 400", "Rs 450", "Rs 500", "Rs 380"],
                    "answer": "Rs 400"
                },
                {
                    "prompt": "Find the unit digit in the expression: (7^95 - 3^58).",
                    "options": ["4", "0", "6", "2"],
                    "answer": "4"
                },
                {
                    "prompt": "If a card is drawn from a pack of 52 cards, what is the probability that it is either a King or a Heart?",
                    "options": ["4/13", "1/4", "16/52", "17/52"],
                    "answer": "4/13"
                },
                {
                    "prompt": "A merchant marks his goods up by 50% and then offers a discount of 20%. If he also uses a false weight of 900g instead of 1 kg, what is his actual profit percentage?",
                    "options": ["33.33%", "30.00%", "25.00%", "35.00%"],
                    "answer": "33.33%"
                }
            ]
        },
        "Coding": {
            "Easy": [
                "Write a function to count occurrences of each character in a string.",
                "Implement a program to check if an integer is a prime number.",
                "Write a function to find the maximum element in an array of numbers."
            ],
            "Medium": [
                "Implement an algorithm to find the first non-repeating character in a stream of characters in O(N) time.",
                "Explain Binary Search and how you would find the pivot element in a rotated sorted array.",
                "Write an efficient function to reverse words in a given sentence string without using auxiliary string arrays."
            ],
            "Hard": [
                "Given a 2D matrix, write a function to search for a target value in O(log(N*M)) time.",
                "Implement an algorithm to find the longest common substring between two strings.",
                "Design a data structure for Min Stack that supports push, pop, top, and retrieving minimum in O(1) time."
            ]
        },
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
        "Aptitude": {
            "Easy": [
                {
                    "prompt": "Two pipes A and B can fill a tank in 20 and 30 minutes respectively. If both pipes are opened together, how long will it take to fill the tank?",
                    "options": ["12 minutes", "15 minutes", "10 minutes", "25 minutes"],
                    "answer": "12 minutes"
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
                    "prompt": "If a number is increased by 10% and then decreased by 10%, what is the net percentage change?",
                    "options": ["1% decrease", "0% change", "1% increase", "2% decrease"],
                    "answer": "1% decrease"
                },
                {
                    "prompt": "What is the HCF of 36, 60, and 84?",
                    "options": ["12", "6", "24", "18"],
                    "answer": "12"
                },
                {
                    "prompt": "If 5 men can complete a painting job in 8 days, how many men are needed to finish it in 4 days?",
                    "options": ["10 men", "8 men", "12 men", "6 men"],
                    "answer": "10 men"
                }
            ],
            "Medium": [
                {
                    "prompt": "Complete the logical series: 4, 18, 48, 100, 180, ?. Explain the underlying pattern.",
                    "options": ["294", "252", "312", "216"],
                    "answer": "294"
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
                    "prompt": "Walking at 3/4 of his usual speed, a person reaches his office 20 minutes late. What is his usual travel time?",
                    "options": ["60 minutes", "45 minutes", "80 minutes", "30 minutes"],
                    "answer": "60 minutes"
                },
                {
                    "prompt": "A bag contains 6 red and 4 black balls. If 2 balls are drawn at random, what is the probability that both are red?",
                    "options": ["1/3", "2/5", "1/2", "3/10"],
                    "answer": "1/3"
                },
                {
                    "prompt": "The diagonal of a square is 8 cm. What is the area of the square?",
                    "options": ["32 sq cm", "64 sq cm", "16 sq cm", "48 sq cm"],
                    "answer": "32 sq cm"
                },
                {
                    "prompt": "A person buys an article for Rs 450 and spends Rs 50 on repairs. If he sells it for Rs 600, find his profit percentage.",
                    "options": ["20%", "25%", "15%", "30%"],
                    "answer": "20%"
                }
            ],
            "Hard": [
                {
                    "prompt": "A sum of money compounded annually doubles itself in 5 years. In how many years will it become 8 times itself at the same compound interest rate?",
                    "options": ["15 years", "10 years", "20 years", "12 years"],
                    "answer": "15 years"
                },
                {
                    "prompt": "In how many ways can 6 persons be seated around a circular table?",
                    "options": ["120", "720", "360", "240"],
                    "answer": "120"
                },
                {
                    "prompt": "A leak in the bottom of a tank can empty the full tank in 8 hours. An inlet pipe fills water at the rate of 6 liters a minute. When the tank is full, the inlet is opened and the tank is emptied in 12 hours. Find capacity of tank.",
                    "options": ["8,640 liters", "7,200 liters", "9,600 liters", "10,800 liters"],
                    "answer": "8,640 liters"
                },
                {
                    "prompt": "Find the sum of all two-digit numbers which leave a remainder of 1 when divided by 4.",
                    "options": ["1210", "1188", "1242", "1150"],
                    "answer": "1210"
                },
                {
                    "prompt": "A bag contains 3 white, 4 black, and 2 red balls. If 2 balls are drawn at random, what is the probability that neither is red?",
                    "options": ["7/12", "5/12", "2/3", "1/2"],
                    "answer": "7/12"
                },
                {
                    "prompt": "The average mark of 50 students in a class was calculated as 64. It was later discovered that a mark of 36 was misread as 86. What is the correct average mark?",
                    "options": ["63.0", "62.5", "63.5", "64.5"],
                    "answer": "63.0"
                },
                {
                    "prompt": "A container contains 50 liters of pure wine. 5 liters of wine is drawn out and replaced with water. This operation is performed twice more. What is the ratio of wine to water left in the container?",
                    "options": ["729:271", "800:200", "750:250", "640:360"],
                    "answer": "729:271"
                },
                {
                    "prompt": "Two trains of lengths 140m and 160m are running on parallel tracks in opposite directions at 60 km/h and 48 km/h. How many seconds will they take to cross each other?",
                    "options": ["10 seconds", "12 seconds", "8 seconds", "15 seconds"],
                    "answer": "10 seconds"
                },
                {
                    "prompt": "A and B together can complete a piece of work in 12 days. B and C together in 15 days, and C and A together in 20 days. How long will A alone take to finish the work?",
                    "options": ["30 days", "20 days", "40 days", "60 days"],
                    "answer": "30 days"
                },
                {
                    "prompt": "Find the remainder when 2^50 is divided by 7.",
                    "options": ["4", "2", "1", "3"],
                    "answer": "4"
                }
            ]
        },
        "Coding": {
            "Easy": [
                "Write an algorithm to reverse an array in-place without using extra array memory.",
                "Implement a program to find the GCD of two positive integers.",
                "Write a function to remove all spaces from a given string."
            ],
            "Medium": [
                "Write an algorithm to print a given N x M matrix in spiral order without using additional matrix memory.",
                "Given a string with nested parentheses and operators, evaluate if the expression is balanced and well-formed.",
                "Implement string multiplication for two arbitrarily large numerical strings without converting directly to standard integers."
            ],
            "Hard": [
                "Design a Low-Level Call Taxi Booking system with drivers, customers, trip fare calculation, and nearest driver allocation.",
                "Write a modular Railway Reservation System CLI with seat allocation, waiting list queuing, and cancellation refunds.",
                "Implement a custom memory pool manager allocator that manages fixed-size block allocations efficiently."
            ]
        },
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
        "Aptitude": {
            "Easy": [
                {
                    "prompt": "In a tournament with 64 teams playing single elimination, how many total matches are played to determine the champion?",
                    "options": ["63 matches", "64 matches", "32 matches", "127 matches"],
                    "answer": "63 matches"
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
                    "prompt": "If a fair coin is flipped 4 times, what is the probability of getting exactly 2 heads?",
                    "options": ["3/8", "1/2", "1/4", "5/8"],
                    "answer": "3/8"
                },
                {
                    "prompt": "What is the acute angle between the hour hand and minute hand of a clock at 3:15?",
                    "options": ["7.5 degrees", "0 degrees", "15 degrees", "11.25 degrees"],
                    "answer": "7.5 degrees"
                },
                {
                    "prompt": "A runner completes a 400-meter lap in 50 seconds. What is his speed in km/h?",
                    "options": ["28.8 km/h", "30 km/h", "25 km/h", "32 km/h"],
                    "answer": "28.8 km/h"
                },
                {
                    "prompt": "If 3 fair coins are tossed together, what is the probability of getting at least 2 heads?",
                    "options": ["1/2", "3/8", "5/8", "1/4"],
                    "answer": "1/2"
                },
                {
                    "prompt": "Find the next term in the logical series: 2, 6, 12, 20, 30, ?",
                    "options": ["42", "40", "36", "48"],
                    "answer": "42"
                },
                {
                    "prompt": "The perimeter of a rectangle is 40 cm and its length is 12 cm. What is its area?",
                    "options": ["96 sq cm", "80 sq cm", "100 sq cm", "90 sq cm"],
                    "answer": "96 sq cm"
                },
                {
                    "prompt": "If 4 cats catch 4 mice in 4 minutes, how many cats are needed to catch 100 mice in 100 minutes?",
                    "options": ["4 cats", "100 cats", "25 cats", "1 cat"],
                    "answer": "4 cats"
                }
            ],
            "Medium": [
                {
                    "prompt": "You have 8 identical-looking balls where 1 is slightly heavier. Using a balance scale only 2 times, how do you find the heavier ball?",
                    "options": ["Weigh 3 vs 3", "Weigh 4 vs 4", "Weigh 2 vs 2", "It's impossible"],
                    "answer": "Weigh 3 vs 3"
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
                    "prompt": "How many ways can a person climb a flight of 10 stairs taking either 1 or 2 steps at a time?",
                    "options": ["89", "55", "144", "100"],
                    "answer": "89"
                },
                {
                    "prompt": "In a sports tournament of 8 players, every pair plays once. How many total matches are played?",
                    "options": ["28 matches", "32 matches", "56 matches", "16 matches"],
                    "answer": "28 matches"
                }
            ],
            "Hard": [
                {
                    "prompt": "You have 12 coins, 1 of which is counterfeit (heavier or lighter). What is the minimum number of weighings on a balance scale to identify the counterfeit coin and determine whether it is heavy or light?",
                    "options": ["3 weighings", "4 weighings", "2 weighings", "5 weighings"],
                    "answer": "3 weighings"
                },
                {
                    "prompt": "What is the expected number of rolls of a fair 6-sided die needed to see all 6 faces at least once (Coupon Collector's Problem)?",
                    "options": ["14.7 rolls", "12.0 rolls", "18.5 rolls", "15.2 rolls"],
                    "answer": "14.7 rolls"
                },
                {
                    "prompt": "Four people need to cross a rickety bridge at night with 1 flashlight. They take 1, 2, 5, and 10 minutes respectively. Max 2 people can cross at once. What is the minimum total time required?",
                    "options": ["17 minutes", "19 minutes", "21 minutes", "15 minutes"],
                    "answer": "17 minutes"
                },
                {
                    "prompt": "There are 100 prisoners numbered 1 to 100 in a room containing 100 closed boxes. Each prisoner can open 50 boxes to find their number. If all find their numbers, all go free. What is the maximum survival probability strategy?",
                    "options": ["31.1%", "50.0%", "1.0%", "25.0%"],
                    "answer": "31.1%"
                },
                {
                    "prompt": "In a random walk on a 1D line starting at position 0, what is the probability of eventually returning to 0 given equal probability step sizes of +1 and -1?",
                    "options": ["100%", "50%", "75%", "25%"],
                    "answer": "100%"
                },
                {
                    "prompt": "If X and Y are independent uniform random variables on [0, 1], what is the probability that X + Y <= 1?",
                    "options": ["0.5", "0.25", "0.75", "0.33"],
                    "answer": "0.5"
                },
                {
                    "prompt": "There are 3 urns. Urn A has 2 red, Urn B has 2 blue, Urn C has 1 red and 1 blue. You pick an urn at random and draw a red ball. What is the probability the other ball in that urn is also red?",
                    "options": ["2/3", "1/2", "1/3", "3/4"],
                    "answer": "2/3"
                },
                {
                    "prompt": "What is the total number of integer grid points inside or on a circle of radius 5 centered at the origin?",
                    "options": ["81", "69", "77", "85"],
                    "answer": "81"
                },
                {
                    "prompt": "A line segment of length 1 is broken at 2 points chosen uniformly at random. What is the probability that the 3 resulting segments form a valid triangle?",
                    "options": ["1/4", "1/2", "1/3", "1/8"],
                    "answer": "1/4"
                },
                {
                    "prompt": "How many ways can 8 non-attacking rooks be placed on an 8x8 chessboard?",
                    "options": ["40,320", "64", "16,384", "262,144"],
                    "answer": "40,320"
                }
            ]
        },
        "Coding": {
            "Easy": [
                "Write a function to merge two sorted arrays into one sorted array.",
                "Implement a program to find the intersection of two array lists.",
                "Write a function to check if a binary tree is height-balanced."
            ],
            "Medium": [
                "Implement an algorithm to find the Median of Two Sorted Arrays in O(log(min(N,M))) time complexity.",
                "Given a stream of integers, design a data structure that efficiently retrieves the top K most frequent elements in O(1) or O(log K).",
                "Given a 2D grid representing a maze with obstacles, find the shortest path from start to target using BFS/A* search."
            ],
            "Hard": [
                "Implement a lock-free concurrent queue using atomic compare-and-swap operations.",
                "Design and implement a distributed graph traversal algorithm using MapReduce / BSP paradigm.",
                "Solve the Word Ladder II problem and return all shortest transformation sequences."
            ]
        },
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
        "Aptitude": {
            "Easy": [
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
                },
                {
                    "prompt": "A warehouse packs 300 boxes per day. If efficiency increases by 10%, how many boxes are packed daily?",
                    "options": ["330", "320", "350", "310"],
                    "answer": "330"
                },
                {
                    "prompt": "If a package dimensions are 10cm x 20cm x 30cm, what is its volume in liters (1 liter = 1000 cm3)?",
                    "options": ["6 liters", "60 liters", "0.6 liters", "12 liters"],
                    "answer": "6 liters"
                },
                {
                    "prompt": "A driver completes 8 deliveries out of 10 scheduled. What percentage of deliveries is incomplete?",
                    "options": ["20%", "15%", "25%", "10%"],
                    "answer": "20%"
                }
            ],
            "Medium": [
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
                    "prompt": "An Amazon warehouse has 3 sorting belts. Belt 1 sorts 500 items/hr, Belt 2 sorts 400 items/hr, Belt 3 sorts 600 items/hr. How many items are sorted in 4 hours together?",
                    "options": ["6,000 items", "5,000 items", "7,500 items", "4,500 items"],
                    "answer": "6,000 items"
                },
                {
                    "prompt": "A shipment contains 40% electronics, 35% apparel, and the rest home goods. If home goods are 250 items, how many total items are in the shipment?",
                    "options": ["1,000", "800", "1,200", "1,500"],
                    "answer": "1,000"
                }
            ],
            "Hard": [
                {
                    "prompt": "A fulfillment hub dispatches trucks to 3 cities A, B, C in ratios 5:3:2. If truck failure rates are 2%, 4%, and 5% respectively, what is the probability a randomly selected failed truck was heading to city B?",
                    "options": ["37.5%", "30.0%", "45.0%", "25.0%"],
                    "answer": "37.5%"
                },
                {
                    "prompt": "Two automated sorting arms A and B start together. A completes a cycle every 45 seconds, B every 60 seconds. How many times will they complete cycles simultaneously in a 3-hour shift?",
                    "options": ["60 times", "45 times", "72 times", "50 times"],
                    "answer": "60 times"
                },
                {
                    "prompt": "An inventory cost model is given by C(x) = 200x + 18000/x. What inventory order size x minimizes total operational cost?",
                    "options": ["9.49", "30", "12", "15"],
                    "answer": "9.49"
                },
                {
                    "prompt": "A logistics network has 4 distribution hubs. Between every pair of hubs there are 3 independent routes. How many total distinct paths connect Hub 1 to Hub 4 visiting every hub exactly once?",
                    "options": ["162", "81", "54", "108"],
                    "answer": "162"
                },
                {
                    "prompt": "A fleet of 20 electric vans degrades capacity by 2% per 10,000 km. If 5 vans drive 50,000 km and 15 vans drive 30,000 km, what is the fleet average capacity retention?",
                    "options": ["93.0%", "90.0%", "95.0%", "91.5%"],
                    "answer": "93.0%"
                },
                {
                    "prompt": "A packaging line operates at 98% efficiency. If line stoppage causes $500/min loss, what is the financial loss over a 40-hour work week?",
                    "options": ["$24,000", "$20,000", "$30,000", "$15,000"],
                    "answer": "$24,000"
                },
                {
                    "prompt": "Three items weighing 10kg, 15kg, 25kg are combined. If weight estimation errors are +/- 5%, +/- 4%, +/- 2% respectively, what is max absolute error in total weight?",
                    "options": ["1.6 kg", "2.0 kg", "1.2 kg", "2.5 kg"],
                    "answer": "1.6 kg"
                },
                {
                    "prompt": "A customer rating score drops from 4.8 to 4.2 after 100 negative reviews out of 1000 total reviews. What was the original number of positive reviews?",
                    "options": ["900", "850", "950", "800"],
                    "answer": "900"
                },
                {
                    "prompt": "If a warehouse aisle layout has 8 rows and 12 columns, how many unique shortest grid paths exist from top-left corner (0,0) to bottom-right corner (8,12)?",
                    "options": ["125,970", "64,320", "256,000", "100,000"],
                    "answer": "125,970"
                },
                {
                    "prompt": "A container ship carries 5,000 TEU. 60% are 20ft containers and 40% are 40ft containers (2 TEU each). How many total physical containers are onboard?",
                    "options": ["3,500", "4,000", "3,000", "4,500"],
                    "answer": "3,500"
                }
            ]
        },
        "Coding": {
            "Easy": [
                "Write a function to check if two arrays contain the same elements in any order.",
                "Implement a program to find the missing number in an array containing numbers from 1 to N.",
                "Write a function to compute the Fibonacci sequence up to N terms."
            ],
            "Medium": [
                "Given a list of customer orders with delivery deadlines, find the minimum number of delivery trucks needed (Interval Scheduling).",
                "Implement LRU (Least Recently Used) Cache with O(1) get and put operations.",
                "Given a binary tree, serialize and deserialize it efficiently into a compact string representation."
            ],
            "Hard": [
                "Design a distributed rate limiter with Sliding Window Counter algorithm across multiple geographic regions.",
                "Implement an algorithm for K-way Merge of K sorted linked lists in O(N log K) time.",
                "Solve the Trapping Rain Water problem on a 2D elevation map."
            ]
        },
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
        "Aptitude": {
            "Easy": [
                {
                    "prompt": "A software processing task takes 45 minutes without optimization. With optimization, time decreases by 60%. How much time is saved over 15 daily runs?",
                    "options": ["405 minutes", "380 minutes", "450 minutes", "270 minutes"],
                    "answer": "405 minutes"
                },
                {
                    "prompt": "Find the missing number in the sequence: 2, 6, 12, 20, 30, 42, ?",
                    "options": ["56", "54", "48", "60"],
                    "answer": "56"
                },
                {
                    "prompt": "If 5 automated units process 5,000 items in 5 seconds, how many units are needed to process 50,000 items in 50 seconds?",
                    "options": ["5", "10", "50", "25"],
                    "answer": "5"
                },
                {
                    "prompt": "The latencies of 5 data transfers are 10ms, 12ms, 15ms, 8ms, and 15ms. What is the average transfer latency?",
                    "options": ["12 ms", "14 ms", "10 ms", "13 ms"],
                    "answer": "12 ms"
                },
                {
                    "prompt": "If 2 units handle 500 requests per second, how many total units are required to scale to 2,000 requests per second linearly?",
                    "options": ["8", "6", "10", "4"],
                    "answer": "8"
                },
                {
                    "prompt": "A system achieves 5,000 operations per second with 4 KB size per operation. What is the throughput in MB per second?",
                    "options": ["20 MB/s", "25 MB/s", "10 MB/s", "40 MB/s"],
                    "answer": "20 MB/s"
                },
                {
                    "prompt": "A file of size 100 MB is compressed to 25 MB. What is the compression ratio?",
                    "options": ["4:1", "3:1", "2:1", "5:1"],
                    "answer": "4:1"
                },
                {
                    "prompt": "If a team of 4 technicians completes 400 work units per day, how many work units can 6 technicians complete in 5 days?",
                    "options": ["3,000 units", "2,400 units", "3,600 units", "1,800 units"],
                    "answer": "3,000 units"
                },
                {
                    "prompt": "A test suite has 120 batch items. If 15% fail, how many items passed?",
                    "options": ["102", "100", "108", "95"],
                    "answer": "102"
                },
                {
                    "prompt": "What is the next number in the geometric series: 4, 12, 36, 108, ?",
                    "options": ["324", "216", "432", "288"],
                    "answer": "324"
                }
            ],
            "Medium": [
                {
                    "prompt": "A 3 GHz clock completes an operation in 6 cycles. What is the execution time of the operation in nanoseconds?",
                    "options": ["2 nanoseconds", "1 nanosecond", "3 nanoseconds", "0.5 nanoseconds"],
                    "answer": "2 nanoseconds"
                },
                {
                    "prompt": "In a system with 4 KB page size, how many total pages exist in a 4 MB total memory space?",
                    "options": ["1,024", "2,048", "512", "4,096"],
                    "answer": "1,024"
                },
                {
                    "prompt": "A tank has capacity 100 liters. An inlet adds 10 liters per second and an outlet drains 8 liters per second. How long until the tank overflows?",
                    "options": ["50 seconds", "40 seconds", "100 seconds", "25 seconds"],
                    "answer": "50 seconds"
                },
                {
                    "prompt": "Find the result of the arithmetic evaluation: (1 + 2 + 3 + 4 + 5) * 2.",
                    "options": ["30", "15", "25", "20"],
                    "answer": "30"
                },
                {
                    "prompt": "A process has 90% fast access with 2ms time, and 10% slow access with 50ms time. Calculate the average access time.",
                    "options": ["6.8 ms", "5.0 ms", "7.2 ms", "10.0 ms"],
                    "answer": "6.8 ms"
                },
                {
                    "prompt": "How many total nodes are in a complete geometric 2-branch pyramid of depth 4 (1 + 2 + 4 + 8)?",
                    "options": ["15", "16", "31", "7"],
                    "answer": "15"
                },
                {
                    "prompt": "What is the maximum stack height when 16 identical blocks of height 2 cm are placed vertically?",
                    "options": ["32 cm", "16 cm", "64 cm", "24 cm"],
                    "answer": "32 cm"
                },
                {
                    "prompt": "If 4 system pauses of 50ms occur during a 10-second execution window, what is the overhead percentage?",
                    "options": ["2%", "5%", "1%", "4%"],
                    "answer": "2%"
                },
                {
                    "prompt": "A query response time is 40ms. An optimization reduces latency by 75%. What is the new response time?",
                    "options": ["10 ms", "15 ms", "20 ms", "5 ms"],
                    "answer": "10 ms"
                },
                {
                    "prompt": "A network link bandwidth is 1 Gbps. How many megabytes per second (MB/s) can it transmit theoretically?",
                    "options": ["125 MB/s", "100 MB/s", "250 MB/s", "500 MB/s"],
                    "answer": "125 MB/s"
                }
            ],
            "Hard": [
                {
                    "prompt": "A multi-unit system running 8 parallel units achieves 80% operational efficiency. What is the effective output multiplier over a single unit?",
                    "options": ["6.4x", "8.0x", "5.6x", "7.2x"],
                    "answer": "6.4x"
                },
                {
                    "prompt": "If 10% of a task is strictly sequential and 90% is parallelizable, what is the theoretical maximum speedup with infinitely many parallel workers?",
                    "options": ["10x", "9x", "100x", "5x"],
                    "answer": "10x"
                },
                {
                    "prompt": "A distributed system uses 3 redundant channels with 99% individual availability. What is the probability that all 3 channels fail simultaneously?",
                    "options": ["0.0001%", "0.01%", "0.001%", "0.1%"],
                    "answer": "0.0001%"
                },
                {
                    "prompt": "A warehouse has 1,000 slots and 800 items randomly distributed. Assuming uniform distribution, what is the probability that a specific slot remains empty?",
                    "options": ["44.9%", "36.8%", "50.0%", "40.0%"],
                    "answer": "44.9%"
                },
                {
                    "prompt": "A storage unit consists of 5 equal disks of 1 TB each. If 1 disk is reserved for parity backup, what is the usable storage capacity?",
                    "options": ["4 TB", "5 TB", "3 TB", "2.5 TB"],
                    "answer": "4 TB"
                },
                {
                    "prompt": "A data bus has a clock frequency of 1.6 GHz and a width of 64 bits (8 bytes). What is peak bandwidth in GB/s?",
                    "options": ["12.8 GB/s", "10.0 GB/s", "16.0 GB/s", "25.6 GB/s"],
                    "answer": "12.8 GB/s"
                },
                {
                    "prompt": "If a multi-tier index node has max capacity of 100 items and min 50 items, what is the minimum height required to store 1,000,000 items?",
                    "options": ["3", "4", "2", "5"],
                    "answer": "3"
                },
                {
                    "prompt": "A transport line experiences 1% item loss. What is the probability that 5 consecutive items are delivered without loss?",
                    "options": ["95.1%", "99.0%", "90.0%", "96.5%"],
                    "answer": "95.1%"
                },
                {
                    "prompt": "A system pauses in 3 recurring cycles: 10ms every 1s, 50ms every 10s, and 200ms every 100s. What is the total pause time over 100 seconds?",
                    "options": ["1.7 seconds", "2.0 seconds", "1.2 seconds", "2.5 seconds"],
                    "answer": "1.7 seconds"
                },
                {
                    "prompt": "A mathematical formula requires N * log2(N) operations. For N = 1,024, calculate total operations.",
                    "options": ["10,240", "2,048", "20,480", "5,120"],
                    "answer": "10,240"
                }
            ]
        },
        "Coding": {
            "Easy": [
                "Write a function to check if a binary search tree key exists.",
                "Implement a program to find the length of the last word in a string.",
                "Write a function to convert a Roman numeral string to an integer."
            ],
            "Medium": [
                "Find the lowest common ancestor (LCA) of two nodes in a binary search tree and in a general binary tree.",
                "Reverse nodes in k-group in a singly linked list in O(1) extra memory.",
                "Design an algorithm to find all unique triplets in an array that sum up to zero in O(N^2) time."
            ],
            "Hard": [
                "Implement a lock-free B-Tree concurrency index with optimistic concurrency control.",
                "Solve the Maximum Path Sum in a Binary Tree problem for arbitrary nodes.",
                "Implement regular expression matching supporting '.' and '*' wildcard operators."
            ]
        },
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
        "Aptitude": {
            "Easy": [
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
                    "prompt": "A startup has $120,000 in bank balance and a net monthly burn rate of $15,000. How many months of runway remain?",
                    "options": ["8 months", "10 months", "6 months", "12 months"],
                    "answer": "8 months"
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
                },
                {
                    "prompt": "A product price increases from $40 to $50. What is the percentage increase?",
                    "options": ["25%", "20%", "30%", "15%"],
                    "answer": "25%"
                },
                {
                    "prompt": "If 8 developers complete a sprint in 2 weeks, how many weeks would 4 developers take for the same workload?",
                    "options": ["4 weeks", "3 weeks", "2 weeks", "5 weeks"],
                    "answer": "4 weeks"
                },
                {
                    "prompt": "A website's page views grow from 50,000 to 75,000 in one month. Find the growth rate.",
                    "options": ["50%", "25%", "40%", "35%"],
                    "answer": "50%"
                },
                {
                    "prompt": "If 1 out of 20 trial users upgrades to a paid plan, what is the conversion percentage?",
                    "options": ["5%", "10%", "2%", "4%"],
                    "answer": "5%"
                }
            ],
            "Medium": [
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
                    "prompt": "What is the LTV : CAC ratio for a product with $480 LTV and $50 CAC?",
                    "options": ["9.6:1", "4.8:1", "12.0:1", "5.0:1"],
                    "answer": "9.6:1"
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
                    "prompt": "If a service P50 response time is 20ms and P99 response time is 200ms, how many times slower is P99 latency compared to P50?",
                    "options": ["10x", "5x", "20x", "2x"],
                    "answer": "10x"
                },
                {
                    "prompt": "AWS S3 storage costs $0.023 per GB per month. What is the monthly storage cost for 500 GB of user uploads?",
                    "options": ["$11.50", "$23.00", "$10.00", "$15.00"],
                    "answer": "$11.50"
                },
                {
                    "prompt": "A startup revenue is $20,000 in Month 1 and grows by 15% each month. What is the expected revenue in Month 3?",
                    "options": ["$26,450", "$23,000", "$25,000", "$27,200"],
                    "answer": "$26,450"
                }
            ],
            "Hard": [
                {
                    "prompt": "A SaaS business has Monthly Recurring Revenue (MRR) of $100,000 with a monthly gross churn rate of 3% and expansion MRR of 5%. What is the net MRR growth rate per month?",
                    "options": ["+2%", "+8%", "-3%", "+5%"],
                    "answer": "+2%"
                },
                {
                    "prompt": "An e-commerce startup offers 3 pricing tiers: $10/mo (50% users), $30/mo (30% users), $100/mo (20% users). What is the Average Revenue Per User (ARPU)?",
                    "options": ["$34/month", "$40/month", "$28/month", "$45/month"],
                    "answer": "$34/month"
                },
                {
                    "prompt": "A venture fund invests $1,000,000 for 20% equity at pre-money valuation. What is the post-money valuation of the startup?",
                    "options": ["$5,000,000", "$4,000,000", "$6,000,000", "$4,500,000"],
                    "answer": "$5,000,000"
                },
                {
                    "prompt": "If customer retention follows R(t) = 100% * (0.85)^t where t is months, after how many months does user retention drop below 50%?",
                    "options": ["5 months", "4 months", "6 months", "3 months"],
                    "answer": "5 months"
                },
                {
                    "prompt": "A cloud infra architecture requires 3 app servers ($200/mo each), 2 DB primary/replica nodes ($500/mo total), and load balancer ($100/mo). If traffic doubles, app servers scale 2x and DB nodes scale 1.5x. What is new monthly infra bill?",
                    "options": ["$2,050", "$1,800", "$2,400", "$2,200"],
                    "answer": "$2,050"
                },
                {
                    "prompt": "A mobile app has 500,000 Monthly Active Users (MAU) and 100,000 Daily Active Users (DAU). What is the DAU/MAU stickiness ratio?",
                    "options": ["20%", "25%", "15%", "30%"],
                    "answer": "20%"
                },
                {
                    "prompt": "A startup spends $60,000 monthly burn. Product margin is 60%. How much monthly gross revenue is needed to reach break-even?",
                    "options": ["$100,000", "$120,000", "$80,000", "$90,000"],
                    "answer": "$100,000"
                },
                {
                    "prompt": "A viral coefficient K is defined as K = i * c, where i is invites sent per user (5) and c is conversion rate per invite (10%). Calculate K.",
                    "options": ["0.5", "0.8", "1.2", "0.2"],
                    "answer": "0.5"
                },
                {
                    "prompt": "An A/B test shows Variant A conversion is 4% (sample 1,000) and Variant B conversion is 6% (sample 1,000). What is the relative percentage improvement of B over A?",
                    "options": ["50%", "20%", "2%", "33%"],
                    "answer": "50%"
                },
                {
                    "prompt": "If a startup valuation increases from $2M to $10M over 3 years, what is the Compound Annual Growth Rate (CAGR) of valuation?",
                    "options": ["71.0%", "50.0%", "65.0%", "80.0%"],
                    "answer": "71.0%"
                }
            ]
        },
        "Coding": {
            "Easy": [
                "Write a utility function to format numbers with commas as currency strings.",
                "Implement a function to check if a string contains valid balanced brackets.",
                "Write a program to generate a random string token of length N."
            ],
            "Medium": [
                "Write a debouncing and throttling utility function and explain their differences in user interface event handling.",
                "Implement a function that deeply flattens a nested object / array structure with circular reference handling.",
                "Write a clean function to implement exponential backoff retry for network requests."
            ],
            "Hard": [
                "Implement a real-time reactive event emitter bus with wildcard subscription pattern.",
                "Design and write a state machine framework for handling multi-step asynchronous workflow transitions.",
                "Write a custom JSON parser implementation with tokens scanning and AST node building."
            ]
        },
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

GENERIC_QUESTIONS_BY_CATEGORY: dict[str, dict[str, list[Any]] | list[Any]] = {
    "Aptitude": {
        "Easy": [
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
                "prompt": "Find the next number in the series: 3, 7, 15, 31, 63, ?",
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
                "prompt": "A sum of money doubles itself at simple interest in 10 years. What is the annual interest rate?",
                "options": ["10%", "12%", "8%", "15%"],
                "answer": "10%"
            },
            {
                "prompt": "If 15% of X is equal to 20% of Y, then what is the ratio X : Y?",
                "options": ["4:3", "3:4", "5:4", "2:3"],
                "answer": "4:3"
            },
            {
                "prompt": "What is the average of the first 5 prime numbers?",
                "options": ["5.6", "5.0", "5.4", "6.2"],
                "answer": "5.6"
            },
            {
                "prompt": "A vendor buys lemons at 6 for Rs 10 and sells them at 4 for Rs 10. Find his profit percentage.",
                "options": ["50%", "40%", "25%", "60%"],
                "answer": "50%"
            },
            {
                "prompt": "The ratio of ages of A and B is 4:5. If the sum of their ages is 36 years, what will be the ratio of their ages after 4 years?",
                "options": ["5:6", "9:10", "4:5", "7:8"],
                "answer": "5:6"
            }
        ],
        "Medium": [
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
            },
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
                "prompt": "A jar contains 5 red marbles, 4 blue marbles, and 3 green marbles. If two marbles are drawn randomly without replacement, what is the probability that both are red?",
                "options": ["5/33", "1/6", "5/22", "1/11"],
                "answer": "5/33"
            },
            {
                "prompt": "The average of 5 consecutive odd numbers is 27. What is the product of the lowest and highest number?",
                "options": ["713", "621", "759", "675"],
                "answer": "713"
            },
            {
                "prompt": "If the radius of a circle is increased by 20%, by what percentage does its area increase?",
                "options": ["44%", "40%", "20%", "48%"],
                "answer": "44%"
            }
        ],
        "Hard": [
            {
                "prompt": "A man can row 6 km/h in still water. If river flows at 2 km/h, it takes him 3 hours to row to a place and back. How far is the place?",
                "options": ["8 km", "6 km", "9 km", "7.5 km"],
                "answer": "8 km"
            },
            {
                "prompt": "In how many ways can 5 men and 4 women be seated in a row so that women always occupy even places?",
                "options": ["2880", "1440", "5760", "720"],
                "answer": "2880"
            },
            {
                "prompt": "A vessel is full of 80 liters of milk. 8 liters is taken out and replaced by water. This is repeated 2 more times. How much milk remains?",
                "options": ["58.32 liters", "60.40 liters", "55.80 liters", "62.10 liters"],
                "answer": "58.32 liters"
            },
            {
                "prompt": "A sum of money invested at compound interest amounts to Rs 4,608 in 2 years and Rs 5,529.60 in 3 years. Find the rate of interest per annum.",
                "options": ["20%", "15%", "18%", "25%"],
                "answer": "20%"
            },
            {
                "prompt": "A and B start a business with investments of Rs 50,000 and Rs 70,000 respectively. After 6 months, C joins with Rs 80,000. What is C's share in an annual profit of Rs 36,000?",
                "options": ["Rs 8,000", "Rs 10,000", "Rs 12,000", "Rs 9,000"],
                "answer": "Rs 8,000"
            },
            {
                "prompt": "Two trains moving in opposite directions at 60 km/h and 90 km/h cross each other in 12 seconds. If the length of one train is 250 meters, what is the length of the other train?",
                "options": ["250 meters", "300 meters", "200 meters", "350 meters"],
                "answer": "250 meters"
            },
            {
                "prompt": "Three pipes A, B and C can fill a reservoir in 6 hours together. After working together for 2 hours, C is closed and A and B can fill it in 7 hours. How long will C alone take to fill it?",
                "options": ["14 hours", "12 hours", "16 hours", "10 hours"],
                "answer": "14 hours"
            },
            {
                "prompt": "Find the compound interest on Rs 10,000 at 10% per annum for 2.5 years, compounded annually.",
                "options": ["Rs 2,705", "Rs 2,500", "Rs 2,850", "Rs 2,625"],
                "answer": "Rs 2,705"
            },
            {
                "prompt": "From a box containing 6 red balls and 4 green balls, 3 balls are drawn at random. What is the probability that at least 1 green ball is drawn?",
                "options": ["5/6", "4/5", "3/4", "7/8"],
                "answer": "5/6"
            },
            {
                "prompt": "A work can be completed by 10 men in 12 days. They worked together for 4 days, then 2 more men joined. In how many days will the remaining work be finished?",
                "options": ["6.67 days", "7 days", "5 days", "8 days"],
                "answer": "6.67 days"
            }
        ]
    },
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

FORBIDDEN_CODING_KEYWORDS = [
    "python", "java", "c++", "code", "coding", "function", "array", "string",
    "loop", "algorithm", "data structure", "class ", "variable", "pointer",
    "linked list", "tree", "graph", "stack", "queue", "hashmap", "binary search",
    "time complexity", "space complexity", "o(n)", "dsa", "leetcode", "compiler"
]


def is_coding_question(prompt_text: str) -> bool:
    """Returns True if the prompt contains programming/coding terminology or concepts."""
    if not prompt_text:
        return False
    import re
    text_lower = prompt_text.lower()
    for kw in FORBIDDEN_CODING_KEYWORDS:
        if " " in kw:
            if kw in text_lower:
                return True
        else:
            if re.search(rf"\b{re.escape(kw)}\b", text_lower):
                return True
    return False


def validate_aptitude_question(q: dict) -> bool:
    """Validates that a question dictionary is a pure Aptitude MCQ with 4 unique options and valid correct answer."""
    if not isinstance(q, dict):
        return False
    prompt = str(q.get("prompt", "")).strip()
    if not prompt or is_coding_question(prompt):
        return False
    options = q.get("options")
    if not isinstance(options, list) or len(options) != 4:
        return False
    options_str = [str(o).strip() for o in options]
    if len(set(options_str)) != 4:  # All options must be unique
        return False
    correct_ans = str(q.get("correct_answer", q.get("answer", ""))).strip()
    if not correct_ans or correct_ans not in options_str:
        return False
    return True


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
    
    diff_clean = difficulty.strip().capitalize() if difficulty else "Medium"
    if diff_clean in ["Difficult", "Challenging"]:
        diff_clean = "Hard"
    elif diff_clean not in ["Easy", "Medium", "Hard"]:
        diff_clean = "Medium"

    # Check if Gemini API is available for dynamic questions
    has_key = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "replace-with-gemini-key")
    logger.info(f"[GEMINI] API key configured: {has_key}")
    if has_key:
        model_name = "gemini-3.6-flash"
        logger.info(f"[GEMINI] model: {model_name}")
        logger.info(f"[GEMINI] {category.lower()} generation started for difficulty: {diff_clean}")
        
        prompt = f"Generate {count} distinct interview questions for {company_name} {role} (Difficulty: {diff_clean}). Round: {category}."
        if category == "Aptitude":
            prompt += " Output ONLY valid JSON containing an array of objects under the key 'questions'. Each question object must have exactly 4 keys: 'prompt' (the question text), 'question_type' (set to 'mcq'), 'options' (an array of exactly 4 strings), and 'correct_answer' (a string matching exactly one of the options). The questions MUST be strictly mathematical or logical quantitative aptitude problems (percentages, ratios, profit/loss, time/work, speed/distance, probability, series, ages). Do NOT include any programming, coding, algorithms, data structures, or code syntax. ALL options must be completely distinct. Do NOT use generic placeholders like 'A', 'B', 'C', 'D'."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7, 
                "maxOutputTokens": 8192,
                "responseMimeType": "application/json"
            }
        }
        
        try:
            res = httpx.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=4.0)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                
                parsed = json.loads(text)
                question_list = parsed.get("questions") if isinstance(parsed, dict) else parsed
                
                if isinstance(question_list, list) and len(question_list) >= count:
                    normalized = []
                    for item in question_list[:count]:
                        if isinstance(item, dict):
                            prompt_text = item.get("prompt", "").strip()
                            if category == "Aptitude":
                                q_obj = {
                                    "prompt": prompt_text,
                                    "question_type": "mcq",
                                    "options": [str(o).strip() for o in item.get("options", [])],
                                    "correct_answer": str(item.get("correct_answer", item.get("answer", ""))).strip()
                                }
                                if validate_aptitude_question(q_obj):
                                    normalized.append(q_obj)
                            else:
                                normalized.append({
                                    "prompt": prompt_text,
                                    "question_type": "text",
                                    "options": None,
                                    "correct_answer": None
                                })
                    if len(normalized) >= count:
                        return normalized[:count]
        except Exception as e:
            logger.warning(f"Gemini API dynamic generation fallback: {e}")

    logger.info("[GEMINI] fallback used: true")
    # Heuristic & company pattern matching
    matched_company = None
    for name in COMPANY_QUESTIONS:
        if name.lower() in company_name.lower():
            matched_company = COMPANY_QUESTIONS[name]
            break

    if not matched_company:
        matched_company = COMPANY_QUESTIONS["Startup"]

    raw_cat_pool = matched_company.get(category, {})

    if isinstance(raw_cat_pool, dict):
        category_pool = list(raw_cat_pool.get(diff_clean, []))
        if not category_pool:
            category_pool = list(raw_cat_pool.get("Medium", []))
        if not category_pool:
            for v in raw_cat_pool.values():
                if isinstance(v, list):
                    category_pool.extend(v)
    elif isinstance(raw_cat_pool, list):
        category_pool = list(raw_cat_pool)
    else:
        category_pool = []

    if category == "Aptitude":
        # Strictly validate all items in category_pool
        validated_pool = [q for q in category_pool if isinstance(q, dict) and validate_aptitude_question(q)]
        category_pool = validated_pool

    if not category_pool:
        gen_cat = GENERIC_QUESTIONS_BY_CATEGORY.get(category, {})
        if isinstance(gen_cat, dict):
            category_pool = list(gen_cat.get(diff_clean, gen_cat.get("Medium", [])))
        elif isinstance(gen_cat, list):
            category_pool = list(gen_cat)
        else:
            category_pool = []
        if category == "Aptitude":
            category_pool = [q for q in category_pool if isinstance(q, dict) and validate_aptitude_question(q)]

    # Perform randomized sampling to guarantee fresh questions for every session
    # and prevent duplicate questions within the same session
    if len(category_pool) >= count:
        result = random.sample(category_pool, count)
    else:
        result = list(category_pool)
        random.shuffle(result)
        fallback_source = GENERIC_QUESTIONS_BY_CATEGORY.get(category, {})
        if isinstance(fallback_source, dict):
            fallback_pool = list(fallback_source.get(diff_clean, fallback_source.get("Medium", [])))
        else:
            fallback_pool = list(fallback_source)
        if category == "Aptitude":
            fallback_pool = [q for q in fallback_pool if isinstance(q, dict) and validate_aptitude_question(q)]
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
                f"You are a hiring manager evaluating a mock interview answer for {company_name} ({role}, {difficulty} difficulty).\n\n"
                f"Question: {question_prompt}\n"
                f"Candidate's Answer: {resp_text}\n\n"
                f"{eval_instructions} Return ONLY a JSON object in this format:\n"
                f"{{\"score\": <integer 0-100>, \"feedback\": \"<2-3 sentences of constructive critique highlighting strengths and missing key elements>\"}}"
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
