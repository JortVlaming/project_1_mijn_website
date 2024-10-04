import base64, time
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv

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
                expires_at DATETIME DEFAULT DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 30 DAY),
                token TEXT UNIQUE NOT NULL
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

class User:
    def __init__(self, id:int, username: str, naam: str, opleiding: str, aboutme: str):
        self.id = id
        self.username = username
        self.naam = naam
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

        cursor.execute("INSERT INTO tokens (token) VALUES (%s)", (token,))

        cursor.close()
        conn.close()

        return token

    def verify_token(self, token: str|None) -> bool:
        if token is None:
            return False
        split = token.split(".")

        gen_b64 = split[0]
        id_b64 = split[1]
        un_b64 = split[2]
        pwd_b64 = split[3]

        gen = base64.b64decode(gen_b64.encode("ascii")).decode("ascii")
        id = base64.b64decode(id_b64.encode("ascii")).decode("ascii")
        un = base64.b64decode(un_b64.encode("ascii")).decode("ascii")
        pwd = base64.b64decode(pwd_b64.encode("ascii")).decode("ascii")

        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tokens WHERE token = %s", (token,))

        result = cursor.fetchone()

        if (result is None):
            return False

        print(result)

        cursor.close()
        conn.close()

        return True

    def token_to_user(self, token:str) -> User|None:
        if self.verify_token(token) is False:
            return None
        if token is None:
            return None

        split = token.split(".")
        gen_b64 = split[0]
        un_b64 = split[1]
        pwd = split[2]

        gen = base64.b64decode(gen_b64.encode("ascii")).decode("ascii")
        un = base64.b64decode(un_b64.encode("ascii")).decode("ascii")
        pwd = base64.b64decode(pwd.encode("ascii")).decode("ascii")

