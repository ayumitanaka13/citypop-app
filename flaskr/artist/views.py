from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from flaskr.forms import CommentForm
from flaskr.models import Artist, Comment, User
from flaskr import db

artist_bp = Blueprint('artist', __name__, url_prefix='/artist') 
test_bp = Blueprint('test', __name__, url_prefix='/test') 

@artist_bp.route('', methods=['GET', 'POST'])
def artist():
    artists = Artist.query.all()
    comments = Comment.query.all()
    # comments = Comment.get_comments(current_user.get_id(), id)
    user_id = current_user.get_id()
    user = User.select_user_by_id(user_id)
    form = CommentForm(request.form)

    if request.method == 'POST' and form.validate():
        new_comment = Comment(current_user.get_id(), Comment.to_artist_id(), form.comment.data)
        with db.session.begin(subtransactions=True):
            new_comment.create_comment()
        db.session.commit()
    return render_template('artist/artist.html', artists=artists, comments=comments, user=user, form=form, to_artist_id=id)

@test_bp.route('')
def test():
    return render_template('artist/test.html')