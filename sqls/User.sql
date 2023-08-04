-- Table for User
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact_no VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    encrypted_password VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    user_role VARCHAR(20) NOT NULL
);

-- Table for Patient
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    prescriptions TEXT,
    details TEXT,
    medical_history TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- Table for ClinicAdmin
CREATE TABLE clinic_admins (
    clinic_admin_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    clinic_internal_id VARCHAR(50) NOT NULL,
    clinic_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- Table for Doctor
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    clinic_id INT NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);



-- Modify patients table
ALTER TABLE patients
DROP FOREIGN KEY patients_ibfk_1;

ALTER TABLE patients
ADD CONSTRAINT patients_ibfk_1
FOREIGN KEY (user_id)
REFERENCES users (user_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Modify clinic_admins table
ALTER TABLE clinic_admins
DROP FOREIGN KEY clinic_admins_ibfk_1;

ALTER TABLE clinic_admins
ADD CONSTRAINT clinic_admins_ibfk_1
FOREIGN KEY (user_id)
REFERENCES users (user_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Modify doctors table
ALTER TABLE doctors
DROP FOREIGN KEY doctors_ibfk_1;

ALTER TABLE doctors
ADD CONSTRAINT doctors_ibfk_1
FOREIGN KEY (user_id)
REFERENCES users (user_id)
ON DELETE CASCADE
ON UPDATE CASCADE;
