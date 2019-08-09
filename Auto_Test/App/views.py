from flask import Blueprint, render_template

blue = Blueprint("blue", __name__)


def init_blue(app):
    app.register_blueprint(blueprint=blue)


@blue.route('/')
def home():
    return render_template("base/base.html")


# CNN route
@blue.route('/createmodel/')
def create_model():
    return render_template("cnn/CreateCnn.html")


@blue.route('/cnns/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cnns():
    return render_template("cnn/Cnns.html")


@blue.route('/modmodel/<int:id>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mod_model(id):
    return render_template("cnn/ModifyCnn.html", c_id=id)


# Data Set route
@blue.route('/dataset/')
def data_set():
    return render_template('data_set/DataSet.html', methods=['GET', 'POST', 'PUT', 'DELETE'])


@blue.route('/createdata/')
def create_data():
    return render_template('data_set/CreateDataSet.html')


@blue.route('/moddataset/<int:id>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mod_data_set(id):
    return render_template('data_set/ModifyDataSet.html', d_id=id)


# Host route
@blue.route('/hosts/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hosts():
    return render_template('host/Hosts.html')


@blue.route('/createhost/')
def create_host():
    return render_template('host/CreateHost.html')


@blue.route('/modhost/<int:id>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mod_host(id):
    return render_template("host/ModifyHost.html", h_id=id)


@blue.route('/apicases/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_cases():
    return render_template('api_cases/ApiCases.html')


@blue.route('/createapi/')
def create_api():
    return render_template('api_cases/CreateApi.html')


@blue.route('/modapi/<int:id>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mod_api(id):
    return render_template("api_cases/ModifyApi.html", a_id=id)


@blue.route('/samplecases/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def sample_cases():
    return render_template('sample_cases/SampleCases.html')


@blue.route('/createsample/')
def create_sample():
    return render_template('sample_cases/CreateSample.html')


@blue.route('/modsample/<int:id>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mod_sample(id):
    return render_template("sample_cases/ModifySample.html", s_id=id)


@blue.route('/tasks/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tasks():
    return render_template('task/Tasks.html')


@blue.route('/createtask/')
def create_task():
    return render_template('task/CreateTask.html')


@blue.route('/modtask/<int:id>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mod_task(id):
    return render_template("task/ModifyTask.html", t_id=id)


@blue.route('/results/')
def results():
    return render_template('result/Results.html')


@blue.route('/result/<int:id>/')
def result(id):
    return render_template('result/Result.html', r_id=id)




