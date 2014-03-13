# app.py

import datetime, os

from flask import flash, request, render_template

from flask.ext.api import FlaskAPI, status, exceptions
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer
from flask.ext.api.exceptions import APIException

from unipath import Path
import heroku


TEMPLATE_DIR = Path(__file__).ancestor(1).child("templates")
app = FlaskAPI(__name__, template_folder=TEMPLATE_DIR)


def get_projects():
    heroku_user = os.environ['HEROKU_USERNAME']
    heroku_pass = os.environ['HEROKU_PASSWORD']
    cloud = heroku.from_pass(heroku_user, heroku_pass)
    return [
        {
            "name": h_app.name,
            "url": "http://{app}.herokuapp.com/".format(app=h_app.name),
        }
        for h_app in cloud.apps
    ]


@app.route("/", methods=['GET'])
@set_renderers([HTMLRenderer])
def index():
    return render_template('index.html', projects=get_projects())


@app.route("/api/", methods=['GET', 'POST'])
def project_list():
    # request.method == 'GET'
    return get_projects(), status.HTTP_200_OK


if __name__ == "__main__":
    app.run(debug=True)