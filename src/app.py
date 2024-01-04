from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game_date = db.Column(db.Date, nullable=True)  # Date of the game the player is attending

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        attending_date = request.form.get('attending_date')

        if attending_date:
            attending_date = date.fromisoformat(attending_date)

        player = Player.query.filter_by(name=player_name).first()
        if player:
            player.game_date = attending_date
            db.session.commit()
        return redirect(url_for('index'))

    players = Player.query.all()
    return render_template('index.html', players=players)

def init_db():
    with app.app_context():
        db.create_all()  # Creates the necessary database tables

if __name__ == '__main__':
    app.run(debug=True)
