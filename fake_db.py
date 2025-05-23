def create_mock_db():
    import sqlite3
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS employees")

    cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary INTEGER
        )
    ''')

    cursor.executemany('''
        INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)
    ''', [
        ("Alice", "HR", 50000),
        ("Bob", "Engineering", 80000),
        ("Charlie", "Engineering", 75000),
        ("Diana", "HR", 52000),
        ("Ethan", "Marketing", 60000),
        ("Fiona", "Finance", 70000),
        ("George", "Engineering", 82000),
        ("Hannah", "Marketing", 62000),
        ("Ian", "Finance", 68000),
        ("Jane", "HR", 53000),
        ("Kevin", "Engineering", 78000),
        ("Laura", "Finance", 71000),
        ("Mike", "Marketing", 59000),
        ("Nina", "HR", 55000),
        ("Oscar", "Engineering", 77000)
    ])

    conn.commit()
    conn.close()
    print("Mock database created successfully!")
