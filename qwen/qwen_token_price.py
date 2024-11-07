# Author: Luying Zhang
# Date: 11/06/2024
# Description: This is a script to call Qwen model and calculate the price based on tokens.
# Results: qwen-vl-max: $2.36, qwen-vl-plus: $0.44

# Refer to the document for workspace information: https://www.alibabacloud.com/help/en/model-studio/developer-reference/model-calling-in-sub-workspace    
import dashscope
from dashscope import MultiModalConversation
from create_dataset import label_class_human_value_list, dict_summary_sentences
import csv
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

def price(file, model):
    # open csv file
    tokens_input = 0
    tokens_output = 0
    
    # Open the file in read mode
    with open(file, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row:
                input_tokens = int(row[0])
                output_tokens = int(row[1])
                tokens_input += input_tokens
                tokens_output += output_tokens

    if model == 'qwen-vl-max':
        return (tokens_input * 0.02 + tokens_output * 0.06) * 59 / 1000 / 7.1  # 59 images in total
    elif model == 'qwen-vl-plus':
        return (tokens_input * 0.004 + tokens_output * 0.012) * 59 / 1000 / 7.1


def qwen_review_with_csv(image, prompts):
    """
    Simple single round multimodal conversation call.
    """
    
    # Write the tokens into a csv file
    with open('max_tokens.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["input_tokens", "output_tokens", "image_tokens"])
        for prompt in prompts:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"image": image},
                        {"text": prompt}
                    ]
                }
            ]
            responses = MultiModalConversation.call(model='qwen-vl-plus',
                                                messages=messages,
                                                stream=False)
            
            # print the last text response
            print(responses['output']['choices'][0]['message']['content'][0]['text'])

            input_tokens = responses["usage"]["input_tokens"]
            output_tokens = responses["usage"]["output_tokens"]
            image_tokens = responses["usage"]["image_tokens"] # 1230
            print("input_tokens: ", input_tokens, "output_tokens: ", output_tokens, "image_tokens: ", image_tokens)
    
            writer.writerow([input_tokens, output_tokens, image_tokens])

def qwen_review(image, prompts):
    """
    Simple single round multimodal conversation call.
    """
    num = 0

    for prompt in prompts:
        num += 1
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
            
        # print the last text response
        print(num)   
        print(responses['output']['choices'][0]['message']['content'][0]['text'])

# def get_prompts():
#     '''
#     Get prompts from create_dataset.py as a list of length 36.
#     '''
#     label_class = ["trauma_head", "trauma_torso", "trauma_lower_ext", "trauma_upper_ext", "alertness_ocular", "severe_hemorrhage"]
#     prompts = []
#     for label in label_class:
#         prompts.extend(label_class_human_value_list[label])
#     for label in label_class:
#         prompts.append(dict_summary_sentences[label])
#     # print(len(prompts)) # 36
#     return prompts

def get_prompts():
    '''
    Get prompts from create_dataset.py as a list of length 8.
    '''
    label_class = ["scene", "trauma_head", "trauma_torso", "trauma_lower_ext", "trauma_upper_ext", "alertness_ocular", "severe_hemorrhage"]
    prompts = []
    for label in label_class:
        prompt = label_class_human_value_list[label]
        prompts.append(" ".join(prompt))
    temp = list(dict_summary_sentences.values())
    prompts.append(" ".join(temp))
    return prompts

if __name__ == '__main__':
    image = "https://github.com/luyingz06/VLMsForInjuryAssessment/blob/main/images/1726253101436713875.png?raw=true"
    prompts = get_prompts()
    qwen_review(image, prompts)
    # print(price('D:\\UPenn\\24Fall\\VLM\\VLMsForInjuryAssessment\\qwen\\max_tokens.csv', 'qwen-vl-max'))