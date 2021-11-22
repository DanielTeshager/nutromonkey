from flask import Flask, app, render_template, request, redirect, url_for, flash, jsonify
import json
import requests
import wikipedia
from flask.wrappers import Response
from wikipedia.wikipedia import API_URL

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
    keyword = request.form['key']
    # pull additional data from wikipedia about the search term
    try:
        additional_info = wikipedia.summary(keyword, sentences=2)
    except:
        additional_info = ""
    # get the first 10 results from usda api
    try:
        API_KEY = "Hal64gsGkYVlg6bhIAn5zQoLR6GqbuSzWa5LsJLj"
        API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search?query="+keyword+"&pageSize=2&api_key="+API_KEY
        response = requests.get(API_URL)
        result = json.loads(response.text)
        data_dict = {data['nutrientName'] : data['value'] for data in result['foods'][0]['foodNutrients']}
        data = dict(sorted(data_dict.items(), key = lambda x: x[1])[-10:])
        label = list(data.keys())
        value = list(data.values())
    except:
        data = {}
        label = []
        value = []
        flash('No result was found for keyword='+keyword)
    return render_template('pages/search.html', resultdata=data, item=keyword, label=label, value=value, additional_info=additional_info)

# auxillary function to get the data from the wikipedia API
@app.route('/lookup/<keyword>')
def lookup(keyword):
    if keyword == 'None':
        return render_template('pages/search.html', resultdata={}, item ="" )
    else:
        if ',' not in keyword:
            keyword = ' '.join(re.findall('[A-Za-z]+', keyword))
        nutrient = keyword.split(',')[0]
        search_key = f'{nutrient} in food'
        try:
            wiki_result = wikipedia.summary(search_key, sentences=5)
        except:
            wiki_result = 'No result found'
        return jsonify(data=wiki_result)

# Handles the page note found error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404 

# Handles the internal server error
@app.errorhandler(500)
def not_found_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)