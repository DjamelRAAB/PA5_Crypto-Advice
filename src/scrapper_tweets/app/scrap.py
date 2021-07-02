import csv
import os
import datetime
import argparse
from time import sleep
import random
import pandas as pd
from functions import init_driver, get_last_date_from_csv, log_search_page, keep_scroling
from google.cloud import pubsub_v1




def scrap(start_date, max_date, words=None, interval=1, lang=None,
          headless=True, limit=float("inf"), resume=False, save_dir="outputs"):
    """
    scrap data from twitter using requests, starting from start_date until max_date. The bot make a search between each start_date and end_date
    (days_between) until it reaches the max_date.

    return:
    data : df containing all tweets scraped with the associated features.
    save a csv file containing all tweets scraped with the associated features.
    """

    # ------------------------- Variables : 
    # header of csv
    header = ['IdName', 'UserName', 'time', 'Text', 'Embtext', 'Emojis','NbComments', 'NbLikes', 'NbRetweets','LinkImage', 'UrlTweet','sentiment_analysis']
    # list that contains all data 
    data = []
    # unique tweet ids
    tweet_ids = set()
    # write mode 
    write_mode = 'w'
    # start scraping from start_date until <max_date>
    init_date = start_date  # used for saving file
    # add the <interval> to <start_dateW to get <end_date> for the first refresh
    end_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=interval)
    # set refresh at 0. we refresh the page for each <interval> of time.
    refresh = 0

    # ------------------------- settings :
    # file path
    if words:
        if type(words) == str : 
            words = words.split("//")
            path = save_dir + "/" + words[0] + '_' + str(init_date).split(' ')[0] + '_' + \
               str(max_date).split(' ')[0] + '.csv'
        else :
            path = save_dir + "/" + words[0] + '_' + str(init_date).split(' ')[0] + '_' + \
                   str(max_date).split(' ')[0] + '.csv'

    # create the <save_dir>
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # show images during scraping (for saving purpose)

    # initiate the driver
    driver = init_driver(headless)
    # resume scraping from previous work
    if resume:
        start_date = str(get_last_date_from_csv(path))[:10]
        write_mode = 'a'

    #------------------------- start scraping : keep searching until max_date
    # open the file
    with open(path, write_mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_mode == 'w':
            # write the csv header
            writer.writerow(header)
        # log search page for a specific <interval> of time and keep scrolling unltil scrolling stops or reach the <max_date>
        while end_date <= datetime.datetime.strptime(max_date, '%Y-%m-%d'):
            # number of scrolls
            scroll = 0
            # convert <start_date> and <end_date> to str
            if type(start_date) != str :
                start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
            if type(end_date) != str :
                end_date = datetime.datetime.strftime(end_date, '%Y-%m-%d')
            # log search page between <start_date> and <end_date>
            path = log_search_page(driver=driver, words=words, start_date=start_date,
                            end_date=end_date, lang=lang)
            # number of logged pages (refresh each <interval>)
            refresh += 1
            # number of days crossed
            #days_passed = refresh * interval
            # last position of the page : the purpose for this is to know if we reached the end of the page or not so
            # that we refresh for another <start_date> and <end_date>
            last_position = driver.execute_script("return window.pageYOffset;")
            # should we keep scrolling ?
            scrolling = True
            print("looking for tweets between " + str(start_date) + " and " + str(end_date) + " ...")
            print(" path : {}".format(path))
            # number of tweets parsed
            tweet_parsed = 0
            # sleep 
            sleep(random.uniform(0.5, 1.5))
            # start scrolling and get tweets
            driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position = \
                keep_scroling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position)

            # keep updating <start date> and <end date> for every search
            if type(start_date) == str:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=interval)
            else:
                start_date = start_date + datetime.timedelta(days=interval)
            if type(start_date) != str:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=interval)
            else:
                end_date = end_date + datetime.timedelta(days=interval)

    data = pd.DataFrame(data, columns = ['IdName', 'UserName', 'time', 'Text', 'Embtext', 'Emojis','NbComments', 'NbLikes', 'NbRetweets','LinkImage', 'UrlTweet','sentiment_analysis'])
    data["coin"] = words[0]

    # close the web driver
    driver.close()

    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrap tweets.')

    parser.add_argument('--words', type=str,
                        help='Queries. they should be devided by "//" : Cat//Dog.', default=None)
    parser.add_argument('--max_date', type=str,
                        help='Max date for search query. example : %%Y-%%m-%%d.', required=True)
    parser.add_argument('--start_date', type=str,
                        help='Start date for search query. example : %%Y-%%m-%%d.', required=True)
    parser.add_argument('--interval', type=int,
                        help='Interval days between each start date and end date for search queries. example : 5.',
                        default=1)
    parser.add_argument('--lang', type=str,
                        help='Tweets language. example : "en" for english and "fr" for french.', default=None)
    parser.add_argument('--headless', type=bool,
                        help='Headless webdrives or not. True or False', default=False)
    parser.add_argument('--limit', type=int,
                        help='Limit tweets per <interval>', default=float("inf"))
    parser.add_argument('--resume', type=bool,
                        help='Resume the last scraping. specify the csv file path.', default=False)

    args = parser.parse_args()


    words = args.words
    max_date = args.max_date
    start_date = args.start_date
    interval = args.interval
    lang = args.lang
    headless = args.headless
    limit = args.limit
    resume = args.resume

    data = scrap(start_date=start_date, max_date=max_date, words=words, interval=interval,
     lang=lang, headless=headless, limit=limit,resume=resume)
