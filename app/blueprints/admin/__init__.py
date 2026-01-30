from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from . import routes
from . import students
from . import faculty
from . import notices
from . import exams
from . import attendance
