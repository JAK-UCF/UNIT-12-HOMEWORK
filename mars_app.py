import pymongo
import scrape_mars
from flask import Flask, render_template, jsonify, redirect

mars_app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.scraped_mars_info
collection = db.mars_info

@mars_app.route("/")
def index():
    mars_scrape_results = collection.find_one()
    return render_template("index.html", scrape_results=mars_scrape_results)

@mars_app.route("/scrape")
def scrape_sites():
    mars_scrape_results = scrape_mars.scrape()
    collection.find_one_and_replace({}, mars_scrape_results, upsert = True)
    print('Mars scrape and replace complete.')
    return redirect("http://localhost:5000/")

if __name__ == "__main__":
    mars_app.run(debug=True)