from flask import Flask, jsonify, request, render_template, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route("/api/posts", methods=["GET", "POST"])
def get_posts():
    """ Sends posts database as JSON
        and adds new posts to database. """
    if request.method == "POST":
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")

        # Validate post data
        missing_fields = []
        if not title:
            missing_fields.append("title")

        if not content:
            missing_fields.append("content")

        if missing_fields:
            return jsonify({
                "error": "Missing required fields.",
                "missing": missing_fields
            }), 400

        if POSTS:
            new_post_id = max(POST['id'] for POST in POSTS) + 1
        else:
            new_post_id = 1

        new_post = {
            "id": new_post_id,
            "title": title,
            "content": content
        }

        POSTS.append(new_post)

        return jsonify(POSTS), 201
    else:
        return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
