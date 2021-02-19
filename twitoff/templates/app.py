"""Main app/routing file for TwitOff"""

import osfrom flask import Flask, render_template, request 
from .models import DB, User
from .twitter import add_or_update_user, update_all_users
from .predict import predict_user

#creates application
def create_app():
    """Creating and configuring an instance of the Flask application"""
    app = Flask(__name__) 
    
    #database and app configurations 
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    
    #initializing database
    DB.init_app(app) 
    with app.app_context():
        DB.drop_all()
        DB.create_all()

    #decorator listens for specific endpoint visits
    @app.route('/') #http://127.0.0.1:5000/compare
    def root(): 
        #renders base.html template and passes down title and users 
        return render_template('base.html', title="Home", users=User.query.all())

    @app.route('/compare', methods=["POST"]) #http://127.0.0.1:500/compare
    def compare(): 
        user0, user1 = sorted(
            [request.values['user1'], request.values['user2']])

        if user0 == user1:
            message = "Cannot compare users to themselves!" 

        else: 
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = '{} is more likely to be said by {} than {}'.format(
                request.values["tweet_text"], user1 if prediction else user0, user0 if prediction else user1
            )
        
        return render_template('prediction.html'- title="Prediction"- message=message)

create_app()

