from flask import request, jsonify
from server.models import Article
from server.extensions import db

def register_article_routes(app):
    @app.route("/articles", methods=["GET"])
    def get_articles():
        articles = Article.query.order_by(Article.created_at.desc()).all()
        return jsonify([article.to_dict() for article in articles]), 200

    @app.route("/articles", methods=["POST"])
    def post_article():
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")
        category = data.get("category")

        if not title or not content:
            return jsonify({"error": "Missing title or content"}), 400

        new_article = Article(
            title=title,
            content=content,
            category=category
        )
        db.session.add(new_article)
        db.session.commit()

        return jsonify(new_article.to_dict()), 201

    @app.route("/articles/<int:id>", methods=["PATCH", "DELETE", "OPTIONS"])
    def modify_article(id):
        print(f"🔧 {request.method} /articles/{id} hit")

        # CORS preflight response
        if request.method == "OPTIONS":
            response = jsonify({"message": "CORS preflight OK"})
            response.status_code = 204
            response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5173")
            response.headers.add("Access-Control-Allow-Methods", "PATCH, DELETE, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type")
            return response

        article = Article.query.get_or_404(id)

        if request.method == "PATCH":
            data = request.get_json()
            print("🔧 PATCH data received:", data)

            try:
                if "title" in data:
                    article.title = data["title"]
                if "category" in data:
                    article.category = data["category"]
                if "status" in data and hasattr(article, "status"):
                    article.status = data["status"]

                db.session.commit()
                print("✅ Article updated successfully")
                return jsonify(article.to_dict()), 200

            except Exception as e:
                print("❌ PATCH error:", str(e))
                db.session.rollback()
                return jsonify({"error": "Failed to update article"}), 500

        if request.method == "DELETE":
            db.session.delete(article)
            db.session.commit()
            return jsonify({"message": "Article deleted"}), 200