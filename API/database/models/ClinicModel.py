from API.database.connection.config import get_connection

class Clinic:
    def __init__(self, clinic_id, location, clinic_name, description):
        self.clinic_id = clinic_id
        self.location = location
        self.clinic_name = clinic_name
        self.description = description

    @classmethod
    def from_db(cls, data):
        return cls(*data)

    def to_dict(self):
        return {
            "clinic_id": self.clinic_id,
            "location": self.location,
            "clinic_name": self.clinic_name,
            "description": self.description,
        }

    @classmethod
    def get_all_clinics(cls):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM clinics")
        clinics_data = cursor.fetchall()
        cursor.close()
        connection.close()

        return [cls.from_db(data) for data in clinics_data]

    @classmethod
    def get_clinic_by_id(cls, clinic_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM clinics WHERE clinic_id = %s", (clinic_id,))
        clinic_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if clinic_data:
            return cls.from_db(clinic_data)
        else:
            return None

    @classmethod
    def get_clinic_by_Name(cls, clinic_name):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clinics WHERE clinic_name LIKE %s", ('%' + clinic_name + '%',))
        clinic_data_list = cursor.fetchall()  # Fetch all matching rows
        cursor.close()
        connection.close()

        clinics = []
        for clinic_data in clinic_data_list:
            clinic = cls.from_db(clinic_data)
            clinics.append(clinic)

        return clinics


    def save(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO clinics (location, clinic_name, description) VALUES (%s, %s, %s)",
            (self.location, self.clinic_name, self.description),
        )
        connection.commit()
        cursor.close()
        connection.close()

    def update(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE clinics SET location = %s, clinic_name = %s, description = %s WHERE clinic_id = %s",
            (self.location, self.clinic_name, self.description, self.clinic_id),
        )
        connection.commit()
        cursor.close()
        connection.close()

    def delete(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM clinics WHERE clinic_id = %s", (self.clinic_id,))
        connection.commit()
        cursor.close()
        connection.close()
