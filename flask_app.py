from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

comments = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)

    comments.append(request.form["contents"])
    return redirect(url_for("index"))


# return "<p>hello</p>"


if __name__ == "__main__":
    app.run(debug=True)
