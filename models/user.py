from clcrypto import password_hash, check_password
import re

class User:

    def __init__(self):
        self._id = -1
        self.username = ""
        self.email = ""
        self._hashed_password = ""

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=None):
        self._hashed_password = password_hash(password, salt)

    def check_password(self, pass_to_check):
        return check_password(pass_to_check, self.hashed_password)

    # Metody active record
    def save_to_db(self, cursor):
        if self.id == -1:
            # tworzymy wpis w bazie danych
            values = (self.username, self.email, self.hashed_password)
            query = """
            INSERT INTO Users(username, email, hashed_password)
            VALUES (%s, %s, %s)
            RETURNING id
            """
            cursor.execute(query, values)
            self._id = cursor.fetchone()[0]
        else:
            # aktualizujemy wpis w bazie danych
            values = (self.username, self.email, self.hashed_password, self.id)
            query = """
            UPDATE Users set username=%s, email=%s, hashed_password=%s
            WHERE id=%s
            """
            cursor.execute(query, values)

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (user_id,))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user._id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user._hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_mail(cursor, user_mail):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE email=%s"
        cursor.execute(sql, (user_mail,))  # (user_mail, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user._id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user._hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM users;"
        cursor.execute(sql)
        res = []
        for data in cursor:
            loaded_user = User()
            loaded_user._id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user._hashed_password = data[3]
            res.append(loaded_user)
        return res

    @classmethod
    def check_email(cls, email_to_check):
        return re.match(r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]{1,})*\.([a-zA-Z]{2,}){1}$', email_to_check)
