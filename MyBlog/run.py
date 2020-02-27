from models import Author, Post, Tag, session, tags_posts_table


def setup_db_state(session):
    def create_object_if_needed(model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items())
            instance = model(**params)
            session.add(instance)
            return instance, True

    alex, _ = create_object_if_needed(Author, username="Alex")
    nick, _ = create_object_if_needed(Author, username="Nick")

    python, _ = create_object_if_needed(Tag, name="python")
    web, _ = create_object_if_needed(Tag, name="web")
    django, _ = create_object_if_needed(Tag, name="Django")

    def create_post_with_tags_if_needed(title, author, tags=None):
        post, is_created = create_object_if_needed(Post, title=title, author=author)
        if is_created and tags is not None:
            post.tags = tags

    create_post_with_tags_if_needed(
        "Django for Python - is it best?", alex, tags=[python, django]
    )
    create_post_with_tags_if_needed(
        "What is the best framework for web in Python?", nick, tags=[python, web]
    )
    create_post_with_tags_if_needed(
        "Django - good choice for web", alex, tags=[web, django]
    )

    session.commit()


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
