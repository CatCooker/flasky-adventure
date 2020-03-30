from flask import Blueprint
result = Blueprint('result',__name__)
from . import views
