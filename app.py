import streamlit as st
import pandas as pd
import numpy as np
# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time as ttt
from tqdm import tqdm

# scroll all data and after run this

# all functions


def scroller():
    for i in tqdm(range(0, 500000, 1000)):
        driver.execute_script("window.scrollTo(0, " + str(i) + ")")
        driver.execute_script("(0,"+str(i)+")")
        ttt.sleep(.1)
    return 'end'

def data_scrape(soups):
    soup = soups.find_all('ytd-rich-item-renderer')
    data1 = []
    for sp in soup:
        try:
            title = sp.find(
                'a', class_="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media").text

        except:
            title = ''
        try:
            video_link = sp.find(
                'a', class_="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media").get('href')

        except:
            video_link = ''
        try:
            views = sp.find_all(
                'span', "inline-metadata-item style-scope ytd-video-meta-block")[0].text.strip(' views')
        except:
            views = ''

        try:
            time = sp.find_all(
                'span', "inline-metadata-item style-scope ytd-video-meta-block")[1].text

        except:
            time = np.nan
        try:
            thumbnail = sp.find('img').get('src').split('?')[0]
        except:
            thumbnail = ''
        data1.append([title, views, time, thumbnail, video_link])

    # print(data)
    data2 = pd.DataFrame(
        data1, columns=['title', 'views', 'time', 'thumbnail', 'video_link'])
    data2.to_csv('Youtube_gfg.csv', index=False)
    return data1

def download_csv_file(data):
    ## takes data and make csv
    df = pd.DataFrame(data)
    
    @st.cache
    def convert_to_csv(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')
    
    csv = convert_to_csv(df)
    
    # display the dataframe on streamlit app
    st.write(df)
    
    # download button 1 to download dataframe as csv
    download1 = st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv'
    )

link = 'https://www.youtube.com/'
# name='gfg'
# final_link=link+name
st.title('Scrap and Analyse')
final_link = 'https://www.youtube.com/@ashishchanchlanivines/videos'
final_link = st.text_input('Enter Chennal link')
driver = webdriver.Firefox()
if final_link:
    but1 = st.button('Scrap Dataset')
    if but1:
        driver.get(final_link)
        ttt.sleep(3)
        scrol = scroller()
        if scrol == 'end':
            st.title('Almost Done')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            data_for_download=data_scrape(soup)
            # download='D:\web_scraping\Youtube_gfg.csv'
            download_csv_file(data_for_download)
