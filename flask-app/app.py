from flask import Flask

app = Flask(__name__)


@app.route('/test')
def hello():
    print('/test endpoint hit')
    return '/test API endpoint'