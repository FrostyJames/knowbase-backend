from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from server.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knowbase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Enable CORS for all routes from your frontend
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5173"}}, supports_credentials=True)

    api = Api(app)

    @app.route("/")
    def home():
        return jsonify({"message": "Knowledge Base API running"}), 200

    # ✅ Register modular route groups
    from server.app_routes.articles import register_article_routes
    register_article_routes(app)

    return app