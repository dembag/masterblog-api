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
    # Add post
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
        # List posts
        sort_by = request.args.get("sort")
        direction = request.args.get("direction", "asc")
        sorted_posts = []

        if sort_by:
            if sort_by != "title" and sort_by != "content":
                return jsonify({
                    "message": "Posts can only be sorted by 'title' or 'content'."
                }), 400
            if direction != "asc" and direction != "desc":
                return jsonify({
                    "message": "Sorting direction can only be 'asc' or 'desc'."
                }), 400

            if sort_by == "title" and direction == "asc":
                sorted_posts = sorted(POSTS, key=lambda post: post['title'].lower())
            elif sort_by == "title" and direction == "desc":
                sorted_posts = sorted(POSTS, key=lambda post: post['title'].lower(), reverse=True)
            elif sort_by == "content" and direction == "asc":
                sorted_posts = sorted(POSTS, key=lambda post: post['content'].lower())
            elif sort_by == "content" and direction == "desc":
                sorted_posts = sorted(POSTS, key=lambda post: post['content'].lower(), reverse=True)
            return jsonify(sorted_posts)

        if direction == "desc" and not sort_by:
            sorted_posts = sorted(POSTS, key=lambda post: post['id'], reverse=True)
            return jsonify(sorted_posts)

        return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """ Allows the user to delete or update a post."""

    start_len = 0
    end_len = 0
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
    original_post = {}

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


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """ Allows the user to search posts by title or content."""
    search_title = request.args.get("title", type=str)
    search_content = request.args.get("content", type=str)

    results = POSTS

    if search_title:
        results = [
            post for post in results
            if search_title.lower() in str(post["title"]).lower()
        ]

    if search_content:
        results = [
            post for post in results
            if search_content.lower() in str(post["content"]).lower()
        ]

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
