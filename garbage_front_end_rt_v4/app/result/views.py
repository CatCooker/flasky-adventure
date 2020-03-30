from flask import render_template, session, redirect, url_for, flash, session, request
from . import result
from .. import db
from ..models import Garbage, GarbageType
import os, stat
import shutil
from ..static.lib._read import read_garbage_info
from ..static.lib.to_predict import model_predict, garbage_t, get_modelPath, reverse_class, class_
import json
import numpy as np


@result.route('/recycle/<string:fname>', methods=["GET"])
def addrecycle(fname):
    recycle = Garbage.query.filter_by(filename=fname).first()
    if recycle is not None:
        flash("该数据已经存在")
    else:
        recyclegarbage = Garbage(filename=fname, gtype=recycle)
        db.session.add(recyclegarbage)
        db.session.commit()
        flash("纠正提交成功")
    return render_template('result/result.html', acc=session.get('acc'), garbage=session.get('garbage'),
                           garbage_type=session.get('garbage_type'),
                           typephoto=session.get('typephoto'), describe=session.get('describe'),
                           deal=session.get('deal'),
                           prevent=session.get('prevent'), filename=fname, img_dir=session.get('img_dir')
                           , labels=session.get('labels'), acc_arr=session.get('acc'),
                           max_index=session.get('max_index'),
                           open_camera=session.get('open_c'))


@result.route('/kitchen/<string:filename>', methods=["GET"])
def addkitchen(filename):
    kitchen = Garbage.query.filter_by(filename=filename).first()
    if kitchen is not None:
        flash("该数据已经存在")
    else:
        kitchengarbage = Garbage(filename=filename, gtype=kitchen)
        db.session.add(kitchengarbage)
        db.session.commit()
        flash("纠正提交成功")
    return render_template('result/result.html', acc=session.get('acc'), garbage=session.get('garbage'),
                           garbage_type=session.get('garbage_type'),
                           typephoto=session.get('typephoto'), describe=session.get('describe'),
                           deal=session.get('deal'),
                           prevent=session.get('prevent'), filename=filename, img_dir=session.get('img_dir')
                           , labels=session.get('labels'), acc_arr=session.get('acc'),
                           max_index=session.get('max_index'),
                           open_camera=session.get('open_c'))


@result.route('/harmful/<string:filename>', methods=["GET"])
def addharmful(filename):
    harmful = Garbage.query.filter_by(filename=filename).first()
    if harmful is not None:
        flash("该数据已经存在")
    else:
        harmfulgarbage = Garbage(filename=filename, gtype=harmful)
        db.session.add(harmfulgarbage)
        db.session.commit()
        flash("纠正提交成功")
    return render_template('result/result.html', acc=session.get('acc'), garbage=session.get('garbage'),
                           garbage_type=session.get('garbage_type'),
                           typephoto=session.get('typephoto'), describe=session.get('describe'),
                           deal=session.get('deal'),
                           prevent=session.get('prevent'), filename=filename, img_dir=session.get('img_dir')
                           , labels=session.get('labels'), acc_arr=session.get('acc'),
                           max_index=session.get('max_index'),
                           open_camera=session.get('open_c'))


@result.route('/other/<string:filename>', methods=["GET"])
def addother(filename):
    other = Garbage.query.filter_by(filename=filename).first()
    if other is not None:
        flash("该数据已经存在")
    else:
        print(filename)
        othergarbage = Garbage(filename=filename, gtype=other)
        db.session.add(othergarbage)
        db.session.commit()
        flash("提交成功")
    return render_template('result/result.html', acc=session.get('acc'), garbage=session.get('garbage'),
                           garbage_type=session.get('garbage_type'),
                           typephoto=session.get('typephoto'), describe=session.get('describe'),
                           deal=session.get('deal'),
                           prevent=session.get('prevent'), filename=filename, img_dir=session.get('img_dir')
                           , acc_arr=session.get('acc'),
                           max_index=session.get('max_index'),
                           open_camera=session.get('open_c')
                           )


@result.route('/capture', methods=["POST", "GET"])
def capture_photo():
    if request.method == "POST":
        captured = request.form.get("captured")
        print(captured)
        if captured == "True":
            print("yes")
            file_count = 0
            img_path = "D:/Download/Browser/capture_photo.png"
            for dirpath, dirnames, filenames in os.walk('app/static/photo/capture_photo'):
                for file in filenames:
                    file_count = file_count + 1
            file_name = "capture_photo{}.jpg".format(str(file_count))
            fullfilename = "app/static/photo/capture_photo/{}".format(file_name)
            while not os.path.exists(img_path):
                continue
            os.chmod(img_path, stat.S_IRWXO)
            shutil.move(img_path, fullfilename)
            labels, acc, max_index = model_predict(model_path=get_modelPath(), img_file=fullfilename)
            label = labels[max_index].split('/')
            garbage_type_us = garbage_t[label[0]]  # 英文
            grabage_type_cn = label[0]  # 中文
            garbage = label[1]
            labels = [item.split("/")[1] for item in labels]
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
            session['filename'] = file_name
            session['labels'] = labels
            session['acc_arr'] = acc
            session['max_index'] = max_index
            session['open_c'] = True
            print("当前使用" + get_modelPath())
            return render_template('result/result.html', acc=acc[max_index], garbage=garbage,
                                   garbage_type=grabage_type_cn,
                                   typephoto='img/{}.png'.format(garbage_type_us), describe=describe, deal=deal,
                                   prevent=prevent, filename=file_name, img_dir=None, labels=labels, acc_arr=acc,
                                   max_index=max_index, open_camera=True)
    return render_template("index.html")


@result.route('/model/<string:model_name>', methods=["GET"])
def my_model(model_name):
    labels = []
    json_file = get_modelPath().split(".pth")[0] + ".json"
    heat_map_file = get_modelPath().split(".pth")[0].split("/")[4].split("_")[0] + "_heat_map.csv"
    with open(json_file, "r") as file:
        data = json.loads(file.read())
        # print(data)
        data = sorted(data.items(), key=lambda item: item[1])
        for tup in data:
            labels.append(tup[0])
    least_error_label = labels[0]
    most_error_label = labels[-1]
    print(most_error_label)
    least_index = reverse_class[least_error_label]
    most_index = reverse_class[most_error_label]
    least_error_file = 'garbageInfo/labels/{}'.format(least_index) + '/' + "img_1.jpg"
    most_error_file = 'garbageInfo/labels/{}'.format(most_index) + '/' + "img_1.jpg"

    split_path = get_modelPath().split('/')
    print(split_path)
    dir = ""
    for i in range(2, 4):
        dir = dir + split_path[i] + "/"
    heat_map = dir + model_name.lower() + "_heat_map.jpg"
    acc_loss = dir + model_name.lower() + "_acc_loss.jpg"
    top_1_file = 'app/'+'static/'+dir + model_name.lower() + "_top1.txt"
    top_5_file =  'app/'+'static/'+dir + model_name.lower() + "_top5.txt"
    top_1 = ""
    top_5 = ""
    with open(top_1_file,'r') as file:
        top_1 = file.readline()
        top_1 = float(top_1) * 100
        top_1 = "{:.2f}".format(top_1)
    with open(top_5_file,'r') as file:
        top_5 = file.readline()
        top_5 = float(top_5) * 100
        top_5 = "{:.2f}".format(top_5)
    heat_map_file = "app/" + "static/" + dir + model_name.lower() + "_heat_map.csv"
    model = split_path[4]
    split_model = model.split('_')
    epoch = split_model[1]
    feature_extract = split_model[2]
    lr = split_model[3].lstrip('lr')
    k = split_model[4].split('.')[0].lstrip('k')

    heat_map_data = np.loadtxt(heat_map_file, delimiter=',')
    for i in range(40):
        heat_map_data[i][i] = 0
    row, col = np.where(heat_map_data == np.max(heat_map_data))
    row = row[0]
    col = col[0]
    left_img = 'garbageInfo/labels/{}'.format(row) + '/' + "img_1.jpg"
    left_label = class_[str(row)].split("/")[1]
    right_img = 'garbageInfo/labels/{}'.format(col) + '/' + "img_1.jpg"
    right_label = class_[str(col)].split("/")[1]
    print("加载" + heat_map)
    return render_template('result/my_model.html', model_name=model_name, epoch=epoch
                           , feature_extract=feature_extract, lr=lr, k=k, least_error_label=least_error_label
                           , heat_map=heat_map, most_error_label=most_error_label, least_error_file=least_error_file,
                           most_error_file=most_error_file
                           , left_img=left_img, right_img=right_img, left_label=left_label, right_label=right_label,
                           acc_loss=acc_loss,top_1=top_1,top_5=top_5)
