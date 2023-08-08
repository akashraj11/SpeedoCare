-- Table for Appointments
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    clinic_id INT NOT NULL,
    booking_date DATE NOT NULL,
    booking_information TEXT,
    comment TEXT,
    price DECIMAL(10, 2),
    status VARCHAR(20),
    follow_up_req VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id),
    FOREIGN KEY (clinic_id) REFERENCES clinic_admins (clinic_id)
);


ALTER TABLE clinic_admins
ADD INDEX clinic_admins_clinic_id_idx (clinic_id);