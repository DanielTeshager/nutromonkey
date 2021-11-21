from flask import Flask, app, render_template, request, redirect, url_for, flash, jsonify
import json
import requests
import wikipedia
from flask.wrappers import Response
from werkzeug.wrappers import response
import re
# Create the application instance
app = Flask(__name__)
# Create secret key for session
app.secret_key = "super secret key"

# Create a URL route in our application for "/"
@app.route('/')
def index():
    return render_template('pages/home.html', resultdata={}, item ="" )

# Create a URL route in our application for "/search"
@app.route('/search', methods=['GET', 'POST'])
def search():
    key = request.form['key']
    wiki_result = wikipedia.summary(f'{key} in diet')
    print(wiki_result)
    try:
        response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?query='+key+'&pageSize=2&api_key=Hal64gsGkYVlg6bhIAn5zQoLR6GqbuSzWa5LsJLj')
        result = json.loads(response.text)
        data_dict = {data['nutrientName'] : data['value'] for data in result['foods'][0]['foodNutrients']}
        data = dict(sorted(data_dict.items(), key = lambda x: x[1])[-10:])
        label = list(data.keys())
        value = list(data.values())
    except:
        data = {}
        label = []
        value = []
        flash('No resulet were found for keyword='+key)
    return render_template('pages/search.html', resultdata=data, item=key, label=label, value=value)

@app.route('/lookup/<keyword>')
def lookup(keyword):
    if keyword == 'None':
        return render_template('pages/search.html', resultdata={}, item ="" )
    else:
        if ',' not in keyword:
            keyword = ' '.join(re.findall('[A-Za-z]+', keyword))
        nutrient = keyword.split(',')[0]
        search_key = f'{nutrient} in diet'
        wiki_result = wikipedia.summary(search_key, sentences=5)
        print(wiki_result)
     
        return jsonify(data=wiki_result) 

if __name__ == '__main__':
    app.run(debug=True)