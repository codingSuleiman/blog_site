from flask import redirect, url_for, render_template, flash
from proj import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

