from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    

@login.user_loader
def load_user(id: int) -> User:
    return db.session.get(User, int(id))

class Manufacturer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    website: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))

    def __repr__(self) -> str:
        return '<Manufacturer {}>'.format(self.name)
    
class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))

    def __repr__(self) -> str:
        return '<Category {}>'.format(self.name)

class Location(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))

    def __repr__(self) -> str:
        return '<Location {}>'.format(self.name)
    
class Financing(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)

    cost: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    price: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    markupPercent: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    markupDollars: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)

    def __repr__(self) -> str:
        return '<Financing {}>'.format(self.name)

class Stock(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    product_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('product.id'))
    quantityInStock: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    quantityOnOrder: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    reorderLevel: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)

    def __repr__(self) -> str:
        return '<Stock {}>'.format(self.product_id)
    
class Product(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    manufacturer_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('manufacturer.id'))
    category_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('category.id'))
    location_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('location.id'))
    financing_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('financing.id'))
    stock_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('stock.id'))

    def __repr__(self) -> str:
        return '<Product {}>'.format(self.name)
