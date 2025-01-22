from . import auth, user, trick

def init_app(db):
    auth.init_app(db)
    user.init_app(db)
    trick.init_app(db)