from flask import Flask, jsonify, render_template
from flask_restful import Api, Resource, reqparse

import db_actions as db_actions
from db import create_db

app = Flask(__name__)
api = Api(app)


db_actions.seed_games()


class Game(Resource):
    def get(self, id=0):
        if not id:
            games = db_actions.get_games()
            return jsonify([{
                "id": game.id,
                "title": game.title,
                "price": game.price,
                "description": game.description
            } for game in games])

        game = db_actions.get_game(id)
        if game:
            return jsonify({
                "id": game.id,
                "title": game.title,
                "price": game.price,
                "description": game.description
            })

        return "Ігри не знайдено", 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title")
        parser.add_argument("price", type=float)
        parser.add_argument("description")
        params = parser.parse_args()
        id = db_actions.add_game(**params)
        return jsonify(f"Гру успішно додано під id {id}")

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("title")
        parser.add_argument("price", type=float)
        parser.add_argument("description")
        params = parser.parse_args()
        return jsonify(db_actions.update_game(id, **params))

    def delete(self, id):
        return jsonify(db_actions.delete_game(id))


api.add_resource(Game, "/api/games/", "/api/games/<int:id>/")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/games")
def games():
    return render_template("games.html", games=db_actions.get_games())

@app.route("/add-game")
def add_game():
    return render_template("add_game.html")


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=3000)