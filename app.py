from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

a_customer = api.model('Customer', {'Savings Account': fields.String("Categorical description of the amount in savings account"),
                                    'Checking Account': fields.String("Categorical description of the amount in savings account"),
                                    'Age': fields.Integer("The age of the applicant"),
                                    'Job': fields.Integer("Job (numeric: 0 - unskilled and non-resident, 1 - unskilled and resident, 2 - skilled, 3 - highly skilled)"),
                                    'Housing': fields.String("The type of house the applicant lives in either owned, rented ot free"),
                                    'Duration': fields.Integer("How long the intended loan is for in months"),
                                    'Purpose': fields.String("The reason for the loan"),
                                    'Sex': fields.String("The sex of the customer either male or female"),
                                    'Credit Amount': fields.Integer("The amount the customer would like to borrow"),
                                   } )

@api.route('/model')
class Model(Resource):

    @api.expect(a_customer)
    def post(self):
        """A function that takes the an input of customer details via an APi
           and returns as an output of the probability of default on the loan
        """
        prediction = 0.87
        return {"status": "success", "prediction": prediction}, 200


if __name__ == "__main__":
    app.run(debug=True)