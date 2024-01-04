# initialize_db.py
from app import app, db, Player

def init_db():
    with app.app_context():
        db.create_all()  # Create tables

        player_names = ["brian", "Marc Flore", "Brian Moore", "Ben Pfistner", 
                        "Ben Reinhold", "Erik Green", "Nathaniel Savard", 
                        "gary manter", "Ricky Chamberland", "David L", "Adam"]

        # Add players if they don't already exist
        for name in player_names:
            if not Player.query.filter_by(name=name).first():
                db.session.add(Player(name=name))

        db.session.commit()

if __name__ == '__main__':
    init_db()
