from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates')

from . import routes, users_mgmt, notices_mgmt, timetable_mgmt
from . import academics_mgmt
