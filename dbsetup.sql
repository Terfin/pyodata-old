CREATE TABLE IF NOT EXISTS pyodata_departments (id INT, name VARCHAR(50));
CREATE TABLE IF NOT EXISTS pyodata_employees (id INT, first_name VARCHAR(20), last_name VARCHAR(30), birth_date DATETIME, department_id INT);

ALTER TABLE pyodata_departments ADD PRIMARY KEY (id);
ALTER TABLE pyodata_departments MODIFY COLUMN id INT AUTO_INCREMENT;
ALTER TABLE pyodata_departments MODIFY COLUMN name VARCHAR(50) UNIQUE;
ALTER TABLE pyodata_employees ADD PRIMARY KEY (id);
ALTER TABLE pyodata_employees MODIFY COLUMN id INT AUTO_INCREMENT;

INSERT INTO pyodata_departments (name) VALUES ('Development');
INSERT INTO pyodata_departments (name) VALUES ('Graphic Design');
INSERT INTO pyodata_departments (name) VALUES ('Administration');

INSERT INTO pyodata_employees (first_name, last_name, birth_date, department_id) VALUES ('Nadav', 'Har Tzvi', '1986-06-07T00:00:00', 1);
INSERT INTO pyodata_employees (first_name, last_name, birth_date, department_id) VALUES ('Nahum', 'Barnea', '1971-03-11T00:00:00', 3);
INSERT INTO pyodata_employees (first_name, last_name, birth_date, department_id) VALUES ('Shmulik', 'Kipod', '2001-09-11T00:00:00', 2);
INSERT INTO pyodata_employees (first_name, last_name, birth_date, department_id) VALUES ('Muli', 'Molobovich', '1993-10-23T00:00:00', 1);
INSERT INTO pyodata_employees (first_name, last_name, birth_date, department_id) VALUES ('Musa', 'Marwani', '1980-04-30T00:00:00', 2);