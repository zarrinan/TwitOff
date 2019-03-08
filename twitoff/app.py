"""Main application configuration and routing logic for TwitOff."""
from decouple import config
from flask import Flask,render_template,request
from .models import DB, User


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/:user')
    def user_tweets():
        twitter_user = TWITTER.get_user(?)
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')



    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB reset', users=[])
    return app
