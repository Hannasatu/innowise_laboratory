
import sqlite3
import os

DB_FOLDER = "lecture_4"
DB_NAME = "school1.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

os.makedirs(DB_FOLDER, exist_ok=True)


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print(f"База данных '{DB_PATH}' успешно создана/открыта.\n")

create_tables_sql = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    FOREIGN KEY (student_id) REFERENCES students(id)
);
"""

create_indexes_sql = """
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades (student_id);
CREATE INDEX IF NOT EXISTS idx_students_full_name ON students (full_name);
CREATE INDEX IF NOT EXISTS idx_students_birth_year ON students (birth_year);
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades (subject);
"""

try:
    cursor.executescript(create_tables_sql)
    cursor.executescript(create_indexes_sql)
    conn.commit()
    print("Таблицы 'students' и 'grades' (и индексы) успешно созданы.\n")
except sqlite3.Error as e:
    print(f"Ошибка при создании таблиц: {e}")
    conn.close()
    exit()

students_data = [
    ('Alice Johnson', 2005),
    ('Brian Smith', 2004),
    ('Carla Reyes', 2006),
    ('Daniel Kim', 2005),
    ('Eva Thompson', 2003),
    ('Felix Nguyen', 2007),
    ('Grace Patel', 2005),
    ('Henry Lopez', 2004),
    ('Isabella Martinez', 2006)
]

grades_data = [
    (1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
    (2, 'Math', 75), (2, 'History', 83), (2, 'English', 79),
    (3, 'Science', 95), (3, 'Math', 91), (3, 'Art', 89),
    (4, 'Math', 84), (4, 'Science', 88), (4, 'Physical Education', 93),
    (5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
    (6, 'Science', 72), (6, 'Math', 78), (6, 'English', 81),
    (7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
    (8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
    (9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92)
]

try:
    cursor.executemany("INSERT INTO students (full_name, birth_year) VALUES (?, ?)", students_data)
    cursor.executemany("INSERT INTO grades (student_id, subject, score) VALUES (?, ?, ?)", grades_data)
    conn.commit()
    print("Образцы данных успешно вставлены в таблицы.\n")
except sqlite3.Error as e:
    print(f"Ошибка при вставке данных: {e}")
    conn.rollback()
    conn.close()
    exit()


def execute_and_print_query(query_name, sql_query):
    print(f"--- {query_name} ---")
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        if rows:
            column_names = [description[0] for description in cursor.description]
            print(column_names)
            for row in rows:
                print(row)
        else:
            print("Нет данных для отображения.")
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
    print("\n")

query_alice_grades = """
SELECT s.full_name, g.subject, g.score
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson';
"""
execute_and_print_query("1. Оценки для Alice Johnson", query_alice_grades)

query_avg_grade_per_student = """
SELECT s.full_name, AVG(g.score) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.full_name
ORDER BY average_grade DESC;
"""
execute_and_print_query("2. Средний балл по каждому студенту", query_avg_grade_per_student)

query_students_after_2004 = """
SELECT full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year, full_name;
"""
execute_and_print_query("3. Студенты, родившиеся после 2004 года", query_students_after_2004)

query_subject_avg_grades = """
SELECT subject, AVG(score) AS average_score
FROM grades
GROUP BY subject
ORDER BY average_score DESC;
"""
execute_and_print_query("4. Средние оценки по предметам", query_subject_avg_grades)

query_top3_students = """
SELECT s.full_name, AVG(g.score) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.full_name
ORDER BY average_grade DESC
LIMIT 3;
"""
execute_and_print_query("5. Топ-3 студента по среднему баллу", query_top3_students)

query_students_below_80 = """
SELECT DISTINCT s.full_name, g.subject, g.score
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.score < 80
ORDER BY s.full_name, g.score;
"""

execute_and_print_query("6. Студенты с оценкой ниже 80", query_students_below_80)


print("Все запросы выполнены.\n")

conn.close()
print("Соединение с базой данных закрыто.")
