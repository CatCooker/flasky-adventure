from flask import render_template, session, redirect, url_for, flash, session, request
from . import result
from .. import db
from ..models import Garbage, GarbageType
import os,stat
import shutil
from ..static.lib._read import read_garbage_info
from ..static.lib.to_predict import model_predict, garbage_t, model_path
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
            os.chmod(img_path,stat.S_IRWXO)
            shutil.move(img_path,fullfilename)
            labels, acc, max_index = model_predict(model_path=model_path, img_file=fullfilename)
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
            return render_template('result/result.html', acc=acc[max_index], garbage=garbage,
                                   garbage_type=grabage_type_cn,
                                   typephoto='img/{}.png'.format(garbage_type_us), describe=describe, deal=deal,
                                   prevent=prevent, filename=file_name, img_dir=None, labels=labels, acc_arr=acc,
                                   max_index=max_index, open_camera=True)
    return render_template("index.html")


@result.route('/analyse/<string:filename>', methods=["GET"])
def analyse(filename):
    print(filename)
    tag = filename.split("_")
    img_dir = ""
    if "capture" in tag:
        img_dir = os.path.join("..\\..\\static\\photo\\capture_photo\\", filename)
    else:
        img_dir = os.path.join("..\\..\\static\\photo\\upload_photo\\", filename)

    return render_template('result/analyse.html', img_dir=img_dir)
