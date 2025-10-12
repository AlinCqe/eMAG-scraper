"""
from flask import Blueprint, render_template, request, jsonify

from core.main import ScrapingSession



views = Blueprint('views', __name__)

session = None

@views.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@views.route('/htmlscraper', methods=['POST'])
def html_scraper():
    global session
    data = request.get_json()
    item = data['query']
    session = ScrapingSession(item)
 
    return jsonify(session.html_scraper())




@views.route('/firstapiscraper', methods=['GET'])
def first_api_scraper():

    global session
    return jsonify(session.first_api_scraper())

@views.route('/secondapiscraper', methods=['GET'])
def second_api_scraper():

    global session
    return jsonify(session.second_api_scraper())
"""