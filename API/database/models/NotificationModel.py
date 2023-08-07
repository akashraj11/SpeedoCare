"""
Models for Notification
"""

class Notification:
    def __init__(self, notification_id, notification_date, user_id, from_, to, cc, bcc, subject, body, digital_image):
        self.notification_id = notification_id
        self.notification_date = notification_date
        self.user_id = user_id
        self.from_ = from_
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.body = body
        self.digital_image = digital_image

