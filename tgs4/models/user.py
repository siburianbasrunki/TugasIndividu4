import bcrypt
from sqlalchemy import Column, Integer, Text
from .meta import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    password_hash = Column(Text)

    def set_password(self, password):
        # Hash password dan simpan dalam bentuk hash
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Memeriksa apakah password yang diberikan cocok dengan hash yang tersimpan
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
