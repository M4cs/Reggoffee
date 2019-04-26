from flask import request, jsonify
from flask_restful import Resource, reqparse
from app import app
from datetime import datetime
import pytz
import json

tz = pytz.timezone('America/New_York')
currentDT = datetime.now(tz)
now = currentDT.strftime("%I:%M:%S %p")

def change_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('left')
    return parser

class MadeCoffee(Resource):
    def post(self):
        data = request.form
        username = data['user_name']
        print(data['text'])
        if data['text'] == 'left':
            with open('app/status.json', 'r+') as json_file:
                obj = json.load(json_file)
                obj['leftpot']['status'] = "Last Pot Was Made At: %s*\n*%s made the pot this time." % (now, username)
                json_file.seek(0)
                json.dump(obj, json_file, indent=4)
                json_file.truncate()
                json_file.close()
        elif data['text'] == 'right':
            with open('app/status.json', 'r+') as json_file:
                obj = json.load(json_file)
                obj['rightpot']['status'] = "Last Pot Was Made At: %s\n%s made the pot this time." % (now, username)
                json_file.seek(0)
                json.dump(obj, json_file, indent=4)
                json_file.truncate()
                json_file.close()
        else:
            return jsonify({
                "text": "Error! Please try again, this time specify which pot you made it in!"
            })
        with open('app/leaderboard.json', 'r+') as json_file:
            obj = json.load(json_file)
            if username not in obj:
                obj[username] = 0
            obj[username] += 1
            json_file.seek(0)
            json.dump(obj, json_file, indent=4)
            json_file.truncate()
            json_file.close()
        return jsonify({
            "text": "Thank you {} for making some coffee in the left pot!".format(data['user_name'])
        })
        
class CheckStatus(Resource):
    def post(self):
        with open('app/status.json', 'r+') as json_file:
            data = json.load(json_file)
            leftstatus = data['leftpot']['status']
            rightstatus = data['rightpot']['status']
            print(leftstatus)
            json_file.close()
            return jsonify({
                "text": "*Current Status Of Coffee*",
                "attachments": [
                    {
                        "text": "*" + leftstatus + "*"
                    },
                    {
                        "text": "*" + rightstatus + "*"
                    }
                ]
            })

class Leaderboard(Resource):
    def post(self):
        with open('app/leaderboard.json', 'r+') as json_file:
            data = json.load(json_file)
            print(data)
            newDict = sorted(data, key=data.get, reverse=True)
            print(newDict)
            
            return jsonify({
                "text": "*Current Coffee Leaderboard (Top 5)*",
                "attachments": [
                    {
                        "text": ":first_place_medal: *#1:* " + newDict[0] + " *|* :star: " + str(data[newDict[0]]) + " Points :star: ",
                    },
                    {
                        "text": ":second_place_medal: *#2:* " + newDict[1] + " *|* :star: " + str(data[newDict[1]]) + " Points :star: ",
                    },
                    {
                        "text": ":third_place_medal: *#3:* " + newDict[2] + " *|* :star: " + str(data[newDict[2]]) + " Points :star: ",
                    },
                    {
                        "text": ":cookie: *#4:* " + newDict[3] + " *|* :star: " + str(data[newDict[3]]) + " Points :star: ",
                    },
                    {
                        "text": ":candy: *#5:* " + newDict[4] + " *|* :star: " + str(data[newDict[4]]) + " Points :star: ",
                    }
                ]
            })

class MyPoints(Resource):
    def post(self):
        data = request.form
        username = data['user_name']
        with open('app/leaderboard.json', 'r+') as json_file:
            obj = json.load(json_file)
            if username not in obj:
                return jsonify({
                    "text": "Error! You haven't gotten any points. Get some by making some coffee!"
                })
            else:
                points = obj[username]
                if points == 0:
                    return jsonify({
                        "text": "You have no points! Make some coffee and then we can talk."
                    })
                else:
                    return jsonify({
                        "text": "Your current points: " + str(points)
                    })
                    
class CoffeeHelp(Resource):
    def post(self):
        return jsonify({
            "text": "*CoffeeBot Commands*",
            "attachments": [
                {
                    "text": "`/coffeestatus` - Checks current status of bots according to bot. (May be inaccurate)"
                },
                {
                    "text": "`/madecoffee [left/right]` - Tells the bot you made coffee in either the left or right pot. Changes status in realtime. *Worth 1 Point on the Leaderboard*"
                },
                {
                    "text": "`/outofcoffee [left/right]` - Opposite of /madecoffee. *Worth 1 Point As Well*"
                },
                {
                    "text": "`/coffeeleaderboard` - Displays Top 5 Leaders with the most points"
                },
                {
                    "text": "`/coffeepoints` - Displays your current point balance."
                }
            ]
        })
    