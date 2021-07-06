import pandas as pd 
import numpy as np
import streamlit
import plotly.graph_objects as go

class User:

    def __init__(self,weight,height):
        self.Wt = numeric_ht(weight)
        self.Ht = numeric_ht(height)
        self.z_Ht = (self.Ht - 70)/4  #avg ht of 70in and std of 4
        self.z_Wt = (self.Wt - 196.6)/51.2 #avg wt of 196.6 and std of 51.2
    
    def compute_distance(self,pnt1,pnt2):
        x= (pnt1[0]-pnt2[0])**2
        y= (pnt1[1]-pnt2[1])**2
        return np.sqrt(x-y)

    def find_matches(self,df):
        df['distance'] = df.apply(lambda x: self.compute_distance((x.z_Ht,x.z_Wt),(self.z_Ht,self.z_Wt)),axis=1)
        df = df.sort_values(by=['distance'])
        df = df.dropna(subset=['distance'])
        df.reset_index(drop=True)
        

def numeric_ht(ht:str):
    ft = ht[0]
    if len(ht) == 4:
        inch = ht[2:4]
    else:
        inch = ht[2]
    int_inch = int(ft)*12 + int(inch)
    return int_inch


def load_data(fname):
    df = pd.read_csv(fname,index_col=0)
    df['Ht'] = df['Ht'].apply(numeric_ht)
    df['z_Ht'] = (df['Ht']-df['Ht'].mean())/df['Ht'].std()
    df['z_Wt'] = (df['Wt']-df['Wt'].mean())/df['Wt'].std()
    return df


df = load_data("src/basketball_players.csv")
fig = go.Figure(data=go.Scatter(x=df['z_Wt'],
                                y=df['z_Ht'],
                                mode= 'markers',
                                text= df['Player']))


fig.show()
