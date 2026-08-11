
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import file_management as fm


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/api/posts", methods=["GET", "POST"])
def get_posts():
    """ Sends posts database as JSON
        and adds new posts to database. """
    posts = fm.get_posts()

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

        if posts:
            new_post_id = max(post['id'] for post in posts) + 1
        else:
            new_post_id = 1

        new_post = {
            "id": new_post_id,
            "title": title,
            "content": content
        }

        posts.append(new_post)
        fm.update_posts_db(posts)

        return jsonify(posts), 201
    else:
        # List posts
        sort_by = request.args.get("sort")
        direction = request.args.get("direction", "asc")


        if sort_by:
            if sort_by != "title" and sort_by != "content":
                return jsonify({
                    "message": "Posts can only be sorted by 'title' or 'content'."
                }), 400
            if direction != "asc" and direction != "desc":
                return jsonify({
                    "message": "Sorting direction can only be 'asc' or 'desc'."
                }), 400

            sorted_posts = sorted(
                posts,
                key=lambda post: post[sort_by].lower(),
                reverse=direction == "desc"
            )

            return jsonify(sorted_posts)

        if direction == "desc" and not sort_by:
            sorted_posts = sorted(posts, key=lambda post: post['id'], reverse=True)
            return jsonify(sorted_posts)

        return jsonify(posts)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """ Allows the user to delete or update a post."""
    posts = fm.get_posts()

    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            fm.update_posts_db(posts)

            return jsonify({
                "message": f"Post with id {post_id} successfully deleted."
            }), 200

    return jsonify({
        "message": f"Post with id {post_id} not found."
    }), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """ Allows user to update a post."""
    posts = fm.get_posts()
    data = request.get_json()

    original_post = {}

    for post in posts:
        if post['id'] == post_id:
            original_post = post
            break

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

    fm.update_posts_db(posts)

    return jsonify(original_post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """ Allows the user to search posts by title or content."""
    search_title = request.args.get("title", type=str)
    search_content = request.args.get("content", type=str)

    if search_title and search_content:
        return jsonify({
                    "message": "Posts can only be searched by 'title' OR 'content'."
                }), 400

    results = fm.get_posts()

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
