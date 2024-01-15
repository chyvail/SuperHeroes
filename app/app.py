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

class HeroesById(Resource):

    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()

        if hero:
            hero_dict = hero.to_dict()

            response = make_response(
                jsonify(hero_dict),
                200
            )

            response.headers["Content-Type"] = "application/json"

            return response
        
        else:
            return make_response({"error":"Hero not found"},404)

api.add_resource(HeroesById, '/heroes/<int:id>')

class Powers(Resource):

    def get(self):

        powers = []

        for power in Power.query.all():

            power_dict = {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }

            powers.append(power_dict)

        return make_response(jsonify(powers),200)

api.add_resource(Powers, '/powers')

class PowersById(Resource):
    
    def get(self, id):

        power = Power.query.filter(Power.id == id).first()

        if power:
            power_dict = power.to_dict()
            return make_response(power_dict,200)
        else:
            return make_response({"error":"Power not found"}, 404)
    
    def patch(self, id):

        power = Power.query.filter(Power.id == id).first()

        for attr in request.form:
            setattr(power, attr, request.form.get(attr))
        
        db.session.add(power)
        db.session.commit()

        power_dict = power.to_dict()

        return make_response(power_dict, 200)
        

api.add_resource(PowersById, '/powers/<int:id>')

if __name__ == '__main__':
    app.run(port=5555,debug=True)
