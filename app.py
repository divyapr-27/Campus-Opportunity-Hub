import os
import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

# AI assistance was used during development for explanations, debugging,
# and code suggestions. The final design and implementation should be
# understood, tested, and adapted by the student before submission.

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r", encoding="utf-8") as f:
        db.executescript(f.read())

    count = db.execute("SELECT COUNT(*) AS count FROM opportunities").fetchone()["count"]
    if count == 0:
        sample_data = [
            ("Python Developer Intern", "TechNova", "Internship",
             "Work on Python APIs, testing, and database features.",
             "https://example.com", "2026-09-30"),
            ("Campus Innovation Hackathon", "OpenBuild", "Hackathon",
             "Build a practical technology solution with a student team.",
             "https://example.com", "2026-10-12"),
            ("AI Foundations Workshop", "Future Skills Lab", "Workshop",
             "Beginner-friendly workshop covering machine learning and AI basics.",
             "https://example.com", "2026-09-18"),
            ("Women in Technology Scholarship", "TechFuture Foundation", "Scholarship",
             "Scholarship opportunity for students interested in technology careers.",
             "https://example.com", "2026-10-05"),
            ("Cloud Engineering Trainee", "CloudWorks", "Placement",
             "Entry-level opportunity focused on cloud and backend technologies.",
             "https://example.com", "2026-11-01"),
        ]
        db.executemany(
            """INSERT INTO opportunities
               (title, organization, type, description, link, deadline)
               VALUES (?, ?, ?, ?, ?, ?)""",
            sample_data
        )
    db.commit()
    db.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def index():
    db = get_db()
    opportunities = db.execute(
        "SELECT * FROM opportunities ORDER BY deadline LIMIT 6"
    ).fetchall()
    db.close()
    return render_template("index.html", opportunities=opportunities)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
            return render_template("register.html")

        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()

        if existing:
            db.close()
            flash("An account with that email already exists.", "danger")
            return render_template("register.html")

        db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password))
        )
        db.commit()
        db.close()

        flash("Account created. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        db.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        next_page = request.args.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
        return redirect(url_for("opportunities"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/opportunities")
def opportunities():
    search = request.args.get("search", "").strip()
    type_filter = request.args.get("type", "").strip()

    db = get_db()
    query = "SELECT * FROM opportunities WHERE 1=1"
    params = []

    if search:
        query += " AND (title LIKE ? OR organization LIKE ? OR description LIKE ?)"
        value = f"%{search}%"
        params.extend([value, value, value])

    if type_filter:
        query += " AND type = ?"
        params.append(type_filter)

    query += " ORDER BY deadline ASC"
    rows = db.execute(query, params).fetchall()
    db.close()

    return render_template(
        "opportunities.html",
        opportunities=rows,
        search=search,
        type_filter=type_filter
    )


@app.route("/opportunity/<int:opportunity_id>")
def opportunity_detail(opportunity_id):
    db = get_db()
    opportunity = db.execute(
        "SELECT * FROM opportunities WHERE id = ?", (opportunity_id,)
    ).fetchone()

    saved = False
    application = None

    if "user_id" in session:
        saved = db.execute(
            """SELECT 1 FROM saved_opportunities
               WHERE user_id = ? AND opportunity_id = ?""",
            (session["user_id"], opportunity_id)
        ).fetchone() is not None

        application = db.execute(
            """SELECT status FROM applications
               WHERE user_id = ? AND opportunity_id = ?""",
            (session["user_id"], opportunity_id)
        ).fetchone()

    db.close()

    if opportunity is None:
        flash("Opportunity not found.", "danger")
        return redirect(url_for("opportunities"))

    return render_template(
        "opportunity_detail.html",
        opportunity=opportunity,
        saved=saved,
        application=application
    )


@app.route("/save/<int:opportunity_id>", methods=["POST"])
@login_required
def save_opportunity(opportunity_id):
    db = get_db()
    existing = db.execute(
        """SELECT 1 FROM saved_opportunities
           WHERE user_id = ? AND opportunity_id = ?""",
        (session["user_id"], opportunity_id)
    ).fetchone()

    if existing:
        db.execute(
            """DELETE FROM saved_opportunities
               WHERE user_id = ? AND opportunity_id = ?""",
            (session["user_id"], opportunity_id)
        )
        flash("Opportunity removed from saved items.", "success")
    else:
        db.execute(
            """INSERT INTO saved_opportunities (user_id, opportunity_id)
               VALUES (?, ?)""",
            (session["user_id"], opportunity_id)
        )
        flash("Opportunity saved.", "success")

    db.commit()
    db.close()
    return redirect(url_for("opportunity_detail", opportunity_id=opportunity_id))


@app.route("/saved")
@login_required
def saved():
    db = get_db()
    rows = db.execute(
        """SELECT o.*
           FROM opportunities o
           JOIN saved_opportunities s ON o.id = s.opportunity_id
           WHERE s.user_id = ?
           ORDER BY o.deadline ASC""",
        (session["user_id"],)
    ).fetchall()
    db.close()
    return render_template("saved.html", opportunities=rows)


@app.route("/apply/<int:opportunity_id>", methods=["POST"])
@login_required
def apply(opportunity_id):
    status = request.form.get("status", "Applied")

    allowed = {"Applied", "Shortlisted", "Interview", "Selected", "Rejected"}
    if status not in allowed:
        status = "Applied"

    db = get_db()
    db.execute(
        """INSERT INTO applications (user_id, opportunity_id, status)
           VALUES (?, ?, ?)
           ON CONFLICT(user_id, opportunity_id)
           DO UPDATE SET status = excluded.status""",
        (session["user_id"], opportunity_id, status)
    )
    db.commit()
    db.close()

    flash("Application tracker updated.", "success")
    return redirect(url_for("opportunity_detail", opportunity_id=opportunity_id))


@app.route("/applications")
@login_required
def applications():
    db = get_db()
    rows = db.execute(
        """SELECT o.title, o.organization, o.type, o.deadline,
                  a.status, a.updated_at
           FROM applications a
           JOIN opportunities o ON a.opportunity_id = o.id
           WHERE a.user_id = ?
           ORDER BY a.updated_at DESC""",
        (session["user_id"],)
    ).fetchall()
    db.close()
    return render_template("applications.html", applications=rows)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_opportunity():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        organization = request.form.get("organization", "").strip()
        opportunity_type = request.form.get("type", "").strip()
        description = request.form.get("description", "").strip()
        link = request.form.get("link", "").strip()
        deadline = request.form.get("deadline", "").strip()

        if not all([title, organization, opportunity_type, description, link, deadline]):
            flash("Please complete every field.", "danger")
            return render_template("add.html")

        db = get_db()
        db.execute(
            """INSERT INTO opportunities
               (title, organization, type, description, link, deadline)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (title, organization, opportunity_type, description, link, deadline)
        )
        db.commit()
        db.close()

        flash("Opportunity added successfully.", "success")
        return redirect(url_for("opportunities"))

    return render_template("add.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


init_db()

if __name__ == "__main__":
    app.run(debug=True)
