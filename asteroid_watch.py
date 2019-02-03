#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 20:50:39 2019

@author: harriet
"""
import requests
import datetime

from flask import Flask, render_template
app = Flask("MyApp")

def manage_result(data):
    number_asteroids = data['element_count']
    asteroids_dict = {}
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    
    print(date)
    
    for item in data['near_earth_objects'][date]:
        
        asteroid_name = item['name']
        diameter = (item['estimated_diameter']['kilometers']['estimated_diameter_min'] + item['estimated_diameter']['kilometers']['estimated_diameter_max']) / 2
        hazardous = item['is_potentially_hazardous_asteroid']
        speed = item['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
        miss_distance = item['close_approach_data'][0]['miss_distance']['kilometers']
        asteroids_dict[asteroid_name] = diameter, hazardous, speed, miss_distance
    
    return number_asteroids, asteroids_dict


@app.route("/")
def index():
    return render_template("index.html", title="Asteroid Watch")


@app.route("/result")
def result():
    endpoint = "https://api.nasa.gov/neo/rest/v1/feed/today?detailed=true&api_key=DEMO_KEY"
    response = requests.get(endpoint)
    data = response.json()
    result = manage_result(data)
    return render_template("result.html", title="Asteroid Check", **locals())


if __name__ == "__main__":
    app.run(debug=True)