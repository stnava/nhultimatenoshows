from app import app, db, Player, GameDay, init_db

# Initialize the database (create tables and populate GameDay)
with app.app_context():
    init_db()

    # List of initial players to add to the database
    player_names = [
        "brian", "Marc Flore", "Brian Moore", "Ben Pfistner", "Ben Reinhold",
        "Erik Green", "Nathaniel Savard", "gary manter", "Ricky Chamberland",
        "David L", "Adam"
    ]

    for name in player_names:
        if not Player.query.filter_by(name=name).first():
            new_player = Player(name=name)
            db.session.add(new_player)

    db.session.commit()
