from app import db, Player

player_names = ["Brian", "Marc Flore", "Brian Moore", "Ben Pfistner", "Ben Reinhold", 
                "Erik Green", "Nathaniel Savard", "Gary Manter", "Ricky Chamberland", 
                "David L", "Adam"]

db.create_all()

for name in player_names:
    if not Player.query.filter_by(name=name).first():
        db.session.add(Player(name=name))

db.session.commit()
