import uuid
from core import db
from sqlalchemy_utils import UUIDType

class TodoModel(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key = True, default=uuid.uuid4)
    created_by = db.Column(UUIDType(binary=False), db.ForeignKey('user_model.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)
    status = db.Column(db.Boolean, default = False)
    
    def __init__(self, created_by, title, desc):
        self.created_by = created_by
        self.title = title
        self.desc = desc
    
    def __repr__(self) -> str:
        return f'<User: {self.title}>'
    