from models import Author, Post, Tag, session, tags_posts_table
from setup import setup_db_state


setup_db_state(session)

tags = session.query(Tag).filter(Tag.name.in_(("python", "Django"))).all()

tags_ids = [tag.id for tag in tags]

posts = (
    session.query(Post)
    .join(Author, Post.author_id == Author.id)
    .join(tags_posts_table, Post.id == tags_posts_table.c.post_id)
    .filter(Author.username == "Alex", tags_posts_table.c.tag_id.in_(tags_ids))
    .all()
)

print(posts)
