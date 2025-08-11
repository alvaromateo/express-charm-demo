import os

from flask import Flask


app = Flask(__name__)


@app.route('/api/test')
def hello():
    print('/test endpoint hit')
    return '{ "message": "API endpoint success!" }'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ['PORT'], debug=True)
