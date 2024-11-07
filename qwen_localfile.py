# Author: Luying Zhang
# Date: 11/06/2024
# Description: This is a script to call Qwen model and upload images through local path.


import dashscope
from dashscope import MultiModalConversation

dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'


def call_with_local_file():
    local_file_path1 = "D:\\UPenn\\24Fall\\VLM\\VLMsForInjuryAssessment\\images\\injured_man.jpg"
    # local_file_path2 = 'file://The_local_absolute_file_path2'
    messages = [{
        'role': 'system',
        'content': [{
            'text': 'You are a helpful assistant.'
        }]
    }, {
        'role':
        'user',
        'content': [
            {
                'image': local_file_path1
            },
            {
                'text': 'What is happening in this image?'
            },
        ]
    }]
    response = MultiModalConversation.call(model='qwen-vl-plus', messages=messages)
    print(response)


if __name__ == '__main__':
    call_with_local_file()