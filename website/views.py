from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Post, Answer
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

    if current_user.role == 'mentor':
        all_posts = Post.query.all()  # Fetch all posts for mentors
    else:
        all_posts = current_user.post  # Fetch only the user's posts

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


# ... (your existing imports and code) ...

@views.route('/answer/<int:post_id>', methods=['GET', 'POST'])
@login_required
def answer(post_id):
    if request.method == 'POST':
        answer_text = request.form.get('post')
        image_file = request.files.get('image')

        if len(answer_text) < 1:
            flash('Answer is too short!', category='error')
        else:
            new_answer = Answer(answer=answer_text, post_id=post_id, mentor_id=current_user.id)
            db.session.add(new_answer)
            db.session.commit()

            if image_file:
                image_bytes = image_file.read()  # Read the image file as bytes
                new_answer.answer_attachment = image_bytes
                db.session.commit()

            flash('Answer added!', category='success')
    return render_template("answer.html", post_id=post_id, user=current_user)

# ... (your existing routes and code) ...



@views.route('/create', methods=['GET','POST'])
def create():
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

    return render_template('create.html', user=current_user)

