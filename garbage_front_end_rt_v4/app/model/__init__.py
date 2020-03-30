from flask import Blueprint
model_info = Blueprint('model',__name__)
from . import views
