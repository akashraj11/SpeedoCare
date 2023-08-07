""" 
NotificationS routes
"""
from flask import request, jsonify
from API.database.models.NotificationModel import Notification
from API.database.connection.config import get_connection
from flask import Blueprint

notification_blueprint = Blueprint('notifications', __name__)

#Fetch all notifications
@notification_blueprint.route("/notifications", methods=["GET"])
def get_notifications():
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM notifications"
        cursor.execute(query)
        result = cursor.fetchall()

        notifications_data = []
        for row in result:
            notification = {
                "notification_id": row[0],        # Access columns by index
                "notification_date": row[1],
                "user_id": row[2],
                "from_": row[3],                  # Access columns by index
                "to_": row[4],                    # Access columns by index
                "cc": row[5],
                "bcc": row[6],
                "subject": row[7],
                "body": row[8],
                "digital_image": row[9],
            }
            notifications_data.append(notification)

        cursor.close()
        connection.close()

        return jsonify(notifications_data), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error retrieving notifications"}), 500



# Create a new notification
@notification_blueprint.route("/notifications", methods=["POST"])
def create_notification():
    try:
        data = request.get_json()
        #print("Received data:", data)  # Debug message
        if not data:
            return jsonify({"message": "Request data is missing"}), 400

        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "INSERT INTO notifications (notification_date, user_id, from_, to_, cc, bcc, subject, body, digital_image) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            data['notification_date'],
            data['user_id'],
            data['from_'],  # Use 'from_' instead of 'from'
            data['to_'],
            data['cc'],
            data['bcc'],
            data['subject'],
            data['body'],
            data['digital_image'],
        )
       # print("Executing query:", query)  # Debug message
        #print("Query values:", values)  # Debug message

        # Execute the query
        cursor.execute(query, values)

        # Commit the changes to the database
        connection.commit()

        # Close the database connection
        connection.close()

        # Return a success response
        return jsonify({"message": "Notification created successfully"}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error creating the notification"}), 500
    
# Get a specific notification by notification_id
@notification_blueprint.route('/notifications/notify/<int:notification_id>', methods=['GET'])
def get_notification_by_id(notification_id):
#@api_blueprint.route('/notifications/<int:notification_id>', methods=['GET'])
#def get_notification(notification_id):
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM notifications WHERE notification_id = %s"
        cursor.execute(query, (notification_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            notification = {
                "notification_id": result[0],      # Access columns by index
                "notification_date": result[1],
                "user_id": result[2],
                "from_": result[3],                # Access columns by index
                "to_": result[4],                  # Access columns by index
                "cc": result[5],
                "bcc": result[6],
                "subject": result[7],
                "body": result[8],
                "digital_image": result[9],
            }
            return jsonify(notification), 200
        else:
            return jsonify({"message": "Notification not found."}), 404

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error retrieving the notification"}), 500
    
# Update a notification by notification_id
@notification_blueprint.route('/notifications/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    data = request.get_json()
    
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM notifications WHERE notification_id = %s"
        cursor.execute(query, (notification_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            notification = {
                "notification_id": result[0],      # Access columns by index
                "notification_date": result[1],
                "user_id": result[2],
                "from_": result[3],                # Access columns by index
                "to_": result[4],                  # Access columns by index
                "cc": result[5],
                "bcc": result[6],
                "subject": result[7],
                "body": result[8],
                "digital_image": result[9],
            }

            # Update the notification with the new data
            notification['notification_date'] = data['notification_date']
            notification['user_id'] = data['user_id']
            notification['from_'] = data['from_']
            notification['to_'] = data['to_']
            notification['cc'] = data['cc']
            notification['bcc'] = data['bcc']
            notification['subject'] = data['subject']
            notification['body'] = data['body']
            notification['digital_image'] = data['digital_image']

            # Update the notification in the database
            connection = get_connection()
            cursor = connection.cursor()

            query = "UPDATE notifications SET notification_date = %s, user_id = %s, from_ = %s, to_ = %s, cc = %s, bcc = %s, subject = %s, body = %s, digital_image = %s WHERE notification_id = %s"
            values = (
                notification['notification_date'],
                notification['user_id'],
                notification['from_'],
                notification['to_'],
                notification['cc'],
                notification['bcc'],
                notification['subject'],
                notification['body'],
                notification['digital_image'],
                notification_id,
            )

            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify(notification), 200
        else:
            return jsonify({"message": "Notification not found."}), 404

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error updating the notification"}), 500
    
    
# Get notifications by user_id
@notification_blueprint.route('/notifications/user/<int:user_id>', methods=['GET'])
def get_notifications_by_user(user_id):
    try:
        print("Attempting to retrieve notifications for user_id:", user_id)

        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM notifications WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        print("Query result:", result)

        if not result:
            print("No notifications found for user_id:", user_id)
            return jsonify({"message": "No notifications found for the given user_id."}), 404

        notifications_data = []
        for row in result:
            notification = {
                "notification_id": row[0],        # Access columns by index
                "notification_date": row[1],
                "user_id": row[2],
                "from_": row[3],                  # Access columns by index
                "to_": row[4],                    # Access columns by index
                "cc": row[5],
                "bcc": row[6],
                "subject": row[7],
                "body": row[8],
                "digital_image": row[9],
            }
            notifications_data.append(notification)

        cursor.close()
        connection.close()

        print("Notifications retrieved successfully for user_id:", user_id)
        return jsonify(notifications_data), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error retrieving notifications for the user"}), 500

# Update notifications by user_id
@notification_blueprint.route("/notifications/user/<int:user_id>", methods=["PUT"])
def update_notifications_by_user(user_id):
    data = request.get_json()

    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM notifications WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        if not results:
            return jsonify({"message": "No notifications found for the given user_id."}), 404

        notifications = []
        for result in results:
            notification = {
                "notification_id": result[0],      # Access columns by index
                "notification_date": result[1],
                "user_id": result[2],
                "from_": result[3],                # Access columns by index
                "to_": result[4],                  # Access columns by index
                "cc": result[5],
                "bcc": result[6],
                "subject": result[7],
                "body": result[8],
                "digital_image": result[9],
            }
            notifications.append(notification)

        # Update all notifications for the user with the new data
        for notification in notifications:
            notification['notification_date'] = data['notification_date']
            notification['from_'] = data['from_']
            notification['to_'] = data['to_']
            notification['cc'] = data['cc']
            notification['bcc'] = data['bcc']
            notification['subject'] = data['subject']
            notification['body'] = data['body']
            notification['digital_image'] = data['digital_image']

        # Update the notifications in the database
        cursor = connection.cursor()

        query = "UPDATE notifications SET notification_date = %s, from_ = %s, to_ = %s, cc = %s, bcc = %s, subject = %s, body = %s, digital_image = %s WHERE user_id = %s"
        values_list = [(n['notification_date'], n['from_'], n['to_'], n['cc'], n['bcc'], n['subject'], n['body'], n['digital_image'], user_id) for n in notifications]

        cursor.executemany(query, values_list)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify(notifications), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error updating notifications for the user"}), 500

 # Update a notification by User_id and then specific notification_id
# Update a specific notification for a user by notification_id
@notification_blueprint.route("/notifications/<int:user_id>/<int:notification_id>", methods=["PUT"])
def update_notification_for_user(user_id, notification_id):
    data = request.get_json()

    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"message": "Error connecting to the database"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM notifications WHERE user_id = %s AND notification_id = %s"
        cursor.execute(query, (user_id, notification_id))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "Notification not found for the given user_id and notification_id."}), 404

        notification = {
            "notification_id": result[0],      # Access columns by index
            "notification_date": result[1],
            "user_id": result[2],
            "from_": result[3],                # Access columns by index
            "to_": result[4],                  # Access columns by index
            "cc": result[5],
            "bcc": result[6],
            "subject": result[7],
            "body": result[8],
            "digital_image": result[9],
        }

        # Update the notification with the new data
        notification['notification_date'] = data['notification_date']
        notification['from_'] = data['from_']
        notification['to_'] = data['to_']
        notification['cc'] = data['cc']
        notification['bcc'] = data['bcc']
        notification['subject'] = data['subject']
        notification['body'] = data['body']
        notification['digital_image'] = data['digital_image']

        # Update the notification in the database
        query = "UPDATE notifications SET notification_date = %s, from_ = %s, to_ = %s, cc = %s, bcc = %s, subject = %s, body = %s, digital_image = %s WHERE user_id = %s AND notification_id = %s"
        values = (
            notification['notification_date'],
            notification['from_'],
            notification['to_'],
            notification['cc'],
            notification['bcc'],
            notification['subject'],
            notification['body'],
            notification['digital_image'],
            user_id,
            notification_id
        )

        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify(notification), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error updating the notification for the user"}), 500
