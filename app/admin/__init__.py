from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates')

from . import routes
from . import users_mgmt
from . import academics_mgmt
from . import notices
