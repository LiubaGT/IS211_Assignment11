import traceback

from flask import Flask
from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
import yaml
import os
import traceback


app = Flask(__name__)

PRIORITIES = {
    0: 'Low',
    1: 'Medium',
    2: 'High'
}


fake_todos = [
    {
        'email': 'm@m.com',
        'task': "TODO 0",
        'priority': 0
     },
    {
        'email': 'a@m.com',
        'task': "TODO 1",
        'priority_idx': 2
    }
]

@app.route('/')
def main():
    todos_list= []
    if os.path.isfile('./todos_list.yaml'):
        with open('./todos_list.yaml') as f:
            todos_list_st = f.read()
            todos_list = yaml.safe_load(todos_list_st)

    print(len(todos_list), todos_list)

    return render_template('list_of_todos.html', todos=todos_list, priorities_len=len(PRIORITIES), Priorities=PRIORITIES)

@app.route("/clear")
def clear():
    with open('./todos_list.yaml', 'w') as f:
        yaml.dump([], f, default_flow_style=False)

    return redirect(url_for('main'))

@app.route("/delete")
def delete():
    try:
        if os.path.isfile('./todos_list.yaml'):
            with open('./todos_list.yaml') as f:
                todos_list_st = f.read()
                todos_list = yaml.safe_load(todos_list_st)

        if request.method == 'GET':
            idx = int(request.args.get('idx'))
            item_pos_tbd = -1
            for i, todo in enumerate(todos_list):
                if int(todo['todo_idx']) == idx:
                    item_pos_tbd = i
            if item_pos_tbd != -1:
                del todos_list[item_pos_tbd]

            with open('./todos_list.yaml', 'w') as f:
                yaml.dump(todos_list, f, default_flow_style=False)

    except Exception as e:
        traceback.print_exc()

    return redirect(url_for('main'))

def valid_email(email:str) -> bool:
    valid = True
    if '@' not in email:
        return False
    if len(email.split('@')[0]) == 0:
        return False
    if len(email.split('@')[1]) == 0:
        return False
    if '.' not in email.split('@')[1]:
        return False
    return True

@app.route("/submit")
def submit():
    todos_list= []
    try:
        if os.path.isfile('./todos_list.yaml'):
            with open('./todos_list.yaml') as f:
                todos_list_st = f.read()
                todos_list = yaml.safe_load(todos_list_st)

        if request.method == 'GET':
            new_todo = {}
            new_todo['priority_idx'] = int(request.args.get('priority'))
            new_todo['task'] = request.args.get('Task')
            if len(new_todo['task']) == 0:
                raise Exception('Task description should be completed!')
            new_todo['email'] = request.args.get('email')
            if not valid_email(new_todo['email']):
                raise Exception('Task description should be completed!')
            new_todo['todo_idx'] = max([-1] + [int(todo['todo_idx']) for todo in todos_list]) + 1

            todos_list.append(new_todo)

            with open('./todos_list.yaml', 'w') as f:
                yaml.dump(todos_list, f, default_flow_style=False)
    except Exception as e:
        traceback.print_exc()

    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run()
