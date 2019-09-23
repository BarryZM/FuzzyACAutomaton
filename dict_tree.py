#coding: utf-8
import sys
import os
import numpy as np 
from utils.utils import *

id = 0
class TreeNode(object):
    def __init__(self,
                char,
                pinyin_dict,
                stroke_dict):
        self.char = char
        self.candidates = [char]
        self.childs = []
        self.is_leaf = False
        self.fail_point = None
        self.id = id
        global id
        id += 1
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
        print "char:", self.char, \
            "fail_point:", self.fail_point.char, \
            "fail_point_id:", self.fail_point.id, \
            "is_leaf:", self.is_leaf, \
            "candidates:", self.candidates
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

    def buildFailPoint(self):
        vect = []
        for node in self.roots:
            vect.append(node)
        while vect:
            father = vect.pop(0)
            ancestor_fail_point = father.fail_point
            for child in father.childs:
                while ancestor_fail_point:
                    node = self.findCharInNodes(ancestor_fail_point.childs, child.char)
                    if node:
                        child.fail_point = node
                        break
                    else:
                        ancestor_fail_point = ancestor_fail_point.fail_point
                if ancestor_fail_point == None:
                    child.fail_point = self.findCharInNodes(self.roots, child.char)
                vect.append(child)
        

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
            node.is_leaf = True
        self.buildFailPoint()
        
    
    def printInfo(self):
        for root in self.roots:
            root.printInfo()
    
    # def roughMatch(self, str)
if __name__ == "__main__":
    same_pinyin_path = './data/same_pinyin.txt'
    same_stroke_path = './data/same_stroke.txt'
    subject_path = './data/dict_tree_test_data'
    pinyin_dict = load_same_pinyin(same_pinyin_path)
    stroke_dict = load_same_stroke(same_stroke_path)
    subject_noun = load_subject_noun(subject_path)
    dict_tree = DictTree(pinyin_dict, stroke_dict, subject_noun)
    dict_tree.printInfo()
                
