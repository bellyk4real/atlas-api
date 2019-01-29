from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route('/model')
class Model(Resource):
    def get(self):
        """A function that takes the an input of customer details via an APi
           and returns as an output of the probability of default on the loan
        """
        prediction = 0.87
        return {"status": "success", "prediction": prediction}


if __name__ == "__main__":
    app.run(debug=False)