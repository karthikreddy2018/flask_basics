from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

@app.route("/homeee")
def home():
    return render_template("home.html")

@app.route("/<int:id>")
def hii(id):
    return f"<h1>this is ur unique number {id}</h1>"
@app.route("/studentinfo/<string:name>/<int:age>")
def student(name,age):
    return render_template("user.html", name = name, age = age)
@app.route("/")
def starting():
    return "you are on the home page"
@app.route("/testing")
def ender():
    name = "karthik"
    age = 20
    return render_template("user.html",name = name, age = age)
@app.route("/stunames")
def students():
    student = ["karthik","nishh","uhuds","iuhas"]
    return render_template("students.html", student_names = student)
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/homess")
def homess():
    return render_template("home.html")
from flask import Flask, render_template, request

app = Flask(__name__)


from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/form", methods=["GET", "POST"])
def form():

    if request.method == "POST":

        name = request.form.get("karthik")
        age = request.form.get("age")

        # Check name
        if not name:
            return "Please enter your name"

        # Check age
        if not age:
            return "Please enter your age"

        # Convert age from string to integer
        age = int(age)

        # Check age
        if age < 18:
            return "Age must be 18 or above"


        return f"<h1>Hello {name}</h1><p>Your age is {age}</p>"

    return render_template("form.html")

@app.route("/formed", methods=["GET", "POST"])
def formee():

    if request.method == "POST":

        name = request.form.get("karthik")

        if not name:
            return render_template(
                "form.html",
                error="Please enter your name"
            )

        return redirect(url_for("success"))

    return render_template("form.html")


@app.route("/success")
def success():
    return "<h1>Form submitted successfully!</h1>"

@app.route("/")
def homesh():
    return redirect(url_for("abouts"))


@app.route("/abouted")
def abouts():
    return "<h1>About Page</h1>"


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)