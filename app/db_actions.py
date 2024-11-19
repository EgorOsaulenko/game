from db import Session, Game


def add_game(title, price, description):
    with Session() as session:
        game = Game(title=title, price=price, description=description)
        session.add(game)
        session.commit()
        session.refresh(game)
        return game.id


def get_games():
    with Session() as session:
        return session.query(Game).all()


def get_game(id):
    with Session() as session:
        return session.query(Game).where(Game.id == id).first()


def update_game(id, title, price, description):
    with Session() as session:
        game = session.query(Game).filter_by(id=id).first()
        if not game:
            return "Гра не знайдена", 404
        game.title = title
        game.price = price
        game.description = description
        session.commit()
        return "Дані оновлено"


def delete_game(id):
    with Session() as session:
        game = session.query(Game).filter_by(id=id).first()
        if not game:
            return "Гра не знайдена", 404
        session.delete(game)
        session.commit()
        return "Гру видалено"


def seed_games():
    with Session() as session:
        if not session.query(Game).first():
            games = [
                {"title": "Cyberpunk 2077", "price": 1499, "description": "Рольова гра у футуристичному світі."},
                {"title": "The Witcher 3", "price": 999, "description": "Епічна пригодницька гра з відкритим світом."},
                {"title": "Minecraft", "price": 799, "description": "Кубічний світ для креативності та досліджень."},
                {"title": "Elden Ring", "price": 1399, "description": "Фентезійний екшн у відкритому світі."},
                {"title": "FIFA 24", "price": 1599, "description": "Симулятор футболу з реалістичною графікою."}
            ]
            for game in games:
                session.add(Game(**game))
            session.commit()