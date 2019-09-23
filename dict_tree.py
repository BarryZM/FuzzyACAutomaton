#coding: utf-8
import sys
import os
import numpy as np 
import copy
from utils.utils import *

id = 0
class TreeNode(object):
    def __init__(self,
                char,
                chars,
                pinyin_dict,
                stroke_dict):
        self.char = char
        self.chars = chars
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
        char = None
        id = None
        if self.fail_point:
            char = self.fail_point.char
            id = self.fail_point.id
        print "char:", self.char, \
            "fail_point:", char, \
            "fail_point_id:", id, \
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
            for index, char in enumerate(temp_str):
                node = self.findCharInNodes(temp_nodes, char)
                if node:
                    temp_nodes = node.childs
                else:
                    node = TreeNode(char, temp_str[0:index+1], self.pinyin_dict, self.stroke_dict)
                    temp_nodes.append(node)
                    temp_nodes = node.childs
            node.is_leaf = True
        self.buildFailPoint()
        
    def match(self, sentence):
        p = None
        temp_nodes = self.roots
        for index, char in enumerate(sentence):
            node = self.findCharInNodes(temp_nodes, char)
            print index, char.encode('utf-8'), node == None
            while node == None and p != None: # p != None表示p不为根节点，此时的None表示根节点
                p = p.fail_point
                temp_nodes = p.childs
                node = self.findCharInNodes(temp_nodes, char)
            if p:
                temp = copy.copy(p) 
                while temp != None:
                    temp = temp.fail_point
                    print "index:", index, "   match:", p.chars

    def printInfo(self):
        for root in self.roots:
            root.printInfo()
    
    # def roughMatch(self, str)

if __name__ == "__main__":
    same_pinyin_path = './data/same_pinyin.txt'
    same_stroke_path = './data/same_stroke.txt'
    subject_path = './data/dict_tree_test_data1'
    pinyin_dict = load_same_pinyin(same_pinyin_path)
    stroke_dict = load_same_stroke(same_stroke_path)
    subject_noun = load_subject_noun(subject_path)
    dict_tree = DictTree(pinyin_dict, stroke_dict, subject_noun)
    dict_tree.printInfo()
    dict_tree.match(u'羊绵公山羊肉山公')
                
