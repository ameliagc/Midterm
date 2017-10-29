from flask import Flask, request, render_template, redirect, url_for, flash, make_response
import requests
import json
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.debug = True 
app.config['SECRET_KEY'] = 'hard to guess string'

# WTF FORMS
# Form - takes in data, submits
class MovieForm(FlaskForm):
    movie = StringField('What is your favorite movie?', validators=[Required()])
    submit = SubmitField('Submit')

# ROUTE 1 - sets cookie - do we have to call and display cookie?
@app.route('/')
def set_cookie():
	# Insert itunes logo image
	response = make_response('<h1>What is the best kind of cookie?</h1>')
	response.set_cookie('type', 'chocolate chip')

	return render_template('home.html', response=response)

# ROUTE 2 - call on form
@app.route('/index')
def index():
    firstForm = MovieForm()
    return render_template('form.html', form=firstForm)

# ROUTE 3 - display form response
@app.route('/result', methods = ['GET', 'POST'])
def result():
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.movie.data

        base_url = "http://theapache64.xyz:8080/movie_db/search"

        params = {}
        params["keyword"] = name

        resp = requests.get(base_url, params=params)
        data_text = resp.text
        python_obj = json.loads(data_text)

        rating_num = float(python_obj['data']['rating'])
        poster_url = python_obj['data']['poster_url']

        return render_template("result.html", results=python_obj['data'], rating_num=rating_num, poster_url=poster_url)

    # flashing error message if form data is incorrect
    flash('All fields are required!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()