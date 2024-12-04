from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
DATABASE = 'database.db'

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            date TEXT NOT NULL,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Рендеринг HTML страницы
@app.route('/blog')
def render_blog():
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles').fetchall()
    conn.close()
    return render_template('blog.html', articles=articles)


# Главная страница
@app.route('/')
def home():
    return render_template('main.html')


# Страница создания статьи
@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')


# API для получения всех статей
@app.route('/api/articles', methods=['GET'])
def get_articles():
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles').fetchall()
    conn.close()
    return jsonify([dict(article) for article in articles])

@app.route('/api/articles', methods=['POST'])
def create_article():
    if 'image' not in request.files:
        return jsonify({'error': 'Image is required'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(image.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(image.filename)

    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    data = request.form
    if not data.get('title') or not data.get('content') or not data.get('author') or not data.get('date'):
        return jsonify({'error': 'All fields are required'}), 400

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO articles (title, content, author, date, image) VALUES (?, ?, ?, ?, ?)',
        (data['title'], data['content'], data['author'], data['date'], filename)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Article created successfully'}), 201

@app.route('/api/articles/<id>', methods=['GET'])
def get_article(id):
    conn = get_db_connection()
    article = conn.execute(
        'SELECT * FROM articles WHERE id = ?',
        (id)
    ).fetchone()
    conn.close()
    if article is None:
        return jsonify({'error': 'Article not found'}), 404
    return jsonify(dict(article))

@app.route('/api/articles/<int:id>', methods=['PUT'])
def update_article(id):
    data = request.json
    required_fields = ['title', 'content', 'author', 'date', 'slug']
    
    # Check if all required fields are present
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400

    conn = get_db_connection()
    conn.execute(
        '''UPDATE articles 
           SET title = ?, content = ?, author = ?, date = ?
           WHERE id = ?''',
        (data['title'], data['content'], data['author'], data['date'], data['slug'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Article updated successfully'}), 200

@app.route('/api/articles/<int:id>', methods=['PATCH'])
def patch_article(id):
    data = request.json
    fields = ['title', 'content', 'author', 'date']
    updates = {key: data[key] for key in fields if key in data}

    if not updates:
        return jsonify({'error': 'No valid fields to update'}), 400

    query = 'UPDATE articles SET ' + ', '.join(f"{key} = ?" for key in updates.keys()) + ' WHERE id = ?'
    values = list(updates.values()) + [id]

    conn = get_db_connection()
    conn.execute(query, values)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Article updated successfully'}), 200

@app.route('/api/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    conn = get_db_connection()
    article = conn.execute('SELECT image FROM articles WHERE id = ?', (id,)).fetchone()
    if article is None:
        conn.close()
        return jsonify({'error': 'Article not found'}), 404

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], article['image'])
    if os.path.exists(image_path):
        os.remove(image_path)

    conn.execute('DELETE FROM articles WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Article deleted successfully'}), 200





if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5123)
