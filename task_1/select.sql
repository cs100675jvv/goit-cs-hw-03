-- 1. Отримати всі завдання певного користувача
SELECT * FROM tasks 
WHERE user_id = 10;

-- 2. Вибрати завдання за певним статусом
SELECT tasks.* FROM tasks
JOIN status ON tasks.status_id = status.id
WHERE status.name = 'new';

-- 3. Оновити статус конкретного завдання
UPDATE tasks 
SET status_id = (SELECT id FROM status WHERE name = 'completed')
WHERE id = 10;

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT name FROM users
WHERE id NOT IN (SELECT user_id FROM tasks);

-- 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, user_id, status_id)
VALUES ('New task for user', 'Adding a new task for a user ID=5.', 5, 1);

-- 6. Отримати всі завдання, які ще не завершено
SELECT tasks.title, tasks.description FROM tasks
JOIN status ON tasks.status_id = status.id
WHERE status.name != 'completed';

-- 7. Видалити конкретне завдання
DELETE FROM tasks 
WHERE id = 1;

-- 8. Знайти користувачів з певною електронною поштою
SELECT * FROM users 
WHERE email LIKE '%example.org'

-- 9. Оновити ім'я користувача
UPDATE users 
SET name = 'Bob'
WHERE name = 'gkelly'

-- 10. Отримати кількість завдань для кожного статусу
SELECT status.name, COUNT(tasks.id) FROM tasks
JOIN status ON tasks.status_id = status.id
GROUP BY status.name;

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
SELECT tasks.* FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.org';

-- 12. Отримати список завдань, що не мають опису
SELECT tasks.title FROM tasks
WHERE description = '' OR description IS NULL

-- 13. Вибрати користувачів та їхні завдання, які є у статусі "в процесі"
SELECT users.name AS user_name, users.email AS user_email, tasks.title AS task_title, tasks.description AS task_description FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';

-- 14. Отримати користувачів та кількість їхніх завдань
SELECT users.id AS user_id, users.name AS user_name, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.id, users.name;