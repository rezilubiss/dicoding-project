# Preparing Needed Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
sns.set(style='whitegrid')

# Creating Helper Functions

def create_daily_users_df(df):
    daily_users_df = df.resample(rule='D', on='dateday').agg({
        'registered': 'sum',
        'casual': 'sum',
        'total': 'sum'
    })
    daily_users_df = daily_users_df.reset_index()
    
    return daily_users_df

def create_casreg_pie(df):
    casreg_pie = df[['casual', 'registered']].sum()
    
    return casreg_pie

def create_sea_hour_df(df):
    sea_hour_df = df.groupby(by='season').agg({
        'registered':'sum',
        'casual':'sum',
        'total':'sum'
    }).sort_values(by='total', ascending=False)
    
    return sea_hour_df

def create_hr_hour_df(df):
    hr_hour_df = df.groupby(by='hour').agg({
        'registered':'sum',
        'casual':'sum',
        'total':'sum'
    }).sort_values(by='total', ascending=False)

    return hr_hour_df

def create_wd_hour_df(df): 
    wd_hour_df = df.groupby(by='workingday').agg({
        'registered':'sum',
        'casual':'sum',
        'total':'sum'
    }).sort_values(by='total', ascending=False)
    
    return wd_hour_df

def create_weat_hour_df(df):
    weat_hour_df = df.groupby(by='weather').agg({
        'registered':'sum',
        'casual':'sum',
        'total':'sum'
    }).sort_values(by='total', ascending=False)

    return weat_hour_df

# Load File as a Dataframe

all_df = pd.read_csv('main_data.csv')
all_df_copy = pd.read_csv('main_data.csv')

# dateday Sorting and Changing Data Type 
all_df.sort_values(by='dateday', inplace=True)
all_df.reset_index(inplace=True)
 
all_df['dateday'] = pd.to_datetime(all_df['dateday'])

# Making Filter for Dashboard

min_date = all_df["dateday"].min()
max_date = all_df["dateday"].max()
 
# Making Sidebar for Dashboard

with st.sidebar:
    # Insert Self Photo
    image = Image.open('DSC_6809 compress.jpg')
    st.image(image)

    # Insert Name, Email, and Dicoding ID
    st.write('''Nama: M. Faridzi A.R. Lubis
             Email: rezilubis212@gmail.com
             Dicoding ID: rezilubis''')
    
    # Mengambil start_date & end_date dari date_input

    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
        )
    
    # Making a Caption
    
    st.caption('Copyright :copyright: M. Faridzi A.R. Lubis 2023')

# Saving Filtered Data to main_df

main_df = all_df[(all_df["dateday"] >= str(start_date)) & 
                (all_df["dateday"] <= str(end_date))]

# Calling Helper Functions

daily_users_df = create_daily_users_df(main_df)
casreg_pie = create_casreg_pie(main_df)
sea_hour_df = create_sea_hour_df(main_df)
hr_hour_df = create_hr_hour_df(main_df)
wd_hour_df = create_wd_hour_df(main_df)
weat_hour_df = create_weat_hour_df(main_df)

# Making Title and Header for Dashboard

st.title('Proyek Analisis Data Bike Sharing oleh M. Faridzi A.R. Lubis :bar_chart:')

st.header('Welcome :sparkle:')

# Making Tabs for Dashboard

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    'About', 'Explanatory Analysis', 'Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Conclusion'
    ])

with tab1:

    # Making a Subheader About The Dataset

    st.subheader('About This Bike Sharing Dataset')

    st.text(
        '''
        This bike sharing dataset contains the hourly and daily count of rental bikes
        between the years 2011 and 2012 in the Capital bike share system with the
        corresponding weather and seasonal information.
        '''
    )

    # Making a Subheader About This Project's Questions

    st.subheader('What are the Questions?')

    st.text(
        '''
        1. Bagaimana perbandingan antara pengguna casual dan pengguna yang terdaftar pada
           bike sharing?
        2. Bagaimana perbandingan penggunaan bike sharing pada hari libur dan hari kerja?
        3. Pada waktu jam berapakah penggunaan bike sharing paling tinggi dan paling
           rendah?
        4. Bagaimana perbandingan penggunaan bike sharing pada 4 musim yang berbeda?
        5. Bagaimana perbandingan penggunaan bike sharing pada 4 tipe cuaca yang berbeda?
        '''
    )

with tab2:

    # Making a Subheader for Daily Bike Sharing Users Interactive Visualization

    st.subheader('Daily Users')

    # Making Columns for This Tab
    
    col1, col2, col3 = st.columns(3)
 
    # Making Sum of Daily Registered Users Metric

    with col1:
        registered_users = daily_users_df.registered.sum()
        st.metric("Registered Users", value=registered_users)
 
    # Making Sum of Daily Casual Users Metric
    
    with col2:
        casual_users = daily_users_df.casual.sum() 
        st.metric("Casual Users", value=casual_users)

    # Making Sum of Daily Total Users Metric
    
    with col3:
        total_users = daily_users_df.total.sum() 
        st.metric("Total Users", value=total_users)
 
    # Making Interactive Visualization with Line Chart for Sum of Daily Total Users
    
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(
        daily_users_df["dateday"],
        daily_users_df["total"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)

with tab3:

    # Making a Subheader About Sum of Casual and Registered Users

    st.subheader('Perbandingan Antara Pengguna Casual dan Pengguna yang Terdaftar Pada Bike Sharing')
    
    # Making a Pie Chart to Compare Sum of Casual and Registered Users
    
    f, ax = plt.subplots(figsize=(10, 5))
    plt.pie(
    x=casreg_pie,
    labels=('casual', 'registered'),
    colors=('#5F9EA0', '#7FFFD4'),
    autopct='%1.1f%%',
    wedgeprops = {'width':0.4}
    )
    
    st.pyplot(f)

with tab4:

    # Making a Subheader About Sum of Total Users on Workingday

    st.subheader('Perbandingan Penggunaan Bike Sharing Pada Hari Kerja dan Bukan Hari Kerja')
    
    # Making a Bar Plot to Compare Sum of Offday and Workday Total Users
    
    f, ax = plt.subplots(figsize=(10, 5))
    sns.despine(f)
    sns.set_style('whitegrid')
    sns.barplot(data=wd_hour_df, x='workingday', y='total', palette='viridis')
    plt.title("Perbandingan Penggunaan Bike Sharing Pada Hari Kerja dan Bukan Hari Kerja")
    plt.xlabel(None)
    plt.ylabel(None)
    
    st.pyplot(f)

with tab5:

    # Making a Subheader About The Most and Least Used Hours

    st.subheader('Waktu (Jam) Saat Penggunaan Bike Sharing Paling Tinggi dan Paling Rendah')
    
    # Making List of Colors for The Barplot

    colors = ['#5F9EA0', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4',
              '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4',
              '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#7FFFD4', '#5F9EA0'
              ]
    
    # Making a Barplot to Compare The Most and Least Used Hours 
    
    f, ax = plt.subplots(figsize=(10, 5))
    sns.despine(f)
    sns.set_style('whitegrid')
    sns.barplot(data=hr_hour_df, x='total', y='hour', palette=colors, orient='h')
    plt.title('Penggunaan Bike Sharing Terbanyak dan Tersedikit Berdasarkan Waktu (Jam)')
    plt.xlabel(None)
    plt.ylabel(None)

    st.pyplot(f)
    
    # Making a Lineplot to Compare The Most and Least Used Hours by Season
    
    f, ax = plt.subplots(figsize=(10, 5))
    sns.despine(f)
    sns.set_style('whitegrid')
    sns.lineplot(x='hour', y='total', data=all_df_copy[['hour', 'season', 'total']], hue='season')
    plt.xticks(rotation=45)
    plt.title('Penggunaan Bike Sharing Berdasarkan Season Dengan Distribusi Waktu (Jam)')
    plt.xlabel(None)
    plt.ylabel(None)

    st.pyplot(f)

    # Making a Lineplot to Compare The Most and Least Used Hours by Weather
    
    f, ax = plt.subplots(figsize=(10, 5))
    sns.despine(f)
    sns.set_style('whitegrid')
    sns.lineplot(x='hour', y='total', data=all_df_copy[['hour', 'weather', 'total']], hue='weather')
    plt.xticks(rotation=45)
    plt.title('Penggunaan Bike Sharing Berdasarkan Weather Dengan Distribusi Waktu (Jam)')
    plt.xlabel(None)
    plt.ylabel(None)

    st.pyplot(f)

    # Making a Lineplot to Compare The Most and Least Used Hours by Workingday
    
    f, ax = plt.subplots(figsize=(10, 5))
    sns.despine(f)
    sns.set_style('whitegrid')
    sns.lineplot(x='hour', y='total', data=all_df_copy[['hour', 'workingday', 'total']], hue='workingday')
    plt.xticks(rotation=45)
    plt.title('Penggunaan Bike Sharing Berdasarkan Workingday Dengan Distribusi Waktu (Jam)')
    plt.xlabel(None)
    plt.ylabel(None)

    st.pyplot(f)

with tab6:

    # Making a Subheader About Sum of Total Users in 4 Different Seasons

    st.subheader('Perbandingan Penggunaan Bike Sharing Pada 4 Musim yang Berbeda')

    # Making a Barplot to Compare The Sum of Total Users in 4 Different Seasons
    
    f, ax = plt.subplots(figsize=(10, 5))
    sns.despine(f)
    sns.set_style('whitegrid')
    sns.barplot(data=sea_hour_df, x='season', y='total', palette='viridis')
    plt.title("Perbandingan Penggunaan Bike Sharing Pada 4 Musim yang Berbeda")
    plt.xlabel(None)
    plt.ylabel(None)

    st.pyplot(f)

with tab7:

    # Making a Subheader About Sum of Total Users in 4 Different Weathers

    st.subheader('Perbandingan Penggunaan Bike Sharing pada 4 Tipe Cuaca yang Berbeda')

    # Making a Barplot to Compare The Sum of Total Users in 4 Different Weathers
    
    f, ax = plt.subplots(figsize=(10, 5))
    sns.despine(f)
    sns.set_style('whitegrid')
    sns.barplot(data=weat_hour_df, x='weather', y='total', palette='viridis')
    plt.title("Perbandingan Penggunaan Bike Sharing Pada 4 Tipe Cuaca yang Berbeda")
    plt.xlabel(None)
    plt.ylabel(None)

    st.pyplot(f)

with tab8:

    # Making a Subheader About The Conclusion of This Project

    st.subheader('Conclusion')

    st.text(
        '''
        1. Pengguna registered lebih banyak daripada pengguna casual (81.2 % vs 18.8 %)
        2. Terdapat lebih banyak pengguna Bike Sharing pada saat hari kerja dibandingkan
           dengan bukan hari kerja
        3. Jam 05 pm merupakan waktu dengan pengguna Bike Sharing terbanyak, sedangkan
           jam 04 am merupakan waktu dengan pengguna Bike Sharing tersedikit
        4. Pada saat hari kerja, jam 05 pm merupakan waktu dengan pengguna Bike Sharing
           terbanyak
        5. Pada saat bukan hari kerja, jam 01 pm merupakan waktu dengan pengguna Bike
           Sharing terbanyak
        6. Fall season merupakan waktu dengan pengguna Bike Sharing terbanyak, sedangkan
           springer season merupakan waktu dengan pengguna Bike Sharing tersedikit
        7. Cuaca cerah merupakan waktu dengan pengguna Bike Sharing terbanyak, sedangkan
           cuaca hujan deras merupakan waktu dengan pengguna Bike Sharing tersedikit
        '''
    )
    
    # Making a Closing Statement With a Subheader
    
    st.subheader('Thank You')

# Making a Caption

st.caption('Copyright :copyright: M. Faridzi A.R. Lubis 2023')