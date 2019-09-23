#coding: utf-8
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
        # print "self.name:", self.name
        self.char_same_pinyin_lists = []
        self.char_same_stroke_lists = []
        for i in name:
            if i in pinyin_dict:
                if i not in pinyin_dict[i]:
                    pinyin_dict[i].add(i)
                self.char_same_pinyin_lists.append(pinyin_dict[i])
                print i, ' 的同音字：'
                for char in pinyin_dict[i]:
                    print char.encode("utf-8")
                print ''
            else:
                self.char_same_pinyin_lists.append(set(i))
                print i," not in pinyin_dict"
            if i in stroke_dict:
                if i not in stroke_dict[i]:
                    stroke_dict[i].add(i)
                self.char_same_stroke_lists.append(stroke_dict[i])
                print i, ' 的同形字：'
                for char in stroke_dict[i]:
                    print char.encode("utf-8")
                print ''
            else:
                self.char_same_stroke_lists.append(set(i))
                print i," not in stroke_dict"
    
    def match_and_replace(self, sentence):
        # print 'sentence:', sentence
        length = len(self.char_same_pinyin_lists)
        for i in range(len(sentence) - length + 1):
            temp_str = sentence[i:i+length]
            print 'temp_str:', temp_str
            match = True
            for j in range(len(temp_str)):
                if not (temp_str[j] in self.char_same_pinyin_lists[j] or 
                    temp_str[j] in  self.char_same_stroke_lists[j]):
                    print 'cannt find:', temp_str[j]
                    match = False
                    break
            if match:
                print sentence, self.name
                for j in range(len(self.name)):
                    sentence[i + j] = self.name[j]
            if match:
                print 'match:', temp_str
        # return sentence


class Replacer(object):
    def __init__(self,
                same_pinyin_path,
                same_stroke_path,
                subject_path):
        self.same_pinyin_dict = load_same_pinyin(same_pinyin_path)
        self.same_stroke_dict = load_same_stroke(same_stroke_path)
        self.subject_noun = load_subject_noun(subject_path)
        
        # for i in self.subject_noun:
        #     print i.encode("utf-8")
        self.noun_matchers = []
        for i in self.subject_noun:
            self.noun_matchers.append(NounMatcher(i, self.same_pinyin_dict, self.same_stroke_dict))
            break
        # print len(self.noun_matchers)

    def match_and_replace(self, sentence):
        for i in self.noun_matchers:
            i.match_and_replace(sentence)
        return sentence

if __name__ == "__main__":
    same_pinyin_path = './data/same_pinyin.txt'
    same_stroke_path = './data/same_stroke.txt'
    subject_path = './data/chem'
    sentence = u'试验表示大量的二氧化炭震荡后不溶于溴水'
    replacer = Replacer(same_pinyin_path, same_stroke_path, subject_path)
    print replacer.match_and_replace(sentence)
