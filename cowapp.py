from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound
import os
from flask.ext.assets import Environment, Bundle
import random
import logging


def globalLogger(level, handle=""):
    '''
    Make a global logging object.
    '''
    global logger
    #print __f__
    logger = logging.getLogger("logger")
    #logger.info(logger.handlers)
    #logger.info(handle)
    if not logger.handlers:
        logger.setLevel(level)
        if handle == "":
            h = logging.StreamHandler()
        else:
            h = logging.FileHandler(handle)
        f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
        h.setFormatter(f)
        logger.addHandler(h)
    #logger.info(logger.handlers)
    return logger

logger = globalLogger(logging.DEBUG)


#instantiate the web app
app = Flask(__name__)

app.debug = True
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('style.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)

with open('templates/index.html', "r") as fail:
    content = fail.readlines()
# logger.info(content)


def mathThing():
    return random.randint(200, 234567)



@app.route('/')
def index():
    # return "hello moo"
    guess = mathThing()
    render_txt = render_template('index.html', guess=guess)
    #logger.info(render_txt)
    return render_txt


@app.route('/<page>')
def show(page):
    """
    this nifty code just makes it so routes will be queried based on what
    the user enters in the URI if the page exists it is displayed :)
    """
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)


#this makes the app initiate
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)