from flask import render_template, session, redirect, url_for, flash, session, request
from . import model_info
from config import Config


@model_info.route('/change', methods=["POST"])
def change():
    if request.method == "POST":
        model_name = request.form.get("model")
        lr = request.form.get("lr")
        epoch = request.form.get("epoch")
        feature_extract = request.form.get("feature_extract")
        if feature_extract == "是":
            f = 0
        else:
            f = 1
        k = request.form.get("k")
        file_name = model_name.lower() + "_" + str(epoch) + "_" + str(f) + "_lr{}".format(lr) + "_k{}".format(k)
        print(file_name)
        Config.MODEL_PATH = 'app/static/model/' + file_name + "/" + file_name + ".pth"
        print(Config.MODEL_PATH)
        Config.MODEL_NAME = model_name
        flash("模型更改成功！")
        return render_template("predict/choose.html", model_name=Config.MODEL_NAME)


@model_info.route('/return', methods=["GET"])
def returnBack():
    return render_template("predict/choose.html",model_name = Config.MODEL_NAME)
