from openai import OpenAI


import os
import datetime
now = datetime.datetime.now()

# client = OpenAI(
#   organization='org-KPWFHjEckT9okVDzImb9chSm',
# )


client = OpenAI(
     api_key=os.getenv("OPENAI_API_KEY")
)

gpt4_model_name="gpt-4o"
gpt3_model_name="gpt-3.5-turbo-0125"
# Specify the path to the text file
date_string = now.strftime("%Y-%m-%d")
download_dir = os.path.join('downloads', date_string)
summaries_dir = os.path.join("summaries", date_string)

today_summary = []

import os

def run_for_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the contents of the file into memory
            contents = file.read()

        # Print the contents of the file
        print("File contents:")
        messages=[{"role": "system", "content": "You are parsing website data. Your goal is to summarize the contents of the article, while ignoring all extranious text that rode along with the webscrape."},
                {  
                "role": "user", "content": contents
                }]
        chat_completion = client.chat.completions.create(
        model=gpt4_model_name,
        messages=messages
    )
        os.makedirs(summaries_dir, exist_ok=True)
        with open(os.path.join(summaries_dir, file_path.split('/')[-1]), 'w', encoding='utf-8') as file:
            file.write(chat_completion.choices[0].message.content)
                  
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(e)
        # print(contents)
    # except FileNotFoundError:
    #     print(f"File not found: {file_path}")
    # except IOError:
    #     print(f"An error occurred while reading the file: {file_path}")


def iterate_files(download_dir):
    print(download_dir)
    for root, dirs, files in os.walk(download_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print(file_path)
            today_summary.append(run_for_file(file_path))


import os

def read_all_text_files(directory):
    os.makedirs(directory, exist_ok=True)
    # This list will store the contents of all text files.
    file_contents = []
    
    # os.listdir() returns a list of all files and directories in the specified path.
    for filename in os.listdir(directory):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        
        # Check if it is a file and has a .txt extension
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            # Open the file and read its content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                file_contents.append(content)
                
    return file_contents

# Example usage
# Replace '/path/to/your/directory' with the actual directory path


def summarize_pages_from_today():
    iterate_files(download_dir)
    today_summary = read_all_text_files(summaries_dir)

    messages=[{"role": "system", "content": "You're a Commercial Real Estate newsletter writer. I'm giving you the summary news of the day. Only deliver explicit learning and news points. Don't summarize anything else. Bullets where possible."},
        {"role": "user", "content":'\n'.join(today_summary)}]
    raw_summary = client.chat.completions.create(
        model=gpt4_model_name,
        messages=messages
    )

    formatted_summary_instructions = messages=[{"role": "system", "content": "You are an html email marketing bot. I am giing you raw text content. Please return this concent in email html format."},
        {"role": "user", "content":raw_summary.choices[0].message.content.replace("```html", "")}]

    formatted_summary = client.chat.completions.create(
        model=gpt4_model_name,
        messages=formatted_summary_instructions
    )
# 
    return formatted_summary.choices[0].message.content