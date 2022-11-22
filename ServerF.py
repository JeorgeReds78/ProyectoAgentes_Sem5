"""
    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 16/11/2022
    Last Modification: 21/11/2022
"""

from flask import Flask, request, jsonify # Flask is a micro web framework written in Python
from Ordenador import * # Import the class Ordenador

PORT = 8585 # Port to use

# Constants
number_boxes = 10 # Number of boxes
width = 30 # Width of the grid
height = 30 # Height of the grid

classModel = None # Model object that the agent is a part of. (Model)

currentStep = 0 # Current step of the simulation

app = Flask("Server") # Create a Flask object

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    """ Initialize a new model.

    Args:
        None

    Returns:
        Json
    """
    global currentStep, classModel, number_boxes, width, height

    if request.method == 'POST':
        number_boxes = int(request.form.get('MAXBoxes'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0

        print(request.form)
        print(number_boxes, width, height)
        classModel = ModelClass(number_boxes, width, height)
        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getBots', methods=['GET'])
def getBots():
    """ Get the bots of the model.

    Args:
        None

    Returns:
        Json
    """
    global classModel

    if request.method == 'GET':
        botsPositions = []
        for (a, x, z) in classModel.grid.coord_iter():
            for agent in a:
                if isinstance(agent, Bot):
                    botsPositions.append({
                        "id": str(agent.unique_id),
                        "x": x,
                        "y": 1,
                        "z": z,
                        "hasBox": str(agent.hasBox)})


        return jsonify({'positions':botsPositions})

@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    """ Get the boxes of the model.

    Args:
        None

    Returns:
        Json
    """
    global classModel

    if request.method == 'GET':
        boxPositions = []
        for (a, x, z) in classModel.grid.coord_iter():
            for agent in a:
                if isinstance(agent, Box):
                    boxPositions.append({
                        "id": str(agent.unique_id),
                        "x": x,
                        "y": 1,
                        "z": z,
                        "pickable": str(agent.pickable)})

        return jsonify({'positions':boxPositions})  

@app.route('/update', methods=['GET'])
def updateModel():
    """ Update the model.

    Args:
        None

    Returns:
        Json
    """
    global currentStep, classModel
    if request.method == 'GET':
        classModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port = PORT, debug=True)