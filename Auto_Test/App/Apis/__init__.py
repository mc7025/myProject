from flask_restful import Api

from App.Apis.ApiCase import ApiCaseModels
from App.Apis.Cnn import CnnModels
from App.Apis.DataSet import DataModels
from App.Apis.Host import HostModels
from App.Apis.Result import ResultModels
from App.Apis.SampleCase import SampleCaseModels
from App.Apis.Task import TaskModels

api = Api()


def init_api(app):
    api.init_app(app=app)


api.add_resource(CnnModels, '/CnnModels/')
api.add_resource(DataModels, '/DataModels/')
api.add_resource(HostModels, '/HostModels/')
api.add_resource(ApiCaseModels, '/ApiCaseModels/')
api.add_resource(SampleCaseModels, '/SampleCaseModels/')
api.add_resource(TaskModels, '/TaskModels/')
api.add_resource(ResultModels, '/ResultModels/')