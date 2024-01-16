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
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": []
            }

            for hero_power in hero.powers:
                power_dict = {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description
                }
                hero_dict["powers"].append(power_dict)

            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)

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

        if power:

            for attr in request.form:
                setattr(power, attr, request.form.get(attr))
            
            db.session.add(power)
            db.session.commit()

            power_dict = power.to_dict()

            return make_response(power_dict, 200)
        
        else:
            return make_response({"error" : "Power not found"}, 404)
        
api.add_resource(PowersById, '/powers/<int:id>')

class HeroPowers(Resource):

    def get(self):

        hero_powers = []

        for hero_power in HeroPower.query.all():

            hero_power_dict =  {
                "id": hero_power.id,
                "strength": hero_power.strength,
                "hero_id": hero_power.hero_id,
                "power_id": hero_power.power_id
            }

            hero_powers.append(hero_power_dict)
        
        return make_response(hero_powers, 200)
    
    def post(self):

        data = request.get_json()
        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']

        new_power = HeroPower(strength = strength, power_id = power_id, hero_id = hero_id)

        db.session.add(new_power)
        db.session.commit()

        new_power_dict = new_power.to_dict()

        print(new_power_dict)

        return make_response(jsonify(new_power_dict), 201)
        

api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555,debug=True)
