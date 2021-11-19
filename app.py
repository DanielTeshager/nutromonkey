from flask import Flask, app, render_template, request, redirect, url_for, flash, jsonify
import json
import requests
from flask.wrappers import Response
from werkzeug.wrappers import response
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/search.html', resultdata={}, item ="" )

@app.route('/search', methods=['GET', 'POST'])
def search():
    key = request.form['key']
    response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?query='+key+'&pageSize=2&api_key=Hal64gsGkYVlg6bhIAn5zQoLR6GqbuSzWa5LsJLj')
    result = json.loads(response.text)
    data_dict = {data['nutrientName'] : data['value'] for data in result['foods'][0]['foodNutrients']}
    data = dict(sorted(data_dict.items(), key = lambda x: x[1])[-10:])
    return render_template('pages/search.html', resultdata=data, item=key)