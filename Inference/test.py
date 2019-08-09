import ast
from os import replace

items = [
    '{"value":532, "top5":[601,735,703,879,619], "top5res":[0.18909,0.14612,0.11206,0.095093,0.053375], "title":" dining table, board", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000241.JPEG"}',
    '{"value":764, "top5":[562,840,982,708,728], "top5res":[0.24658,0.095825,0.047455,0.025604,0.020905], "title":" rifle", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000244.JPEG"}',
    '{"value":678, "top5":[773,643,678,719,903], "top5res":[0.22876,0.10638,0.065552,0.053741,0.046844], "title":" neck brace", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000243.JPEG"}',
    '{"value":1, "top5":[4,3,5,2,149], "top5res":[0.66553,0.090088,0.045288,0.038757,0.023499], "title":" goldfish, Carassius auratus", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000236.JPEG"}',
    '{"value":121, "top5":[845,585,998,731,898], "top5res":[0.16553,0.089294,0.026505,0.026184,0.025009], "title":" king crab, Alaska crab, Alaskan king crab, Alaska king crab, Paralithodes camtschatica", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000238.JPEG"}',
    '{"value":445, "top5":[562,475,828,818,876], "top5res":[0.45312,0.027557,0.026825,0.025284,0.022491], "title":" bikini, two-piece", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000239.JPEG"}',
    '{"value":702, "top5":[422,702,602,543,416], "top5res":[0.35156,0.15845,0.1283,0.12537,0.072021], "title":" parallel bars, bars", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000240.JPEG"}',
    '{"value":167, "top5":[212,246,167,166,210], "top5res":[0.28638,0.22302,0.15454,0.1521,0.096008], "title":" English foxhound", "image":"/home/hddl/Pictures/ILSVRC2012_val_img/ILSVRC2012_val_00000237.JPEG"}'
]

a = [{'top5res': [0.18909, 0.14612, 0.11206, 0.095093, 0.053375], 'title': ' dining table, board', 'image': 'static/img/ILSVRC2012_val_00000241.JPEG', 'top5': [601, 735, 703, 879, 619], 'top5_title': ['hoopskirt, crinoline', 'poncho', 'park bench', 'umbrella', 'lampshade, lamp shade'], 'value': 532},
     {'top5res': [0.24658, 0.095825, 0.047455, 0.025604, 0.020905], 'title': ' rifle', 'image': 'static/img/ILSVRC2012_val_00000244.JPEG', 'top5': [562, 840, 982, 708, 728], 'top5_title': ['fountain', 'swab, swob, mop', 'groom, bridegroom', 'pedestal, plinth, footstall', 'plastic bag'], 'value': 764},
     {'top5res': [0.22876, 0.10638, 0.065552, 0.053741, 0.046844], 'title': ' neck brace', 'image': 'static/img/ILSVRC2012_val_00000243.JPEG', 'top5': [773, 643, 678, 719, 903], 'top5_title': ['saltshaker, salt shaker', 'mask', 'neck brace', 'piggy bank, penny bank', 'wig'], 'value': 678}, {'top5res': [0.66553, 0.090088, 0.045288, 0.038757, 0.023499], 'title': ' goldfish, Carassius auratus', 'image': 'static/img/ILSVRC2012_val_00000236.JPEG', 'top5': [4, 3, 5, 2, 149], 'top5_title': ['hammerhead, hammerhead shark', 'tiger shark, Galeocerdo cuvieri', 'electric ray, crampfish, numbfish, torpedo', 'great white shark, white shark, man-eater, man-eating shark, Carcharodon carcharias', 'dugong, Dugong dugon'], 'value': 1}, {'top5res': [0.16553, 0.089294, 0.026505, 0.026184, 0.025009], 'title': ' king crab, Alaska crab, Alaskan king crab, Alaska king crab, Paralithodes camtschatica', 'image': 'static/img/ILSVRC2012_val_00000238.JPEG', 'top5': [845, 585, 998, 731, 898], 'top5_title': ['syringe', 'hair spray', 'ear, spike, capitulum', "plunger, plumber's helper'", 'water bottle'], 'value': 121}, {'top5res': [0.45312, 0.027557, 0.026825, 0.025284, 0.022491], 'title': ' bikini, two-piece', 'image': 'static/img/ILSVRC2012_val_00000239.JPEG', 'top5': [562, 475, 828, 818, 876], 'top5_title': ['fountain', 'car mirror', 'strainer', 'spotlight, spot', 'tub, vat'], 'value': 445}, {'top5res': [0.35156, 0.15845, 0.1283, 0.12537, 0.072021], 'title': ' parallel bars, bars', 'image': 'static/img/ILSVRC2012_val_00000240.JPEG', 'top5': [422, 702, 602, 543, 416], 'top5_title': ['barbell', 'parallel bars, bars', 'horizontal bar, high bar', 'dumbbell', 'balance beam, beam'], 'value': 702}, {'top5res': [0.28638, 0.22302, 0.15454, 0.1521, 0.096008], 'title': ' English foxhound', 'image': 'static/img/ILSVRC2012_val_00000237.JPEG', 'top5': [212, 246, 167, 166, 210], 'top5_title': ['English setter', 'Great Dane', 'English foxhound', 'Walker hound, Walker foxhound', 'German short-haired pointer'], 'value': 167}]





with open("data.txt") as f:
    datas = f.readlines()

print(datas)
dict = {}

for i in datas:
    a = i.split("\\")
    b = a[0].strip().split("\t")
    dict[str(eval(b[0]) - 1)] = b[1]

print(dict)

data = []
top5s = []
for i in items:
    data.append(eval(i))
    # top5s.append(top5title)
# print(top5title)


for i in data:
    img = i.get("image").split("/")
    top5 = i.get("top5")
    top5res = i.get("top5res")
    top5res = [eval(("%.2f" % (i * 100))) for i in top5res]
    print(top5res)
    top5title = []
    for t in top5:
        title = dict.get(str(t))
        top5title.append(title)
    i["top5_title"] = top5title
    i["image"] = "static/img/" + img[-1]
    i["top5res"] = top5res
print(data)
