from faker import Faker
from flask import Flask, render_template, request, redirect, url_for
from models import Author, Post, new_session
from sqlalchemy.orm import joinedload, defer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET'])
def registration_form():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register():
    session = new_session()
    author = Author(
        login=request.form['login'],
        password=request.form['password']
    )
    session.add(author)
    session.commit()
    return redirect(url_for('index'))


@app.route('/generate_fake_data')
def generate_fake_data():
    session = new_session()
    for post in session.query(Post).all():
        session.delete(post)

    for author in session.query(Author).all():
        session.delete(author)

    session.flush()

    count = 10
    faker = Faker(locale='ru_RU')

    for _ in range(count):
        profile = faker.simple_profile()
        author = Author(
            login=profile['username'],
            full_name=profile['name'],
            password=faker.password(length=12)
        )
        session.add(author)
        session.flush()

        for _ in range(count):
            post = Post(
                author_id=author.id,
                title=faker.sentence(),
                text=faker.paragraph(nb_sentences=5),
                is_published=False,
                published_at=faker.date_time()
            )
            session.add(post)

    session.commit()
    return redirect(url_for('index'))


@app.route('/posts')
def posts():
    session = new_session()
    all_posts = session.query(Post).options(defer('text')).options(joinedload('author')).all()
    return render_template('posts.html', posts=all_posts)


@app.route('/post/<int:pk>')
def post(pk):
    session = new_session()
    post = session.query(Post).filter(Post.id == pk).one()
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
