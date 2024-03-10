from flask import Flask

from HumePrueba import hello_world2

app = Flask(__name__)
print(__name__)
@app.route("/")
def hello_world():
    result = hello_world2()
    return f"<p>Hello, World! Result: {result}</p>"
