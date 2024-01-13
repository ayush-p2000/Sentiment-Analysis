import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
st.title("SENTIMENT ANALYSIS SYSTEM")
choice=st.sidebar.selectbox("My Menu",("Home","Sentiment Analysis","Result Visualization"))
if(choice=="Home"):
    st.image("https://user-images.githubusercontent.com/57702598/90991088-264c8880-e56c-11ea-9895-90029d3c2139.gif")
    st.markdown("<center><h1>WELCOME</h1></center>",unsafe_allow_html=True)
elif(choice=="Sentiment Analysis"):
    sid=st.text_input("Enter Sheet ID")
    r=st.text_input("enter starting column : ending columns")
    c=st.text_input("Enter Column to analyze")
    btn=st.button("Analyze")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file("key.json",["https://www.googleapis.com/auth/spreadsheets"])
            st.session_state['cred']=f.run_local_server(port=0)
        service=build("Sheets","v4",credentials=st.session_state['cred']).spreadsheets().values()
        data=service.get(spreadsheetId=sid,range=r).execute()
        d=data['values']
        df=pd.DataFrame(data=d[1:],columns=d[0])
        mymodel=SentimentIntensityAnalyzer()
        l=[]
        for i in range(0,len(df)):
            text=df._get_value(i,c)    
            pred=mymodel.polarity_scores(text)
            if(pred['compound']>0.5):
                l.append("Positive")
            elif(pred['compound']<-0.5):        
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment']=l
        df.to_csv("results.csv",index=False)
        st.subheader("Sentiment Analysis is completed and results are saved by the name of result.csv")
elif(choice=="Result Visualization"):
    df=pd.read_csv("results.csv")
    st.dataframe(df)
    choice2=st.selectbox("Choose Visualization",("NONE","PIE","HISTOGRAM"))
    if(choice2=="PIE"):
        posper=(len(df[df['Sentiment']=="Positive"])/len(df))*100
        negper=(len(df[df['Sentiment']=="Negative"])/len(df))*100
        neuper=(len(df[df['Sentiment']=="Neutral"])/len(df))*100
        fig=px.pie(values=[posper,negper,neuper],names=["Positive","Negative","Neutral"])
        st.plotly_chart(fig)
    elif(choice2=="HISTOGRAM"):
        c=st.selectbox("Choose the Column",df.columns)
        if c:
            fig=px.histogram(x=df['Sentiment'],color=df[c])
            st.plotly_chart(fig)






    