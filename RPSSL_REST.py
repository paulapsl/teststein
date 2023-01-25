from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)  # Die Flask API

# Speichert den Score zu bestimmten Namen
score = {}


class SimpleNameScore(Resource):
    def get(self, name=""):
        if name in score:
            return {name: score[name]}
        if name == "":
            return {score}
        return {"Message": "Nicht vorhanden"}

    def put(self, name):
        existing = name in score
        score[name] = request.form['score']
        if existing:
            return {"Message": "Überschrieben"}
        return {"Message": "Neu hinzugefügt"}

    def delete(self, name):
        del score[name]
        return {"Message": "%s gelöscht" % name}

    def patch(self, name):  # Hier das gleiche wie put, weil ja nur ein Attribut (score) vorhanden ist
        score[name] = request.form['score']
        return {"Message": "%s gepatched" % name}


# Hier passiert das Mapping auf die Klasse
api.add_resource(SimpleNameScore, '/score/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)  # debug=True lädt nach den Änderungen neu
