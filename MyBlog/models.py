from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Table,
                        Text, UniqueConstraint, create_engine, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

DB_FILE = "myblog.db"


Base = declarative_base()


tags_posts_table = Table(
    "tags_posts",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
    UniqueConstraint("post_id", "tag_id")
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String(128), unique=True)
    text = Column(Text)
    is_published = Column(Boolean)
    published_at = Column(DateTime)
    author = relationship("Author", back_populates="posts", lazy="select")  # joined
    tags = relationship("Tag", secondary=tags_posts_table, back_populates="posts")

    def __repr__(self):
        return f"<Post #{self.id} {self.title}>"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)

    posts = relationship("Post", secondary=tags_posts_table, back_populates="tags")

    def __repr__(self):
        return f"<Tag #{self.id} {self.name}>"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    login = Column(String(128), nullable=False, unique=True)
    full_name = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<Author #{self.id} {self.username}>"


engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def new_session():
    return Session()
