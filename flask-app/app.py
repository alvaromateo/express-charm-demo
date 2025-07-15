from flask import Flask

app = Flask(__name__)


@app.route('/api/test')
def hello():
    print('/test endpoint hit')
    return '{ "message": "API endpoint success!" }'