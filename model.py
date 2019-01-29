import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb
from sklearn.model_selection import train_test_split
import pickle


data = pd.read_csv(r"C:\Users\wakanda\Documents\Resources\DATASETS\german-credit-risk\german_credit_data.csv")

#Replace nulls with the mode
data["Saving accounts"]=data["Saving accounts"].fillna(data["Saving accounts"].mode()[0])
data["Checking account"]=data["Checking account"].fillna(data["Checking account"].mode()[0])

#Create categories from the Age column
interval = (18, 25, 35, 60, 120)
cats = ['Student', 'Young', 'Adult', 'Senior']
data["Age"] = pd.cut(data.Age, interval, labels=cats)

categorical_columns = ["Age","Sex", "Housing", "Saving accounts",  "Purpose"]
numeric_columns = ["Job", "Credit amount" , "Duration"]

def create_ohe(df, col):
    """Function that will takes the raw dataframe and the
       column name and return a one hot encoded DF
    """
    le = LabelEncoder()
    a=le.fit_transform(data[col]).reshape(-1,1)
    ohe = OneHotEncoder(sparse=False)
    column_names = [col+ "_"+ str(i) for i in le.classes_]
    return(pd.DataFrame(ohe.fit_transform(a),columns =column_names))

#We create a loop to create the final dataset with all features
temp = data[numeric_columns]
for column in categorical_columns:
    temp_df = create_ohe(data,column)
    temp = pd.concat([temp,temp_df],axis=1)

data["Risk"] = data["Risk"].map({"good":1, "bad":0})

x_train, x_test, y_train, y_test = train_test_split(temp, data["Risk"], test_size=0.2,random_state=2019)

classifier = xgb.sklearn.XGBClassifier(nthread=-1, seed=1)
classifier.fit(x_train, y_train)
y_pred = classifier.predict(x_test)
predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

with open('model/atlas-api.pkl', 'wb') as file:
    pickle.dump(classifier, file)
