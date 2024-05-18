# worki in progress
import streamlit as st
import pandas as pd
import numpy as np
# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time as ttt
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# scroll all data and after run this

# all functions


def scroller(count):
    if count == 200:
        count = count*1000
    elif count == 500:
        count = count*10000
    elif count == 1000:
        count = count*100000
    else:
        count = count*5000000
    for i in tqdm(range(0, count, 1000)):
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


def download_csv_file(data, flage=False):
    # takes data and make csv
    if flage:
        df = pd.DataFrame(
            data, columns=['Title', 'views', 'time', 'likes', 'video_links'])

        @st.cache
        def convert_to_csv(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_to_csv(df)

        st.write(df)

        # download button 1 to download dataframe as csv
        download1 = st.download_button(
            label="Download data as CSV2",
            data=csv,
            file_name='large_df.csv',
            mime='text/csv'
        )
        return df
    else:
        df = pd.DataFrame(
            data, columns=['Title', 'views', 'time', 'thumbnail', 'video_links'])

        @st.cache
        def convert_to_csv(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_to_csv(df)

        # display the dataframe on streamlit app
        st.write(df)

        # download button 1 to download dataframe as csv
        download2 = st.download_button(
            label="Download data as CSV1",
            data=csv,
            file_name='large_df.csv',
            mime='text/csv'
        )
        return df


def data_scrape2(dataframe):
    youtube = 'https://www.youtube.com'
    driver.get(youtube)
    # soup=BeautifulSoup(driver.page_source,'html.parser')
    data = []
    for i in tqdm(dataframe['video_links']):
        link = youtube+i
        driver.get(link)
        ttt.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            title = soup.find('yt-formatted-string',
                              class_="style-scope ytd-watch-metadata").text
        except:
            title = ''
        # because description is close so it is none
        try:
            views = soup.find_all(
                'span', class_="style-scope yt-formatted-string bold")[0].text
        except:
            views = np.nan
        try:
            time = soup.find_all(
                'span', class_="style-scope yt-formatted-string bold")[2].text
        except:
            time = np.nan

        try:
            likes = soup.find('like-button-view-model', class_="YtLikeButtonViewModelHost").find(
                'div', class_="yt-spec-button-shape-next__button-text-content").text
        except:
            likes = ''

        # likes = soup.find('like-button-view-model').find('div',
        #                                                  class_="yt-spec-button-shape-next__button-text-content").text
        # # description code
        # len(soup.find_all('span',class_="yt-core-attributed-string--link-inherit-color"))
        # for i in soup.find_all('span',class_="yt-core-attributed-string--link-inherit-color"):
        #    print(i.text)

        # print(title,views, time, likes, link)
        data.append([title, views, time, likes, link])
    return data


with st.echo():
    @st.cache_resource
    def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(
                    chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")
driver = get_driver()
    
link = 'https://www.youtube.com/'
st.title('Scrap and Analyse')
# final_link = 'https://www.youtube.com/@ashishchanchlanivines/videos'
final_link = st.text_input('Enter Chennal link')
# driver = webdriver.Chrome()

video_count = st.selectbox('How much videos has chennal', [
                           200, 500, 1000, 10000, 50000])

if final_link and video_count:
    but1 = st.button('Scrap Dataset')
    if but1:
        st.write('Please wait we are working')
        driver.get(final_link)
        ttt.sleep(3)
        scrol = scroller(video_count)
        if scrol == 'end':
            st.title('Almost Done')

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            data_for_download = data_scrape(soup)
            dataframe = download_csv_file(data_for_download)

            data_for_download2 = data_scrape2(dataframe)
            download_csv_file(data_for_download2, flage=True)
