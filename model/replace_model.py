import sys
import os
import numpy as np 
from utils.utils import *
class NounMatcher(object):
    def __init__(self,
                name,
                pinyin_dict,
                stroke_dict):
        self.name = name
        self.char_same_pinyin_lists = []
        self.char_same_stroke_lists = []
        for i in name:
            if i in pinyin_dict:
                self.char_same_pinyin_lists.append(pinyin_dict[i])
            if i in stroke_dict:
                self.char_same_stroke_lists.append(stroke_dict[i])
    
    
class Replacer(object):
    def __init__(self,
                same_pinyin_path,
                same_stroke_path,
                subject_path):
        self.same_pinyin_dict = load_same_pinyin(same_pinyin_path)
        self.same_stroke_dict = load_same_stroke(same_stroke_path)
        self.subject_noun = load_subject_noun(subject_path)
