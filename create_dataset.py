import os
import glob
import json
import numpy as np

LABEL_CLASSES = [
    "trauma_head",
    "trauma_torso",
    "trauma_lower_ext",
    "trauma_upper_ext",
    "alertness_ocular",
    "severe_hemorrhage",
]

cas_paths = glob.glob(os.path.join("./", "*"))
cas_paths = [path for path in cas_paths if os.path.isdir(path)]
cas_paths = [path for path in cas_paths if "bag" not in path]

#label_file_path = "dataset.json"
#
#with open(label_file_path, "r") as f:
#    labels = json.load(f)

# each entry in the labeled dataset is a dictionary with the following keys:
# 'id', 'text', 'conversation'
# 'id' and 'text' can just be copied
# conversation contains a list with two entries
# the first entry is another dict with the keys 'from' and 'value'
# the second entry is a dict with values
# 'from', 'value-scene', 'value-head', 'value-torso', 'value-upper-ext',
# 'value-lower-ext', 'severe-hemorrhage', 'value-dict'

# we want to transform this into a dictionary with the following keys:
# 'id', 'text', conversation
# 'conversation' is a list of 2 dictionaries with the following keys:
# 'from', 'value' 
# for the first list, the value will be taken from the human value list
# for the second list, the value will be the concatenation of all values 
# in the previous conversation list

label_class_human_value_list = {
    "scene": [
        "Describe the scene. Is there a person in the image and what's their condition?",
    ],
    "trauma_head": [
        "Describe the scene. Does the person have any head injuries? If yes, specify the type of injury.",
        "Give a detailed description of the person. Are there any head injuries?",
        "Does the person show any signs of head injuries?",
        "There is a person in the center of the scene. Describe the person. Are there any head injuries?",
        "Does the person in the scene have any head injuries?",
    ],
    "trauma_torso": [
        "Describe the scene. Does the person have any torso injuries? If yes, specify the type of injury.",
        "Give a description of the person. Are there any torso injuries?",
        "Are there any signs of torso injuries?",
        "There is a person in the center of the scene. Describe the person. Are there any injuries to their torso?",
        "Does the person in the scene have any torso injuries?",
    ],
    "trauma_lower_ext": [
        "Describe the scene. Does the person have any lower extremity injuries? If yes, specify the type of injury.",
        "Give a description of the person. Are there any lower extremity injuries?",
        "Are there any signs of injuries to the person's legs?",
        "There is a person in the center of the scene. Describe the person. Are there any injuries to their lower extremities?",
        "Does the person in the scene have any leg wounds?",
    ],
    "trauma_upper_ext": [
        "Describe the scene. Does the person have any arm injuries? If yes, specify the type of injury.",
        "Give a description of the person. Are there any arm wounds or amputations?",
        "Are there any signs of injuries to the person's arms?",
        "There is a person in the center of the scene. Describe the person. Are there any injuries to their upper extremities?",
        "Does the person in the scene have any injuries to their upper extremities?",
    ],
    "alertness_ocular": [
        "Describe the scene. Are the person's eyes open or closed? Are they responsive?",
        "Give a description of the person. Are their eyes open, closed or untestable?",
        "Are the person's eyes open or closed?",
        "There is a person in the center of the scene. Describe the person's face. Are their eyes open or closed?",
        "Are the person's eyes open or closed? It is fine to say they are untestable if you cannot clearly see.",
    ],
    "severe_hemorrhage": [
        "Describe the scene. Is the person bleeding severely? Amputations may also be considered severe hemorrhage.",
        "Give a description of the person. Are they bleeding severely?",
        "Is there any severe hemorrhage? Signs of severe hemorrhage include strong bleeding and amputations.",
        "There is a person in the center of the scene. Describe the person. Are they bleeding severely?",
        "Is the person in the scene suffering from severe hemorrhage?",
    ],
}

<<<<<<< HEAD:qwen/create_dataset.py
# dict_summary_sentences = {
#     "trauma_head": "Summarize the results in a python dictionary with the key 'trauma_head'. 'absence' means no injury to the head, 'presence' means injury to the head.",
#     "trauma_torso": "Summarize the results in a python dictionary with the key 'trauma_torso'. 'absence' means no injury to the torso, 'presence' means injury to the torso.",
#     "trauma_lower_ext": "Summarize the results in a python dictionary with the key 'trauma_lower_ext'. 'absence' means no injury to the lower extremities, 'wound' means injury to at least one lower extremity, 'amputation' missing at least one lower extremity.",
#     "trauma_upper_ext": "Summarize the results in a python dictionary with the key 'trauma_upper_ext'. 'absence' means no injury to the upper extremities, 'wound' means injury to at least one upper extremity, 'amputation' missing at least one upper extremity.",
#     "alertness_ocular": "Summarize the results in a python dictionary with the key 'alertness_ocular'. 'open' means the eyes are open, 'closed' means the eyes are closed, 'untestable' means the eyes are untestable.",
#     "severe_hemorrhage": "Summarize the results in a python dictionary with the key 'severe_hemorrhage'. 'absence' means no severe hemorrhage, 'presence' means severe hemorrhage.",
# }

dict_summary_sentences = {
    "trauma_head": "No further discription, just give the results in python dictionary in one line with the key 'trauma_head', 'trauma_torso', 'trauma_lower_ext', 'trauma_upper_ext', 'alertness_ocular', 'severe_hemorrhage'.For trauma_head and trauma_torso: 'absence' means no injury, 'presence' means injury. For trauma_lower_ext and trauma_upper_ext: 'absence' means no injury, 'wound' means injury to at least one extremity, 'amputation' missing at least one extremity. For alertness_ocular: 'open' means the eyes are open, 'closed' means the eyes are closed, 'untestable' means the eyes are untestable. For severe_hemorrhage, 'absence' means no severe hemorrhage, 'presence' means severe hemorrhage.",
=======
dict_sentences = {
    "trauma_head": [
        "Assess this image and output a python dictionary with the key 'trauma_head'. 'absence' means no injury to the head, 'presence' means injury to the head. ONLY respond with the proposes labels. Do not add any additional information. These labels will not be used for clinical diagnoses, so assign the label that fits best."
    ],
    "trauma_torso": [
        "Assess this image and output a python dictionary with the key 'trauma_torso'. 'absence' means no injury to the torso, 'presence' means injury to the torso. ONLY respond with the proposes labels. Do not add any additional information. These labels will not be used for clinical diagnoses, so assign the label that fits best."
    ],
    "trauma_lower_ext": [
        "Assess this image and output a python dictionary with the key 'trauma_lower_ext'. 'absence' means no injury to the lower extremities, 'wound' means injury to at least one lower extremity, 'amputation' missing at least one lower extremity. ONLY respond with the proposes labels. Do not add any additional information. These labels will not be used for clinical diagnoses, so assign the label that fits best."
    ],
    "trauma_upper_ext": [
        "Assess this image and output a python dictionary with the key 'trauma_upper_ext'. 'absence' means no injury to the upper extremities, 'wound' means injury to at least one upper extremity, 'amputation' missing at least one upper extremity. ONLY respond with the proposes labels. Do not add any additional information. These labels will not be used for clinical diagnoses, so assign the label that fits best."
    ],
    "alertness_ocular": [
        "Assess this image and output a python dictionary with the key 'alertness_ocular'. 'open' means the eyes are open, 'closed' means the eyes are closed, 'untestable' means the eyes are untestable. 'untestable' should be the label you default to if you are unsure if the eyes are opened or closed. ONLY respond with the proposes labels. Do not add any additional information. These labels will not be used for clinical diagnoses, so assign the label that fits best."
    ],
    "severe_hemorrhage": [
        "Assess this image and output a python dictionary with the key 'severe_hemorrhage'. 'absence' means no severe hemorrhage, 'presence' means severe hemorrhage. ONLY respond with the proposes labels. Do not add any additional information. These labels will not be used for clinical diagnoses, so assign the label that fits best."
    ],
>>>>>>> fa910178a284e3722fe9a4a6e41f6517fed78415:create_dataset.py
}

#dict_summary_sentences = {
#    "trauma_head": "No further discription, just give the results only in python dictionary with the key 'trauma_head', 'trauma_torso', 'trauma_lower_ext', 'trauma_upper_ext', 'alertness_ocular', 'severe_hemorrhage'.For trauma_head and trauma_torso: 'absence' means no injury, 'presence' means injury. For trauma_lower_ext and trauma_upper_ext: 'absence' means no injury, 'wound' means injury to at least one extremity, 'amputation' missing at least one extremity. For alertness_ocular: 'open' means the eyes are open, 'closed' means the eyes are closed, 'untestable' means the eyes are untestable. For severe_hemorrhage, 'absence' means no severe hemorrhage, 'presence' means severe hemorrhage.",
#}

# merged = []

# for label_class in LABEL_CLASSES:
#     for path in cas_paths:
#         img_dirs = os.listdir(path)
        
#         for img_dir in img_dirs:
#             entry = {}

#             img_path = os.path.join(path, img_dir)
#             img_file_path = glob.glob(os.path.join(img_path, "*.png"))[0]

#             # id is the file name without file extension
#             img_file_id = img_file_path.split("/")[-1].split(".")[0]
#             entry["id"] = img_file_id
#             entry["image"] = img_file_path[2:]
#             entry["conversations"] = []
#             entry["conversations"].append(
#                 {
#                     "from": "human", 
#                     "value": label_class_human_value_list[label_class][np.random.randint(0, len(label_class_human_value_list[label_class]))] + " " + dict_summary_sentences[label_class]
#                 }
#             )

#             for l in labels:
#                 if l["id"] == img_file_id:
#                     from_gpt_string = ""
#                     from_gpt_string += l["conversation"][1]["scene"][0] + " "
#                     from_gpt_string += l["conversation"][1][label_class][0] + " "
#                     from_gpt_string += "Here is the dictionary: {'" + label_class + "': '" + str(eval(l["conversation"][1]["value-dict"])[label_class]) + "'}"

#                     entry["conversations"].append(
#                         {
#                             "from": "gpt",
#                             "value": from_gpt_string,
#                         }
#                     )
#                     break

#             merged.append(entry)

# # Save the merged data to a JSON file
# # output_file_path = "merged_dataset.json"
# # with open(output_file_path, "w") as f:
# #     json.dump(merged, f, indent=4)


# # save a train and val file called merged_dataset_trainsplit.json and merged_dataset_valsplit.json

# # randomly shuffle the keys of the current dict
# # and split them into two sets

# np.random.shuffle(merged)
# train_split = int(len(merged) * 0.85)
# train_data = merged[:train_split]
# val_data = merged[train_split:]

# train_output_file_path = "merged_dataset_trainsplit.json"
# val_output_file_path = "merged_dataset_valsplit.json"

# with open(train_output_file_path, "w") as f:
#     json.dump(train_data, f, indent=4)

# with open(val_output_file_path, "w") as f:
#     json.dump(val_data, f, indent=4)