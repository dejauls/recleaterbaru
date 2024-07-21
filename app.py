from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from slugify import slugify
from markupsafe import Markup
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv('MONGO_URI')
mongo_dbname = os.getenv('MONGO_DBNAME')

# MongoDB connection setup
client = MongoClient(mongo_uri)
db = client[mongo_dbname]
collection = db['artikel']

PER_PAGE = 20

@app.template_filter('render_html')
def render_html(content):
    return Markup(content)

app.jinja_env.filters['render_html'] = render_html

@app.context_processor
def utility_processor():
    return dict(str=str)

def trim_content(content, limit=300):
    return content if len(content) <= limit else content[:limit] + '...'

@app.route('/')
def homes():
    articles = list(collection.find().limit(6))
    for article in articles:
        article['content'] = trim_content(article['content'])
    return render_template('index.html', articles=articles)

@app.route('/about')
def about():
    articles = list(collection.find().limit(6))
    for article in articles:
        article['content'] = trim_content(article['content'])
    return render_template('about.html', articles=articles)

@app.route('/proyek')
def proyek():
    articles = list(collection.find().limit(6))
    for article in articles:
        article['content'] = trim_content(article['content'])
    return render_template('proyek.html', articles=articles)

@app.route('/artikel')
@app.route('/page/<int:page>')
def home(page=1):
    articles = list(collection.find().skip((page - 1) * PER_PAGE).limit(PER_PAGE))
    total_articles = collection.count_documents({})
    total_pages = (total_articles + PER_PAGE - 1) // PER_PAGE
    return render_template('artikel.html', articles=articles, page=page, total_pages=total_pages)

@app.route('/category/<category_name>')
@app.route('/category/<category_name>/page/<int:page>')
def category(category_name, page=1):
    articles = list(collection.find({'category': category_name}).skip((page - 1) * PER_PAGE).limit(PER_PAGE))
    total_articles = collection.count_documents({'category': category_name})
    total_pages = (total_articles + PER_PAGE - 1) // PER_PAGE
    return render_template('artikel.html', articles=articles, page=page, total_pages=total_pages, category=category_name)

@app.route('/add', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.form['image']
        source = request.form['source']
        author = request.form['author']
        date = request.form['date']
        category = request.form['category']
        meta_description = request.form['meta_description']
        meta_keywords = request.form['meta_keywords']
        meta_title = request.form['meta_title']

        slug = slugify(title)
        
        article = {
            "title": title,
            "slug": slug,
            "content": content,
            "image": image,
            "source": source,
            "author": author,
            "date": date,
            "category": category,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
            "meta_title": meta_title
        }
        
        collection.insert_one(article)
        return redirect('/artikel')
    return render_template('posting-artikel.html')

@app.route('/article/<slug>')
def article_detail(slug):
    article = collection.find_one({'slug': slug})
    if not article:
        return redirect(url_for('home'))
    
    other_articles = list(collection.find({'slug': {'$ne': slug}}).limit(4))
    
    return render_template('detail-artikel.html', article=article, articles=other_articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)