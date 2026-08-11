import json

def get_posts():
    """ Retrieves the post data.
        returns JSON object."""
    try:
        with open("posts.json", "r", encoding="utf-8") as file_obj:
            posts = json.load(file_obj)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return posts


def get_post_by_id(post_id):
    """ Returns the post data that matches post_id or None if not found."""
    retrieved_post = None
    posts_db = get_posts()
    for p in posts_db:
        if p["id"] == post_id:
            retrieved_post = p
            break
    return retrieved_post


def update_posts_db(new_db):
    """ Saves the new database data to posts.json."""
    with open("posts.json", "w", encoding="utf-8") as file_obj:
            json.dump(new_db, file_obj)
