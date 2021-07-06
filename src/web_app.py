import pandas as pd 
import numpy as np
import streamlit as st
import plotly.graph_objects as go

class User:

    def __init__(self,weight,height):
        self.Wt = weight
        self.Ht = height
        self.z_Ht = (self.Ht - 70)/4  #avg ht of 70in and std of 4
        self.z_Wt = (self.Wt - 196.6)/51.2 #avg wt of 196.6 and std of 51.2
    
    def compute_distance(self,pnt1,pnt2):
        x= (pnt1[0]-pnt2[0])**2
        y= (pnt1[1]-pnt2[1])**2
        return np.sqrt(x+y)

    def find_matches(self,df):
        df['distance'] = df.apply(lambda x: self.compute_distance((x.z_Ht,x.z_Wt),(self.z_Ht,self.z_Wt)),axis=1)
        df = df.sort_values(by=['distance'])
        df = df.dropna(subset=['distance'])
        df = df.reset_index(drop=True)
        return df 
        

def numeric_ht(ht:str):
    ft = ht[0]
    if len(ht) == 4:
        inch = ht[2:4]
    else:
        inch = ht[2]
    int_inch = int(ft)*12 + int(inch)
    return int_inch

@st.cache
def load_data(fname):
    df = pd.read_csv(fname,index_col=0)
    df['num_Ht'] = df['Ht'].apply(numeric_ht)
    df['z_Ht'] = (df['num_Ht']-df['num_Ht'].mean())/df['num_Ht'].std()
    df['z_Wt'] = (df['Wt']-df['Wt'].mean())/df['Wt'].std()
    return df

header = st.beta_container()
ranking = st.beta_container()
vis_area = st.beta_container()

height_input = st.sidebar.text_input("Your Height","6'0")
try:
    user_height = numeric_ht(height_input)
except:
    st.error('Please enter a valid height')

weight_input = st.sidebar.text_input("Your Weight","190")
try:
    user_weight = int(weight_input)
except:
    st.error('Please enter a valid weight')

user = User(user_weight,user_height)


with header:
    st.title("Which NBA Player Are You?")

with ranking:
    st.header("Most Comparable Ranking!")
    src_df = load_data("basketball_players.csv")
    df = user.find_matches(src_df.copy())
    st.write(df.iloc[:,:])

with vis_area:
    st.header("Visualized")
    fig = go.Figure(data=go.Scatter(x = df['z_Wt'],
                                    y = df['z_Ht'],
                                    mode = 'markers',
                                    text = df['Player'],
                                    name = "NBA Players"
                                    ))
    fig.add_trace(go.Scatter(x=[user.z_Wt],
                             y=[user.z_Ht],
                             marker=dict(color="red"),
                             mode= 'markers',
                             text= "User",
                             name= "User"
                 ))
    
    fig.update_layout(title = "Standard Deviation of Height and Weight",
                      title_x=.5,
                      xaxis_title = "Weight Std",
                      yaxis_title = "Height Std",
                      width=800,
                      height=600
                     )
    st.plotly_chart(fig)
