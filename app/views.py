from flask import Blueprint, render_template, request

from core.main import main

views = Blueprint('views', __name__)



@views.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@views.route('/search', methods=['POST'])
def hola():
    item = request.form['item']
    main(item)
    return f'Hello World item {item}'
    

