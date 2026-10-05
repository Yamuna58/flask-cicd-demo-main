from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello from Flask! 🚀"


@app.route('/health')
def health():
    return "OK"

@app.route('/test')
def test():
    return "It looks cool!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
