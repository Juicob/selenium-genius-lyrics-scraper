from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import date
import sys
import pandas as pd
import json


options = webdriver.ChromeOptions()
options.add_argument ("lang = en_us")
options.page_load_strategy = 'eager'
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='chromedriver.exe',options = options)
driver.set_window_position(-1500, 100)

def csss(parent, sel):
    return parent.find_elements_by_css_selector(sel)
def css(parent, sel):
    return parent.find_element_by_css_selector(sel)
def xpaths(parent, sel):
    return parent.find_elements_by_xpath(sel)
def xpath(parent, sel):
    return parent.find_element_by_xpath(sel)


# * saving this in case I work out iframs so I don't need to gather album urls for each artist should I expand
# def make_album_row():
#     album_row = {}
#     album_row['album_title'] = None
#     album_row['album_url'] = None
#     # * album cover?
#     return album_row
    
    
# albums = []
# def scrape_albums():
#     # print(len(csss(driver, 'div.profile_list_item mini-album-card')))
#     for album in csss('div.profile_list_item mini-album-card'):
#         print(album)
#         album_row = make_album_row()
#         album_row['album_title'] = album.css('a').get_attribute('href')
#         album_row['album_url'] = album.css('a').get_attribute('title')
#         albums.append(album_row)
#     return albums

#                         # ? I'm thinkin I'll have it first run through to gather albums then songs titles, then lyrics for each - 11/6/2020
                        
# def try_hard(key, value):
#     ''' Wrap the world in try/excepts
#         I'm so tired of running into random ass elements that don't have things that it should
#         so it's defaulting to none and if it's there it'll be filled - this could be doc'd better
#         but this is the mood atm - but wooooww idek how to write this write now...'''
        
#     tryddd:
#         key = value
#         return ....
#     except:
#         print(f'tried to find {key} with {value} but nah')


def make_track_row():
    track_row = {}
    track_row['album'] = None
    track_row['track_title'] = None
    track_row['track_url'] = None
    track_row['track_views'] = None
    return track_row

tracks = []
def scrape_tracks():
    for track in csss(driver, 'div.chart_row'):
        track_row = make_track_row()
        track_row['album'] =  css(driver, 'h1.header_with_cover_art-primary_info-title').text
        track_row['track_title'] = css(track, 'h3').text.strip()
        try:
            track_row['track_url'] = css(track, 'a').get_attribute('href')
        except:
            print(f'tried to find track_url')
        try:
            track_row['track_views'] = css(track, 'div.chart_row-metadata_element').text.strip()
        except:
            print(f'tried to find track_views')
        # todo consider standardizing view values (thousands vs millions) or keep numbers only - 11/6/2020
        # todo and filter by < small number to denote views in millions as hits - 11/6/2020
        print(track_row)
        tracks.append(track_row)
    return tracks

def make_lyrics_row():
    lyrics_row = {}
    lyrics_row['album'] = None
    lyrics_row['lyrics_title'] = None
    lyrics_row['lyrics_url'] = None
    lyrics_row['lyrics'] = None
    lyrics_row['track_views'] = None
    return lyrics_row

lyrics = []
def scrape_lyrics():
    for track in tracks:
        lyrics_row = make_lyrics_row()
        try:
            driver.get(track['track_url'])
        except:
            continue
        sleep(1)
        # pages sometimes seem to get stuck until you scroll down a bit so adding a few page downs seems to move things along
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        lyrics_row['album'] = track['album']
        lyrics_row['lyrics_url'] = track['track_url']
        lyrics_row['lyrics_title'] = track['track_title']
        lyrics_row['track_views'] = track['track_views']
        # there are one or two tracks that don't actually have lyrics 
        try:
            lyrics_row['lyrics'] = css(driver, 'section p').text
            print(lyrics_row['lyrics'].split(' ')[:2])
        except:
            print('no lyrics found')
        # added to view progress while the scraper is running
        print(lyrics_row['lyrics_title'])
        print(f'{len(lyrics) + 1} / {len(tracks)}')
        print()
        lyrics.append(lyrics_row)
        # could probably save this for the end so it's not writing every iteration but I had some issues with errors at first so I put it here and think I'll just leave it for now
        with open(r'C:\Users\Juice\Python_Projects\ye_lines\drake_lyrics.json', 'w') as fp:
            json.dump(lyrics, fp)
    return lyrics
                        #  todo test make albums and scrape by itself on genius - possible issue with iframes - 11/4/2020
                        # todo try scrapping individual album first and going from there - 11/4/2020
        
# set source urls
# * manually gathereing album urls because I'm a scrub and haven't figured out switching through iframes yet
# * at least I think that's the issue -_-' - be better yo - 11/6/2020
album_urls = [
    # 'https://genius.com/artists/Drake',
    'https://genius.com/albums/Drake/Certified-lover-boy',
    'https://genius.com/albums/Drake/Dark-lane-demo-tapes',
    'https://genius.com/albums/Drake/Care-package',
    'https://genius.com/albums/Drake/The-best-in-the-world-pack',
    'https://genius.com/albums/Drake/Scorpion',
    'https://genius.com/albums/Drake/Scary-hours',
    'https://genius.com/albums/Drake/More-life',
    'https://genius.com/albums/Drake/Views',
    'https://genius.com/albums/Drake/If-youre-reading-this-its-too-late',
    'https://genius.com/albums/Drake/Nothing-was-the-same',
    'https://genius.com/albums/Drake/Take-care',
    'https://genius.com/albums/Drake/Thank-me-later',
    'https://genius.com/albums/Drake/So-far-gone-ep',
    'https://genius.com/albums/Drake/So-far-gone',
    'https://genius.com/albums/Drake/Comeback-season',
    'https://genius.com/albums/Drake/Room-for-improvement',
    'https://genius.com/albums/Drake/Drake-demo-disk',
    'https://genius.com/albums/Drake/Unreleased-songs'

    ]

# go to all album links and scrape information
for album in album_urls:
    driver.get(album)
    scrape_tracks()
# using the scraped links from the albums, go to each track and grab lyrics
scrape_lyrics()

lyrics_df = pd.DataFrame(lyrics)

# just a few quality of life things for myself for when the program finishes
print(lyrics_df.head())
print(f'{lyrics_df["lyrics"].count()} items scraped')
print('Exporting df to csv')

save_path = r'C:\Users\Juice\Python_Projects\ye_lines\drake_data' + str(date.today()).replace('-','') + '.csv'
print(f'Saved to - {save_path}')
lyrics_df.to_csv(f'{save_path}', index = False, encoding='utf-8-sig')
    
sleep(3)
print('Closing')
driver.quit()
sys.exit()