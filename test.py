from database import Database

db = Database()

token = db.generate_token("test", "test")
print(token)
db.verify_token(token)