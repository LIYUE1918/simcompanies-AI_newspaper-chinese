import os
import re
from datetime import datetime

def extract_datetime_from_filename(filename):
    match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\.\d{3}Z', filename)
    if match:
        return datetime.strptime(match.group(), '%Y-%m-%dT%H-%M-%S.%fZ')
    return None

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def sanitize_content(content):
    # Replace company names with a placeholder if needed (customize this as needed)
    content = re.sub(r'@\w+-corp\.|\b(某公司|另一家公司)\b', '[公司名称]', content)
    return content

def process_lines(lines):
    processed_lines = []
    current_company = None

    for line in lines:
        if line.startswith("Company:"):
            current_company = line.replace("Company:", "").strip()
        elif line.startswith("Body:"):
            body = line.replace("Body:", "").strip()
            if current_company:
                processed_lines.append(f"Company: {current_company}\nBody: {body}")
            else:
                processed_lines.append(f"Company: [未知公司]\nBody: {body}")
    
    return processed_lines

def merge_files(input_folder, output_folder):
    files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    files.sort(key=extract_datetime_from_filename)

    current_time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    output_file = os.path.join(output_folder, f'sim聊天_{current_time}.txt')

    seen_lines = set()
    with open(output_file, 'w', encoding='utf-8') as outfile:
        previous_content = ""
        for filename in files:
            filepath = os.path.join(input_folder, filename)
            file_content = read_file(filepath)
            file_content = sanitize_content(file_content)  # Sanitize the content
            lines = file_content.split('\n')
            processed_lines = process_lines(lines)
            new_content = []

            for line in processed_lines:
                if line not in seen_lines:
                    new_content.append(line)
                    seen_lines.add(line)

            if new_content:
                if previous_content:
                    # Check if there is an overlap between previous content and new content
                    overlap = False
                    for line in previous_content.split('\n'):
                        if line in new_content:
                            overlap = True
                            break
                    # Optionally write a separator if there's no overlap
                    # if not overlap:
                    #     outfile.write("###断片###\n\n")
                previous_content = '\n'.join(new_content)

                outfile.write(f"=== {filename} ===\n")
                outfile.write('\n'.join(new_content))
                outfile.write("\n")

    print(f"All files have been merged into {output_file}")

def ensure_directory_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created directory: {folder_path}")

def main():
    current_dir = os.path.dirname(__file__)
    input_folder = os.path.join(current_dir, 'GL')
    output_folder = os.path.join(current_dir, 'output')

    ensure_directory_exists(input_folder)
    ensure_directory_exists(output_folder)

    merge_files(input_folder, output_folder)

if __name__ == '__main__':
    main()
