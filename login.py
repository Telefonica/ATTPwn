from flask import session, redirect
from app import app

def login_user(usuario):
    session["id"] = usuario.id
    session["username"] = usuario.username
    session["admin"] = usuario.admin
    session["latchAccountId"] = usuario.latchAccountId


def logout_user():
    session.pop("id", None)
    session.pop("username", None)
    session.pop("admin", None)

def is_login():
    if "id" in session:
        return True
    else:
        return False

def is_admin():
    return session.get("admin", False)

@app.context_processor
def login():
    if "id" in session:
        return {'is_login': True}
    else:
        return {'is_login': False}


@app.context_processor
def admin():
    return {'is_admin': session.get("admin", False)}