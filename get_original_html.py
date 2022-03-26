''' 将原始文本转换成html '''
import os


def get_data(text_fn):
    data = []
    with open(text_fn, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            data.append(line)
    return data


text_dir = "original_text"
html_dir = "original_html"
os.makedirs(html_dir, exist_ok=True)

for fn in os.listdir(text_dir):
    cid = fn.split(".")[0]
    text_fn = os.path.join(text_dir, fn)
    ori_data = get_data(text_fn)

    html_fn = os.path.join(html_dir, f"{cid}.html")
    with open(html_fn, "w") as f:
        f.write("<html>\n")
        f.write("<head>\n") 
        f.write("<meta charset=\"utf-8\">\n")
        f.write(f"<title>raw text {cid}</title>\n")
        f.write("</head>\n")
        f.write("<body style=\"background-color:#FFFFCC\">\n")

        for i, line in enumerate(ori_data):
            if i == 0:
                f.write(f"<h2>{line}</h2>\n")
            else:
                f.write(f"<p>{line}</p>\n")
        f.write("</body>\n")
        f.write("</html>")