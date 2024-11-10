# Author: Luying Zhang
# Date: 11/06/2024
# Description: This is a script to call Qwen model and generate labels for each image.

# Refer to the document for workspace information: https://www.alibabacloud.com/help/en/model-studio/developer-reference/model-calling-in-sub-workspace    
import dashscope
from dashscope import MultiModalConversation
from create_dataset import label_class_human_value_list, dict_summary_sentences
import json
import os
from image import image

dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

def qwen_review(image, prompts):
    """
    Call Qwen model for each prompt and return the structured conversation output.
    """
    conversation = {}

    # Iterate through prompts, calling the model for each, and storing in the conversation structure
    for i, prompt in enumerate(prompts):
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": image},
                    {"text": prompt}
                ]
            }
        ]
        responses = MultiModalConversation.call(model='qwen-vl-max',
                                                messages=messages,
                                                stream=False)
        # Parse response text for each label category
        response_text = responses['output']['choices'][0]['message']['content'][0]['text']
        print("-----------------------------------")
        print(prompt)
        print(response_text)
        print("-----------------------------------")
        # Map each prompt response to the correct conversation field based on order
        if i == 0:
            conversation["scene"] = [response_text]
        if i == 1:
            conversation["trauma_head"] = [response_text]
        elif i == 2:
            conversation["trauma_torso"] = [response_text]
        elif i == 3:
            conversation["trauma_lower_ext"] = [response_text]
        elif i == 4:
            conversation["trauma_upper_ext"] = [response_text]
        elif i == 5:
            conversation["alertness_ocular"] = [response_text]
        elif i == 6:
            conversation["severe_hemorrhage"] = [response_text]
        elif i == 7:
            conversation["value-dict"] = response_text

    return conversation

def get_prompts():
    '''
    Get prompts from create_dataset.py as a list of length 8.
    '''
    label_class = ["scene", "trauma_head", "trauma_torso", "trauma_lower_ext", "trauma_upper_ext", "alertness_ocular", "severe_hemorrhage"]
    prompts = []
    for label in label_class:
        prompt = label_class_human_value_list[label]
        if len(prompt) > 1:
            prompts.append(prompt[1])
        else:
            prompts.append(prompt[0])
    temp = list(dict_summary_sentences.values())
    temp = [" ".join(temp)]
    prompts.extend(temp)
    return prompts

def generate_label(image, json_path='D:\\UPenn\\24Fall\\VLM\\VLMsForInjuryAssessment\\qwen\\dataset_qwen.json'):
    """
    Run model for each prompt on a single image and append structured JSON output.
    """
    prompts = get_prompts()
    conversation = qwen_review(image, prompts)
    
    # Extract ID from image URL
    image_id = image.split("/")[-1].split(".")[0]
    image_path = '/'.join(image.split("/")[-3:])
    
    # Structure JSON output
    output = {
        
        "id": image_id,
        "image": image_path,
        "conversations": [
            {
                "from": "human",
                "value": "LEAVE BLANK"
            },
            {
                "from": "gpt",
                **conversation
            }
        ]
    }
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        data = []
    
    data.append(output)
    
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    num = 0
    for img in image:
        num += 1
        print(num)
        generate_label(img)