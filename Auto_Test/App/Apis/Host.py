import math

from flask import request
from flask_restful import Resource, marshal_with

from App import settings
from App.ext import db
from App.models import Hosts


class HostModels(Resource):
    @marshal_with(settings.all_fields(settings.host_fields))
    def get(self):
        host = Hosts()
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or 10)
        page_num = math.ceil(len(host.query.all()) / 10)
        hosts = host.query.paginate(page=page, per_page=per_page, error_out=False).items

        return {"status": "200", "msg": "ok", "data": hosts, "page_num": page_num}

    @marshal_with(settings.single_fields(settings.host_fields))
    def post(self):
        h_ip = request.form.get("h_ip")
        h_os = request.form.get("h_os")
        h_username = request.form.get("h_username")
        h_password = request.form.get("h_password")

        host = Hosts()
        host.h_ip = h_ip
        host.h_os = h_os
        host.h_username = h_username
        host.h_password = h_password

        db.session.add(host)
        db.session.commit()

        return {"status": "201", "msg": "ok", "data": host}

    @marshal_with(settings.single_fields(settings.host_fields))
    def put(self):
        h_ip = request.form.get("h_ip")
        h_os = request.form.get("h_os")
        h_username = request.form.get("h_username")
        h_password = request.form.get("h_password")
        h_id = request.form.get("h_id")

        host = Hosts.query.get(h_id)
        if host:
            host.h_ip = h_ip
            host.h_os = h_os
            host.h_username = h_username
            host.h_password = h_password

        db.session.add(host)
        db.session.commit()

        return {"status": "202", "msg": "ok", "data": host}

    @marshal_with(settings.single_fields(settings.host_fields))
    def delete(self):
        h_id = request.form.get("h_id")
        host = Hosts.query.get(h_id)
        if host:
            try:
                db.session.delete(host)
                db.session.commit()
                return {"status": "203", "msg": "ok", "data": host}
            except:
                return {"msg": "Can not delete this host."}


