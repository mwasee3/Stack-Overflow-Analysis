import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

## funtion popularity_answers() will extract scores from the answers dataset and sort their counts based on the score ranges
def popularity_answers(merged_data_full):
    j=merged_data_full[["Score_y"]]
    pd.options.mode.chained_assignment = None
    conditions = [(j['Score_y'] <0),(j['Score_y'] == 0),(j['Score_y'] >0) & (j['Score_y'] < 5),(j['Score_y'] >= 5) & (j['Score_y'] < 10),(j['Score_y']>=10) & (j['Score_y'] < 20),(j['Score_y'] >= 20) & (j['Score_y'] < 50),(j['Score_y'] >= 50) & (j['Score_y'] < 100),(j['Score_y'] >= 100)]
    values = ['Less than 0','Exactly 0','Between 0 and 5', 'Between 5 and 10', 'Between 10 and 20', 'Between 20 and 50','Between 50 and 100', 'Greater than 100']
    j['group_y'] = np.select(conditions, values)
    pd.options.mode.chained_assignment = 'warn'
    x=j.groupby('group_y', as_index=False)['Score_y'].count()
    x['Score_y'] = x['Score_y'].div(1000).round(2)
    x.columns=["Group","Answers"]
    return x


    
## funtion popularity_answers() will extract scores from the questions dataset and sort their counts based on the score ranges
def popularity_questions(merged_data_full):
    sef=merged_data_full[["Score_x"]]
    pd.options.mode.chained_assignment = None
    conditions = [(sef['Score_x'] <0),(sef['Score_x'] == 0),(sef['Score_x'] >0) & (sef['Score_x'] < 5),(sef['Score_x'] >= 5) & (sef['Score_x'] < 10),(sef['Score_x']>=10) & (sef['Score_x'] < 20),(sef['Score_x'] >= 20) & (sef['Score_x'] < 50),(sef['Score_x'] >= 50) & (sef['Score_x'] < 100),(sef['Score_x'] >= 100)]
    values = ['Less than 0','Exactly 0','Between 0 and 5', 'Between 5 and 10', 'Between 10 and 20', 'Between 20 and 50','Between 50 and 100', 'Greater than 100']
    sef['group_x'] = np.select(conditions, values)
    pd.options.mode.chained_assignment = 'warn'
    sed=sef.groupby('group_x', as_index=False)['Score_x'].count()
    sed['Score_x'] = sed['Score_x'].div(1000).round(2)
    sed.columns=["Group","Questions"]
    return sed
def popularity_ans_ques(merged_data_full):
    ques=popularity_questions(merged_data_full)
    ans=popularity_answers(merged_data_full)
    mer = pd.merge(ans, ques, on ='Group')
    ax3 = sns.lineplot('Group', 'value', hue='variable', data=pd.melt(mer, 'Group'))
    ax3.set(xlabel='Group Based on Popularity Scores', ylabel = 'Count Per 1000')
    ax3.set_title("Popularity of Answers and Questions")
    plt.legend(["Answers", "Questions"], title = "")
    g2=plt.setp(ax3.get_xticklabels(), rotation=30, ha='right')
    
def cleaned_data():
    ans = pd.read_csv("Answers.csv", encoding = "ISO-8859-1", low_memory = False)
    tags = pd.read_csv("Tags.csv")
    ques = pd.read_csv("Questions.csv", encoding = "ISO-8859-1", low_memory = False)
    tags = tags.groupby(['Id'])['Tag'].agg(list).reset_index()
    agg_func = {'Body':list, 'CreationDate':'first'}
    ans[["ParentId","Body", "CreationDate"]] = ans.groupby(['ParentId']).agg(agg_func).reset_index()
    df = ques.merge(ans, left_on='Id', right_on='ParentId')
    df2 = df.merge(tags, left_on='Id_x', right_on='Id')
    df2.drop(columns=['Id_y', 'OwnerUserId_y', 'ParentId', 'Id'])
    stack_overflow_data = df2.rename(columns={"Id_x": "Id", "OwnerUserId_x": "OwnerUserId", "Score_x": "Question_score", "Body_x": "QuestionBody", "Score_y": "Answer_score", "Body_y":"Answer"})
    return stack_overflow_data

def popular_tags():
    stack_overflow_data=cleaned_data()
    df_ques = pd.DataFrame().assign(Question_Score=stack_overflow_data['Question_score'], Tags=stack_overflow_data['Tag'])
    df_ques = df_ques.explode('Tags')
    df_ques = df_ques.groupby('Tags', as_index=False)['Question_Score'].mean()
    df_ques = df_ques.sort_values('Question_Score', ascending=False)
    df_first10 = df_ques.iloc[:10]
    ax = sns.barplot(x='Tags', y='Question_Score', palette='mako_r', data = df_first10)
    ax = plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    
def answer_quality(merged_data_full):
    df_plot = pd.DataFrame().assign(Year=merged_data_full['CreationDate_x'], Score=merged_data_full['Score_y'])
    df_plot['year'] = pd.DatetimeIndex(df_plot['Year']).year
    df_plot.pop('Year')
    df_plot = df_plot.groupby('year', as_index=False)['Score'].mean()
    df_plot= df_plot.sort_values('Score',ascending=True)
    ax2 = sns.barplot(x='year', y='Score', palette='Set2', data = df_plot, order=df_plot.sort_values('Score').year)
    ax2.set(xlabel='Years', ylabel='Answer Score (Upvotes)')
    ax2.set_title("Quality of Answers over the years")
    ax2 = plt.setp(ax2.get_xticklabels(), rotation=45)

def min_reply_time(merged_data_full):
    stf1 = merged_data_full.loc[:,["Id", 'Score_x', 'ParentId',"Body_x",'CreationDate_x','CreationDate_y']]
    stf1["MinTime_raw"] =  pd.to_datetime(stf1['CreationDate_y']) - pd.to_datetime(stf1['CreationDate_x'])
    stf1 =stf1.drop(columns=['ParentId','CreationDate_y',"Body_x",'CreationDate_x']).sort_values(by=['MinTime_raw'])
    stf1 = stf1[stf1["MinTime_raw"] > timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)]
    # print(stf1)
    stf1["MinTime"] = stf1["MinTime_raw"].dt.total_seconds()#days*(60*60*24) + (stf1["MinTime_raw"].dt.seconds) + (stf1["MinTime_raw"].dt.minute)*60*60 +stf1["MinTime_raw"].dt.hour*60
    j=stf1
    conditions = [(j["Score_x"] <50),(j["Score_x"] >=50) & (j["Score_x"] < 100),(j["Score_x"] >=100) & (j["Score_x"] < 150),(j["Score_x"] >=150) & (j["Score_x"] <200),(j["Score_x"] >=200) & (j["Score_x"] < 250),(j["Score_x"] >=250) & (j["Score_x"] <300),(j["Score_x"] >=300) & (j["Score_x"] <350),(j["Score_x"] >=350) & (j["Score_x"] < 400),(j["Score_x"] >=400) & (j["Score_x"] < 450),(j["Score_x"] >= 450) & (j["Score_x"] <500)]
    values = ['1','2','3','4','5','6','7','8','9','10']
    pd.options.mode.chained_assignment = None
    j['Div'] = np.select(conditions, values)
    j = j[j['Div'] != '0']
    pd.options.mode.chained_assignment = 'warn'
    ax = sns.boxplot(x="Div" ,y ="MinTime",data=j)
    plt.ylim([0,10000])
    plt.legend(["score < 50", "50 >= score < 100", "100 >= score < 150", "150 >= score < 200", "200 >= score < 250", "250 >= score < 300", "300 >= score < 350", "350 >= score < 400", "400 >= score < 450", "450 >= score < 500"], loc=(1.04,0))
    axes = plt.gca()
    axes.yaxis.grid()

    ax.set(xlabel='Question Score Divisions', ylabel='Min Time')

    plt.title("Min time box plot for different question scores")