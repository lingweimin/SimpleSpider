from flask import render_template
from . import app


@app.route('/')
def home():
    return 'Spider lists'