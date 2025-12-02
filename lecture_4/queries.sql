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

-- Создание индексов для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades (student_id);
CREATE INDEX IF NOT EXISTS idx_students_full_name ON students (full_name);
CREATE INDEX IF NOT EXISTS idx_students_birth_year ON students (birth_year);
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades (subject);

-- Вставка образцов данных
-- Вставка студентов (id автоинкрементируются)
INSERT INTO students (full_name, birth_year) VALUES
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Вставка оценок
-- Важно: student_id здесь соответствуют id студентов, которые были созданы при вставке выше.
INSERT INTO grades (student_id, subject, score) VALUES
(1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
(2, 'Math', 75), (2, 'History', 83), (2, 'English', 79),
(3, 'Science', 95), (3, 'Math', 91), (3, 'Art', 89),
(4, 'Math', 84), (4, 'Science', 88), (4, 'Physical Education', 93),
(5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
(6, 'Science', 72), (6, 'Math', 78), (6, 'English', 81),
(7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
(8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
(9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92);


-- SQL-ЗАПРОСЫ:

-- 1. Найти все оценки для конкретного студента (Alice Johnson).
SELECT s.full_name, g.subject, g.score
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson';

-- 2. Вычислить средний балл по каждому студенту.
SELECT s.full_name, AVG(g.score) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.full_name
ORDER BY average_grade DESC;

-- 3. Вывести всех студентов, родившихся после 2004 года.
SELECT full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year, full_name;

-- 4. Вывести все предметы и их средние оценки.
SELECT subject, AVG(score) AS average_score
FROM grades
GROUP BY subject
ORDER BY average_score DESC;

-- 5. Найти топ-3 студентов с самыми высокими средними баллами.
SELECT s.full_name, AVG(g.score) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- 6. Показать всех студентов, набравших менее 80 баллов по любому предмету.
SELECT DISTINCT s.full_name, g.subject, g.score
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.score < 80
ORDER BY s.full_name, g.score;
