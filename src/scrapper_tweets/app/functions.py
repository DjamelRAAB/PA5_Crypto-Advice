import os
import re
from time import sleep
import numpy as np
from textblob import TextBlob
import random
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import pandas as pd
from selenium.webdriver.common.keys import Keys
# import pathlib

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_data(page, save_images = False, save_dir = None):
    """Extract data from tweet page"""
    image_links = []

    try:
        username = page.find_element_by_xpath('.//span').text
    except:
        return

    try:
        handle = page.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except:
        return

    try:
        postdate = page.find_element_by_xpath('.//time').get_attribute('datetime')
        #postdate = postdate
    except:
        return 
    

    try:
        text = page.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    except:
        text = ""

    try:
        embedded = page.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    except:
        embedded = ""

    #text = comment + embedded

    try:
        reply_cnt = page.find_element_by_xpath('.//div[@data-testid="reply"]').text
    except:
        reply_cnt = 0

    try:
        retweet_cnt = page.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    except:
        retweet_cnt = 0

    try:
        like_cnt = page.find_element_by_xpath('.//div[@data-testid="like"]').text
    except:
        like_cnt = 0

    try:
        elements = page.find_elements_by_xpath('.//div[2]/div[2]//img[contains(@src, "https://pbs.twimg.com/")]')
        for element in elements:
        	image_links.append(element.get_attribute('src'))

    except:
        image_links = []

    #image_links = ''.join(image_links)

    #if save_images == True:
    #	for image_url in image_links:
    #		save_image(image_url, image_url, save_dir)
    # handle promoted tweets

    try:
        promoted = page.find_element_by_xpath('.//div[2]/div[2]/[last()]//span').text == "Promoted"
    except:
        promoted = False
    if promoted:
        return

    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = page.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute('src')
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)

    # tweet url
    try:
        element = page.find_element_by_xpath('.//a[contains(@href, "/status/")]')
        tweet_url = element.get_attribute('href')
    except:
        return

    try:
        sentiment_analysis = scorer_handler(text)
        print("llaa")
    except:
        sentiment_analysis = 0

    print("----------------------------",sentiment_analysis)

    #sentiment_analysis = scorer_handler(text)

    tweet = (username, handle, postdate, text, embedded, emojis, reply_cnt,retweet_cnt, like_cnt, image_links, tweet_url,sentiment_analysis)
    return tweet



def init_driver(headless=True, proxy=None, show_images=False):
    """ initiate a chromedriver instance """

    # create instance of web driver
    chromedriver_path = chromedriver_autoinstaller.install()
    options = Options()
    if headless is True:

        print("Scraping on headless mode.")
        '''
        options.add_argument('--disable-gpu')
        options.headless = True'''

        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
    if show_images == False:
    	prefs = {"profile.managed_default_content_settings.images": 2}
    	options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.set_page_load_timeout(100)
    return driver


def log_search_page(driver, start_date, end_date, lang, words):
    """ Search for this query between start_date and end_date"""


    if words is not None:
        if len(words)==1:
            words = "(" +  str(''.join(words)) + ")%20"
        else :
            words = "(" + str('%20OR%20'.join(words)) + ")%20"
    else:
        words = ""

    if lang is not None:
        lang = 'lang%3A' + lang
    else:
        lang = ""

    end_date = "until%3A" + end_date + "%20"
    start_date = "since%3A" + start_date + "%20"



    path = 'https://twitter.com/search?q='+words+end_date+start_date+lang+'&src=typed_query'
    driver.get(path)
    return path


def get_last_date_from_csv(path):
    df = pd.read_csv(path)
    return datetime.datetime.strftime(max(pd.to_datetime(df["time"])), '%Y-%m-%dT%H:%M:%S.000Z')


def keep_scroling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position):
    """ scrolling function for tweets crawling"""


    while scrolling and tweet_parsed < limit:
        sleep(random.uniform(0.5, 1.5))
        # get the page of tweets
        pages = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        for page in pages:
            tweet = get_data(page)
            if tweet:
                # check if the tweet is unique
                tweet_id = ''.join(tweet[:-3])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                    last_date = str(tweet[2])
                    print("Tweet made at: " + str(last_date) + " is found.")
                    writer.writerow(tweet)
                    tweet_parsed += 1
                    if tweet_parsed >= limit:
                        break
        scroll_attempt = 0
        while tweet_parsed < limit:
            # check scroll position
            scroll += 1
            print("scroll ", scroll)
            sleep(random.uniform(0.5, 1.5))
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(random.uniform(0.5, 1.5))  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position



def check_exists_by_link_text(text, driver):
    try:
        driver.find_element_by_link_text(text)
    except NoSuchElementException:
        return False
    return True


def scorer_handler(stories):
    """Handler for vader scoring method accross source files."""

    stories_sentences = [stories.split('. ')]
    print(stories_sentences)

    #frame['vader_score'], frame['textblob_score'] = self.sentiment_scorer(stories_sentences)
    frame= sentiment_scorer(stories_sentences)
    return frame[0]


def sentiment_scorer(stories_sentences):
    """
    TextBlob scoring function; splits stories by sentence,
    takes respective sentence sentiment, averages sentences for overall story sentiment.
    """
    textblob_scores = [np.mean([TextBlob(sentence).sentiment.polarity for sentence in story]) for story in stories_sentences]

    return textblob_scores