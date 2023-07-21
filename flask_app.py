from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("main_page.html")
    # return "<p>hello</p>"


if __name__ == "__main__":
    app.run(debug=True)
