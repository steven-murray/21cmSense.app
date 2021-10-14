from . import interactive
from flask import render_template

@interactive.route('/')
def welcome():  # put application's code here
    return render_template('interactive/welcome.html')
#    return 'Welcome to Project 43!'


