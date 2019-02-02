import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb
from sklearn.model_selection import train_test_split
import pickle

# import data
URL = r"C:\Users\wakanda\Documents\Resources\DATASETS\german-credit-risk\german_credit_data.csv"
data = pd.read_csv(URL)

#Replace nulls in the savings account with the mode
data["Saving accounts"]=data["Saving accounts"].fillna(data["Saving accounts"].mode()[0])
data["Checking account"]=data["Checking account"].fillna(data["Checking account"].mode()[0])

# Reformat and drop the target variable Risk
data["Risk"] = data["Risk"].map({"good":1, "bad":0})
target = data["Risk"]
data.drop(["Unnamed: 0"], axis=1, inplace = True)
data.drop(["Risk"], axis=1, inplace = True)

#Convert Sex, Housing, Saving accounts, Checking account, Purpose to ints
# Categorical boolean mask
categorical_feature_mask = data.dtypes==object
# filter categorical columns using mask and turn it into a list
categorical_cols = data.columns[categorical_feature_mask].tolist()


# apply le on categorical feature columns
le = LabelEncoder()
data[categorical_cols] = data[categorical_cols].apply(lambda col: le.fit_transform(col))

#Split the data into training and validation sets
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2,random_state=2019)

#Create a classifier to fit the model
classifier = xgb.sklearn.XGBClassifier(nthread=-1, seed=1)
classifier.fit(x_train, y_train)

#Make predictions using the test dataset
y_pred = classifier.predict(x_test)
predictions = [round(value) for value in y_pred]


# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

#Save the model in okl format to the local directory model
with open('model/atlas-api.pkl', 'wb') as file:
    pickle.dump(classifier, file)
