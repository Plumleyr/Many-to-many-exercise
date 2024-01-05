from flask import render_template,redirect, request, Blueprint
from models import db, User, Blogpost

blogposts_bp = Blueprint('blogposts', __name__)


@blogposts_bp.route('/posts/<blogpost_id>')
def show_posts(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    user = blogpost.user
    return render_template('show_post.html', blogpost = blogpost, user = user)

@blogposts_bp.route('/posts/<blogpost_id>/edit')
def edit_blogpost_form(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    user = blogpost.user
    return render_template('edit_post.html', blogpost =blogpost, user = user)

@blogposts_bp.route('/posts/<blogpost_id>/edit', methods = ['POST'])
def edit_blogpost(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    user = blogpost.user

    blogpost.title = request.form['title']
    blogpost.content = request.form['content']

    db.session.add(blogpost)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@blogposts_bp.route('/posts/<blogpost_id>/delete')
def delete_blogpost(blogpost_id):

    blogpost = Blogpost.query.get_or_404(blogpost_id)
    user = blogpost.user

    db.session.delete(blogpost)
    db.session.commit()

    return redirect(f'/users/{user.id}')