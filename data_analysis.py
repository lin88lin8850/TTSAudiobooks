''' check 各个系统的差异 '''
import os
import re

ssml_pattern = re.compile('<.*?>')


def get_info_data(info_fn):
    data = []
    with open(info_fn, "r") as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            idx = line[0]
            speaker_tag = line[1]
            text = line[5]
            # 去除ssml信息
            text = re.sub(ssml_pattern, '', text) 
            assert len(text) > 0
            data.append([idx, speaker_tag, text])

    return data

def get_cids(fn):
    data = []
    with open(fn, "r") as f:
        for i, line in enumerate(f.readlines()):
            if i == 0:
                continue
            book_name, _, cid = line.strip().split(",")
            data.append([book_name, cid])
    return data

info_fn = "book_info.txt"
id_info = get_cids(info_fn)

for book_name, cid in id_info:
    label_fn = os.path.join(f"human/info/{cid}.json")
    baseline_fn = os.path.join(f"baseline/info/{cid}.json")
    ours_fn = os.path.join(f"ours/info/{cid}.json")

    label_data = get_info_data(label_fn)
    baseline_data = get_info_data(baseline_fn)
    ours_data = get_info_data(ours_fn)
    assert len(label_data) == len(baseline_data) == len(ours_data)

    # 统计系统错误占比
    N_conv = 0
    N_wrong_baseline, N_wrong_ours = 0, 0
    for lab_item, baseline_item, ours_item in zip(label_data, baseline_data, ours_data):
        # check 句子文本
        # try:
        #     assert lab_item[2] == baseline_item[2] == ours_item[2]
        # except:
        #     print(lab_item[2])
        #     print(baseline_item[2])
        #     print(ours_item[2])
        #     print()

        if lab_item[1] == "旁白":
            continue
        if baseline_item[1] != lab_item[1]:
            N_wrong_baseline += 1
        if ours_item[1] != lab_item[1]:
            N_wrong_ours += 1
        N_conv += 1
    print(cid)
    print("baseline: {:.2f}\t({}/{})".format(N_wrong_baseline/N_conv, N_wrong_baseline, N_conv))
    print("ours: {:.2f}\t({}/{})".format(N_wrong_ours/N_conv, N_wrong_ours, N_conv))
    print()
