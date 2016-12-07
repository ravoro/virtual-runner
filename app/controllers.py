from flask import url_for, redirect, render_template

from app import app


@app.route('/')
def home():
    return redirect(url_for('journeys'))


@app.route('/journeys')
def journeys():
    return render_template('journeys.html')
