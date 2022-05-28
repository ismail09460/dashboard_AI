#company function (search by company name)
from ast import literal_eval
import numpy as np
import pandas as pd

# read data
data = pd.read_csv("statistics_data.csv")

def search(company):
    dct = {}
    dct['Main_ORG'] = company
    texts = []
    orgs = []
    regex = ".*"+company+".*"
    df_company = data[data.MAIN_ORG.str.match(regex)].reset_index(drop=True)
    #number of posts by company
    posts_number = df_company.shape[0]
    #get texts
    texts = df_company['text'].values.tolist()
    dct['texts'] = texts
    #orgs
    for i in range(len(df_company)):
        if df_company['ORGS'][i] != 'no organisation':
            orgs.extend(literal_eval(df_company['ORGS'][i]))
    dct['orgs'] = orgs
    #group by month
    df_company = df_company.groupby('month')
    #get group for avril
    df_avril = df_company.get_group('avril')
    #get group for mai
    df_mai = df_company.get_group('mai')
    
    #positive and negative rate
    #statistics for avril
    dct['avril'] = {}
    positive_rate_avril = np.round((len(df_avril.loc[df_avril['score'] == 1]) / len(df_avril['score']))*100 , 2)
    negative_rate_avril = np.round((len(df_avril.loc[df_avril['score'] == 0]) / len(df_avril['score']))*100 , 2)
    dct['avril']['positive_rate'] = positive_rate_avril
    dct['avril']['negative_rate'] = negative_rate_avril
    #number of posts by company by month
    dct['avril']['number_of_posts'] = df_avril.shape[0]
    
    #statistics for mai
    dct['mai'] = {}
    positive_rate_mai = np.round((len(df_mai.loc[df_mai['score'] == 1]) / len(df_mai['score']))*100 , 2)
    negative_rate_mai = np.round((len(df_mai.loc[df_mai['score'] == 0]) / len(df_mai['score']))*100 , 2)
    dct['mai']['positive_rate'] = positive_rate_mai
    dct['mai']['negative_rate'] = negative_rate_mai
    #number of posts by company by month
    dct['mai']['number_of_posts'] = df_mai.shape[0]
    
    return dct