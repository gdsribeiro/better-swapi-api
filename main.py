from flask import Flask
from routes.characters import characters_bp
from routes.films import films_bp
from routes.planets import planets_bp
from routes.starships import starships_bp

app = Flask(__name__)

app.register_blueprint(characters_bp)
app.register_blueprint(films_bp)
app.register_blueprint(planets_bp)
app.register_blueprint(starships_bp)

@app.errorhandler(404)
def not_found(e):
    return "Not Found", 404

main_http = app