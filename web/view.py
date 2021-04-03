from flask import Blueprint, render_template, request, flash,redirect,url_for,session

view = Blueprint('view',__name__)

@view.route('/app')
def app():
    return render_template('app.html')