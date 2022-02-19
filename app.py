from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
# session helps us for cookies
# jsonify for API
import json
import os.path
# this allows us to check the uploaded file and make sure its safe to save
from werkzeug.utils import secure_filename


# by using render template we can link our html files to the code
# by using request we can specify how our request is comming is it GET or POST
# by using redirect we can redirect our users to homepage
# this is our flask app
app = Flask(__name__)
app.secret_key = "hdgfcthd"
# here we are routing to base site .


@app.route('/')
def home():
    # by using codes=session.keys() we are passing our cookie info to homepage
    return render_template("home.html", codes=session.keys())
    # we can put a variable inside the rendertemplate and print it out by mentiong that in our HTML file {{}}
# here we are creating another page by routing our users to base home page \your-url
# by default the method used will be get so here we are making our app use POST method


@app.route("/your-url", methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        # we are creating a dictionary with the values passed by user
        urls = {}
# here we are checking if existing shortform exists or not in the dictionary and if it exists user will be redirected back to home page
        if os.path.exists("urls.json"):
            with open("urls.json") as urls_file:
                urls = json.load(urls_file)
        if request.form["code"] in urls.keys():
            # flash helps us to display messages , we have to link it inside our html as well
            flash("that shortname exists already , please select another name")
            return redirect(url_for("home"))
        if "url" in request.form.keys():
            urls[request.form["code"]] = {"url": request.form["url"]}
        else:
            # here we are giving code for our upload file option
            f = request.files["file"]
            full_name = request.form["code"] + secure_filename(f.filename)
            f.save("/Users/aksha/URL_shortner/static/user_files/" + full_name)
            urls[request.form["code"]] = {"file": full_name}

        # save our dictionary to json file
        with open("urls.json", "w") as url_file:
            json.dump(urls, url_file)
            session[request.form["code"]] = True    # cookie saving
        return render_template("your_url.html", code=request.form["code"])
    else:
        # we are redirecting the user to homepage , we have the function "home" above which points to our homepage
        return redirect(url_for("home"))

# here what we are doing is we can enabling our site to go to the original sites/files if we use \shortcut in brpwser


@app.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists("urls.json"):
        with open("urls.json") as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
                else:
                    return redirect(url_for("static", filename="user_files/" + urls[code]["file"]))
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

# creating API


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
