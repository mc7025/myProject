import math

from flask import request
from flask_restful import Resource, marshal_with

from App import settings
from App.ext import db
from App.models import Cnns


class CnnModels(Resource):
    @marshal_with(settings.all_fields(settings.cnn_fields))
    def get(self):
        cnn = Cnns()
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or 10)
        page_num = math.ceil(len(cnn.query.all()) / 10)
        cnns = cnn.query.paginate(page=page, per_page=per_page, error_out=False).items

        return {"status": "200", "msg": "ok", "data": cnns, "page_num": page_num}

    @marshal_with(settings.single_fields(settings.cnn_fields))
    def post(self):
        c_name = request.form.get("c_name")
        c_type = request.form.get("c_type")
        c_format = request.form.get("c_format")
        c_path = request.form.get("c_path")
        c_isPublic = request.form.get("c_isPublic")
        cnn = Cnns()

        cnn.c_name = c_name
        cnn.c_type = c_type
        cnn.c_format = c_format
        cnn.c_path = c_path
        cnn.c_isPublic = c_isPublic == str(True)

        db.session.add(cnn)
        db.session.commit()

        return {"status": "201", "msg": "ok", "data": cnn}

    @marshal_with(settings.single_fields(settings.cnn_fields))
    def put(self):
        c_name = request.form.get("c_name")
        c_type = request.form.get("c_type")
        c_format = request.form.get("c_format")
        c_path = request.form.get("c_path")
        c_isPublic = request.form.get("c_isPublic")
        c_id = request.form.get("c_id")

        cnn = Cnns.query.get(c_id)
        if cnn:
            cnn.c_name = c_name
            cnn.c_type = c_type
            cnn.c_format = c_format
            cnn.c_path = c_path
            cnn.c_isPublic = c_isPublic == str(True)

        db.session.add(cnn)
        db.session.commit()

        return {"status": "202", "msg": "ok", "data": cnn}

    @marshal_with(settings.single_fields(settings.cnn_fields))
    def delete(self):
        id = request.form.get("c_id")
        cnn = Cnns.query.get(id)
        if cnn:
            try:
                db.session.delete(cnn)
                db.session.commit()
                return {"status": "203", "msg": "ok", "data": cnn}
            except:
                return {"msg": "Can not delete this model."}

