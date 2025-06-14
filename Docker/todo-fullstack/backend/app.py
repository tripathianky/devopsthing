from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change this!
jwt = JWTManager(app)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"msg": "Username already exists"}), 409

    hashed_password = generate_password_hash(password)
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not check_password_hash(user[1], password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user[0])
    return jsonify(access_token=access_token)

@app.route("/todos", methods=["GET"])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM todos WHERE user_id = %s", (user_id,))
    todos = cur.fetchall()
    cur.close()
    conn.close()
    todos_list = [{"id": t[0], "title": t[1], "done": t[2]} for t in todos]
    return jsonify(todos_list)

@app.route("/todos", methods=["POST"])
@jwt_required()
def add_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"msg": "Title required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (user_id, title) VALUES (%s, %s) RETURNING id", (user_id, title))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": todo_id, "title": title, "done": False}), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    done = data.get("done")
    if done is None:
        return jsonify({"msg": "Done status required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET done = %s WHERE id = %s AND user_id = %s", (done, todo_id, user_id))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"msg": "Todo not found or unauthorized"}), 404
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": todo_id, "done": done})

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s AND user_id = %s", (todo_id, user_id))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"msg": "Todo not found or unauthorized"}), 404
    conn.commit()
    cur.close()
    conn.close()
    return '', 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
