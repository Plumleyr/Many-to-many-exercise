from flask import render_template,redirect, request, Blueprint
from models import db, User, Blogpost, Tag, PostTag

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('/tags')
def show_tags_list():

    tags = Tag.query.all()
    return render_template('tag_list.html', tags = tags)

@tags_bp.route('/tags/new')
def create_tag_form():

    return render_template('add_tag.html')

@tags_bp.route('/tags/new', methods = ['POST'])
def create_tag():

    tag_name = request.form['tag_name']
    
    new_tag = Tag(tag_name = tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@tags_bp.route('/tags/<tag_id>')
def detail_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag = tag)

@tags_bp.route('/tags/<tag_id>/edit')
def edit_tag_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag = tag)

@tags_bp.route('/tags/<tag_id>/edit', methods = ['POST'])
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.tag_name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag_id}')

@tags_bp.route('/tags/<tag_id>/delete')
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')