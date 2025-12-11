import os

from flask import Flask

import webapp.constants as constants


app = Flask(__name__)


@app.route('/api/test')
def hello():
    print('/test endpoint hit')
    return f'{{ "message": "{constants.API_MESSAGE}" }}'

@app.route('/api/ssr')
def ssr_message():
    print('/ssr endpoint hit')
    return f'{{ "message": "{constants.SSR_MESSAGE}" }}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ['PORT'], debug=True)
