import logging
import random
from locust import HttpUser, task, between
from statistics import mean, stdev
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/people/<person_id>')
def get_person(person_id):
    try:
        if person_id == "1":
            resp = {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/6/",
                    "https://swapi.dev/api/films/3/",
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/7/"
                ],
                "species": [
                    "https://swapi.dev/api/species/1/"
                ],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/14/",
                    "https://swapi.dev/api/vehicles/30/"
                ],
                "starships": [
                    "https://swapi.dev/api/starships/12/",
                    "https://swapi.dev/api/starships/22/"
                ],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.dev/api/people/1/"
            }
            return resp, 200
        # processing 404s 
        return 'NOT_FOUND', 404
    except Exception as e:
        logging.error(str(e))
        return 'SERVER_ERROR', 500

@app.route('/planets/<planet_id>')
def get_planet(planet_id):
    try:
        if planet_id == "3":
             #OR load test like this: time.sleep(random.uniform(0.01, 0.1))
            resp = {
                "name": "Yavin IV",
                "rotation_period": "24",
                "orbital_period": "4818",
                "diameter": "10200",
                "climate": "temperate, tropical",
                "gravity": "1 standard",
                "terrain": "jungle, rainforests",
                "surface_water": "8",
                "population": "1000",
                "residents": [],
                "films": [
                    "https://swapi.dev/api/films/1/"
                ],
                "created": "2014-12-10T11:37:19.144000Z",
                "edited": "2014-12-20T20:58:18.421000Z",
                "url": "https://swapi.dev/api/planets/3/"
            }
            return resp, 200
        # same 404
        return 'NOT_FOUND', 404
    except Exception as e:
        logging.error(str(e))
        return 'SERVER_ERROR', 500
    
@app.route('/starships/<starship_id>')
def get_starship(starship_id):
    try:
        if int(starship_id) > 100:
            error_resp = {
                "error": "Starship not found.",
                "message": f"No starship with id {starship_id} exists."
            }
            return error_resp, 404
        
        resp = {
            "name": "Millennium Falcon",
            "model": "YT-1300 light freighter",
            "manufacturer": "Corellian Engineering Corporation",
            "cost_in_credits": "100000",
            "length": "34.37",
            "max_atmosphering_speed": "1050",
            "crew": "4",
            "passengers": "6",
            "cargo_capacity": "100000",
            "consumables": "2 months",
            "hyperdrive_rating": "0.5",
            "MGLT": "75",
            "starship_class": "Light freighter",
            "pilots": [
                "https://swapi.dev/api/people/13/",
                "https://swapi.dev/api/people/14/",
                "https://swapi.dev/api/people/25/",
                "https://swapi.dev/api/people/31/"
            ],
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/2/",
                "https://swapi.dev/api/films/3/"
            ],
            "created": "2014-12-10T16:59:45.094000Z",
            "edited": "2014-12-20T21:23:49.880000Z",
            "url": f"https://swapi.dev/api/starships/{starship_id}/"
        }
        return resp, 200
    except Exception as e:
        logging.error(str(e))
        return 'SERVER_ERROR', 500


logging.basicConfig(filename='flask.log',level=logging.DEBUG)
app.run()

class LoadTest(HttpUser):
    wait_time = between(0.1, 2)
    
    @task
    def test_endpoint(self):
        person_id = random.choice(["1", "2", "3"])
        self.client.get(f"/people/{person_id}")
        
        planet_id = random.choice(["1", "2", "3"])
        self.client.get(f"/planets/{planet_id}")
        
        starship_id = str(random.randint(1, 100))
        self.client.get(f"/starships/{starship_id}")
    def on_start(self):
        person_id = random.choice(["1", "2", "3"])
        self.client.get(f"/people/{person_id}")
        self.response_times = []

    def on_stop(self):
        mean_response_time = mean(self.response_times)
        stdev_response_time = stdev(self.response_times)
        print(f"Mean Response Time: {mean_response_time} ms")
        print(f"Standard Deviation of Response Time: {stdev_response_time} ms")

    def on_request_success(self, request_type, name, response_time, response_length):
        self.response_times.append(response_time)

