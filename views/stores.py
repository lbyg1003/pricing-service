import json
from flask import Blueprint, render_template, request
from models.store import Store

store_blueprint = Blueprint("stores", __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route("/new", methods=["GET", "POST"])
def create_store():
    if request.method == "POST":
        store_name = request.form["store_name"]
        url_prefix = request.form["url_prefix"]
        tag_name = request.form["tag_name"]
        attrs = json.loads(request.form["attrs"])

        Store(store_name, url_prefix, tag_name, attrs).save_to_mongo()

    return render_template("stores/new_store.html")