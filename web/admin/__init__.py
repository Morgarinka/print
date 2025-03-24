from flask import Blueprint

admin_bp= Blueprint("ammin", __name__, template_folder="templates")

from . import routes