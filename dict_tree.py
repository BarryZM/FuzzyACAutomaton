#coding: utf-8
import sys
import os
import numpy as np 
from utils.utils import *

class TreeNode(object):
    def __init__(self,
                char,
                pinyin_dict,
                stroke_dict):
        self.char = char
        self.candidates = [char]
        self.childs = []
        if char in pinyin_dict:
            self.candidates += list(pinyin_dict[char])
        if char in stroke_dict:
            self.candidates += list(stroke_dict[char])
    def match(self,char):
        if char in candidates:
            return True
        else:
            return False
    
    def printInfo(self):
        print "char:", self.char, "candidates:", self.candidates
        for child in  self.childs:
            child.printInfo()
    
class DictTree(object):
    def __init__(self,
                pinyin_dict,
                stroke_dict,
                str_list):
        self.pinyin_dict = pinyin_dict
        self.stroke_dict = stroke_dict
        self.str_list = str_list
        self.roots = []
        self.buildDict()
    
    def findCharInNodes(self, temp_nodes, char):
        for node in temp_nodes:
            if char == node.char:
                return node
        return None

    def buildDict(self):
        for temp_str in self.str_list:
            temp_nodes = self.roots
            for char in temp_str:
                node = self.findCharInNodes(temp_nodes, char)
                if node:
                    temp_nodes = node.childs
                else:
                    node = TreeNode(char, self.pinyin_dict, self.stroke_dict)
                    temp_nodes.append(node)
                    temp_nodes = node.childs
    
    def printInfo(self):
        for root in self.roots:
            root.printInfo()
    
if __name__ == "__main__":
    same_pinyin_path = './data/same_pinyin.txt'
    same_stroke_path = './data/same_stroke.txt'
    subject_path = './data/dict_tree_test_data'
    pinyin_dict = load_same_pinyin(same_pinyin_path)
    stroke_dict = load_same_stroke(same_stroke_path)
    subject_noun = load_subject_noun(subject_path)
    dict_tree = DictTree(pinyin_dict, stroke_dict, subject_noun)
    dict_tree.printInfo()
                
