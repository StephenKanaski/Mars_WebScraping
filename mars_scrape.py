#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


# # Mac User

# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
# !which chromedriver

# /usr/local/bin/chromedriver

# def init_browser():
#   executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#   browser = Browser('chrome', **executable_path, headless=False)


# # Windows User

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
# # NASA Mars News

    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    articles = soup.find('div', class_='list_text')
    news_title = articles.find('div', class_='content_title').text
    news_p = articles.find('div', class_='article_teaser_body').text

    browser.quit()

    print(f"The latest news title is: '{news_title}.'")
    print(f"The article concerns: '{news_p}'")


# # JPL Mars Space Images - Featured Image

    browser = init_browser()

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    results = soup.find('div', class_='carousel_items')
    img_link = results.a['data-fancybox-href']
    print(f"https://www.jpl.nasa.gov" + img_link)


# print out address of largesize of featured image. click by partial text required
    element_full = browser.links.find_by_partial_text("FULL IMAGE")
    element_full.click()
    time.sleep(1)

    element_more = browser.links.find_by_partial_text("more info")
    element_more.click()
    time.sleep(1)

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    img_element = img_soup.find('figure', class_='lede')
    lrg_img = img_element.find('a')['href']

    # print(f"https://www.jpl.nasa.gov" + lrg_img)
    featured_img = f'https://www.jpl.nasa.gov{lrg_img}'

    print(featured_img)

    browser.quit()


# # Mars Weather via Twitter

    # browser = init_browser()

    # twitter_url = 'https://www.twitter.com/marswxreport?lang=en'
    # browser.visit(twitter_url)

    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')

    # tweet = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    # weather = tweet.find('span').text
    # print(f"Mars weather: {weather}")

    # browser.quit()


# # Mars Facts

    browser = init_browser()

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    tables = pd.read_html(facts_url)
    # tables

    mars_facts = tables[0]
    mars_facts.columns = ['Fact_Categories', 'Martian Facts']
    # mars_facts.head()

    mars_facts.set_index('Fact_Categories', inplace=True)
    # mars_facts.head()

    html_marstable = mars_facts.to_html(header=True, index=True)
    # html_marstable

    html_marstable.replace('\n', '')

    mars_facts.to_html('mars_table.html')

    browser.quit()

# # Mars Hemispheres

    browser = init_browser()

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    astrogeology_url = 'https://astrogeology.usgs.gov'

    hems_url = soup.find_all('div', class_="item")

    hemispheres = []

    for hem in hems_url:
        hemis_url = hem.find('a')['href']
        hemispheres.append(hemis_url)
    
    print(hemispheres)


    hem_image_url = []
    for hemisphere in hemispheres:
        hem_astro_url = astrogeology_url + hemisphere
#        print(hem_astro_url)
    
        browser.visit(hem_astro_url)
        time.sleep(2)
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        title = soup.find('h2', class_="title").text
        hemi_title = title.split(' Enhanced')[0]
#       print(hemi_title)
    
        img = soup.find('div', class_="downloads")
        img_url = img.find('li').a['href']
    
        hem_image_url.append({"title": hemi_title, "img_url": img_url})

    browser.quit()

    print(hem_image_url)

# # Create a Dictionary to house all Mars Data

    mars_data = {}

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p
    mars_data['featured_image_url'] = featured_img
    mars_data['mars_facts_table'] = html_marstable
    mars_data['hemisphere_images_urls'] = hem_image_url

    print("Scrape Competed")

    return mars_data


