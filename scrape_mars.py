import pandas as pd
import pymongo
from datetime import datetime
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():
    mars_scrape_results = {}

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    # ran browser: headless=False during build and testing, set to True for submission

    news_url = "http://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    news_response = browser.html
    soup_news = bs(news_response, 'html.parser')
    news_title = soup_news.find('div', class_='content_title').text.strip()
    news_teaser = soup_news.find('div', class_='article_teaser_body' ).text.strip()
    mars_scrape_results['news_title'] = news_title
    mars_scrape_results['news_teaser'] = news_teaser

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_response = browser.html
    soup_jpl = bs(jpl_response, 'html.parser')
    footer = soup_jpl.find('footer')
    featured_img_a = footer.find('a')
    url_tag = featured_img_a['data-fancybox-href']
    featured_image_url = ("https://www.jpl.nasa.gov" + url_tag)
    mars_scrape_results['jpl_featured_image'] = featured_image_url

    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_twitter_url)
    twitter_response = browser.html
    soup_twitter = bs(twitter_response, 'html.parser')
    mars_weather = soup_twitter.find('p', class_="TweetTextSize--normal").text
    mars_scrape_results['mars_weather'] = mars_weather

    mars_facts_url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(mars_facts_url)
    mars_facts_df = mars_table[1]
    mars_facts_df.to_html("mars_facts.html")
    mars_facts_html = mars_facts_df.to_html(index=False, header=False)
    mars_scrape_results['fact_table_html'] = mars_facts_html

    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)
    astro_response = browser.html
    soup_astro = bs(astro_response, 'html.parser')
    hem_image_set = soup_astro.find_all("div", class_="description")

    mars_image_urls = []

    for link in hem_image_set:
        url_dict = {}
        hem_name = link.find("h3").text[:-9]
        hem_search = link.find("h3").text[:5]
        url_dict['title'] = hem_name
        browser.click_link_by_partial_text(hem_search)
        browser.click_link_by_partial_text("Sample")
        url_dict['img_url'] = browser.windows[1].url
        browser.windows[1].close()
        browser.back()
        mars_image_urls.append(url_dict)
        mars_scrape_results['hemisphere_images'] = mars_image_urls

    mars_scrape_results["query_time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    return mars_scrape_results
