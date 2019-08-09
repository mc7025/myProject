import math

from flask import request
from flask_restful import Resource, marshal_with

from App import settings
from App.ext import db
from App.models import SampleCases, Cnns, DataSets


class SampleCaseModels(Resource):
    @marshal_with(settings.all_fields(settings.sample_get_fields))
    def get(self):
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or 10)
        page_num = math.ceil(len(SampleCases.query.all()) / 10)
        samples = SampleCases.query.paginate(page=page, per_page=per_page, error_out=False).items

        sample_data = []
        for sample in samples:
            data = {}
            clsModel = Cnns.query.filter_by(id=sample.s_modelClsId)
            detModel = Cnns.query.filter_by(id=sample.s_modelDetId)
            dataSet = DataSets.query.filter_by(id=sample.s_dataId)
            id = sample.id
            s_description = sample.s_description
            s_type = sample.s_type
            s_modelClsName = clsModel[0].c_name
            s_modelDetName = detModel[0].c_name
            s_dataName = dataSet[0].d_name
            data["id"] = id
            data["s_description"] = s_description
            data["s_type"] = s_type
            data["s_modelClsName"] = s_modelClsName
            data["s_modelDetName"] = s_modelDetName
            data["s_dataName"] = s_dataName
            sample_data.append(data)

        return {"status": "200", "msg": "ok", "data": sample_data, "page_num": page_num}

    @marshal_with(settings.single_fields(settings.sample_fields))
    def post(self):
        s_type = request.form.get("s_type")
        s_modelClsId = request.form.get("s_modelClsId")
        s_modelDetId = request.form.get("s_modelDetId")
        s_dataId = request.form.get("s_dataId")
        s_description = request.form.get("s_description")

        sample = SampleCases()
        sample.s_type = s_type
        sample.s_modelClsId = s_modelClsId
        sample.s_modelDetId = s_modelDetId
        sample.s_dataId = s_dataId
        sample.s_description = s_description

        db.session.add(sample)
        db.session.commit()

        return {"status": "201", "msg": "ok", "data": sample}

    @marshal_with(settings.single_fields(settings.sample_fields))
    def put(self):
        s_type = request.form.get("s_type")
        s_modelClsId = request.form.get("s_modelClsId")
        s_modelDetId = request.form.get("s_modelDetId")
        s_dataId = request.form.get("s_dataId")
        s_description = request.form.get("s_description")
        s_id = request.form.get("s_id")

        sample = SampleCases.query.get(s_id)

        if sample:
            sample.s_type = s_type
            sample.s_modelClsId = s_modelClsId
            sample.s_modelDetId = s_modelDetId
            sample.s_dataId = s_dataId
            sample.s_description = s_description

        db.session.add(sample)
        db.session.commit()

        return {"status": "202", "msg": "ok", "data": sample}

    @marshal_with(settings.single_fields(settings.sample_fields))
    def delete(self):
        s_id = request.form.get("s_id")

        sample = SampleCases.query.get(s_id)

        if sample:
            try:
                db.session.delete(sample)
                db.session.commit()
                return {"status": "203", "msg": "ok", "data": sample}
            except:
                return {"msg": "Can not delete this case."}