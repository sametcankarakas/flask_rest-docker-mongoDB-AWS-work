"""
Registration of a user 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token ()
Retrieve his stored sentence on out database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api= Api(app)

client = MongoClient("mongodb://db:27017") # same name(db) in docker compose
db = client.SentencesDatabase # its the name of the db(SentencesDatabase) that we created.
users = db["Users"] # created collection named UserNum




class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the users
        postedData = request.get_json()

        # Get the database
        username = postedData["username"]
        password = postedData["password"]

        # Hash(password + salt) = h5glkhj4g5ş45!!^% MV%+'!E'
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Store username and pw into the data base
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

class Store(Resource):
    def post(self):
        #Step 1 is to get posted data by the users
        postedData = request.get_json()

        #Step 2 is to read the data.
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step 3 is verify username and pw.
        correct_pw = verifyPW(username, password)

        if not correct_pw:
            retJson = {
            "status": 302,
            "msg": "Password or username doesnt match"
            }
            return jsonify(retJson)
        #Step 4 verify user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
            "status": 301,
            "msg": "Not enough tokens"
            }
            return jsonify(retJson)
        #Step 5 store the sentence, take one token away and return 200
        users.update_one({
            "Username": username
        },  {
              "$set":{
                  "Sentence": sentence,
                  "Tokens":num_tokens-1
                  }
        })

        retJson = {
            "status": 200,
            "msg": "Sentence saved successfully"
        }
        return jsonify(retJson)


class Get(Resource):
    def post(self):
        #Step 1 is to get posted data by the users
        postedData = request.get_json()

        #Step 2 is to read the data.
        username = postedData["username"]
        password = postedData["password"]
        #Step 3 is verify username and pw.
        correct_pw = verifyPW(username, password)

        if not correct_pw:
            retJson = {
            "status": 302,
            "msg": "Password or username doesnt match"
            }
            return jsonify(retJson)
        #Step 4 verify user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
            "status": 301,
            "msg": "Not enough tokens"
            }
            return jsonify(retJson)

        #MAKE THE USER PAY
        users.update_one({
            "Username": username
        },  {
              "$set":{
                  "Tokens":num_tokens-1
                  }
        })

        sentence = users.find({
        "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "msg": sentence
        }
        return jsonify(retJson)


def verifyPW(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens

api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")



if __name__ == "__main__":
    app.run(host='0.0.0.0')

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api= Api(app)

client = MongoClient("mongodb://db:27017") # same name(db) in docker compose
db = client.aNewDB # its the name of the db(aNewDB) that we created.
UserNum = db["UserNum"] # created collection named UserNum

UserNum.insert_one({
'num_of_users':0
}) # Document that number of users... that going to keep visited users number.

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update_one({}, {"$set":{"num_of_users": new_num}})
        return str( f"Hello user {new_num} ")

def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 # Missing parameters
        else:
            return 200
    elif (functionName== "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301 # Missing parameters
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200
class Add(Resource):
    def post(self):
        # If I'm here, then the resource Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)
        # If I am here, than status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        #Step 2: Add posted data
        ret = x+y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        # If I'm here, then the resource Subtract was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)
        # If I am here, than status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        #Step 2: Subtract posted data
        ret = x-y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        # If I'm here, then the resource Multiply was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)
        # If I am here, than status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        #Step 2: Multiply posted data
        ret = x*y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        # If I'm here, then the resource Divide was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)
        # If I am here, than status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        #Step 2: Divide posted data
        ret = (x*1.0)/y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/visit")

@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
"""
