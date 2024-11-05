import os
from dotenv import load_dotenv
import anthropic
import openai
import base64
import json
import requests
import pandas as pd
import random
from http import HTTPStatus
from dashscope import Generation
load_dotenv()
Generation.api_key = "sk-c16fefb5dcb24e6e9f0c3ec21ae10beb"

def qwen_review(filepath, prompt):
    #TODO: Implement Qwen review
    #https://www.alibabacloud.com/help/en/model-studio/developer-reference/use-qwen-by-calling-api
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'Who are you'}]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # Specify the random seed. If you leave this parameter empty, the random seed is set to 1234 by default.
                               seed=random.randint(1, 10000),
                               # Set the output format to message.
                               result_format='message',
                               workspace='llm-3r47xiptxl7jdjam')
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        
qwen_review(r'images\\injured_man.jpg', r'This is a test prompt')