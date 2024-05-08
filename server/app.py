#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.clear()
    return jsonify({'message': 'Successfully cleared session data.'}), 200

@app.route('/articles/<int:id>')
def show_article(id):
    print("NU" + '1')
    # print(session['page_views'])
    session['page_views'] = session.get('page_views', 0)
    love = int(session['page_views'])
    print(love)
    session['page_views'] += 1
    
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    
    article = Article.query.get_or_404(id)
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author': article.author,
        'preview': article.content[:100],  # Example preview
        'minutes_to_read': article.minutes_to_read,  # Example minutes_to_read
        'date': article.date.strftime('%Y-%m-%d')  # Example date formatting
    })

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    article_list = []
    for article in articles:
        article_list.append({
            'id': article.id,
            'title': article.title,
            'author': article.author
        })
    return jsonify(article_list)

if __name__ == '__main__':
    app.run(port=5555)
