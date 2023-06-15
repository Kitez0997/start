import os
import json

if __name__ == '__main__':
    # 获取文件夹路径下目录
    file_path = "D:/pyproject/InformationExtraction/data/劳资劳务纠纷"
    file_list = os.listdir(file_path)
    for file in file_list:
        count = 0
        new_path = os.path.join(file_path, file)
        #print(new_path)
        with open(new_path, 'r',encoding='utf - 8') as f:  # 以读模式打开原文件
            content = f.read()  # 读取文件内容
            data = json.loads(content)  # 将文件内容解析为Python对象
            label_list = []
            for item in data['answer']:
                item['label'] = item['type'].split("_", 1)[0]#取出answer中每个字段的type内容
                if len(item['type'].split("_", 1)) >= 2:
                    item['type'] = item['type'].split("_", 1)[1]
      
            new_content = json.dumps(data, ensure_ascii=False)  # 将Python对象转换为json字符串
            #print(new_content)
        with open(new_path, 'w', encoding='utf - 8') as f:  # 以写模式打开原文件
            f.write(new_content)  # 写入新内容
            #print(new_content)
