from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)


@main.app_context_processor
def inject_premissions():
    return dict(Permisson=Permission)

from . import views, errors