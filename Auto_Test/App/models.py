from App.ext import db


class Cnns(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(32))
    c_type = db.Column(db.String(16))
    c_format = db.Column(db.String(16))
    c_path = db.Column(db.String(64))
    c_isPublic = db.Column(db.Boolean, default=True)


class DataSets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    d_name = db.Column(db.String(32))
    d_type = db.Column(db.String(16))
    d_size = db.Column(db.String(16))
    d_path = db.Column(db.String(64))


class Hosts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    h_ip = db.Column(db.String(16))
    h_os = db.Column(db.String(64))
    h_username = db.Column(db.String(16))
    h_password = db.Column(db.String(16))


class ApiCases(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_description = db.Column(db.String(64))
    a_level = db.Column(db.String(16))
    a_type = db.Column(db.String(32))
    a_modelId = db.Column(db.Integer, db.ForeignKey(Cnns.id))
    a_dataId = db.Column(db.Integer, db.ForeignKey(DataSets.id))


class SampleCases(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_description = db.Column(db.String(64))
    s_type = db.Column(db.String(32))
    s_modelClsId = db.Column(db.Integer, db.ForeignKey(Cnns.id))
    s_modelDetId = db.Column(db.Integer, db.ForeignKey(Cnns.id))
    s_dataId = db.Column(db.Integer, db.ForeignKey(DataSets.id))


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_description = db.Column(db.String(64))
    t_caseType = db.Column(db.String(16))
    t_hostId = db.Column(db.Integer, db.ForeignKey(Hosts.id))
    t_apiCaseId = db.Column(db.Integer, db.ForeignKey(ApiCases.id))
    t_sampleCaseId = db.Column(db.Integer, db.ForeignKey(SampleCases.id))
    t_duration = db.Column(db.Integer, default=1)
    t_status = db.Column(db.String(16))


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    r_description = db.Column(db.String(64))
    r_taskId = db.Column(db.Integer, db.ForeignKey(Tasks.id))
    r_result = db.Column(db.Boolean, default=True)
    r_errorLog = db.Column(db.String(1024))
