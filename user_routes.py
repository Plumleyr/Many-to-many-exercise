from flask import render_template,redirect, request, Blueprint
from models import db, User, Blogpost, Tag, PostTag

users_bp = Blueprint('users', __name__)

@users_bp.route("/")
def redirect_to_users():
    return redirect('/users')

@users_bp.route('/users')
def list_users():

    users = User.query.all()
    return render_template("list.html", users = users)

@users_bp.route('/users/new')
def create_user_form():
    return render_template("add_user.html")

@users_bp.route('/users/new', methods = ['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@users_bp.route('/users/<user_id>')
def detail_user(user_id):
    user = User.query.get_or_404(user_id)
    blogposts = user.blogposts
    return render_template("details.html", user = user, blogposts = blogposts)

@users_bp.route('/users/<user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user = user)

@users_bp.route('/users/<user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@users_bp.route('/users/<user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@users_bp.route('/users/<user_id>/posts/new')
def create_blogpost_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('add_post.html', user = user, tags = tags)

@users_bp.route('/users/<user_id>/posts/new', methods = ['POST'])
def create_blogpost(user_id):
    user = User.query.get_or_404(user_id)

    selected_tags = request.form.getlist('selected_tags')

    title = request.form['title']
    content = request.form['content']

    new_blogpost = Blogpost(title = title, content = content, user = user)

    db.session.add(new_blogpost)
    db.session.commit()

    for tag_name in selected_tags:
        tag = Tag.query.filter_by(tag_name = tag_name).first()
        if tag:
            post_tag = PostTag(post_id = new_blogpost.id, tag_id = tag.id)
            db.session.add(post_tag)
        
    db.session.commit()

    return redirect(f'/users/{user_id}')
