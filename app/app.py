#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    
    def get(self):
         
        response_dict = {
            "Message": "Super Heroes API",
        }
        
        response = make_response(
            response_dict,
            200,
        )

        return response

api.add_resource(Home, '/')

class Heroes(Resource):
    def get(self):

        heroes = []

        for hero in Hero.query.all():
            heroes_dict = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            }
            heroes.append(heroes_dict)

        response = make_response(
            jsonify(heroes),
            200
        )

        return response
    

api.add_resource(Heroes, '/heroes')


if __name__ == '__main__':
    app.run(port=5555,debug=True)
