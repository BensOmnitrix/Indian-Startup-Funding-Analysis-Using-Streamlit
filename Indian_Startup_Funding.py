import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Investors'] = df['Investors'].fillna('Undisclosed') 

def progress_bar():
    value = st.progress(0)
    for i in range(1,101):
        time.sleep(0.01)
        value.progress(i)

def load_investor_details(investor):

    progress_bar()

    st.header(investor)
    #Load the latest 5 investments of the investors
    last5_df = df[df['Investors'].str.contains(investor)].head()[['Date','Startup','Vertical','City','Round','Amount']]
    st.subheader('Recent Investments')
    st.dataframe(last5_df)

    col1,col2= st.columns(2)

    with col1:
        #Biggest Investments
        big_investment = df[df['Investors'].str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Biggest Investments')
        fig,ax = plt.subplots()
        ax.bar(big_investment.index,big_investment.values)
        st.pyplot(fig)

    with col2:
        sector = df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount'].sum()
        st.subheader('Sector Division')
        fig1,ax1 = plt.subplots()
        ax1.pie(sector,labels=sector.index,autopct='%0.1f%%')
        st.pyplot(fig1)

    col3,col4 = st.columns(2)

    with col3:
        stage = df[df['Investors'].str.contains(investor)].groupby('Round')['Amount'].sum()
        st.subheader('Stage Division')
        fig2,ax2 = plt.subplots()
        ax2.pie(stage,labels=stage.index,autopct='%0.1f%%')
        st.pyplot(fig2)

    with col4:
        city = df[df['Investors'].str.contains(investor)].groupby('City')['Amount'].sum()
        st.subheader('City Division')
        fig3,ax3 = plt.subplots()
        ax3.pie(city,labels=city.index,autopct='%0.1f%%')
        st.pyplot(fig3)


    df['Year'] = df['Date'].dt.year
    yoy = df[df['Investors'].str.contains(investor)].groupby('Year')['Amount'].sum()
    st.subheader('YoY Investments')
    fig4,ax4 = plt.subplots(figsize = (12,5))
    ax4.plot(yoy.index,yoy.values)
    st.pyplot(fig4)
    
    st.subheader('Similar Investors')
    investors_investing_sectors = df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount'].count().sort_values(ascending=False).reset_index()['Vertical'].tolist()
    temp_df = df.groupby(['Investors','Vertical'])['Amount'].count().reset_index().sort_values('Amount',ascending=False).reset_index()
    new_df = temp_df[temp_df['Vertical'].isin(investors_investing_sectors)].head(10)

    st.dataframe(new_df)

def load_startup_details(startup):

    progress_bar()

    st.header(startup)
    
    col1,col2,col3,col4,col5 = st.columns (5)

    with col1:
        st.subheader('Industry')
        temp = list(set(df[df['Startup'].str.contains(startup)]['Vertical'].tolist()))
        st.text(temp)

    with col3:
        st.subheader('Subindustry')
        temp = list(set(df[df['Startup'].str.contains(startup)]['Subvertical'].tolist()))
        st.text(temp)

    with col5:
        st.subheader('Location')
        temp = list(set(df[df['Startup'].str.contains(startup)]['City'].tolist()))
        st.text(temp)

    col6,col7 = st.columns(2)
    with col6:
        stage = df[df['Startup'].str.contains(startup)].groupby('Round')['Amount'].sum()
        st.subheader('Amount Raised in different Rounds')
        fig,ax = plt.subplots(figsize = (3,2))
        ax.pie(stage,labels=stage.index,autopct="%0.1f%%")
        st.pyplot(fig)

    with col7:
        investor_funding = df[df['Startup'].str.contains('UrbanClap')].groupby('Investors')['Amount'].sum()
        st.subheader('Funding by different Investors')
        fig,ax = plt.subplots(figsize = (10,10))
        ax.pie(investor_funding,labels=investor_funding.index,autopct="%0.1f%%")
        st.pyplot(fig)

    df['Year'] = df['Date'].dt.year
    year_series = df[df['Startup'].str.contains('UrbanClap')].groupby('Year')['Amount'].sum()
    st.subheader('YoY Funding Raised')
    fig,ax = plt.subplots(figsize = (6,2))
    ax.plot(year_series.index,year_series.values)
    st.pyplot(fig)


def load_overall_analysis(option1,option2):
    progress_bar()

    st.title('Overall Analysis')

    #Month on Month Funding Chart
    st.subheader('Month Wise Analysis')
    if option2 == 'Total Funding':
        df['Year'] = df['Date'].dt.year
        df['Month Name'] = df['Date'].dt.month_name()
        df['Month Number'] = df['Date'].dt.month
        temp_df = df.groupby(['Year','Month Number','Month Name'])['Amount'].sum().reset_index().sort_values(['Year','Month Number'],ascending=[True,True])

        fig5,ax5 = plt.subplots(figsize = (15,5))
        temp = temp_df[temp_df['Year'] == int(option1)]
        ax5.plot(temp['Month Name'],temp['Amount'])
        st.pyplot(fig5)
    else:
        df['Year'] = df['Date'].dt.year
        df['Month Name'] = df['Date'].dt.month_name()
        df['Month Number'] = df['Date'].dt.month
        temp_df = df.groupby(['Year','Month Number','Month Name'])['Startup'].count().reset_index()

        fig5,ax5 = plt.subplots(figsize = (15,5))
        temp = temp_df[temp_df['Year'] == int(option1)]
        ax5.plot(temp['Month Name'],temp['Startup'])
        st.pyplot(fig5)


    col1,col2,col3,col4 = st.columns(4)

    with col1:
        #Total Funding
        total_funding = round(df['Amount'].sum())
        st.metric('Total Funding',str(total_funding)+' Cr')

    with col2:
        #Max Funding
        max_funding = df.groupby(['Startup'])['Amount'].sum().sort_values(ascending=False).head(1).values[0]
        company = df.groupby(['Startup'])['Amount'].sum().sort_values(ascending=False).head(1).index[0]
        st.metric(f'Max Funding taken by {company}',str(max_funding) + " Cr")

    with col3:
        #Avg ticket price
        avg_ticket_price = round(df.groupby(['Startup'])['Amount'].sum().mean())
        st.metric('Avg ticket size',str(avg_ticket_price) + " Cr")

    with col4:
        total_funded_startup = df.groupby(['Startup'])['Amount'].sum().count()
        st.metric('Total Funded Startups',str(total_funded_startup))

    #Sector Based Pie chart
    st.subheader('Sector wise analysis')
    fig, ax = plt.subplots(figsize = (10,10))
    sector = df.groupby(['Vertical'])['Amount'].sum()
    ax.pie(
        sector
    )
    st.pyplot(fig)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    df['Year'] = df['Date'].dt.year
    df['Month Name'] = df['Date'].dt.month_name()
    df['Month Number'] = df['Date'].dt.month
    temp_df = df.groupby(['Year','Month Number','Month Name'])['Amount'].sum().reset_index().sort_values(['Year','Month Number'],ascending=[True,True])
    option1 = st.sidebar.selectbox('Year',temp_df['Year'].unique().tolist())
    option2 = st.sidebar.selectbox('Select option',['Total Funding','Number of companies funded'])
    btn0 = st.sidebar.button('Find Overall Analysis')
    if btn0:
        load_overall_analysis(option1,option2)
elif option == 'Startup':
    startup_name = st.sidebar.selectbox('Select Startup Name',sorted(df['Startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startups')
    if btn1:
        load_startup_details(startup_name)
elif option == 'Investor':
    investor_name = st.sidebar.selectbox('Select Investor Name',sorted(set(df['Investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors')
    if btn2:
        load_investor_details(investor_name)