from flask import Flask, request
from flask_restplus import Api, Resource, fields, reqparse
import pandas as pd

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

parser = reqparse.RequestParser()
parser.add_argument('Savings Account', required=True, 
                         choices=('little', 'moderate', 'quite rich', 'rich'), 
                         help='String - little, moderate, quite rich, rich')
parser.add_argument('Checking Account', required=True, 
                     choices=('little', 'moderate', 'quite rich', 'rich'), help='String- little, moderate, quite rich, rich')
parser.add_argument('Age', type=int, required=True, choices=(range(100)),help='Numeric')
parser.add_argument('Job', type=int, required=True, choices=(range(4)), help='Numeric: 0 - unskilled and non-resident, 1 - unskilled and resident, 2 - skilled, 3 - highly skilled')
parser.add_argument('Housing', required=True, choices=('own', 'rent','free'),
                    help='String: own, rent, or free')
parser.add_argument('Duration', required=True, choices=(range(241)), 
                    type=int, help='numeric, in month, Duration limit of 20 years/ 240 months') #Duration limit of 20 years/ 240 months
parser.add_argument('Purpose', required=True, 
                   choices=('car', 'furniture/equipment', 'radio/TV', 
                   'domestic appliances', 'repairs', 'education', 'business', 'vacation/others'),
                    help='text: car, furniture/equipment, radio/TV, domestic appliances, repairs, education, business, vacation/others')
parser.add_argument('Sex', required=True, choices=('male', 'female'), help='text: male, female')
parser.add_argument('Credit Amount', type=int, choices=(range(1500001)), required=True, help='Numeric, loan limit of 15 million') #loan limit of 15 million

@api.route('/model')
class Model(Resource):

    @api.expect(a_customer)
    def post(self):
        """A function that takes the an input of customer details via an APi
           and returns as an output of the probability of default on the loan
        """
        args = parser.parse_args()
        df = pd.read_json(args, orient='columns')
        df.head()

        
        prediction = 0.87
        return {"status": "success", "prediction": prediction, "text":args}, 200
        


if __name__ == "__main__":
    app.run(debug=True)