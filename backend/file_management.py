import json
import os

from backend.backend_app import POSTS_FILE


def get_posts():
    """ Retrieves the post data.
        returns JSON object."""
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w", encoding="utf-8") as file_obj:
            json.dump([], file_obj)
            return []

    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as file_obj:
            posts = json.load(file_obj)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []
        with open(POSTS_FILE, "w", encoding="utf-8") as file_obj:
            json.dump(posts, file_obj)
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
    with open(POSTS_FILE, "w", encoding="utf-8") as file_obj:
            json.dump(new_db, file_obj)
