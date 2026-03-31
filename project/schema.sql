CREATE DATABASE IF NOT EXISTS skin_diagnosis_db;
USE skin_diagnosis_db;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'user',
  is_active_user BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diseases (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL,
  category VARCHAR(50) NOT NULL,
  description TEXT NOT NULL,
  remedies TEXT NOT NULL,
  precautions TEXT NOT NULL,
  doctor_advice TEXT NOT NULL,
  validated BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE remedies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  disease_id INT NOT NULL,
  remedy_name VARCHAR(150) NOT NULL,
  details TEXT NOT NULL,
  reference_url VARCHAR(255),
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
);

CREATE TABLE chatbot_knowledge (
  id INT AUTO_INCREMENT PRIMARY KEY,
  question_pattern VARCHAR(255) NOT NULL,
  answer TEXT NOT NULL,
  category VARCHAR(50) NOT NULL
);

CREATE TABLE analysis_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  image_path VARCHAR(255),
  symptoms TEXT,
  predicted_disease VARCHAR(120) NOT NULL,
  confidence FLOAT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE disease_update_requests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  disease_id INT NOT NULL,
  expert_id INT NOT NULL,
  update_notes TEXT NOT NULL,
  reference VARCHAR(255),
  approved BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE,
  FOREIGN KEY (expert_id) REFERENCES users(id) ON DELETE CASCADE
);
