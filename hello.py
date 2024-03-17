from flask import Flask, render_template
from filtros_html import today
from datetime import datetime

app = Flask(__name__)

app.add_template_filter(today, 'today')



@app.route('/')
@app.route('/<name>')
@app.route('/index')
def hello_world(name=None):
    data = {
        'name': name,
        'date': datetime.now()
    }
    
    return render_template('index.html', data=data)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    if name:
        return f'Hello, {name}!'
    return 'Hello, World2!'

# Run the app
# flask --app hello --debug run 