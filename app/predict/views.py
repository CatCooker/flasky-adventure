from flask import render_template,session,redirect,url_for,request,flash
from . import pred
from ..static.lib.open_camera import capture_photo
import os
from ..static.lib._read import read_garbage_info
from ..static.lib.to_predict import model_predict,garbage_t,model_path

@pred.route('/cam_or_file',methods=["GET","POST"])
def cam_or_file():
    acc = 0
    garbage=""
    garbage_type_us=""
    filename = ""
    grabage_type_cn=""
    fullfilename = ""
    if request.method == "GET":
        flash("启动相机按Q键拍照")
        return render_template('predict/choose.html')
    if request.method == "POST":
        open_camera = request.form.get("open_camera")
        if open_camera == 'TRUE':
            fullfilename = capture_photo()
            print("predicting....")
        if open_camera == 'FALSE':
            file = request.files["file"]
            if file is not None:
                filename = file.filename
                fullfilename = os.path.join("app/static/photo/upload_photo", file.filename)
                file.save(fullfilename)
        label, acc = model_predict(model_path=model_path, img_file=fullfilename)
        garbage_type_us = garbage_t[label[0]]  # 英文
        grabage_type_cn = label[0] # 中文
        garbage = label[1]
        print("received!")
    print("predict {}".format(filename))
    print(garbage_type_us)
    inforlist = read_garbage_info(dir = "app/static/garbageInfo",garbagetype=garbage_type_us)
    describe = inforlist['describe']
    prevent = inforlist['prevent']
    deal = inforlist['deal']
    session['acc'] = acc
    session['garbage'] = garbage
    session['garbage_type'] = grabage_type_cn
    session['typephoto'] = 'img/{}.png'.format(garbage_type_us)
    session['describe'] = describe
    session['deal'] = deal
    session['prevent'] = prevent
    session['filename'] = filename
    return render_template('result/result.html',acc=acc,garbage=garbage,garbage_type=grabage_type_cn,typephoto='img/{}.png'.format(garbage_type_us),describe=describe,deal=deal,
                           prevent=prevent,filename=filename)
