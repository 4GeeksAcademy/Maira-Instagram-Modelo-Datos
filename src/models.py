from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list['Post']] = relationship(back_populates='user_who_posts')
    comments: Mapped[list['Comment']] = relationship(back_populates='commenting_user')
    who_do_i_follow: Mapped[list['Follow']] = relationship(back_populates='')
    who_follows_me: Mapped[list['Follow']] = relationship(back_populates='')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Follow(db.Model):
    __tablename__ = 'follow'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    follower: Mapped[list['User']] = relationship(back_populates='user.who_follows_me')
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    to_follow: Mapped[list['User']] = relationship(back_populates='user.who_do_i_follow')


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    the_post: Mapped['Post'] = relationship(back_populates='publications')

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_who_posts: Mapped['User'] = relationship(back_populates='posts')
    publications: Mapped[list['Media']] = relationship(back_populates='the_post')
    description: Mapped['Comment'] = relationship(back_populates='post_comment')

class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(400))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    commenting_user: Mapped['User'] = relationship(back_populates='comments')
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post_comment: Mapped['Post'] = relationship(back_populates='description')