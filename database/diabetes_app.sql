-- Create database
CREATE DATABASE IF NOT EXISTS diabetes_app;
USE diabetes_app;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- Diabetes data table for storing prediction results
CREATE TABLE IF NOT EXISTS diabetes_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pregnancies FLOAT NOT NULL,
    glucose FLOAT NOT NULL,
    blood_pressure FLOAT NOT NULL,
    skin_thickness FLOAT NOT NULL,
    insulin FLOAT NOT NULL,
    bmi FLOAT NOT NULL,
    pedigree FLOAT NOT NULL,
    age FLOAT NOT NULL,
    result VARCHAR(20) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);


