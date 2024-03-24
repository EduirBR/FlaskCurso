import uuid
from sqlalchemy_utils import UUIDType
from core import db

class UserModel(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key = True, default=uuid.uuid4)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
    
    def __repr__(self) -> str:
        return f'<User: {self.username}>'