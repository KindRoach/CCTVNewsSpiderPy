import os
import re

import jieba

news_path = r"data/news"
words_path = r"data/words"

file_num = len(os.listdir(news_path))
count = 0
for file in os.listdir(news_path):
    with open(os.path.join(news_path, file), 'r', encoding="utf-8") as in_f:
        with open(os.path.join(words_path, file), 'w', encoding="utf-8") as out_f:
            for line in in_f.readlines():
                # 过滤所有非中文字符
                p = re.compile(r"[\u4e00-\u9fa5]")
                res = re.findall(p, line)
                result = ''.join(res)
                # 分词
                words = jieba.cut(result)
                for word in words:
                    out_f.write(word + " ")
            count += 1
            print("{}/{} done.".format(count, file_num))
