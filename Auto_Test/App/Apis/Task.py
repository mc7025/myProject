import math

from flask import request
from flask_restful import Resource, marshal_with

from App import settings
from App.ext import db
from App.models import Tasks, Hosts, ApiCases, SampleCases, Cnns, DataSets


class TaskModels(Resource):
    @marshal_with(settings.all_fields(settings.task_get_fields))
    def get(self):
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or 10)
        page_num = math.ceil(len(Tasks.query.all()) / 10)
        tasks = Tasks.query.paginate(page=page, per_page=per_page, error_out=False).items
        task_data = []

        for task in tasks:
            data = {}
            host = Hosts.query.filter_by(id=task.t_hostId)
            apiCase = ApiCases.query.filter_by(id=task.t_apiCaseId)
            sampleCase = SampleCases.query.filter_by(id=task.t_sampleCaseId)
            id = task.id
            t_description = task.t_description
            t_caseType = task.t_caseType
            t_duration = task.t_duration
            t_status = task.t_status
            t_hostId = task.t_hostId
            t_hostIp = host[0].h_ip
            t_apiCase = apiCase[0].a_description
            t_apiCaseId = task.t_apiCaseId
            t_sampleCase = sampleCase[0].s_description
            t_sampleCaseId = task.t_sampleCaseId
            data["id"] = id
            data["t_description"] = t_description
            data["t_caseType"] = t_caseType
            data["t_hostIp"] = t_hostIp
            data["t_hostId"] = t_hostId
            data["t_apiCase"] = t_apiCase
            data["t_apiCaseId"] = t_apiCaseId
            data["t_sampleCase"] = t_sampleCase
            data["t_sampleCaseId"] = t_sampleCaseId
            data["t_duration"] = t_duration
            data["t_status"] = t_status
            task_data.append(data)

        return {"status": "200", "msg": "ok", "data": task_data, "page_num": page_num}

    @marshal_with(settings.single_fields(settings.task_fields))
    def post(self):
        t_caseType = request.form.get("t_caseType")
        t_hostId = request.form.get("t_hostId")
        t_apiCaseId = request.form.get("t_apiCaseId")
        t_sampleCaseId = request.form.get("t_sampleCaseId")
        t_duration = request.form.get("t_duration")
        t_description = request.form.get("t_description")
        t_status = "New"

        if t_apiCaseId == "False":
            api = ApiCases.query.all()
            t_apiCaseId = api[0].id
        if t_sampleCaseId == "False":
            sample = SampleCases.query.all()
            t_sampleCaseId = sample[0].id

        task = Tasks()
        task.t_caseType = t_caseType
        task.t_hostId = t_hostId
        task.t_apiCaseId = t_apiCaseId
        task.t_sampleCaseId = t_sampleCaseId
        task.t_duration = t_duration
        task.t_status = t_status
        task.t_description = t_description

        db.session.add(task)
        db.session.commit()

        return {"status": "201", "msg": "ok", "data": task}

    @marshal_with(settings.single_fields(settings.task_fields))
    def put(self):
        t_id = request.form.get("t_id")
        if t_id:
            t_caseType = request.form.get("t_caseType")
            t_hostId = request.form.get("t_hostId")
            t_apiCaseId = request.form.get("t_apiCaseId")
            t_sampleCaseId = request.form.get("t_sampleCaseId")
            t_duration = request.form.get("t_duration")
            t_description = request.form.get("t_description")
            task = Tasks.query.get(t_id)
            if task:
                if t_apiCaseId == "False":
                    api = ApiCases.query.all()
                    t_apiCaseId = api[0].id
                if t_sampleCaseId == "False":
                    sample = SampleCases.query.all()
                    t_sampleCaseId = sample[0].id
                task.t_caseType = t_caseType
                task.t_hostId = t_hostId
                task.t_apiCaseId = t_apiCaseId
                task.t_sampleCaseId = t_sampleCaseId
                task.t_duration = t_duration
                task.t_description = t_description
                task.t_status = "New"

            db.session.add(task)
            db.session.commit()

            return {"status": "202", "msg": "ok", "data": task}
        else:
            id = request.form.get("r_id")
            hostid = request.form.get("hostid")
            apiCaseId = request.form.get("apiCaseId")
            sampleCaseId = request.form.get("sampleCaseId")

            task = Tasks.query.get(id)

            duration = task.t_duration

            host = Hosts.query.get(hostid)
            hostIp = host.h_ip
            hostOs = host.h_os
            hostUserName = host.h_username
            hostPassWord = host.h_password

            if apiCaseId == "False":
                sample = SampleCases.query.get(sampleCaseId)
                sampleModelClsId = sample.s_modelClsId
                sampleModelDetId = sample.s_modelDetId
                sampleDataId = sample.s_dataId

                sampleType = sample.s_type
                sampleModelCls = Cnns.query.get(sampleModelClsId).c_path
                sampleModelDet = Cnns.query.get(sampleModelDetId).c_path
                sampleData = DataSets.query.get(sampleDataId).d_path

                # Run test case
                if hostOs.lower() == "linux":
                    pass
                elif hostOs.lower() == "windows":
                    pass

            else:
                api = ApiCases.query.get(apiCaseId)
                apiModelId = api.a_modelId
                apiDataId = api.a_dataId

                apiLevel = api.a_level
                apiType = api.a_type
                apiModel = Cnns.query.get(apiModelId).c_path
                apiData = DataSets.query.get(apiDataId).d_path

                # Run test case
                if hostOs.lower() == "linux":
                    pass
                elif hostOs.lower() == "windows":
                    pass

            task.t_status = "Running"
            db.session.add(task)
            db.session.commit()

            return {"msg": "The task running successfully"}

    @marshal_with(settings.single_fields(settings.task_fields))
    def delete(self):
        t_id = request.form.get("t_id")
        task = Tasks.query.get(t_id)
        if task:
            db.session.delete(task)
            db.session.commit()

        return {"status": "203", "msg": "ok", "data": task}