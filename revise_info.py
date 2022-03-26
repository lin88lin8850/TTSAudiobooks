'''将info文件重新整理，去掉无用信息'''

import os
import re


ssml_pattern = re.compile('<.*?>')
systems = {"baseline", "human", "ours"}

def get_info_data(info_fn):
    data = []
    with open(info_fn, "r") as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            idx = line[0]
            speaker_tag = line[1]
            emotion_tag = line[4]
            text = line[5]
            # 去除ssml信息
            text = re.sub(ssml_pattern, '', text) 
            assert len(text) > 0
            new_line = f"{idx}\t\t{speaker_tag}\t\t{emotion_tag}\t\t{text}"
            data.append(new_line)

    return data


for system in systems:
    info_dir = os.path.join(system, "info")
    revised_info_dir = os.path.join(system, "info_1")
    os.makedirs(revised_info_dir, exist_ok=True)

    for fn in os.listdir(info_dir):
        cid = fn.split(".")[0]
        info_fn = os.path.join(info_dir, fn)
        info_data = get_info_data(info_fn)

        save_fn = os.path.join(revised_info_dir, f"{cid}.json")
        with open(save_fn, "w") as f:
            f.write("id  speaker_tag   emotion_tag     text\n")
            f.write("\n".join(info_data))
