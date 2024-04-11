import sys
import time
import os
import requests

# 指定要上传的文件夹路径
upload_dir = sys.argv[1]

# Flask服务器的上传接口URL
upload_url = 'http://127.0.0.1:12345/upload'

# 遍历文件夹内的所有文件
for filename in os.listdir(upload_dir):
    file_path = os.path.join(upload_dir, filename)
    
    # 跳过文件夹,只上传文件
    if os.path.isfile(file_path):
        # 打开文件并上传
        with open(file_path, 'rb') as file:
            files = {'images': file}
            response = requests.post(upload_url, files=files)
        time.sleep(0.2)
        # 检查上传是否成功
        if response.status_code == 200:
            print(f"{filename} uploaded successfully")
        else:
            print(f"Failed to upload {filename}")
