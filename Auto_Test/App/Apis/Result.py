import math

from flask import request
from flask_restful import Resource, marshal_with

from App import settings
from App.ext import db
from App.models import Results, Tasks


class ResultModels(Resource):
    @marshal_with(settings.all_fields(settings.result_get_fields))
    def get(self):
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or 10)
        page_num = math.ceil(len(Results.query.all()) / 10)
        r_id = int(request.args.get("r_id") or 0)
        if r_id:
            data = {}
            result = Results.query.filter_by(id=r_id)
            task = Tasks.query.filter_by(id=result[0].r_taskId)
            r_taskName = task[0].t_description
            r_result = result[0].r_result
            r_errorLog = result[0].r_errorLog
            data["id"] = r_id
            data["r_taskName"] = r_taskName
            data["r_result"] = r_result
            data["r_errorLog"] = r_errorLog
            return {"status": "200", "msg": "ok", "data": data}
        else:
            results = Results.query.paginate(page=page, per_page=per_page, error_out=False).items
            result_data = []

            for result in results:
                data = {}
                task = Tasks.query.filter_by(id=result.r_taskId)
                r_taskName = task[0].t_description
                r_result = result.r_result
                r_errorLog = result.r_errorLog
                id = result.id
                data["id"] = id
                data["r_taskName"] = r_taskName
                data["r_result"] = r_result
                data["r_errorLog"] = r_errorLog
                result_data.append(data)
            return {"status": "200", "msg": "ok", "data": result_data, "page_num": page_num}

    # @marshal_with(settings.single_fields(settings.result_fields))
    # def post(self):
    #     r_description = request.form.get("r_description")
    #     r_taskId = request.form.get("r_taskId")
    #     r_result = request.form.get("r_result")
    #     r_errorLog = request.form.get("r_errorLog")
    #
    #     result = Results()
    #
    #     result.r_description = r_description
    #     result.r_taskId = r_taskId
    #     result.r_result = r_result == str(True)
    #     result.r_errorLog = r_errorLog
    #
    #     db.session.add(result)
    #     db.session.commit()
    #
    #     return {"status": "201", "msg": "ok", "data": result}