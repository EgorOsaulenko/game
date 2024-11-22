from db import Session, Game


def add_game(title, price):
    with Session() as session:
        game = Game(title=title, price=price)
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


def update_game(id, title, price):
    with Session() as session:
        game = session.query(Game).filter_by(id=id).first()
        if not game:
            return "Гра не знайдена", 404
        game.title = title
        game.price = price
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
