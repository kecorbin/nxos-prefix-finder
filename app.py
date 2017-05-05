from flask import Flask, render_template, request, flash, redirect
from nxos_prefix_finder.Devices import Nexus
import logging
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import IPAddress
import os


app = Flask(__name__)
app.secret_key = "qsdlkfjasdlkfjawlk4j324lj2wlkrfjasdlkfjsa"

ROUTE_SERVER_IP='192.168.51.128'
ROUTE_SERVER_USERNAME='admin'
ROUTER_SERER_PASSWORD='c!sco123'


def logo():
    """
    Check env for presence of custom logo
    :return:
    """
    return os.getenv("LOGO", "static/logo.png")


def title():
    return os.getenv("TITLE", "ACME Enterprise Routing")

class PrefixLookupForm(FlaskForm):
    prefix = StringField('ip', validators=[])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = PrefixLookupForm()
        return render_template('lookup.html',
                               title=title(),
                               logo=logo(),
                               form=form)

    if request.method == 'POST':
        form = PrefixLookupForm(request.form)
        if form.validate():
            prefix = form.prefix.data
            n = Nexus(ROUTE_SERVER_IP,
                      ROUTE_SERVER_USERNAME,
                      ROUTER_SERER_PASSWORD
                      )
            vrfs = n.search_for_prefix(prefix)
            if len(vrfs) > 0:
                flash("Success",
                      category='alert-success')
                msg = "This IP address was found in VRF: {}".format(vrfs[0])
            else:
                flash("Could not find this prefix in any routing table",
                      category='alert-danger')
                msg = "No prefix information found for {}".format(prefix)

        else:
            flash('Please enter a valid IP address',
                      category="alert-danger")

        return render_template('lookup.html',
                               title=title(),
                               logo=logo(),
                               form=form,
                               result=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=os.getenv("DEBUG", True))