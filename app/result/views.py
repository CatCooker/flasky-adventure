from flask import render_template,session,redirect,url_for,flash,session,request
from . import result
from .. import db
from ..models import Garbage,GarbageType


@result.route('/recycle/<string:fname>',methods=["GET"])
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
                           prevent=session.get('prevent'), filename=fname)


@result.route('/kitchen/<string:filename>',methods=["GET"])
def addkitchen(filename):
    kitchen = Garbage.query.filter_by(filename=filename).first()
    if kitchen is not None:
        flash("该数据已经存在")
    else:
        kitchengarbage = Garbage(filename=filename, gtype=kitchen)
        db.session.add(kitchengarbage)
        db.session.commit()
        flash("纠正提交成功")
    return render_template('result/result.html', acc=session.get('acc'), garbage=session.get('garbage'), garbage_type=session.get('garbage_type'),
                    typephoto=session.get('typephoto'), describe=session.get('describe'), deal=session.get('deal'),
                    prevent=session.get('prevent'),filename=filename)


@result.route('/harmful/<string:filename>',methods=["GET"])
def addharmful(filename):
    harmful = Garbage.query.filter_by(filename=filename).first()
    if harmful is not None:
        flash("该数据已经存在")
    else:
        harmfulgarbage = Garbage(filename=filename, gtype=harmful)
        db.session.add(harmfulgarbage)
        db.session.commit()
        flash("纠正提交成功")
    return render_template('result/result.html', acc=session.get('acc'), garbage=session.get('garbage'), garbage_type=session.get('garbage_type'),
                    typephoto=session.get('typephoto'), describe=session.get('describe'), deal=session.get('deal'),
                    prevent=session.get('prevent'),filename=filename)


@result.route('/other/<string:filename>',methods=["GET"])
def addother(filename):
    other = Garbage.query.filter_by(filename=filename).first()
    if other is not None:
        flash("该数据已经存在")
    else:
        othergarbage = Garbage(filename=filename, gtype=other)
        db.session.add(othergarbage)
        db.session.commit()
        flash("提交成功")
    return render_template('result/result.html', acc=session.get('acc'), garbage=session.get('garbage'), garbage_type=session.get('garbage_type'),
                    typephoto=session.get('typephoto'), describe=session.get('describe'), deal=session.get('deal'),
                    prevent=session.get('prevent'),filename=filename)
