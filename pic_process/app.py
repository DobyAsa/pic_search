import json
import os

import image_process as ip

from flask import Flask, request, jsonify
from pymilvus import MilvusClient

imagePath = "../images/"

client = MilvusClient(
    uri="http://localhost:19530"
)

# 创建应用实例
app = Flask(__name__)

# 接受用户上传的图片
@app.route('/process/<filename>', methods=['GET'])
def process(filename):
    feature = ip.get_image_features(imagePath+filename)
    client.insert(
        collection_name="pic_search",
        data=[{
            "feature": feature,
            "image_id": filename,
        }]
    )
    return "process success", 200

@app.route('/search/<filename>', methods=['GET'])
def search(filename):
    feature = ip.get_image_features(imagePath+filename)
    res = client.search(
        collection_name="pic_search",
        data=[feature],
        limit=10,
        output_fields=["image_id"]
    )
    return jsonify(res[0])

# 搜索相似图片
# @app.route('/search', methods=['POST'])
# def search():
#     # 获取上传的图片
#     image = request.files['image']
#     # 获取图片特征
#     feature= ip.get_image_features(image)
#     # 在Milvus中搜索相似图片
#     res = client.search(
#         collection_name="pic_search",
#         data=[feature],
#         top_k=3,
#         output_fields=["image_name", "image_path"]
#     )

#     res[0][0]
#     # 返回搜索结果
#     return jsonify(res[0])

# 启动服务
if __name__ == '__main__':
   app.run(host="127.0.0.1", port=12345)
