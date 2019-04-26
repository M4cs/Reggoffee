from flask import Flask, jsonify
from flask_restful import Api
import json

app = Flask(__name__)

@app.route("/")
def get():
    return jsonify({  "message": "Coffee Bot API" })

api = Api(app)

from app import resources

api.add_resource(resources.MadeCoffee, '/madecoffee')
api.add_resource(resources.OutOfCoffee, '/outofcoffee')
api.add_resource(resources.CheckStatus, '/status')
api.add_resource(resources.Leaderboard, '/leaderboard')
api.add_resource(resources.MyPoints, '/mypoints')
api.add_resource(resources.CoffeeHelp, '/help')

if __name__ == '__main__':
    app.run(host='0.0.0.0')