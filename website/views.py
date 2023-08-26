from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Post
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    all_posts = []
    if request.method == 'POST':
        post_text = request.form.get('post')
        image_file = request.files.get('image')

        if len(post_text) < 1:
            flash('Post is too short!', category='error')
        else:
            new_post = Post(data=post_text, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()

            if image_file:
                image_bytes = image_file.read()  # Read the image file as bytes
                new_post.attachment = image_bytes
                db.session.commit()

            flash('Post added!', category='success')

        if current_user.role == 'mentor':
            # Fetch all posts if the user is a mentor
            all_posts = Post.query.all()
        else:
            # Fetch only the user's posts
            all_posts = current_user.post

    return render_template("home.html", user=current_user, posts=all_posts)


@views.route('/delete-post', methods=['POST'])
def delete_post():  
    post = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})
