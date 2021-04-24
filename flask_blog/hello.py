# import statements
from flask import Flask

# application instance
app = Flask(__name__)

#route to main url
@app.route('/')
def hello():
    #return string 'Hello, World!'
    return 'Hello, World!'