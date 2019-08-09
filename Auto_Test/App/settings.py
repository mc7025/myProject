from flask_restful import fields


def get_db_info(dbinfo):
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")
    db = dbinfo.get("DB")
    driver = dbinfo.get("DRIVER")

    return "{}+{}://{}:{}@{}:{}/{}".format(db, driver, user, password, host, port, name)


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "110"


class DevelopConfig(Config):
    DATABASE = {
        "USER": "root",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskTest4",
        "DB": "mysql",
        "DRIVER": "pymysql",
    }
    SQLALCHEMY_DATABASE_URI = get_db_info(DATABASE)


class IntelConfig(Config):
    DATABASE = {
        "USER": "root",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskDatabase",
        "DB": "mysql",
        "DRIVER": "pymysql",
    }
    SQLALCHEMY_DATABASE_URI = get_db_info(DATABASE)


envs = {
    "develop": DevelopConfig,
    "intel": IntelConfig,
}


def single_fields(dict):
    single_fields = {
        "status": fields.String,
        "msg": fields.String,
        "data": fields.Nested(dict)
    }

    return single_fields


def all_fields(dict):
    all_fields = {
        "status": fields.String,
        "msg": fields.String,
        "page_num": fields.Integer,
        "data": fields.List(fields.Nested(dict))
    }

    return all_fields


cnn_fields = {
    "id": fields.Integer,
    "c_name": fields.String,
    "c_type": fields.String,
    "c_format": fields.String,
    "c_path": fields.String,
    "c_isPublic": fields.Boolean,
}

data_set_fields = {
    "id": fields.Integer,
    "d_name": fields.String,
    "d_type": fields.String,
    "d_size": fields.String,
    "d_path": fields.String,
}

host_fields = {
    "id": fields.Integer,
    "h_ip": fields.String,
    "h_os": fields.String,
    "h_username": fields.String,
    "h_password": fields.String,
}

api_fields = {
    "id": fields.Integer,
    "a_level": fields.String,
    "a_type": fields.String,
    "a_modelId": fields.Integer,
    "a_dataId": fields.Integer,
    "a_description": fields.String,
}

api_get_fields = {
    "id": fields.Integer,
    "a_level": fields.String,
    "a_type": fields.String,
    "c_name": fields.String,
    "d_name": fields.String,
    "a_description": fields.String,
}

sample_fields = {
    "id": fields.Integer,
    "s_type": fields.String,
    "s_modelClsId": fields.Integer,
    "s_modelDetId": fields.Integer,
    "s_dataId": fields.Integer,
    "s_description": fields.String,
}

sample_get_fields = {
    "id": fields.Integer,
    "s_type": fields.String,
    "s_modelClsName": fields.String,
    "s_modelDetName": fields.String,
    "s_dataName": fields.String,
    "s_description": fields.String,
}

task_fields = {
    "id": fields.Integer,
    "t_caseType": fields.String,
    "t_hostId": fields.Integer,
    "t_apiCaseId": fields.Integer,
    "t_sampleCaseId": fields.Integer,
    "t_duration": fields.Integer,
    "t_status": fields.String,
}

task_get_fields = {
    "id": fields.Integer,
    "t_description": fields.String,
    "t_caseType": fields.String,
    "t_hostIp": fields.String,
    "t_hostId": fields.Integer,
    "t_apiCase": fields.String,
    "t_apiCaseId": fields.Integer,
    "t_sampleCase": fields.String,
    "t_sampleCaseId": fields.Integer,
    "t_duration": fields.Integer,
    "t_status": fields.String,
}

result_get_fields = {
    "id": fields.Integer,
    "r_taskName": fields.String,
    "r_result": fields.Boolean,
    "r_errorLog": fields.String,
}

result_fields = {
    "id": fields.Integer,
    "r_description": fields.String,
    "r_taskId": fields.Integer,
    "r_result": fields.Boolean,
    "r_errorLog": fields.String,
}
