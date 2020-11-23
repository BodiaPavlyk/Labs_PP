from flask import Flask,jsonify,request,render_template
app = Flask(__name__)


@app.route('/Bodia')
def hello_world():
    test = request.args.get('test', '')
    return "test = " + test


if __name__ == '__main__':
    app.run()
