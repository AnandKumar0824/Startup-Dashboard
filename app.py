import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('startup-cleaned.csv')
st.set_page_config(layout='wide',page_title='Startup Analysis')

df['date'] = df['date'].str.strip()
df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def investor_details(selected_investor):
    st.title(selected_investor)
    last_5 = df[df['investors'].str.contains(selected_investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Last 5 Investments')
    st.dataframe(last_5)

    col1 , col2 = st.columns(2)

    with col1:
        # Highest investment
        big_series = df[df['investors'].str.contains(selected_investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values,color=colors[:len(big_series)])
        st.pyplot(fig)

    with col2:
        st.subheader("Sectors Invested in")
        vertical_series = df[df['investors'].str.contains(selected_investor)].groupby('vertical')['amount'].sum()
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%.01f%%")
        st.pyplot(fig1)


    col3 , col4 = st.columns(2)
    with col3:
        st.subheader("Stage wise Investments")
        stage = df[df['investors'].str.contains(selected_investor)].groupby('round')['amount'].sum()
        fig3,ax2 = plt.subplots()
        ax2.pie(stage,labels=stage.index,autopct="%0.01f%%")
        st.pyplot(fig3)

    with col4:
        st.subheader("City Wise Investments")
        city = df[df['investors'].str.contains(selected_investor)].groupby('city')['amount'].sum()
        fig4,ax3 = plt.subplots()
        ax3.pie(city,labels=city.index,autopct="%0.01f%%")
        st.pyplot(fig4)

    st.subheader("Year of Year Investments")
    df['year'] = df['date'].dt.year
    year = df[df['investors'].str.contains(selected_investor)].groupby('year')['amount'].sum()
    fig5,ax4 = plt.subplots()
    ax4.plot(year.index,year.values)
    st.pyplot(fig5)

    st.subheader("Similar Investments")
    similar = df[df['investors'].str.contains(selected_investor, na=False)].groupby('vertical')['amount'].sum()
    st.dataframe(similar)

def over_all_analysis():
    st.subheader('Over All Analysis')
    col1 ,col2,col3,col4 = st.columns(4)

    with col1:
        # Total invested amount
        total = round(df['amount'].sum(), 2)
        st.metric('Total', str(total) + ' CR')

    with col2:
        # Maximum amount invested
        maxamount = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max',str(maxamount)+' CR')

    with col3:
        # Average amount Investment
        avg = df.groupby('startup')['amount'].sum().mean()
        st.metric('Average',str(round(avg,2))+" CR")

    with col4:
        # Total startup funding
        num_startups = df['startup'].nunique()
        st.metric("Funded Startups",str(num_startups)+' CR')

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Month on Month Graph")
        selected_option = st.selectbox('Select Type',['Total Amount','Count'])
        if selected_option == 'Total Amount':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
            temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
            fig3, ax3 = plt.subplots(figsize=(6,4))
            plt.tight_layout()
            ax3.plot(temp_df['x_axis'],temp_df['amount'])
            st.pyplot(fig3)
        else:
            temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
            temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
            fig3, ax3 = plt.subplots()
            ax3.plot(temp_df['x_axis'], temp_df['amount'])
            st.pyplot(fig3)
    with col6:
        st.subheader("Top Sectors ")
        selected_option = st.selectbox('Select Type',['Total','Count'])
        if selected_option == 'Total':
            fig,ax = plt.subplots(figsize=(6,4))
            plt.tight_layout()
            ax.pie(df['vertical'].value_counts().head(5), labels=list(df['vertical'].value_counts().head(5).index),
                    autopct='%0.1f%%')
            ax.set_aspect('equal')

            st.pyplot(fig)

        else:
            sector = df['vertical'].value_counts().head()
            sector_sum = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
            fig, ax = plt.subplots()
            sns.barplot(
                x=sector_sum.values,
                y=sector_sum.index,
                hue=sector_sum.index,
                palette='Set2',
                ax=ax,
                legend=False
            )

            ax.set_xlabel("Total Funding")
            ax.set_ylabel("Sector")
            ax.set_title("Top Sectors by Funding")
            st.pyplot(fig)

    col7, col8 = st.columns(2)
    with col7:
        st.subheader("Top Fundings")
        temp = df['round'].value_counts().head(5)
        fig,ax = plt.subplots()
        sns.barplot(x=temp.index, y=temp.values,hue = temp.index)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col8:
        st.subheader("City-wise Funding")
        city = df.groupby('city')['round'].count().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(4,4.8))
        sns.barplot(x=city.values, y=city.index, hue=city.index)
        st.pyplot(fig)

    col9, col10 = st.columns(2)
    with col9:
        st.subheader('Top Startups By Year')
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        yr = st.selectbox('Select Year',[2020, 2019, 2018, 2017, 2016, 2015],key='startup_year')
        temp = df[df['year'] == yr]
        temp_year = temp.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=temp_year.values, y=temp_year.index, hue=temp_year.index)
        st.pyplot(fig)

    with col10:
        st.subheader("Overall Top Startups")
        yrr = st.selectbox('Overall', ['Overall'])
        overall = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=overall.values, y=overall.index, hue=overall.index)
        st.pyplot(fig)

    col11, col12 = st.columns(2)

    with col11:
        st.subheader("Top Investors by Year")
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        yr1 = st.selectbox('Select Year', [2020, 2019, 2018, 2017, 2016, 2015],key='Investor_year')
        top_invest = df[df['year'] == yr1]
        top_invest = top_invest.groupby('investors')['amount'].sum().sort_values(ascending=False).head(5)
        fig1, ax2 = plt.subplots()
        sns.barplot(x=top_invest.values, y=top_invest.index, hue=top_invest.values)
        st.pyplot(fig1)

    with col12:
        st.subheader("Top investors")
        st.selectbox('Overall Top Investors', ['Overall'],key='Investor_yearr')
        top_invest = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(5)
        fig, ax1 = plt.subplots()
        sns.barplot(x=top_invest.values, y=top_invest.index, hue=top_invest.values)
        st.pyplot(fig)




st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Investor'])


if option == 'Overall Analysis':
    over_all_analysis()

else:
    selected_investor = st.sidebar.selectbox('Select Startup',set(df['investors'].str.split(',').sum()))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        investor_details(selected_investor)