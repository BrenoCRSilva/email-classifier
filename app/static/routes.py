from flask import Blueprint, send_from_directory
import os

static_bp = Blueprint("static", __name__)


@static_bp.route("/")
def index():
    return send_from_directory("../static", "index.html")


@static_bp.route("/styles.css")
def styles():
    return send_from_directory("../static", "styles.css")


@static_bp.route("/app.js")
def app_js():
    return send_from_directory("../static", "app.js")
