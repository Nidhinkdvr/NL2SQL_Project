from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sqlite3
import pandas as pd
from fake_db import create_mock_db
import os
from difflib import SequenceMatcher

model_name = "suriya7/t5-base-text-to-sql"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

DB_PATH = "sample.db"

def run_sql_query(query):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        return f"SQL Error: {e}"
    finally:
        conn.close()

def nl_to_sql(nl_query):
    prompt = f"translate English to SQL: {nl_query}"
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    output = model.generate(**inputs, max_length=128)
    sql_query = tokenizer.decode(output[0], skip_special_tokens=True)
    return sql_query.strip()

def evaluate_exact_match_percentage(actual_sql, pred_sql):
    actual_sql = actual_sql.strip().lower()
    pred_sql = pred_sql.strip().lower()
    ratio = SequenceMatcher(None, actual_sql, pred_sql).ratio()
    return ratio  # 0.0 to 1.0

def evaluate_execution_accuracy_percentage(actual_sql, pred_sql):
    try:
        actual_df = run_sql_query(actual_sql)
        pred_df = run_sql_query(pred_sql)

        if isinstance(actual_df, pd.DataFrame) and isinstance(pred_df, pd.DataFrame):
            if actual_df.empty and pred_df.empty:
                return 1.0  # both empty → full match

            # Sort and reset index to align rows for fair comparison
            actual_df_sorted = actual_df.sort_values(by=actual_df.columns.tolist()).reset_index(drop=True)
            pred_df_sorted = pred_df.sort_values(by=pred_df.columns.tolist()).reset_index(drop=True)

            # Check if columns sets are same
            if set(actual_df_sorted.columns) != set(pred_df_sorted.columns):
                return 0.0

            actual_df_sorted = actual_df_sorted[sorted(actual_df_sorted.columns)]
            pred_df_sorted = pred_df_sorted[sorted(pred_df_sorted.columns)]

            total_rows = max(len(actual_df_sorted), len(pred_df_sorted))
            matching_rows = 0

            for gold_row, pred_row in zip(actual_df_sorted.itertuples(index=False), pred_df_sorted.itertuples(index=False)):
                if gold_row == pred_row:
                    matching_rows += 1

            return matching_rows / total_rows if total_rows > 0 else 0.0
        else:
            return 0.0
    except Exception:
        return 0.0

def main():
    if not os.path.exists(DB_PATH):
        print("Creating mock database...")
        create_mock_db()

    print("NL2SQL Query System\n")

    test_cases = [
        {
            "nl": "Show me all employees in Engineering department.",
            "actual_sql": "SELECT * FROM employees WHERE department = 'Engineering';"
        },
        {
            "nl": "List employees with salary greater than 70000.",
            "actual_sql": "SELECT * FROM employees WHERE salary > 70000;"
        },
        {
            "nl": "How many employees are in HR?",
            "actual_sql": "SELECT COUNT(*) FROM employees WHERE department = 'HR';"
        },
        {
            "nl": "Find employees in Marketing with salary less than 60000.",
            "actual_sql": "SELECT * FROM employees WHERE department = 'Marketing' AND salary < 60000;"
        },
        {
            "nl": "Get the names of employees earning exactly 52000.",
            "actual_sql": "SELECT name FROM employees WHERE salary = 52000;"
        }
    ]

    exact_match_sum = 0.0
    exec_accuracy_sum = 0.0

    print("Running Evaluation...\n")
    for i, test in enumerate(test_cases, 1):
        nl = test["nl"]
        actual_sql = test["actual_sql"]
        pred_sql = nl_to_sql(nl)

        exact_pct = evaluate_exact_match_percentage(actual_sql, pred_sql)
        exec_pct = evaluate_execution_accuracy_percentage(actual_sql, pred_sql)

        exact_match_sum += exact_pct
        exec_accuracy_sum += exec_pct

        print(f"Test Case {i}:")
        print(f"NL Query:        {nl}")
        print(f"Predicted SQL:   {pred_sql}")
        print(f"Actual SQL:      {actual_sql}")
        print(f"Exact Match:     {exact_pct * 100:.2f}%")
        print(f"Execution Match: {exec_pct * 100:.2f}%")
        print("-" * 50)

    total = len(test_cases)
    print(f"\nSummary:")
    print(f"Average Exact Match Accuracy:     {exact_match_sum}/{total} = {exact_match_sum/total:.2f}")
    print(f"Average Execution Accuracy:       {exec_accuracy_sum}/{total} = {exec_accuracy_sum/total:.2f}\n")

    # Interactive mode
    while True:
        user_input = input("Enter a natural language query (or 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        sql_query = nl_to_sql(user_input)
        print(f"Generated SQL: {sql_query}")

        result = run_sql_query(sql_query)
        print("Query Result:")
        print(result)
        print()

if __name__ == "__main__":
    main()
