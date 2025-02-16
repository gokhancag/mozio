import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello Mozio! - v2"

@app.route('/whoareyou')
def hello():
    return 'I am DevOps Engineer at Mozio! - v2'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
