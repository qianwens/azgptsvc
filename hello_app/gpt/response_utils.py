from ._constants import DELIMITER, SYSTEM_PROMPT
from .template_utils import get_template
import openai
import json
from time import time

def get_completion_from_messages(messages, 
                                 model="gpt-35-turbo-16k", 
                                 temperature=0, max_tokens=8000):
    openai.api_base = "https://qianwenai.openai.azure.com/"
    openai.api_key = ""
    openai.api_type = "azure"
    openai.api_version = "2023-06-01-preview"
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
        engine="gpt-35-turbo-16k",      
    )
    return response.choices[0].message["content"]

def get_sub_prompts(user_prompt):
    messages =  [  
        {
            'role':'system', 
            'content': SYSTEM_PROMPT
        },    
        {
            'role':'user', 
            'content': f"{DELIMITER}{user_prompt}{DELIMITER}"
        },  
    ] 
    sub_prompts = get_completion_from_messages(messages)
    sub_prompts = json.loads(sub_prompts)
    return sub_prompts

def fill_in_templates(sub_prompt):
    action = sub_prompt['action']
    if action == "create resource":
      return get_template[action][sub_prompt['resource_type']]()
    elif action == "connect resources":
      return get_template[action](sub_prompt['source_resource_type'], sub_prompt['target_resource_type'])
    else:
       print("waiting for future release")
       return None

def get_payload(assistant_template, user_prompt):
    messages =  [  
        {
            'role':'system', 
            'content': assistant_template
        },    
        {
            'role':'user', 
            'content': f"{DELIMITER}{user_prompt}{DELIMITER}"
        },  
    ] 
    payload = get_completion_from_messages(messages)
    return payload

def process_prompt(prompt):
    print("Analyzing your prompt...")
    sub_prompts = get_sub_prompts(prompt)
    
    print(f"Finish analyzing your prompt.")
    print(sub_prompts)

    payloads = []
    
    # generate payload for each sub_prompt and call rest apis
    for i, sub_prompt in enumerate(sub_prompts):
        print(f"Waking your copilot for Action {i + 1}...")
        assistant_template = fill_in_templates(sub_prompt)
        
        print("Start generating payload...")
        payload = get_payload(assistant_template, sub_prompt['sub_prompt'])
        print("Sudcess. Operations will be done according to the payload below:")
        print(payload)
    return payloads
