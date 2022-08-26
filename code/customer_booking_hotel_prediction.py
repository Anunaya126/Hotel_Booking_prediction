# -*- coding: utf-8 -*-
"""Customer booking hotel prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11Vq6OfUdqlWRmWjaPaZd6QGhGkY64jl3

#Importing required modules#
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""# Importing the required data set (CSV files)#"""

df_train=pd.read_csv("/content/train_data_evaluation_part_2.csv")
df_test=pd.read_csv("/content/test_data_evaluation_part2.csv")
df_train.head(10)
df_test.head(10)

"""Understanding the data"""

df_train.columns

df_test.columns

df_train.describe()

df_test.describe()

df_train.info()
df_test.info()

"""#Imputing the missing values in the data set#"""

df_train.isnull().sum()
df_test.isnull().sum()

"""Finding the mode of Age column"""

print(df_train['Age'].mode())
print(df_test['Age'].mode())

"""Imputing the missing vlaue in the column "Age""""

missing_col =['Age']

#Using mode of the age calculated before to impute the missing values
for i in missing_col:
  df_train.loc[df_train.loc[:,i].isnull(),i] = 50
  df_test.loc[df_test.loc[:,i].isnull(),i] = 46

df_train.isnull().sum()
df_test.isnull().sum()

print(df_train.shape)
print(df_test.shape)

df_train.nunique()
df_test.nunique()

df_train.head()

df_test.head()

"""Setting the ID column as index

"""

df_train.set_index('ID')
df_test.set_index('ID')

"""#Data Preparation #

In our data we have various booking status under one ID reference, here we are going to calculate how many times a certain ID number has initiated a booking and store it in TotalBookingInitiated, then calculate the ratio of total initiation with succesful check-in, and use that value as a measure for making further decision.
"""

sum_col_train=df_train['BookingsCanceled']+df_train['BookingsNoShowed']+df_train['BookingsCheckedIn']
sum_col_test=df_test['BookingsCanceled']+df_test['BookingsNoShowed']+df_test['BookingsCheckedIn']

df_train['TotalBookingInitiated']=sum_col_train
df_test['TotalBookingInitiated']=sum_col_test

score_train=df_train['BookingsCheckedIn']/df_train['TotalBookingInitiated']
score_test=df_test['BookingsCheckedIn']/df_test['TotalBookingInitiated']

df_train['BookingScore']=score_train
df_test['BookingScore']=score_test

df_train['BookingScore'].unique()

df_train['BookingScore'] = df_train['BookingScore'].replace(np.nan, 0)
df_test['BookingScore'] = df_test['BookingScore'].replace(np.nan, 0)

"""We have found the ratio of BookingsCheckedIn to TotalBookingInitiated, now using this value we will put a threshold of 0.5. Anything above the threshold we will assign 1 as checkin made, else we will assign 0 as checkin not made."""

df_train.loc[df_train['BookingScore'] >0.7,'BookingPrediction'] = 1
df_train.loc[df_train['BookingScore']<=0.7,'BookingPrediction'] = 0
df_test.loc[df_test['BookingScore'] >0.7,'BookingPrediction'] = 1
df_test.loc[df_test['BookingScore']<=0.7,'BookingPrediction'] = 0
 
df_train.head()

"""## Correlation map to check correlation between each variable
Initially we lacked a proper target vector, now that we have derived the target vector using the data available to us, we are going to view how the variables available tous are related with each other. 
"""

corr=df_train.corr()
plt.figure(figsize = (1,1)) 
corr.style.background_gradient(cmap='coolwarm')

"""#Dropping extra features:
ID is highly corelated with unnamed index column, lets drop unnamed column, similarly,DaysSinceCreation is highly correlated with DaysSinceLastStay and DaysSinceFirstStay
"""

df_train = df_train.drop(columns = ['Unnamed: 0','DaysSinceLastStay', 'DaysSinceFirstStay'])
df_test = df_test.drop(columns = ['Unnamed: 0','DaysSinceLastStay', 'DaysSinceFirstStay'])

df_train.columns

"""Viewing how the remaining data correlates with the target vector:"""

correlation = df_train.corr()['BookingPrediction'].abs().sort_values(ascending = False)
correlation

"""Dropping those columns which are not effecting the target vector as much, these are unnecessary for out prediction model."""

drop_col=['SRHighFloor', 'SRLowFloor',
       'SRAccessibleRoom', 'SRMediumFloor', 'SRBathtub', 'SRShower', 'SRCrib','AverageLeadTime',
       'SRKingSizeBed', 'SRTwinBed', 'SRNearElevator', 'SRAwayFromElevator','TotalBookingInitiated','BookingScore',
       'SRNoAlcoholInMiniBar', 'SRQuietRoom','Age','BookingsCheckedIn','Nationality','ID','BookingsNoShowed','BookingsCanceled']
df_train.drop(drop_col,axis=1,inplace=True)  
df_test.drop(drop_col,axis=1,inplace=True)

df_train.head()
df_test.head()

"""Separating the categorical columns to perform encoding"""

cat_cols_train = [col for col in df_train.columns if df_train[col].dtype == 'O']
cat_cols_test = [col for col in df_test.columns if df_test[col].dtype == 'O']
cat_cols_train
cat_cols_test

cat_df_train = df_train[cat_cols_train]
cat_df_test = df_test[cat_cols_test]
cat_df_train.head()
cat_df_test.head()

# printing unique values of categorical column
for col in cat_df_train.columns:
    print(f"{col}: \n{cat_df_train[col].unique()}\n")

"""Encoding of the categorical variables"""

cat_df_train['MarketSegment'] = cat_df_train['MarketSegment'].map({'Direct': 0, 'Corporate': 1, 'Travel Agent/Operator': 2,'Complementary': 3, 'Groups': 5, 'Other': 6, 'Aviation': 7})
cat_df_test['MarketSegment'] = cat_df_test['MarketSegment'].map({'Direct': 0, 'Corporate': 1, 'Travel Agent/Operator': 2,'Complementary': 3, 'Groups': 5, 'Other': 6, 'Aviation': 7})

cat_df_train['DistributionChannel'] = cat_df_train['DistributionChannel'].map({'Direct': 0, 'Corporate': 1, 'Travel Agent/Operator': 2, 'Electronic Distribution': 3})
cat_df_test['DistributionChannel'] = cat_df_test['DistributionChannel'].map({'Direct': 0, 'Corporate': 1, 'Travel Agent/Operator': 2, 'Electronic Distribution': 3})

cat_df_train.head()

"""Separating the numerical variable columns from target vector"""

num_df_train = df_train.drop(columns = cat_cols_train, axis = 1)
num_df_test = df_test.drop(columns = cat_cols_train, axis = 1)
num_df_train.drop('BookingPrediction', axis = 1, inplace = True)
num_df_test.drop('BookingPrediction', axis = 1, inplace = True)
num_df_train
num_df_test

num_df_train.var()

"""Normalising the numerical variable , the test and train dataset is normallised separately because the mean will change if we do it together."""

num_df_train['DaysSinceCreation'] = np.log(num_df_train['DaysSinceCreation'] + 1)
num_df_test['DaysSinceCreation'] = np.log(num_df_test['DaysSinceCreation'] + 1)

num_df_train['LodgingRevenue'] = np.log(num_df_train['LodgingRevenue'] + 1)
num_df_test['LodgingRevenue'] = np.log(num_df_test['LodgingRevenue'] + 1)

num_df_train['OtherRevenue'] = np.log(num_df_train['OtherRevenue'] + 1)
num_df_test['OtherRevenue'] = np.log(num_df_test['OtherRevenue'] + 1)

num_df_train['PersonsNights'] = np.log(num_df_train['PersonsNights'] + 1)
num_df_test['PersonsNights'] = np.log(num_df_test['PersonsNights'] + 1)

num_df_train['RoomNights'] = np.log(num_df_train['RoomNights'] + 1)
num_df_test['RoomNights'] = np.log(num_df_test['RoomNights'] + 1)

num_df_train.var()

num_df_train.head()

"""Assigning Input and Output variables for further application of model and predictions"""

X_train= pd.concat([cat_df_train, num_df_train], axis = 1)
X_test= pd.concat([cat_df_test, num_df_test], axis = 1)
y_train=df_train['BookingPrediction']
y_test=df_test['BookingPrediction']

X_train.shape,y_train.shape,X_test.shape,y_test.shape
X_train.head()
y_train.head()

"""#Model Building#

Logistic  regression
"""

#import logistic regression model
from sklearn.linear_model import LogisticRegression

#Importing metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

lr = LogisticRegression()
lr.fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)

acc_lr = accuracy_score(y_test, y_pred_lr)
conf = confusion_matrix(y_test, y_pred_lr)
clf_report = classification_report(y_test, y_pred_lr)

print(f"Accuracy Score of Logistic Regression is : {acc_lr}")
print(f"Confusion Matrix : \n{conf}")
print(f"Classification Report : \n{clf_report}")

"""#Decision Tree Classifier"""

#import decision tree classifier
from sklearn.tree import DecisionTreeClassifier

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)

y_pred_dtc = dtc.predict(X_test)

acc_dtc = accuracy_score(y_test, y_pred_dtc)
conf = confusion_matrix(y_test, y_pred_dtc)
clf_report = classification_report(y_test, y_pred_dtc)

print(f"Accuracy Score of Decision Tree is : {acc_dtc}")
print(f"Confusion Matrix : \n{conf}")
print(f"Classification Report : \n{clf_report}")

"""#ADA Boost Classifier"""

#Import ada boost classifier
from sklearn.ensemble import AdaBoostClassifier

# Ada Boost Classifier

ada = AdaBoostClassifier(base_estimator = dtc)
ada.fit(X_train, y_train)

y_pred_ada = ada.predict(X_test)

acc_ada = accuracy_score(y_test, y_pred_ada)
conf = confusion_matrix(y_test, y_pred_ada)
clf_report = classification_report(y_test, y_pred_ada)

print(f"Accuracy Score of Ada Boost Classifier is : {acc_ada}")
print(f"Confusion Matrix : \n{conf}")
print(f"Classification Report : \n{clf_report}")

"""#Gradient Boost Classifier"""

#Import gradient boosting classifier
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier()
gb.fit(X_train, y_train)

y_pred_gb = gb.predict(X_test)

acc_gb = accuracy_score(y_test, y_pred_gb)
conf = confusion_matrix(y_test, y_pred_gb)
clf_report = classification_report(y_test, y_pred_gb)

print(f"Accuracy Score of Ada Boost Classifier is : {acc_gb}")
print(f"Confusion Matrix : \n{conf}")
print(f"Classification Report : \n{clf_report}")

"""#CAT Boost Classifier"""

pip install catboost

#importing Cat  boost classifier
from catboost import CatBoostClassifier

cat = CatBoostClassifier(iterations=100)
cat.fit(X_train, y_train)

y_pred_cat = cat.predict(X_test)

acc_cat = accuracy_score(y_test, y_pred_cat)
conf = confusion_matrix(y_test, y_pred_cat)
clf_report = classification_report(y_test, y_pred_cat)

print(f"Accuracy Score of Ada Boost Classifier is : {acc_cat}")
print(f"Confusion Matrix : \n{conf}")
print(f"Classification Report : \n{clf_report}")

"""#ANN(Artificial Neural Network)"""

from tensorflow.keras.utils import to_categorical

X1 = pd.concat([cat_df_train, num_df_train], axis = 1)
X2 = pd.concat([cat_df_test, num_df_test], axis = 1)
y1 = to_categorical(df_train['BookingPrediction'])
y2 = to_categorical(df_test['BookingPrediction'])

# splitting data into training set and test set

X_train, X_test, y_train, y_test = X1,X2,y1,y2

X_train.shape

# from keras import optimizers
# sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

import keras
from keras.layers import Dense
from keras.models import Sequential
from keras import optimizers


num_epochs = 10
x_shape = (None, X_train.shape[-1])

model  = Sequential()
model.add(Dense(50, activation = 'relu', input_shape = x_shape))
model.add(Dense(50, activation = 'relu'))
model.add(Dense(2, activation = 'sigmoid'))
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
model_history = model.fit(X_train, y_train, validation_data = (X_test, y_test),epochs = num_epochs)

import plotly.express as px

plt.figure(figsize = (12, 6))

train_loss = model_history.history['loss']
val_loss = model_history.history['val_loss'] 
epoch = range(1, num_epochs+1)

loss = pd.DataFrame({'train_loss' : train_loss, 'val_loss' : val_loss})

px.line(data_frame = loss, x = epoch, y = ['val_loss', 'train_loss'], title = 'Training and Validation Loss',
        template = 'plotly_dark')

plt.figure(figsize = (12, 6))

train_acc = model_history.history['accuracy']
val_acc = model_history.history['val_accuracy'] 
epoch = range(1, num_epochs+1)


accuracy = pd.DataFrame({'train_acc' : train_acc, 'val_acc' : val_acc})

px.line(data_frame = accuracy, x = epoch, y = ['val_acc', 'train_acc'], title = 'Training and Validation Accuracy',
        template = 'plotly_dark')

acc_ann = model.evaluate(X_test, y_test)[1]

print(f'Accuracy of model is {acc_ann}')

"""#Model comparison"""

models = pd.DataFrame({
    'Model' : ['Logistic Regression', 'Decision Tree Classifier','Ada Boost Classifier',
             'Gradient Boosting Classifier', 'Cat Boost', 'ANN'],
    'Score' : [acc_lr, acc_dtc, acc_ada, acc_gb, acc_cat, acc_ann]
})


models.sort_values(by = 'Score', ascending = False)

px.bar(data_frame = models, x = 'Score', y = 'Model', color = 'Score', template = 'plotly_dark', title = 'Models Comparison')

