# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .home import home_views
from .login import login_views



views = [user_views, index_views, auth_views, home_views, login_views] 
# blueprints must be added to this list