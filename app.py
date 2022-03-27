from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api= Api(app)

class Add(Resource):
    def post(self):
        # If I'm here, then the resource Add was requested using the method POST
        pass
    def get(self):
        # If I'm here, then the resource Add was requested using get
        pass
    def put(self):
        pass
    def delete(self):
        pass


class Subtract(Resource):
    pass

class Multiply(Resource):
    pass

class Divide(Resource):
    pass


@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
