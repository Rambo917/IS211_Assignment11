import json
import os
import re
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATA_FILE = 'todos.json'
PRIORITIES = ('Low', 'Medium', 'High')


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


todos = load_tasks()


@app.route('/')
def index():
    return render_template('index.html', todos=todos)


@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task', '').strip()
    email = request.form.get('email', '').strip()
    priority = request.form.get('priority', '')

    email_valid = re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email)
    if not task or not email_valid or priority not in PRIORITIES:
        return redirect(url_for('index'))

    todos.append({'task': task, 'email': email, 'priority': priority})
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear():
    todos.clear()
    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save():
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(todos, file, indent=2)
    return redirect(url_for('index'))


@app.route('/delete/<int:item_index>', methods=['POST'])
def delete(item_index):
    if 0 <= item_index < len(todos):
        todos.pop(item_index)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
