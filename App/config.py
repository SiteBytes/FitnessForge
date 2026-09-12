import os

def load_config(app, overrides):
    if os.path.exists(os.path.join('./App', 'custom_config.py')):
        app.config.from_object('App.custom_config')
    else:
        app.config.from_object('App.default_config')
    app.config.from_prefixed_env()

    # Fallback to local SQLite if DATABASE_URL or FLASK_SQLALCHEMY_DATABASE_URI is empty, invalid, or points to the decommissioned Postgres instance
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if not db_uri or 'dpg-d7algefkijhs738u8th0-a' in db_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp-database.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = os.getenv('JWT_COOKIE_SECURE', 'False').lower() == 'true'
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    for key in overrides:
        app.config[key] = overrides[key]

