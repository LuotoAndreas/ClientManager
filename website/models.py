from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pre_factura = db.Column(db.String(100))  # PRE FACTURA
    documento = db.Column(db.String(100))  # DOCUMENTO
    fecha_emision = db.Column(db.DateTime(timezone=True))  # Fecha Emisión
    pagado = db.Column(db.DateTime, nullable=True)  # Pagado
    ruc = db.Column(db.String(20))  # RUC
    compania = db.Column(db.String(200))  # Compania
    moneda = db.Column(db.String(50))  # Moneda
    cantidad = db.Column(db.Float)  # Cantidad
    precio_unitario = db.Column(db.Float)  # Precio Unitario
    parcial = db.Column(db.Float)  # Parcial
    igv = db.Column(db.Float)  # IGV
    total = db.Column(db.Float)  # Total
    descripcion = db.Column(db.Text)  # DESCRIPCIÓN
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key linking to User
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Record creation date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    clients = db.relationship('Client')
