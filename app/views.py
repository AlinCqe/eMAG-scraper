from flask import Blueprint, render_template, request

from core.main import main

views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        item = request.form['item']
        main(item)

    return render_template('index.html')

