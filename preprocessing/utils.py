import json
import os
from glob import glob
from pathlib import Path


def get_original_video_paths(root_dir, basename=False):#输入一个路径
    originals = set() #创建一个无序不重复元素集
    originals_v = set()
    for json_path in glob(os.path.join(root_dir, "*/metadata.json")): #在目录下找metadata文件
        dir = Path(json_path).parent #json文件的父路径
        with open(json_path, "r") as f:
            metadata = json.load(f)
        for k, v in metadata.items(): #返回可遍历的(键, 值) 元组数组 k：key v：value
            original = v.get("original", None) # get() 函数返回指定键的值 此处将值为original的找出来
            if v["label"] == "REAL":
                original = k #original是real文件的文件名？
                originals_v.add(original)
                originals.add(os.path.join(dir, original))
    originals = list(originals)
    originals_v = list(originals_v)
    print(len(originals))
    return originals_v if basename else originals #返回的是一个列表 basename为false的时候 返回originals


def get_original_with_fakes(root_dir):
    pairs = []
    for json_path in glob(os.path.join(root_dir, "*/metadata.json")):
        with open(json_path, "r") as f:
            metadata = json.load(f)
        for k, v in metadata.items():
            original = v.get("original", None)
            if v["label"] == "FAKE":
                pairs.append((original[:-4], k[:-4] ))

    return pairs


def get_originals_and_fakes(root_dir):
    originals = []
    fakes = []
    for json_path in glob(os.path.join(root_dir, "*/metadata.json")):
        with open(json_path, "r") as f:
            metadata = json.load(f)
        for k, v in metadata.items():
            if v["label"] == "FAKE":
                fakes.append(k[:-4])
            else:
                originals.append(k[:-4])

    return originals, fakes
