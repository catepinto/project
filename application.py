from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
import sys


from helpers import phone

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Custom filter
app.jinja_env.filters["phone"] = phone

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///resources.db")


@app.route("/")
def index():
    """Show home page"""

    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    """Search for resources using filters"""

    if request.method == "POST":

        # check for filters
        if not request.form:
            error_msg = "Please select at least one filter"
            return render_template("search.html", error_msg=error_msg)

        # get data from form
        submission = dict(request.form)

        # create empty list to store filters
        filters = []

        # get number of tags selected by user
        number_tags = len(submission["tags"])

        # add tags to a list
        for i in range(number_tags):
            filters.append(submission["tags"][i])

        # get all potential matches from database
        all_results = db.execute("SELECT * FROM tags WHERE tag IN (:filters)", filters=filters)

        # get list of resource ids
        resource_ids = []
        number_results = len(all_results)
        for k in range(number_results):
            resource_ids.append(all_results[k]["resource"])

        # get number of resources currently in database
        find_length = db.execute("SELECT resource_id FROM resources")
        number_resources = len(find_length)

        # make list for scores
        scores = []
        for s in range(number_resources):
            scores.append(0)

        # update scores
        for j in range(number_results):
            scores[resource_ids[j] - 1] += 1

        # get best resources
        # SOURCE: https://stackoverflow.com/questions/364621/how-to-get-items-position-in-a-list
        # SOURCE: https://stackoverflow.com/questions/9304408/how-to-add-an-integer-to-each-element-in-a-list
        # SOURCE: https://www.tutorialspoint.com/python/list_max.htm
        best = max(scores)
        best_resources = []
        best_resources = [a for a, x in enumerate(scores) if x == best]
        best_resources = [x + 1 for x in best_resources]

        # get percent match
        percent_match = int(best / number_tags * 100)

        # get resource information from database
        resources = db.execute(
            "SELECT * FROM resources WHERE resource_id IN (:best_resources)", best_resources=best_resources)

        return render_template("results.html", resources=resources, percent_match=percent_match)

    else:
        return render_template("search.html")


@app.route("/resources", methods=["GET", "POST"])
def resources():
    """See a list of all resources"""

    resources = db.execute("SELECT * FROM resources")
    return render_template("resources.html", resources=resources)


@app.route("/search_all")
def search_all():
    """Search for resources that match query"""

    # get user input plus wildcard
    q = request.args.get("q") + "%"

    # find potential results
    resources = db.execute("SELECT * FROM resources WHERE name LIKE :q", q=q)

    return jsonify(resources)
