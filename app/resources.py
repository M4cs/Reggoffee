from flask import request, jsonify
from flask_restful import Resource, reqparse
from app import app
import json

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
                if obj['leftpot']['status'] == False:
                    obj['leftpot']['status'] = True
                    obj['leftpot']['reported_by'] = username
                else:
                    return jsonify({
                        "response_type": "in_channel",
                        "text": "The left pot already had coffee in it!",
                        "attachments": [
                            {
                            "text": "If you had to make a new pot and there was none left in the left pot, please use the command `/outofcoffee left` and then use this command again."
                            }
                        ]
                    })
                json_file.seek(0)
                json.dump(obj, json_file, indent=4)
                json_file.truncate()
                json_file.close()
        elif data['text'] == 'right':
            with open('app/status.json', 'r+') as json_file:
                obj = json.load(json_file)
                if obj['rightpot'] == False:
                    obj['rightpot']['status'] = True
                    obj['rightpot']['reported_by'] = username
                else:
                    return jsonify({
                        "response_type": "in_channel",
                        "text": "The right pot already had coffee in it!",
                        "attachments": [
                            {
                            "text": "If you had to make a new pot and there was none left in the right pot, please use the command `/outofcoffee right` and then use this command again."
                            }
                        ]
                    })
                json_file.seek(0)
                json.dump(obj, json_file, indent=4)
                json_file.truncate()
                json_file.close()
        else:
            return jsonify({
                "response_type": "in_channel",
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
            "response_type": "in_channel",
            "text": "Thank you {} for making some coffee in the left pot!".format(data['user_name'])
        })
        
class OutOfCoffee(Resource):
    def post(self):
        data = request.form
        username = data['user_name']
        if data['text'] == 'left':
            with open('app/status.json', 'r+') as json_file:
                obj = json.load(json_file)
                if obj['leftpot']['status'] == True:
                    obj['leftpot']['status'] = False
                    obj['leftpot']['reported_by'] = username
                else:
                    return jsonify({
                        "response_type": "in_channel",
                        "text": "Error! The pot was marked as empty already!",
                        "attachments": [
                            {
                            "text": "If you go make a new pot make sure to use the command `/madecoffee left` to switch the status!"
                            }
                        ]
                    })
                json_file.seek(0)
                json.dump(obj, json_file, indent=4)
                json_file.truncate()
                json_file.close()
        elif data['text'] == 'right':
            with open('app/status.json', 'r+') as json_file:
                obj = json.load(json_file)
                if obj['rightpot']['status'] == True:
                    obj['rightpot']['status'] = False
                    obj['rightpot']['reported_by'] = username
                else:
                    return jsonify({
                        "response_type": "in_channel",
                        "text": "Error! The pot was marked as empty already!",
                        "attachments": [
                            {
                            "text": "If you go make a new pot make sure to use the command `/madecoffee right` to switch the status!"
                            }
                        ]
                    })
                json_file.seek(0)
                json.dump(obj, json_file, indent=4)
                json_file.truncate()
                json_file.close()
        else:
            return jsonify({
                "response_type": "in_channel",
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
            "response_type": "in_channel",
            "text": "Thank you {} for marking the pot as empty!".format(data['user_name']),
            "attachments": [
                {
                    "text": "*(It'd be nice if you made some after you finish :wink: )*"
                }
            ]
        })

class CheckStatus(Resource):
    def post(self):
        with open('app/status.json', 'r+') as json_file:
            data = json.load(json_file)
            leftstatus = data['leftpot']['status']
            leftreport = data['leftpot']['reported_by']
            rightstatus = data['rightpot']['status']
            rightreport = data['rightpot']['reported_by']
            if leftstatus == True:
                lstat = 'There Is Coffee!'
            else:
                lstat = 'No Coffee At The Moment :cry:'
            if rightstatus == True:
                rstat = 'There Is Coffee!'
            else:
                rstat = 'No Coffee At The Moment :cry:'
            json_file.close()
            return jsonify({
                "response_type": "in_channel",
                "text": "*Current Status Of Coffee*",
                "attachments": [
                    {
                        "text": "*Left Pot Status:* " + lstat + "\nReported by: " + leftstatus
                    },
                    {
                        "text": "*Right Pot Status:* " + rstat + "\nReported by: " + rightstatus
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
                "response_type": "in_channel",
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
                    "response_type": "in_channel",
                    "text": "Error! You haven't gotten any points. Get some by making some coffee!"
                })
            else:
                points = obj[username]
                if points == 0:
                    return jsonify({
                        "response_type": "in_channel",
                        "text": "You have no points! Make some coffee and then we can talk."
                    })
                else:
                    return jsonify({
                        "response_type": "in_channel",
                        "text": "Your current points: " + str(points)
                    })
                    
class CoffeeHelp(Resource):
    def post(self):
        return jsonify({
            "response_type": "in_channel",
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
    