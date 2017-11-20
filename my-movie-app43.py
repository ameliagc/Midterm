from flask import Flask, request, render_template, redirect, url_for, flash, make_response
import json
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.debug = True 
app.config['SECRET_KEY'] = 'hard to guess string'

# add for heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/movie_data"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Set up Shell context so it's easy to use the shell to debug
# Define function
def make_shell_context():
    return dict( app=app, db=db, Song=Song, Artist=Artist, Album=Album)
# Add function use to manager
manager.add_command("shell", Shell(make_context=make_shell_context))

# WTF form class
class MovieForm(FlaskForm):
    movie = StringField('What is your favorite movie?', validators=[Required()])
    submit = SubmitField('Submit')

# ROUTE 1 - sets cookie
@app.route('/')
def set_cookie():
	response = make_response('<h1>What is the best kind of cookie?</h1>')
	response.set_cookie('type', 'chocolate chip')

	return render_template('home.html', response=response)

# ROUTE 2 - render template to display form
@app.route('/index')
def index():
    firstForm = MovieForm()
    return render_template('form.html', form=firstForm)

# ROUTE 3 - get api data based on form response, render template to display data
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