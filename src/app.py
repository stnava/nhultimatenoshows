from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Association table for the many-to-many relationship
attendance = db.Table('attendance',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('game_day_id', db.Integer, db.ForeignKey('game_day.id'), primary_key=True)
)

class GameDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    players = db.relationship('Player', secondary=attendance, backref=db.backref('game_days', lazy=True))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        attending_date = request.form.get('attending_date')

        if attending_date:
            attending_date = date.fromisoformat(attending_date)
            game_day = GameDay.query.filter_by(date=attending_date).first()
            player = Player.query.filter_by(name=player_name).first()

            if game_day and player:
                game_day.players.append(player)
                db.session.commit()

        return redirect(url_for('index'))

    players = Player.query.all()
    game_days = GameDay.query.all()
    return render_template('index.html', players=players, game_days=game_days)

def init_db():
    with app.app_context():
        db.create_all()
        # Populate the GameDay table with dates for the year 2024
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)
        one_day = timedelta(days=1)
        current_date = start_date

        while current_date <= end_date:
            if not GameDay.query.filter_by(date=current_date).first():
                new_game_day = GameDay(date=current_date)
                db.session.add(new_game_day)
            current_date += one_day

        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
