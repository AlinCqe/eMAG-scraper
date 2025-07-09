from flask import Blueprint, render_template, request, jsonify

from core.main import main



views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        item = data['query']
        return jsonify(main(item))

    return render_template('index.html')

