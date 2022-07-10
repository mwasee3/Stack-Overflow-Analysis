from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt

def check_dataset_granularity(df):
    print("Number of questions answered within a day: ", df[df["label"] == 1].shape[0])
    print("Number of questions answered after a day: ", df[df["label"] == 0].shape[0])
    return

def balance_dataset(df):
    after_day = df[df["label"] == 0]
    within_day = df[df["label"] == 1]
    num_rec = after_day.shape[0]
    df = after_day
    df = df.append(within_day.iloc[0:num_rec, :])
    return df

def create_model(df):
    df = df.dropna()
    X = df[["questions","answered_percent", "avg_response_time_min"]]
    y = df["label"]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.30,random_state=0)

    logreg = LogisticRegression()
    logreg.fit(X_train,y_train)
    #y_pred=logreg.predict(X_test)
    
    return X_test, y_test, logreg

def compute_stats(y_test, y_pred):
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    print("Precision:",metrics.precision_score(y_test, y_pred))
    print("Recall:",metrics.recall_score(y_test, y_pred))
    print("F1 score: ",metrics.f1_score(y_test, y_pred))

    
def plot_confusion_matrix(y_test, y_pred):
    cf_matrix = metrics.confusion_matrix(y_test, y_pred)
    ax = sns.heatmap(cf_matrix, annot=True, cmap="YlGnBu", fmt='g')

    ax.set_title('Perfomance of Logistic regression ');
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ');

    ax.xaxis.set_ticklabels(['False','True'])
    ax.yaxis.set_ticklabels(['False','True'])

    ## Display the visualization of the Confusion Matrix.
    plt.show()