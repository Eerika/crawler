from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

# Importing our Scraping Functions
from scrape.scrape.spiders.notfound_scraping import NotFoundSpider
from scrape.scrape.spiders.amazon_scraping import ReviewspiderSpider
from scrape.scrape.spiders.oda_scraping import OdaSpider

import crochet
import time
import os


crochet.setup()  # TODO what is this?
app = Flask(__name__)
CORS(app)

SPIDERS = {"Oda": OdaSpider, "Amazon": ReviewspiderSpider, "NotFound": NotFoundSpider}

output_data = []
spider = OdaSpider
crawl_runner = CrawlerRunner()
baseURL = ""


@app.route("/output_data", methods=["GET"])
def get_data():
    response = jsonify({"status": "success", "output_data": output_data})
    return response


# After clicking the Submit Button FLASK will come into this
@app.route("/", methods=["POST"])
def submit():
    if request.method == "POST":
        global output_data
        global baseURL

        output_data = []  # Resetting output data
        post_data = request.get_json()  # Getting the form inputs
        print(post_data, output_data)
        baseURL = post_data["url"]
        scraper = post_data["scraperOption"]
        time = post_data["time"]

        # Passing to the Scrape function
        return redirect(
            url_for("scrape", scrape_option=scraper, scrape_time=time)
        )


@app.route("/scrape/<scrape_option>/<scrape_time>", methods=["GET"])
def scrape(scrape_option, scrape_time):
    spider = SPIDERS[scrape_option]

    # Passing that URL to our Scraping Function
    scrape_with_crochet(baseURL=baseURL, spider=spider)
    # Pause the function while the scrapy spider is running
    time.sleep(int(scrape_time))
    print("output_data: ", output_data)
    # Returns the scraped data after being running for 20 seconds.
    return jsonify(output_data)


@crochet.run_in_reactor
def scrape_with_crochet(baseURL, spider=OdaSpider):
    global crawl_runner
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    # This will connect to the spider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(spider, category=baseURL)
    dispatcher.connect(_crawler_Stop, signals.engine_stopped)
    return eventual


# This will append the data to the output data list.
def _crawler_result(item, response, spider):
    print(len(output_data), item)
    if len(output_data) < 30:
        output_data.append(dict(item))


def _crawler_Stop():
    # Perform any operation which is relevant to your application, like notify user
    print("*** Crawler has finished ***")


if __name__ == "__main__":
    app.run(debug=True)
