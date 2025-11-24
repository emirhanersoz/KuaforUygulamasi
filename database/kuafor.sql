DROP DATABASE IF EXISTS kuafor_db;
CREATE DATABASE kuafor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE kuafor_db;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    role_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
);

CREATE TABLE salons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    salon_id INT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (salon_id) REFERENCES salons(id) ON DELETE RESTRICT
);

CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE employee_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    service_id INT NOT NULL,
    duration_minutes INT NOT NULL DEFAULT 30,
    price_tl DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    UNIQUE (employee_id, service_id),
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);

CREATE TABLE employee_availability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    day_of_week INT NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    UNIQUE (employee_id, day_of_week),
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, 
    salon_id INT NOT NULL,
    employee_id INT NOT NULL,
    service_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_confirmed BOOLEAN DEFAULT FALSE,
    is_cancelled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (employee_id, appointment_date, start_time),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (salon_id) REFERENCES salons(id) ON DELETE RESTRICT,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE RESTRICT,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE RESTRICT
);

INSERT INTO roles (role_name) VALUES ('Müşteri'), ('Çalışan'), ('Yönetici');

INSERT INTO salons (name, address, phone_number) VALUES 
('Merkez Şube', 'İstanbul / Beşiktaş', '0212 123 45 67'),
('Kadıköy Şubesi', 'İstanbul / Kadıköy', '0216 987 65 43');

INSERT INTO services (service_name) VALUES 
('Saç Kesimi'), 
('Sakal Tıraşı'), 
('Saç Boyama'), 
('Fön'), 
('Cilt Bakımı');

INSERT INTO users (first_name, last_name, email, password_hash, role_id, phone_number) VALUES
('Sistem', 'Yöneticisi', 'admin@kuafor.com', '123', 3, '5550000000'),
('Ahmet', 'Makas', 'ahmet@kuafor.com', '123', 2, '5551111111'),
('Ayşe', 'Tarak', 'ayse@kuafor.com', '123', 2, '5552222222'),
('Mehmet', 'Müşteri', 'mehmet@kuafor.com', '123', 1, '5553333333');


INSERT INTO employees (user_id, salon_id, is_admin) VALUES (2, 1, FALSE);
INSERT INTO employees (user_id, salon_id, is_admin) VALUES (3, 2, FALSE);

INSERT INTO employee_services (employee_id, service_id, duration_minutes, price_tl) VALUES (1, 1, 30, 200.00);
INSERT INTO employee_services (employee_id, service_id, duration_minutes, price_tl) VALUES (1, 2, 15, 100.00);

INSERT INTO employee_services (employee_id, service_id, duration_minutes, price_tl) VALUES (2, 1, 45, 250.00);
INSERT INTO employee_services (employee_id, service_id, duration_minutes, price_tl) VALUES (2, 3, 120, 800.00);

INSERT INTO employee_availability (employee_id, day_of_week, start_time, end_time) VALUES
(1, 0, '09:00', '18:00'),
(1, 1, '09:00', '18:00'),
(1, 2, '09:00', '18:00'),
(1, 3, '09:00', '18:00'),
(1, 4, '09:00', '18:00'); 

INSERT INTO employee_availability (employee_id, day_of_week, start_time, end_time) VALUES
(2, 5, '10:00', '16:00'),
(2, 6, '10:00', '16:00'); 

INSERT INTO appointments (user_id, salon_id, employee_id, service_id, appointment_date, start_time, end_time, is_confirmed) 
VALUES (4, 1, 1, 1, CURDATE() + INTERVAL 1 DAY, '10:00', '10:30', FALSE);