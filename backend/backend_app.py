from flask import Flask, jsonify, request
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


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """ Allows the user to delete or update a post."""

    for post in POSTS:
        start_len = len(POSTS)
        if post['id'] == post_id:
            POSTS.remove(post)
        end_len = len(POSTS)
    if start_len == end_len:
        return jsonify({
            "message": f"Post with id {post_id} not found."
        }), 404
    else:
        return jsonify({
            "message": f"Post with id {post_id} successfully deleted."
        }), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """ Allows user to update a post."""
    data = request.get_json()

    for post in POSTS:
        if post['id'] == post_id:
            original_post = post
        else:
            original_post = None
    if not original_post:
        return jsonify({
            "message": f"Post with id {post_id} not found."
        }), 404

    if "title" in data:
        if not data["title"]:
            pass
        else:
            original_post['title'] = data['title']

    if "content" in data:
        if not data["content"]:
            pass
        else:
            original_post['content'] = data['content']


    return jsonify(original_post), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
