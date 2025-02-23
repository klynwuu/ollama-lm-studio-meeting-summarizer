#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re
import yaml
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

# Load environment variables
API_KEY = os.getenv("API_KEY")
LLM_SERVER_BASE_URL = os.getenv("LLM_SERVER_BASE_URL")
LLM_SERVER_ENDPOINT = os.getenv("LLM_SERVER_ENDPOINT")
LLM_MODEL = os.getenv("LLM_MODEL")
TEMPERATURE = os.getenv("TEMPERATURE")
TARGET_FOLDER = os.getenv("TARGET_FOLDER")
# Load prompts
with open("prompts/system_prompts.yaml", "r") as f:
    SYSTEM_PROMPT_MEETING_SUMMARIZER = yaml.safe_load(f)["system_prompt_meeting_summarizer"]

with open("prompts/user_prompts.yaml", "r") as f:
    USER_PROMPT = yaml.safe_load(f)["user_prompt_meeting_summarizer_v1"]

# print(TARGET_FOLDER)
# print(LLM_SERVER_BASE_URL)
# print(LLM_SERVER_ENDPOINT)
# print(LLM_MODEL)
# print(SYSTEM_PROMPT_MEETING_SUMMARIZER)
# print(USER_PROMPT)

# Load the latest file from the TARGET_FOLDER with allowed extensions
allowed_extensions = ('.txt', '.srt', '.md')
filtered_files = [f for f in os.listdir(TARGET_FOLDER) if f.lower().endswith(allowed_extensions)]

if not filtered_files:
    raise FileNotFoundError(f"No .txt, .srt, or .md files found in {TARGET_FOLDER}")

latest_file = max(filtered_files, key=lambda x: os.path.getmtime(os.path.join(TARGET_FOLDER, x)))
TARGET_FILENAME = os.path.splitext(latest_file)[0]  # Save filename for later use

# Read the content of the latest file
with open(os.path.join(TARGET_FOLDER, latest_file), "r") as f:
    transcript_content = f.read()

print(transcript_content)

print(f"{LLM_SERVER_BASE_URL}{LLM_SERVER_ENDPOINT}")

# Call the LLM server
client = OpenAI(base_url=f"{LLM_SERVER_BASE_URL}", api_key=API_KEY)

# Call the LLM server
response_completion = client.chat.completions.create(
    model=LLM_MODEL,
    temperature=TEMPERATURE,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT_MEETING_SUMMARIZER},
        {"role": "user", "content": USER_PROMPT + transcript_content}
    ]
)

# # save it as a raw json file in project folter for local debugging
# with open("response_completion.json", "w") as f:
#     json.dump(response_completion.model_dump(), f)

# print(response_completion.choices[0].message.content)
response_completion_message_content = response_completion.choices[0].message.content

# Format and save the response to a file with the same name as the latest file as a markdown file
with open(os.path.join(TARGET_FOLDER, f"{TARGET_FILENAME}_summary.md"), "w") as f:
    content_think_tag_removed = re.sub(r'<think>.*?</think>', '', response_completion_message_content, flags=re.DOTALL)
    f.write(content_think_tag_removed)
    f.write(f"\n Summary generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Now generate log file
with open(os.path.join(TARGET_FOLDER, f"{TARGET_FILENAME}.log"), "w") as f:
    f.write(f"# {TARGET_FILENAME} meeting summary processed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"by {LLM_MODEL} with temperature {TEMPERATURE}\n")
    f.write(f"with user prompt: \n {USER_PROMPT}\n")
    f.write(f"Answer:\n")
    f.write(response_completion_message_content)