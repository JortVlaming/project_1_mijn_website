import base64, time
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

class Database:
    def __init__(self):
        load_dotenv()

        self.db_config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_DATABASE"),
        }

        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id BIGINT UNIQUE PRIMARY KEY AUTO_INCREMENT,
                username TEXT(20) UNIQUE NOT NULL,
                displayname TEXT(40),
                password_hash TEXT,
                opleiding TEXT(20),
                aboutme TINYTEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME DEFAULT (CURRENT_TIMESTAMP + INTERVAL 30 DAY),
                token TEXT UNIQUE NOT NULL,
                user_id BIGINT,
                password_hash TEXT,
                CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        self.userManager = UserManager(self)
        self.tokenManager = TokenManager(self)
        pass

    def get_db_connection(self):
        return mysql.connector.connect(**self.db_config)

class UserManager:
    def __init__(self, db:Database):
        self.db = db
        pass

    def add_user(self, username, displayname, password_hash, opleiding, aboutme):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users(username, displayname, password_hash, opleiding, aboutme) VALUES (%s, %s, %s, %s, %s)", (username, displayname, password_hash, opleiding, aboutme,))

        result = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        if result is None:
            return False
        elif len(result) == 0:
            return False

        return True

    def user_exists(self, *args):
        if len(args) == 0:
            return False

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        if isinstance(args[0], int):
            cursor.execute("SELECT * FROM users WHERE id = %s", (args[0],))
        elif isinstance(args[0], str):
            cursor.execute("SELECT * FROM users WHERE username = %s", (args[0],))
        else:
            return False

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return False

        return True

    def search_for_users(self, query):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username LIKE %s", ("%{}%".format(query),))

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    def verify_login(self, username: str, password: str):
        if not self.user_exists(username):
            return False

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return check_password_hash(result, password)

    def username_to_id(self, username:str) -> int|None:
        if not self.user_exists(username):
            return None

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))

        result = cursor.fetchone()

        if result is None:
            return None

        if len(result) == 0:
            return None

        return result[0]

    def get_user_information(self, *args):
        if len(args) == 0:
            return False

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        if isinstance(args[0], int):
            cursor.execute("SELECT id, username, displayname, opleiding, aboutme FROM users WHERE id = %s", (args[0],))
        elif isinstance(args[0], str):
            cursor.execute("SELECT id, username, displayname, opleiding, aboutme FROM users WHERE username = %s", (args[0],))
        else:
            return False

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return None

        return User(result[0], result[1], result[2], result[3], result[4])

class User:
    def __init__(self, id:int, username: str, displayName: str, opleiding: str, aboutme: str):
        self.id = id
        self.username = username
        self.displayName = displayName
        self.opleiding = opleiding
        self.aboutme = aboutme

class Post:
    def __init__(self, poster: str, post_id:int, content: str, posted: datetime=datetime.now(), deleted: bool=False):
        self.poster = poster
        self.post_id = post_id
        self.content = content
        self.posted = posted
        self.deleted = deleted

class TokenManager:
    def __init__(self, db:Database):
        self.db = db

    def generate_token(self, id:int, username: str, password: str) -> str:
        now = str(time.time())
        now_bytes = now.encode("ascii")
        now_b64 = base64.b64encode(now_bytes)

        id_b64 = base64.b64encode(str(id).encode("ascii"))
        username_b64 = base64.b64encode(username.encode("ascii"))
        password_b64 = base64.b64encode(password.encode("ascii"))

        token = now_b64 + b"." + id_b64 + b"." + username_b64 + b"." + password_b64

        token = token.decode("ascii")

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO tokens (token, user_id, password_hash) VALUES (%s, %s, %s)", (token, id, password,))

        conn.commit()
        cursor.close()
        conn.close()

        return token

    def verify_token(self, token: str|None) -> bool:
        if token is None:
            return False

        gen, UID, un, pwd = self.__extract_user_info_from_token(token)

        if not self.db.userManager.user_exists(un) and not self.db.userManager.user_exists(UID):
            return False

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tokens WHERE token = %s and user_id = %s and password_hash = %s", (token, UID, pwd,))

        result = cursor.fetchone()

        if result is None:
            return False

        cursor.close()
        conn.close()

        return True

    def token_to_user(self, token:str) -> User|None:
        if self.verify_token(token) is False:
            return None

        gen, UID, un, pwd = self.__extract_user_info_from_token(token)

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (UID,))

        result = cursor.fetchone()

        if result is None:
            return None

        if len(result) == 0:
            return None

        cursor.close()
        conn.close()

        return User(result[0], result[1], result[2], result[4], result[5])

    def __extract_user_info_from_token(self, token:str) -> tuple|None:
        if token is None:
            return None

        split = token.split(".")
        gen_b64 = split[0]
        id_b64 = split[1]
        un_b64 = split[2]
        pwd_b64 = split[3]

        gen = base64.b64decode(gen_b64.encode("ascii")).decode("ascii")
        id = base64.b64decode(id_b64.encode("ascii")).decode("ascii")
        un = base64.b64decode(un_b64.encode("ascii")).decode("ascii")
        pwd = base64.b64decode(pwd_b64.encode("ascii")).decode("ascii")

        return (gen, id, un, pwd)


