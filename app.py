#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 20:50:39 2019

@author: harriet
"""


from flask import Flask, render_template
app = Flask(__name__)

def manage_result(data):
    import datetime
    number_asteroids = data['element_count']
    asteroids_dict = {}
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    
    for item in data['near_earth_objects'][date]:
        
        asteroid_name = item['name']
        diameter = (item['estimated_diameter']['kilometers']['estimated_diameter_min'] + item['estimated_diameter']['kilometers']['estimated_diameter_max']) / 2
        hazardous = item['is_potentially_hazardous_asteroid']
        speed = round(float(item['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))
        miss_distance = item['close_approach_data'][0]['miss_distance']['kilometers']
        asteroids_dict[asteroid_name] = diameter, hazardous, speed, miss_distance
        
    hazard_count = 0
    
    for item in data['near_earth_objects'][date]:
        if item ['is_potentially_hazardous_asteroid'] == True:
            hazard_count += 1
    
    return number_asteroids, asteroids_dict, hazard_count


@app.route("/")
def index():
    return render_template("index.html", title="Asteroid Watch")


@app.route("/result")
def result():
    import requests
    endpoint = "https://api.nasa.gov/neo/rest/v1/feed/today?detailed=true&api_key=WyVsafj4w6SQYVarw6xOzp54OwYtuVUhXA90AzSV"
    response = requests.get(endpoint)
    data = response.json()
    if response.status_code == 200:
        number_asteroids, asteroids_dict, hazard_count = manage_result(data)
    return render_template("result.html", title="Asteroid Check", **locals())


if __name__ == "__main__":
    app.run(debug=True)