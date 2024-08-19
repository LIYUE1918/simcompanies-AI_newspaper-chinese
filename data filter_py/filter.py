import os
import json
import html
from bs4 import BeautifulSoup

def decode_unicode(text):
    return html.unescape(text)

def process_data(data):
    processed_data = []
    for entry in data:
        company = entry['sender']['company']
        if "mod" in company.lower():
            company += " MOD"
        
        body = decode_unicode(entry['body'])
        
        processed_data.append({
            'company': company,
            'body': body
        })
    
    return processed_data

def process_file(input_path, output_path):
    # 读取TXT文件
    with open(input_path, 'r', encoding='utf-8') as file:
        txt_data = file.read()

    # 解析HTML内容
    soup = BeautifulSoup(txt_data, 'html.parser')

    # 提取<pre>标签内容
    pre_tags = soup.find_all('pre')
    if not pre_tags:
        print("Error: <pre> tags not found in the TXT file.")
        return
    
    for pre_tag in pre_tags:
        json_data = pre_tag.get_text(strip=True)
        
        # 打印提取的 JSON 数据以进行调试
        print(f"Extracted JSON Data:\n{json_data[:500]}")  # 打印前500个字符以检查
        
        # 解析JSON数据
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            continue
        
        # 处理数据
        result = process_data(data)
        
        # 将数据写入TXT文件
        with open(output_path, 'w', encoding='utf-8') as file:
            for item in result:
                file.write(f"Company: {item['company']}\n")
                file.write(f"Body: {item['body']}\n")
                file.write("\n")
        
        print(f"Processed {input_path} -> {output_path}")
        break  # 只处理第一个找到的<pre>标签，若有多个请移除此行
def main():
    input_folder = '/'#加上自己的文件地址
    output_folder = '/'#加上自己的文件地址

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_filename = filename.replace('.txt', '_归类.txt')
            output_path = os.path.join(output_folder, output_filename)

            # 处理文件
            process_file(input_path, output_path)

if __name__ == '__main__':
    main()
