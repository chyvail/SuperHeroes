import sys
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, app
from models import Hero, Power, HeroPower

with app.app_context():

    # Create heroes
    hero1 = Hero(name='Superman', super_name='Clark Kent')
    hero2 = Hero(name='Batman', super_name='Bruce Wayne')
    hero3 = Hero(name='Wonder Woman', super_name='Diana Prince')

    # Create powers
    power1 = Power(name='Flight', description='Ability to fly through the air.')
    power2 = Power(name='Super Strength', description='Enhanced physical strength.')
    power3 = Power(name='Invisibility', description='Ability to become invisible.')

    # Create hero powers
    hero_power1 = HeroPower(strength='Strong', hero=hero1, power=power1)
    hero_power2 = HeroPower(strength='Average', hero=hero2, power=power2)
    hero_power3 = HeroPower(strength='Weak', hero=hero3, power=power3)

    # Add objects to the session
    db.session.add_all([hero1, hero2, hero3, power1, power2, power3, hero_power1, hero_power2, hero_power3])

    # Commit the changes
    db.session.commit()


    print("🦸‍♀️ Done seeding!")

