from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="c.ronaldo",
        database="news_feed"
    )

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"message": "User created successfully"}), 201

# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"message": "User deleted successfully"}), 204


# Create Post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data['user_id']
    title = data['title']
    content = data['content']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Post created successfully"}), 201

# Update post details
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    title = data['title']
    content = data['content']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Post updated successfully"})

# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(posts)

# Get a single post by id
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404
    
# Delete a post
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Post deleted successfully"}), 204