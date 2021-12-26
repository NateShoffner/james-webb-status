from decimal import Decimal
from distutils.util import strtobool
from dotenv import dotenv_values
from flask import Flask
from flask import jsonify
from flask.json import JSONEncoder
from jwst.statscraper import StatScraper

# add support for Decimal type
class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.json_encoder = JsonEncoder

config = dotenv_values('.env')
scraper = StatScraper(config)

@app.route('/')
def hello():
    return 'hi :)'

@app.route('/status')
def status():
    stats = scraper.get_stats()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=strtobool(config.get('DEBUG')), host=config.get('HOST'), port=int(config.get('PORT')))