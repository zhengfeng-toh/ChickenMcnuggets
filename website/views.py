from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Post
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
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

    return render_template("home.html", user=current_user)


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
