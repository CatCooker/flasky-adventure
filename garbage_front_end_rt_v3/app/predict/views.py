from flask import render_template, session, redirect, url_for, request, flash
from . import pred
from ..static.lib.open_camera import capture_photo
import os
from ..static.lib._read import read_garbage_info
from ..static.lib.to_predict import model_predict, garbage_t, model_path


@pred.route('/cam_or_file', methods=["GET", "POST"])
def cam_or_file():
    acc = 0
    garbage = ""
    garbage_type_us = ""
    filename = ""
    grabage_type_cn = ""
    fullfilename = ""
    labels = None
    acc = None
    if request.method == "GET":
        return render_template('predict/choose.html')
    if request.method == "POST":
        open_camera = request.form.get("open_camera")
        captured = request.form.get("captured")
        print("-----")
        print(captured)
        if open_camera == 'TRUE':
            # fullfilename = capture_photo()
            # filename = fullfilename.split("/")[4]
            print("yes")
            captured = request.form.get("captured")
            print(captured)
            labels = ["Type-1", "Type-2", "Type-3", "Type-4"]
            acc = [0, 0, 0, 0]
            max_index = -1
            garbage = "等待识别"
            garbage_type_us = "other"
            grabage_type_cn = "等待识别"
            print("predicting....")
        if open_camera == 'FALSE':
            file = request.files["file"]
            if file is not None:
                filename = file.filename
                fullfilename = os.path.join("app/static/photo/upload_photo", file.filename)
                file.save(fullfilename)
                labels, acc, max_index = model_predict(model_path=model_path, img_file=fullfilename)
                label = labels[max_index].split('/')
                garbage_type_us = garbage_t[label[0]]  # 英文
                grabage_type_cn = label[0]  # 中文
                garbage = label[1]
                labels = [item.split("/")[1] for item in labels]
        if labels == "None" and acc == -1:
            flash("请上传正确的图片文件！")
            return render_template("predict/choose.html")
        # if max_index == -1:
        #     garbage = "等待识别"
        #     garbage_type_us = "other"
        #     grabage_type_cn = "等待识别"

        # else:
            # label = labels[max_index].split('/')
            # garbage_type_us = garbage_t[label[0]]  # 英文
            # grabage_type_cn = label[0]  # 中文
            # garbage = label[1]
            # labels = [item.split("/")[1] for item in labels]
        print("received!")
    print("predict ", end="")
    print(fullfilename)
    print(filename)
    print(garbage_type_us)
    tag = filename.split("_")
    img_dir = ""
    if "capture" in tag:
        img_dir = os.path.join("..\\..\\static\\photo\\capture_photo\\", filename)
    else:
        img_dir = os.path.join("..\\..\\static\\photo\\upload_photo\\", filename)
    inforlist = read_garbage_info(dir="app/static/garbageInfo", garbagetype=garbage_type_us)
    describe = inforlist['describe']
    prevent = inforlist['prevent']
    deal = inforlist['deal']
    session['acc'] = acc[max_index]
    session['garbage'] = garbage
    session['garbage_type'] = grabage_type_cn
    session['typephoto'] = 'img/{}.png'.format(garbage_type_us)
    session['describe'] = describe
    session['deal'] = deal
    session['prevent'] = prevent
    session['filename'] = filename
    session['img_dir'] = img_dir
    session['labels'] = labels
    session['acc_arr'] = acc
    session['max_index'] = max_index
    open_c = False
    if open_camera == "TRUE":
        open_c = True
    if open_camera == "FALSE" or open_camera is None:
        open_c = False
    print(open_camera)
    session['open_c'] = open_c
    return render_template('result/result.html', acc=acc[max_index], garbage=garbage, garbage_type=grabage_type_cn,
                           typephoto='img/{}.png'.format(garbage_type_us), describe=describe, deal=deal,
                           prevent=prevent, filename=filename, img_dir=img_dir,labels=labels,acc_arr=acc,max_index=max_index,open_camera=open_c)
