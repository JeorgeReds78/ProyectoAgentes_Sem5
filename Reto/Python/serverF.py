"""
    Server for simulation using flask.

    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 22/11/2022
    Last Modification: 2/12/2022
"""

from flask import Flask, request, jsonify # Flask is a micro web framework written in Python
from model import *  # Model is the class that contains the model
from agents import * # Agents is the class that contains the agents

PORT = 8585 # Port to use

# Constants
numberOfCars = 4

classModel = None # Model object that the agent is a part of. (Model)

currentStep = 0 # Current step of the simulation

app = Flask("Server") # Create a Flask object

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, classModel, numberOfCars

    if request.method == 'POST':
        numberOfCars = int(request.form.get('MAXCARS'))
        currentStep = 0

        print(request.form)
        classModel = Model(numberOfCars)
        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getCars', methods=['GET'])
def getCars():
    global classModel

    if request.method == 'GET':
        carsPositions = []
        for (a, x, z) in classModel.grid.coord_iter():
            for agent in a:
                if isinstance(agent, Car):
                    carsPositions.append({
                        "id": str(agent.unique_id),
                        "x": x,
                        "y": 1,
                        "z": z,
                        "arrived": bool(agent.arrived),
                        "status": bool(agent.status),
                        "facing": str(agent.facing)})

        return jsonify({'positions':carsPositions})

@app.route('/getRoads', methods=['GET'])
def getRoads():
    global classModel

    if request.method == 'GET':
        roadsPositions = []
        for (a, x, z) in classModel.grid.coord_iter():
            for agent in a:
                if isinstance(agent, Road):
                    roadsPositions.append({
                        "id": str(agent.unique_id),
                        "x": x,
                        "y": 1,
                        "z": z})

        return jsonify({'positions':roadsPositions})

@app.route('/getTraficlights', methods=['GET'])
def getTraficlights():

    global classModel

    if request.method == 'GET':
        TLPositions = []
        for (a, x, z) in classModel.grid.coord_iter():
            for agent in a:
                if isinstance(agent, Traffic_Light):
                    TLPositions.append({
                        "id": str(agent.unique_id),
                        "x": x,
                        "y": 1,
                        "z": z,
                        "state": bool(agent.state)})

        return jsonify({'positions':TLPositions})  

@app.route('/getDestination', methods=['GET'])
def getDestination():

    global classModel

    if request.method == 'GET':
        destinationPositions = []
        for (a, x, z) in classModel.grid.coord_iter():
            for agent in a:
                if isinstance(agent, Destination):
                    destinationPositions.append({
                        "id": str(agent.unique_id),
                        "x": x,
                        "y": 1,
                        "z": z})

        return jsonify({'positions':destinationPositions}) 

@app.route('/getObstacles', methods=['GET'])
def getObstacles():

    global classModel

    if request.method == 'GET':
        obstaclesPositions = []
        for (a, x, z) in classModel.grid.coord_iter():
            for agent in a:
                if isinstance(agent, Obstacle):
                    obstaclesPositions.append({
                        "id": str(agent.unique_id),
                        "x": x,
                        "y": 1,
                        "z": z})

        return jsonify({'positions':obstaclesPositions})  

@app.route('/update', methods=['GET'])
def updateModel():

    global currentStep, classModel
    if request.method == 'GET':
        classModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port = PORT, debug=True)