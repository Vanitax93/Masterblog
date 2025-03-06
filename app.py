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

def fetch_post_by_id(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_posts = load_blog_posts()
        new_id = max([post['id'] for post in blog_posts], default=0) + 1  #makes sure the added blog has a unique ID
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing posts
    blog_posts = load_blog_posts()

    # Find and remove the post with the given ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the post by ID
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with form data
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Load all posts, update the specific one, and save
        blog_posts = load_blog_posts()
        for i, p in enumerate(blog_posts):
            if p['id'] == post_id:
                blog_posts[i] = post
                break
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    blog_posts = load_blog_posts()

    # Find the post and increase likes
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1  # default likes are 0
            break

    save_blog_posts(blog_posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)