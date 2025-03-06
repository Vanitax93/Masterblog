from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Function to load blog posts from JSON file
def load_blog_posts():
    try:
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save blog posts to JSON file
def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing posts
        blog_posts = load_blog_posts()

        # Generate a new ID (e.g., max ID + 1)
        new_id = max([post['id'] for post in blog_posts], default=0) + 1

        # Create new blog post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Add new post and save
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)

        # Redirect to index page
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)