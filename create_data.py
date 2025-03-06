import json

# Initial blog posts data structure
blog_posts = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
]

# Save to a JSON file
with open('blog_posts.json', 'w') as file:
    json.dump(blog_posts, file, indent=4)

print("Blog posts saved to blog_posts.json")