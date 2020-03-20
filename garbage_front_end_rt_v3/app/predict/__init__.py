from flask import Blueprint
pred = Blueprint('pred',__name__)
from . import views
