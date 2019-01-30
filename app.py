from flask import Flask, request
from flask_restplus import Api, Resource, fields, reqparse
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb
from sklearn.model_selection import train_test_split
from werkzeug.contrib.fixers import ProxyFix
import os

# Use pickle to load in the pre-trained model
with open(f'model/atlas-api.pkl', 'rb') as f:
    model = pickle.load(f)



app = Flask(__name__)
api = Api(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
port = int(os.environ.get("PORT", 5000))


a_customer = api.model('Customer', {'Saving accounts': fields.String("Categorical description of the amount in savings account"),
                                    'Checking account': fields.String("Categorical description of the amount in savings account"),
                                    'Age': fields.Integer("The age of the applicant"),
                                    'Job': fields.Integer("Job (numeric: 0 - unskilled and non-resident, 1 - unskilled and resident, 2 - skilled, 3 - highly skilled)"),
                                    'Housing': fields.String("The type of house the applicant lives in either owned, rented ot free"),
                                    'Duration': fields.Integer("How long the intended loan is for in months"),
                                    'Purpose': fields.String("The reason for the loan"),
                                    'Sex': fields.String("The sex of the customer either male or female"),
                                    'Credit amount': fields.Integer("The amount the customer would like to borrow"),
                                   } )

parser = reqparse.RequestParser()
parser.add_argument('Saving accounts', required=True, 
                         choices=('little', 'moderate', 'quite rich', 'rich'), 
                         help='String - little, moderate, quite rich, rich')
parser.add_argument('Checking account', required=True, 
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
parser.add_argument('Credit amount', type=int, choices=(range(1500001)), required=True, help='Numeric, loan limit of 15 million') #loan limit of 15 million




@api.route('/model')
class Model(Resource):

    @api.expect(a_customer)
    def post(self):
        """A function that takes the an input of customer details via an APi
           and returns as an output of the probability of default on the loan
        """
        args = parser.parse_args()
        # Convert json input to a pandas dataframe
        df = pd.DataFrame(args,columns=['Age','Sex','Job','Housing','Saving accounts',
                                          'Checking account', 'Credit amount', 'Duration','Purpose'],
                                           index=[1])

        
        #Convert Sex, Housing, Saving accounts, Checking account, Purpose to ints
        # Categorical boolean mask
        categorical_feature_mask = df.dtypes==object
        # filter categorical columns using mask and turn it into a list
        categorical_cols = df.columns[categorical_feature_mask].tolist()
        categorical_cols

        le = LabelEncoder()
        # apply le on categorical feature columns
        df[categorical_cols] = df[categorical_cols].apply(lambda col: le.fit_transform(col))

        
        # Get the model's prediction
        prediction = model.predict(df)[0] 
        return {"status": "success", "prediction": str(prediction)}, 200


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=port)