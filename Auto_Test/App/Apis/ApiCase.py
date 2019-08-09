import math

from flask import request
from flask_restful import Resource, marshal_with

from App import settings
from App.ext import db
from App.models import ApiCases, Cnns, DataSets


class ApiCaseModels(Resource):
    @marshal_with(settings.all_fields(settings.api_get_fields))
    def get(self):
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or 10)
        page_num = math.ceil(len(ApiCases.query.all()) / 10)
        api_cases = ApiCases.query.paginate(page=page, per_page=per_page, error_out=False).items
        api_data = []
        for api_case in api_cases:
            data = {}
            cnn = Cnns.query.filter_by(id=api_case.a_modelId)
            data_set = DataSets.query.filter_by(id=api_case.a_dataId)
            id = api_case.id
            a_level = api_case.a_level
            a_type = api_case.a_type
            a_description = api_case.a_description
            c_name = cnn[0].c_name
            d_name = data_set[0].d_name
            data["id"] = id
            data["a_level"] = a_level
            data["a_type"] = a_type
            data["c_name"] = c_name
            data["d_name"] = d_name
            data["a_description"] = a_description
            api_data.append(data)

        return {"status": "200", "msg": "ok", "data": api_data, "page_num": page_num}

    @marshal_with(settings.single_fields(settings.api_fields))
    def post(self):
        a_level = request.form.get("a_level")
        a_type = request.form.get("a_type")
        a_modelId = request.form.get("a_modelId")
        a_dataId = request.form.get("a_dataId")
        a_description = request.form.get("a_description")

        api_case = ApiCases()
        api_case.a_level = a_level
        api_case.a_type = a_type
        api_case.a_modelId = a_modelId
        api_case.a_dataId = a_dataId
        api_case.a_description = a_description

        db.session.add(api_case)
        db.session.commit()

        return {"status": "201", "msg": "ok", "data": api_case}

    @marshal_with(settings.single_fields(settings.api_fields))
    def put(self):
        a_level = request.form.get("a_level")
        a_type = request.form.get("a_type")
        a_modelId = request.form.get("a_modelId")
        a_dataId = request.form.get("a_dataId")
        a_description = request.form.get("a_description")
        a_id = request.form.get("a_id")

        api_case = ApiCases.query.get(a_id)

        if api_case:
            api_case.a_level = a_level
            api_case.a_type = a_type
            api_case.a_modelId = a_modelId
            api_case.a_dataId = a_dataId
            api_case.a_description = a_description

        db.session.add(api_case)
        db.session.commit()

        return {"status": "202", "msg": "ok", "data": api_case}

    @marshal_with(settings.single_fields(settings.api_fields))
    def delete(self):
        a_id = request.form.get("a_id")
        api_case = ApiCases.query.get(a_id)

        if api_case:
            try:
                db.session.delete(api_case)
                db.session.commit()
                return {"status": "203", "msg": "ok", "data": api_case}
            except:
                return {"msg": "Can not delete this case."}