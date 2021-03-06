from flaskr import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from uuid import uuid4



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    picture_path = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password).decode("utf-8")

    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def create_new_user(self):
        db.session.add(self)

    @classmethod
    def select_user_by_id(cls, id):
        return cls.query.get(id)

    # def save_new_password(self, new_password):
    #     self.password = generate_password_hash(new_password)
    #     self.is_active = True
    


class PasswordResetToken(db.Model):

    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(
        db.String(64),
        unique=True,
        index=True,
        server_default=str(uuid4)
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expire_at = db.Column(db.DateTime, default=datetime.now)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, token, user_id, expire_at):
        self.token = token
        self.user_id = user_id
        self.expire_at = expire_at

    @classmethod
    def publish_token(cls, user):

        token = str(uuid4())
        new_token = cls(
            token,
            user.id,
            datetime.now() + timedelta(days=1)
        )
        db.session.add(new_token)
        return token

    @classmethod
    def get_user_id_by_token(cls, token):
        now = datetime.now()
        record = cls.query.filter_by(token=str(token)).filter(cls.expire_at > now).first()
        if record:
            return record.user_id
        else:
            return None

    @classmethod
    def delete_token(cls, token):
        cls.query.filter_by(token=str(token)).delete()



class Age(db.Model):

    __tablename__ = 'ages'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(128))
    info = db.Column(db.Text)

    def __init__(self, age, info):
        self.age = age
        self.info = info



class Album(db.Model):

    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    from_age_id = db.Column(
        db.Integer, db.ForeignKey('ages.id'), index=True
    )
    year = db.Column(db.Integer)
    name = db.Column(db.String(128))
    name_j = db.Column(db.String(128))
    title = db.Column(db.String(128))
    title_j = db.Column(db.String(128))
    info = db.Column(db.Text)
    album_picture_path = db.Column(db.Text)
    artist_picture_path = db.Column(db.Text)

    def __init__(self, from_age_id, year, name, name_j, title, title_j, info, album_picture_path, artist_picture_path):
        self.from_age_id = from_age_id
        self.year = year
        self.name = name
        self.name_j = name_j
        self.title = title
        self.title_j = title_j
        self.info = info
        self.album_picture_path = album_picture_path
        self.artist_picture_path = artist_picture_path

    # @classmethod
    # def search_by_name(cls, name):
    #     return cls.query.filter(
    #         cls.name.like(f'%{name}%')
    #     ).with_entities(
    #         cls.id, cls.name, cls.title, cls.album_picture_path, cls.artist_picture_path
    #     ).all()



class AlbumArtist(db.Model):

    __tablename__ = 'album_artists'

    id = db.Column(db.Integer, primary_key=True)
    from_album_id = db.Column(
        db.Integer, db.ForeignKey('albums.id'), index=True
    )
    to_artist_id = db.Column(
        db.Integer, db.ForeignKey('artists.id'), index=True
    )

    def __init__(self, from_album_id, to_artist_id):
        self.from_album_id = from_album_id
        self.to_artist_id = to_artist_id



class Artist(db.Model):

    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    from_album_id = db.Column(
        db.Integer, db.ForeignKey('albums.id'), index=True
    )
    year = db.Column(db.Integer)
    name = db.Column(db.String(128))
    name_j = db.Column(db.String(128))
    title = db.Column(db.String(128))
    title_j = db.Column(db.String(128))
    youtube = db.Column(db.Text)
    song_info = db.Column(db.Text)
    artist_info = db.Column(db.Text)
    song_picture_path = db.Column(db.Text)
    artist_picture_path = db.Column(db.Text)

    def __init__(self, from_album_id, year, name, name_j, title, title_j, youtube, song_info, artist_info, song_picture_path, artist_picture_path):
        self.from_album_id = from_album_id 
        self.year = year
        self.name = name
        self.name_j = name_j
        self.title = title
        self.title_j = title_j
        self.youtube = youtube
        self.song_info = song_info
        self.artist_info = artist_info
        self.song_picture_path = song_picture_path
        self.artist_picture_path = artist_picture_path



class LikeAlbum(db.Model):

    __tablename__ = 'like_albums'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True
    )
    to_album_id = db.Column(
        db.Integer, db.ForeignKey('albums.id'), index=True
    )
    create_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, from_user_id, to_album_id):
        self.from_user_id = from_user_id
        self.to_album_id = to_album_id

    def add_like(self):
        db.session.add(self)

    def delete_like(self):
        db.session.delete(self)
    
    def is_liked(cls, album_id):
        return cls.query.filter_by(
            from_user_id = current_user.get_id(),
            to_album_id = album_id
        ).count() > 0



class LikeSong(db.Model):

    __tablename__ = 'like_songs'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True
    )
    to_artist_id = db.Column(
        db.Integer, db.ForeignKey('artists.id'), index=True
    )
    create_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, from_user_id, to_artist_id):
        self.from_user_id = from_user_id
        self.to_artist_id = to_artist_id

    def add_like(self):
        db.session.add(self)

    def delete_like(self):
        db.session.delete(self)

    def is_liked(cls, artist_id):
        return cls.query.filter_by(
            from_user_id = current_user.get_id(),
            to_artist_id = artist_id
        ).count() > 0



class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True
    )
    to_artist_id = db.Column(
        db.Integer, db.ForeignKey('artists.id'), index=True
    )
    comment = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, from_user_id, to_artist_id, comment):
        self.from_user_id = from_user_id
        self.to_artist_id = to_artist_id
        self.comment = comment

    def create_comment(self):
        db.session.add(self)