class User:
    def __init__(self, user_id, username, first_name, last_name, contact_no, email, encrypted_password, address, date_of_birth, user_role):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.contact_no = contact_no
        self.email = email
        self.encrypted_password = encrypted_password
        self.address = address
        self.date_of_birth = date_of_birth
        self.user_role = user_role
        self.patient = None
        self.clinic_admin = None
        self.doctor = None
        
    def get_id(self):
        return str(self.user_id)

    def is_authenticated(self):
        return True  # Replace with your logic for user authentication

    def is_active(self):
        return True  # Replace with your logic for active/inactive users

    def is_anonymous(self):
        return False        