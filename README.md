# NL2SQL_Project


# Overview
This project is part of the internship evaluation for the Junior Data Scientist / Gen AI Intern position at CAS. The objective is to implement an NL2SQL system that converts natural language queries into SQL statements using a pre-trained model.


# Objective
Convert natural language (NL) questions into valid SQL queries and evaluate the model’s performance using:
1.Exact Match Accuracy
2.Execution Accuracy

# Tools & Technologies Used
Language: Python
Libraries: transformers, pandas, sqlite3, difflib
Model: suriya7/t5-base-text-to-sql (used due to access limitations with recommended models)
Environment: Local system (PyCharm IDE)

# Implementation Steps
1.Mock Database Creation
 *Built a SQLite database named sample.db with an employees table.
 *Inserted mock employee records with name, department, and salary columns.
 
2.Model Selection & Setup
*Due to unavailability of suggested models (like tscholak/optimum-nl2sql, b-mc2/sqlcoder), used suriya7/t5-base-text-to-sql from Hugging Face.
*Loaded model and tokenizer using Hugging Face’s transformers library.

3.Natural Language to SQL Conversion
*Defined a nl_to_sql() function that constructs a prompt and generates SQL using the model.

4.SQL Execution & Evaluation
*Created two evaluation metrics:
*Exact Match: Uses SequenceMatcher to compare predicted vs. actual SQL string.
*Execution Accuracy: Runs both predicted and actual SQL against the database and compares the results.

5.Test Cases
*Defined 5 test cases to evaluate the model on common employee database queries.
*Captured and printed:
*Natural language input
*Model’s predicted SQL

6.Exact SQL match percentage
*Execution match percentage
*Interactive Mode

# Result 
The model performed poorly in terms of execution accuracy due to incorrect SQL structure and table references.

# Realtime output:

Test Case 1
NL Query: Show me all employees in Engineering department.
Predicted SQL: SELECT employees FROM table_name_65 WHERE department = "ingénience"
Actual SQL: SELECT * FROM employees WHERE department = 'Engineering';
Exact Match: 62.90%
Execution Match: 0.00%

Test Case 2
NL Query: List employees with salary greater than 70000.
Predicted SQL: SELECT employees FROM table_name_65 WHERE salary > 70000
Actual SQL: SELECT * FROM employees WHERE salary > 70000;
Exact Match: 73.27%
Execution Match: 0.00%

Test Case 3
NL Query: How many employees are in HR?
Predicted SQL: SELECT COUNT() FROM HR
Actual SQL: SELECT COUNT(*) FROM employees WHERE department = 'HR';
Exact Match: 58.97%
Execution Match: 0.00%

Test Case 4
NL Query: Find employees in Marketing with salary less than 60000.
Predicted SQL: SELECT marketing_team FROM table_name_55 WHERE salary 60000
Actual SQL: SELECT * FROM employees WHERE department = 'Marketing' AND salary < 60000;
Exact Match: 49.25%
Execution Match: 0.00%

Test Case 5
NL Query: Get the names of employees earning exactly 52000.
Predicted SQL: SELECT employees_name FROM employees AS a number_ FROM employees AS numbers___numbers FROM employees AS numbers__numbers = "52000"
Actual SQL: SELECT name FROM employees WHERE salary = 52000;
Exact Match: 45.65%
Execution Match: 0.00%

Summary
Average Exact Match Accuracy: 58.41%
Average Execution Match Accuracy: 0.00%







