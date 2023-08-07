use speedocare;
-- Table for notifications
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    notification_date DATE NOT NULL,
    user_id INT,
    from_ VARCHAR(255) NOT NULL,
    to_ VARCHAR(255) NOT NULL,
    cc VARCHAR(255),
    bcc VARCHAR(255),
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    digital_image VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
