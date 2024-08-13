# -*- coding: utf-8 -*-
"""CreditCardFraudDectection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17XVkrlC_Moe15_-08ejf-QBdLFPnXqZ3
"""

import pandas as pd
from numpy import mean
from numpy import std
import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import ADASYN

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
import lightgbm as lgb

from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

# get the dataset
train_df = pd.read_csv('drive/MyDrive/Colab Notebooks/fraudTrain.csv')
reduced_train_df = train_df.sample(n=300000, random_state=42)
# train_df.head()

#get dataset for training
test_df = pd.read_csv('drive/MyDrive/Colab Notebooks/fraudTest.csv')
reduced_test_df = test_df.sample(n=250000, random_state=42)
test_df.head()

#training mode
train_col_list = reduced_train_df.columns.tolist()
print(train_col_list)
train_col_to_drop = ['trans_num', 'unix_time', 'Unnamed: 0']
train_col_to_drop = [col for col in train_col_to_drop if col in reduced_train_df.columns]  # Filter out columns that do not exist
reduced_train_df = reduced_train_df.drop(columns=train_col_to_drop, axis=1)
#reduced_train_df.head()

#testing mode
test_col_list = reduced_test_df.columns.tolist()
print(test_col_list)
test_col_to_drop = ['trans_num', 'unix_time', 'Unnamed: 0']
test_col_to_drop = [col for col in test_col_to_drop if col in reduced_test_df.columns]  # Filter out columns that do not exist
reduced_test_df = reduced_test_df.drop(columns=test_col_to_drop, axis=1)
#test_df.head()

#train section
x_train = reduced_train_df.drop('is_fraud', axis=1)
y_train = reduced_train_df['is_fraud']
# reduced_train_df.info()
# print(reduced_train_df.is_fraud.value_counts())
# print(x_train.shape)

#test section
x_test = reduced_test_df.drop('is_fraud', axis=1)
y_test = reduced_test_df['is_fraud']
# reduced_test_df.info()
# print(x_test.shape)

# Handling Preprocessing
label_encoder = LabelEncoder()
#x_train.isnull().sum()

# train section
x_train_encoded = x_train.copy()
for col in x_train.columns:
    if x_train[col].dtype == 'object':
        x_train_encoded[col] = label_encoder.fit_transform(x_train[col])

# test section
x_test_encoded = x_test.copy()
for col in x_test.columns:
    if x_test[col].dtype == 'object':
        x_test_encoded[col] = label_encoder.fit_transform(x_test[col])

print(x_train_encoded.head())
print(x_test_encoded.head())

#Print the numbers of rows and columns after encoding
print(x_train_encoded.shape)
print(x_test_encoded.shape)

# Apply SMOTE to balance the training data
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(x_train_encoded, y_train)

# Print the class distribution after SMOTE
print(y_train_smote.value_counts())

# Apply ADASYN to balance the training data
adasyn = ADASYN(random_state=42)
X_train_adasyn, y_train_adasyn = adasyn.fit_resample(x_train_encoded, y_train)

# Print the class distribution after ADASYN
print(y_train_adasyn.value_counts())

# Print the class distribution
print(y_train.value_counts())

#Random Forest

#==============================================
# train with SMOTE Balnced data
#==============================================
rf_smote = RandomForestClassifier(n_estimators=100)
rf_smote.fit(X_train_smote, y_train_smote)

# make predictions
y_smote_predict = rf_smote.predict(x_test_encoded)

# testing set performance
rf_smote_f1_score = f1_score(y_test, y_smote_predict, average='weighted')
rf_smote_precision = precision_score(y_test, y_smote_predict, average='weighted',)
rf_smote_recall = recall_score(y_test, y_smote_predict, average='weighted',)

print('===================================')
# result
print('SMOTE Performance Result')
print('Acc F1:', rf_smote_f1_score)
print('Acc Precision:', rf_smote_precision)
print('Acc Recall:', rf_smote_recall)

#==============================================
# train with ADASYN Balanced data
#==============================================
rf_adasyn = RandomForestClassifier(n_estimators=100)
rf_adasyn.fit(X_train_adasyn, y_train_adasyn)

# make predictions
y_adasyn_predict = rf_adasyn.predict(x_test_encoded)

# testing set performance
rf_adasyn_f1_score = f1_score(y_test, y_adasyn_predict, average='weighted')
rf_adasyn_precision = precision_score(y_test, y_adasyn_predict, average='weighted',)
rf_adasyn_recall = recall_score(y_test, y_adasyn_predict, average='weighted',)

print('===================================')
# result
print('ADASYN Performance Result')
print('Acc F1:', rf_adasyn_f1_score)
print('Acc Precision:', rf_adasyn_precision)
print('Acc Recall:', rf_adasyn_recall)

#Neural Network Classifier

#==============================================
#train with SMOTE
#==============================================

nn_smote_classifier = MLPClassifier(alpha=1, max_iter=50)
nn_smote_classifier.fit(X_train_smote, y_train_smote)

# make predictions
y_smote_predict = nn_smote_classifier.predict(x_test_encoded)

# training set performance
nn_smote_f1_score = f1_score(y_test, y_smote_predict, average='weighted')
nn_smote_precision = precision_score(y_test, y_smote_predict, average='weighted', zero_division=1)
nn_smote_recall = recall_score(y_test, y_smote_predict, average='weighted', zero_division=1)

print('===================================')
print('SMOTE Performance Result')
print('Acc F1:', nn_smote_f1_score)
print('Acc Precision:', nn_smote_precision)
print('Acc Recall:', nn_smote_recall)

#==============================================
#train with ADASYN
#==============================================

nn_adasyn_classifier = MLPClassifier(alpha=1, max_iter=50)
nn_adasyn_classifier.fit(X_train_adasyn, y_train_adasyn)

# make predictions
y_adasyn_predict = nn_adasyn_classifier.predict(x_test_encoded)

# training set performance
nn_adasyn_f1_score = f1_score(y_test, y_adasyn_predict, average='weighted')
nn_adasyn_precision = precision_score(y_test, y_adasyn_predict, average='weighted' , zero_division=1)
nn_adasyn_recall = recall_score(y_test, y_adasyn_predict, average='weighted', zero_division=1)

print('===================================')
print('ADASYN Performance Result')
print('Acc F1:', nn_adasyn_f1_score)
print('Acc Precision:', nn_adasyn_precision)
print('Acc Recall:', nn_adasyn_recall)

#Decision Tree Classifier

# Finding the optimal max_depth using cross-validation on the training data
depths = range(1, 10)

#==============================================
#train with SMOTE
#==============================================

cv_scores_smote = [cross_val_score(DecisionTreeClassifier(max_depth=d), X_train_smote, y_train_smote, cv=5, scoring='f1_weighted').mean() for d in depths]
smote_optimal_depth = depths[np.argmax(cv_scores_smote)]
print(f"Optimal max_depth: {smote_optimal_depth}")

dt_smote_classifier = DecisionTreeClassifier(max_depth=smote_optimal_depth)
dt_smote_classifier.fit(X_train_smote, y_train_smote)

# make predictions
y_smote_predict = dt_smote_classifier.predict(x_test_encoded)

# testing set performance
dt_smote_f1_score = f1_score(y_test, y_smote_predict, average='weighted')
dt_smote_precision = precision_score(y_test, y_smote_predict)
dt_smote_recall = recall_score(y_test, y_smote_predict)

print('===================================')
# result
print('SMOTE Performance Result')
print('Acc F1:', dt_smote_f1_score)
print('Acc Precision:', dt_smote_precision)
print('Acc Recall:', dt_smote_recall)

#==============================================
#train with ADASYN
#==============================================

cv_scores_adasyn = [cross_val_score(DecisionTreeClassifier(max_depth=d), X_train_adasyn, y_train_adasyn, cv=5, scoring='f1_weighted').mean() for d in depths]
adasyn_optimal_depth = depths[np.argmax(cv_scores_adasyn)]
print(f"Optimal max_depth: {adasyn_optimal_depth}")

dt_adasyn_classifier = DecisionTreeClassifier(max_depth=adasyn_optimal_depth)
dt_adasyn_classifier.fit(X_train_adasyn, y_train_adasyn)

# make predictions
y_adasyn_predict = dt_adasyn_classifier.predict(x_test_encoded)

# testing set performance
dt_adasyn_f1_score = f1_score(y_test, y_adasyn_predict, average='weighted')
dt_adasyn_precision = precision_score(y_test, y_adasyn_predict)
dt_adasyn_recall = recall_score(y_test, y_adasyn_predict)


print('================================')
# result
print('ADASYN Performance Result')
print('Acc F1:', dt_adasyn_f1_score)
print('Acc Precision:', dt_adasyn_precision)
print('Acc Recall:', dt_adasyn_recall)

#LightGBM Classifier

#==============================================
# train with ADASYN
#==============================================

lgb_adasyn_classifier = lgb.LGBMClassifier()
lgb_adasyn_classifier.fit(X_train_adasyn, y_train_adasyn)

# make predictions
y_adasyn_predict = lgb_adasyn_classifier.predict(x_test_encoded)

# testing set performance
lgb_adasyn_f1_score = f1_score(y_test, y_adasyn_predict, average='weighted')
lgb_adasyn_precision = precision_score(y_test, y_adasyn_predict, average='weighted')
lgb_adasyn_recall = recall_score(y_test, y_adasyn_predict, average='weighted')

# result

print('===================================')
# result
print('ADASYN Performance Result')
print('Acc F1:', lgb_adasyn_f1_score)
print('Acc Precision:', lgb_adasyn_precision)
print('Acc Recall:', lgb_adasyn_recall)

#==============================================
# train with SMOTE
#==============================================

lgb_classifier_smote = lgb.LGBMClassifier()

# Predict and evaluate
lgb_classifier_smote.fit(X_train_smote, y_train_smote)

y_smote_predict = lgb_classifier_smote.predict(x_test_encoded)

lgb_smote_f1_score = f1_score(y_test, y_smote_predict, average='weighted')
lgb_smote_precision = precision_score(y_test, y_smote_predict, average='weighted')
lgb_smote_recall = recall_score(y_test, y_smote_predict, average='weighted')

print('===================================')
print('SMOTE Performance Result')
print('Acc F1:', lgb_smote_f1_score)
print('Acc Precision:', lgb_smote_precision)
print('Acc Recall:', lgb_smote_recall)

#XGBOOST Classifier

#==============================================
# train with SMOTE
#==============================================
xgb_classifier_smote = XGBClassifier()
xgb_classifier_smote.fit(X_train_smote, y_train_smote)
# make predictions
y_smote_predict = xgb_classifier_smote.predict(x_test_encoded)

# training set performance
xgb_smote_f1_score = f1_score(y_test, y_smote_predict, average='weighted')
xgb_smote_precision = precision_score(y_test, y_smote_predict, average='weighted')
xgb_smote_recall = recall_score(y_test, y_smote_predict, average='weighted')


print('===================================')
# result
print('SMOTE Performance Result')
print('Acc F1:', xgb_smote_f1_score)
print('Acc Precision:', xgb_smote_precision)
print('Acc Recall:', xgb_smote_recall)
#==============================================
# train with ADASYN
#==============================================

xgb_adasyn_classifier = XGBClassifier()
xgb_adasyn_classifier.fit(X_train_adasyn, y_train_adasyn)

# make predictions
y_adasyn_predict = xgb_adasyn_classifier.predict(x_test_encoded)

# testing set performance
xgb_adasyn_f1_score = f1_score(y_test, y_adasyn_predict, average='weighted')
xgb_adasyn_precision = precision_score(y_test, y_adasyn_predict, average='weighted')
xgb_adasyn_recall = recall_score(y_test, y_adasyn_predict, average='weighted')


print('===================================')
print('ADASYN Performance Result')
print('Acc F1:', xgb_adasyn_f1_score)
print('Acc Precision:', xgb_adasyn_precision)
print('Acc Recall:', xgb_adasyn_recall)

# esemble parformance
estimator_list = [
    ('dt', dt_smote_classifier),
    ('rf', rf_smote),
    ('nlp', nn_adasyn_classifier),
    ('lgb', lgb_classifier_smote),
    ('xgb', xgb_classifier_smote)
]

# Build stack model
stack = StackingClassifier( estimators =estimator_list, final_estimator=LogisticRegression())

# Train stacked model
stack.fit(X_train_smote, y_train_smote)

# make predictions
y_predict = stack.predict(x_test_encoded)

# testing set performance
stack_f1_score = f1_score(y_test, y_predict, average='weighted')
stack_precision = precision_score(y_test, y_predict, average='weighted')
stack_recall = recall_score(y_test, y_predict, average='weighted')

# result
print('===================================')
print('Testing Performance Result')
print('Acc F1:', stack_f1_score)
print('Acc Precision:', stack_precision)
print('Acc Recall:', stack_recall)

from google.colab import drive
drive.mount('/content/drive')
