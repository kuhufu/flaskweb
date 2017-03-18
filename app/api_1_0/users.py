from .errors import forbidden
from . import api
from ..models import User, Permission
from .. import db
from flask import g, jsonify, request, url_for, current_app
from .decorators import permission_required


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=user.id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=user.id, page=page+1, _external=True)
    posts = pagination.items
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.paginate(
        page, per_page=current_app.config['FLAKSY_POSTS_PER_PAGE'],
        error_out=False)
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=user.id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=user.id, page=page+1, _external=True)
    posts = pagination.items
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })