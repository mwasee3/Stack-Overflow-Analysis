from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn
import time
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_log_error
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import max_error
import pandas as pd

def getTimeDiff(x , y):
  x_Dobj = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
  y_Dobj = datetime.strptime(y, '%Y-%m-%d %H:%M:%S')
  x_seconds = time.mktime((x_Dobj).timetuple())
  y_seconds = time.mktime((y_Dobj).timetuple())

  return y_seconds - x_seconds


def time_estimate():
    data = pd.read_csv('stackoverflow_2008_clean.csv')
    data["Text"] = data["Title"] + data["Body_x"] + data["Tag"]
    data["rep_time_sec"] = data.apply(lambda x: getTimeDiff(x['CreationDate_x'], x['CreationDate_y']), axis=1)
    X = data["Text"]
    y = data["rep_time_sec"]
    X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.3, random_state=42)
    tfidfvectorizer = TfidfVectorizer()
    X_train_vect = tfidfvectorizer.fit_transform(X_train.values.astype('U'))
    reg = LinearRegression().fit(X_train_vect, y_train)
    X_test_vect = tfidfvectorizer.transform(X_test.values.astype('U'))
    Y_pred = reg.predict(X_test_vect)
    return max_error(y_test, Y_pred)

print(time_estimate())