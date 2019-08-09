import math

from flask import request
from flask_restful import Resource, marshal_with

from App import settings
from App.ext import db
from App.models import DataSets


class DataModels(Resource):
    @marshal_with(settings.all_fields(settings.data_set_fields))
    def get(self):
        data_set = DataSets()
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or 10)
        page_num = math.ceil(len(data_set.query.all()) / 10)
        data_sets = data_set.query.paginate(page=page, per_page=per_page, error_out=False).items

        return {"status": "200", "msg": "ok", "data": data_sets, "page_num": page_num}

    @marshal_with(settings.single_fields(settings.data_set_fields))
    def post(self):
        d_name = request.form.get("d_name")
        d_type = request.form.get("d_type")
        d_size = request.form.get("d_size")
        d_path = request.form.get("d_path")

        data_set = DataSets()
        data_set.d_name = d_name
        data_set.d_type = d_type
        data_set.d_size = d_size
        data_set.d_path = d_path

        db.session.add(data_set)
        db.session.commit()

        return {"status": "201", "msg": "ok", "data": data_set}

    @marshal_with(settings.single_fields(settings.data_set_fields))
    def put(self):
        d_name = request.form.get("d_name")
        d_type = request.form.get("d_type")
        d_size = request.form.get("d_size")
        d_path = request.form.get("d_path")
        d_id = request.form.get("d_id")

        data_set = DataSets.query.get(d_id)
        if data_set:
            data_set.d_name = d_name
            data_set.d_type = d_type
            data_set.d_size = d_size
            data_set.d_path = d_path

        db.session.add(data_set)
        db.session.commit()

        return {"status": "202", "msg": "ok", "data": data_set}

    @marshal_with(settings.single_fields(settings.data_set_fields))
    def delete(self):
        d_id = request.form.get("d_id")
        data_set = DataSets.query.get(d_id)
        if data_set:
            try:
                db.session.delete(data_set)
                db.session.commit()
                return {"status": "203", "msg": "ok", "data": data_set}
            except:
                return {"msg": "Can not delete this data."}

