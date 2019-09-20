#coding: utf-8
import codecs
import os

def load_same_stroke(path, sep='\t'):
    """
    加载形似字
    :param path:
    :param sep:
    :return:
    """
    result = dict()
    if not os.path.exists(path):
        # logger.warn("file not exists:" + path)
        return result
    with codecs.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split(sep)
            for i in range(len(parts)):
                parts[i] = parts[i].encode("utf-8")
            if parts and len(parts) > 1:
                for i, c in enumerate(parts):
                    result[c] = set(list(parts[:i] + parts[i + 1:]))
    return result

def load_same_pinyin(path, sep='\t'):
    """
    加载同音字
    :param path:
    :param sep:
    :return:
    """
    result = dict()
    if not os.path.exists(path):
        # logger.warn("file not exists:" + path)
        return result
    with codecs.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split(sep)
            for i in range(len(parts)):
                parts[i] = parts[i].encode("utf-8")
            if parts and len(parts) > 2:
                key_char = parts[0]
                same_pron_same_tone = set(list(parts[1]))
                same_pron_diff_tone = set(list(parts[2]))
                value = same_pron_same_tone.union(same_pron_diff_tone)
                if len(key_char) > 1 or not value:
                    continue
                result[key_char] = value
    return result

def load_subject_noun(path):
    if not os.path.exists(path):
        # logger.warn("file not exists:" + path)
        return result
    res = []
    with codecs.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            res.append(line)
    return res
