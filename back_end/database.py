from pymongo import MongoClient
import random
#lock
from threading import Lock
lock = Lock()
random.seed = 42

client = MongoClient('mongodb://localhost:27017/')
db = client['history']  # 你的数据库名称
collection = db['history']  # 你的集合名称，相当于关系数据库中的表
# 获取所有_id
ids = [doc["_id"] for doc in collection.find({}, {"_id": 1})]
# 随机初始化_id列表
random.shuffle(ids)


def update_database(_id, role, result, name='匿名'):
    # 设置要更新的路径
    document = collection.find_one({"_id": _id})
    ai_path = "{}.ai.{}".format(role, document[role]["idx"])
    idx_path = "{}.idx".format(role)

    # 执行更新操作
    collection.update_one(
        {'_id': _id},
        {
            '$set': {ai_path: result},
            '$inc': {idx_path: 1}
        },
        upsert=True
    )
    with lock:
        with open('contributor.txt', 'w') as file:
            file.write(name+' '+result+' '+_id)


def get_document(index):
    # if fatal and idx is not in collection, add it
    document = collection.find_one({"_id": ids[index % len(ids)]})
    for role in document:
        if role != "_id":
            # 检查是否有 'idx' 和 'fatal' 键
            if "idx" not in document[role]:
                # 如果没有，添加并设置值为0
                collection.update_one({"_id": document["_id"]}, {"$set": {f"{role}.idx": 0}})
            if "fatal" not in document[role]:
                collection.update_one({"_id": document["_id"]}, {"$set": {f"{role}.fatal": 0}})
    return collection.find_one({"_id": ids[index % len(ids)]})


def fatal(_id, role):
    collection.update_one(
        {'_id': _id},
        {
            '$set': {"{}.fatal".format(role): 1}
        },
        upsert=True
    )