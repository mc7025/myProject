import json

from flask import Flask, render_template, request, jsonify
from flask_script import Manager
import threading

import sys
sys.path.append("/home/hddl/hddl-accuracy-test")
import os

import m_run as run
import globalvar


app = Flask(__name__)
#manager = Manager(app=app)


@app.route('/')
def ssd():
	return render_template("index.html")


@app.route('/data/', methods=["GET", "POST"])
def data():
	flag = False
	with open("/home/hddl/new_demo/data.txt") as f:
		comp = f.readlines()
	dict = {}
	for i in comp:
		a = i.split("\\")
		b = a[0].strip().split("\t")
		dict[str(eval(b[0]) - 1)] = b[1]

	if request.method == "GET":
		print("\n get \n")
		lists = globalvar.gl_topresult8
		list_dic = []
		if all(lists):
			for i in lists:
				list_dic.append(eval(i))
			for i in list_dic:
				top5 = i.get("top5")
				img = i.get("image").split("/")
				top5res = i.get("top5res")
				top5res = [eval(("%.2f" % (j * 100))) for j in top5res]
				top5title = []
				for t in top5:
					title = dict.get(str(t))
					top5title.append(title)
				i["top5_title"] = top5title
				i["image"] = "static/img/ILSVRC2012/" + img[-1]
				i["top5res"] = top5res
		throughput = ("%.2f" % globalvar.gl_fps )
		myx_power = ("%.2f" % (globalvar.gl_corepower * 8))
		main_power = ("%.2f" % globalvar.gl_mainpower)
		temp = ("%.2f" % globalvar.gl_temper)
		try:
			efficiency = ("%.2f" % (eval(throughput) / eval(myx_power)))
		except:
			efficiency = 0
		top1_accuracy = ("%.2f" % (globalvar.gl_top1_accuracy * 100))
		top5_accuracy = ("%.2f" % (globalvar.gl_top5_accuracy * 100))
		return jsonify({"data": list_dic, "throughput": throughput, "myx_power": myx_power, "main_power": main_power,
						"efficiency": efficiency, "temp": temp, "top1_accuracy": top1_accuracy, "top5_accuracy": top5_accuracy})
	elif request.method == "POST":
		playFlag = request.form.get("playFlag")
		stopFlag = request.form.get("stopFlag")
		pf = request.form.get("pf")
		network = request.form.get("network")
		if playFlag == "1":
			flag = True
			platform = pf
			network = network
		if stopFlag == "1":
			flag = False
		if flag:
			star(network, platform)
		else:
			print("stop")
			run.stop()

		return jsonify({"msg": "ok"})


def star(network, platfrom):
	os.system("bash hddldaemon_start.sh &")
	os.chdir("/home/hddl/hddl-accuracy-test")
	run.begain(network, platfrom)


if __name__ == '__main__':
	app.run()
