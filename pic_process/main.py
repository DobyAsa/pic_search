import json

import image_process as ip

from flask import Flask, request, jsonify
from pymilvus import MilvusClient
    
client = MilvusClient(
    uri="http://localhost:19530"
)

# 创建应用实例
app = Flask(__name__)

# 接受用户上传的图片
@app.route('/upload', methods=['POST'])
def upload():
    # 获取上传的图片
    images = request.files.getlist("images")
    # 获取图片特征
    for image in images:
        image_id = ip.get_image_id()
        # 将图片保存到images目录
        save_path = f"images/{image_id}.jpg"
        image.save(save_path)
        feature = ip.get_image_features(save_path)
        # 将图片特征插入到Milvus中
        client.insert(
            collection_name="pic_search",
            data=[{
                "feature": feature,
                "image_name": image.filename,
                "image_path": image_id
                }])
    return "Upload success"

# 搜索相似图片
@app.route('/search', methods=['POST'])
def search():
    # 获取上传的图片
    image = request.files['image']
    # 获取图片特征
    feature= ip.get_image_features(image)
    # 在Milvus中搜索相似图片
    res = client.search(
        collection_name="pic_search",
        data=[feature],
        top_k=3,
        output_fields=["image_name", "image_path"]
    )

    res[0][0]
    # 返回搜索结果
    return jsonify(res[0])

# 启动服务
if __name__ == '__main__':
   app.run(port=12345)
