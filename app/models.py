from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('HeroPower', backref='hero')

    serialize_rules = ('-powers.hero',)

    def __repr__(self):
        return f'<Hero id: {self.id} , name is {self.name} and alias is {self.super_name} >'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_power = db.relationship('HeroPower', backref='power')

    serialize_rules = ('-hero_powers.power',)
    
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20 :
            raise ValueError("Description must have more than 20 characters")
        return description
    
    def __repr__(self):
        return f'<Power id: {self.id} , name is {self.name}  and description is {self.description} >'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    serialize_rules = ('-hero.powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Value not valid. Provide either Strong, Weak or Average")
        return strength

    def __repr__(self):
        return f'<HeroPower id: {self.id} , strength is {self.strength} >'


