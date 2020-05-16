from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   s = "Hello World"
   return s

if __name__ == '__main__':
   app.run()