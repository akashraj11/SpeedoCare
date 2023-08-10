CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    clinic_id INT NOT NULL,
    rating INT NOT NULL,
    review_text TEXT,
    reported BOOLEAN NOT NULL,
    reviewed_for DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id),
    FOREIGN KEY (clinic_id) REFERENCES clinics (clinic_id)
);