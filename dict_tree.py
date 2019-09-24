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
        if char in self.candidates:
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

    def matchCharInNodes(self, temp_nodes, char):
        for node in temp_nodes:
            if node.match(char):
                return node
        return None

    def allMatchCharInNodes(self, temp_nodes, char):
        res = []
        for node in temp_nodes:
            if node.match(char):
                res.append(node) 
        return res

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
            while True:
                node = self.matchCharInNodes(temp_nodes, char)
                print index, char.encode('utf-8'), node == None
                if index == 8:
                    print 'index=8: ', p == None, [i.chars for i in temp_nodes]
                if node == None and p != None: # p != None表示p不为根节点，此时的None表示根节点
                    p = p.fail_point
                    if p == None:
                        # temp_nodes = self.roots
                        break
                    temp_nodes = p.childs  # 需要判断p不为None
                else:
                    break
            if node != None:
                p = node
                temp_nodes = p.childs
            if p:
                temp = copy.copy(p)  
                while temp != None:
                    if temp.is_leaf or True:
                        print "index:", index, "   match:", temp.chars
                    temp = temp.fail_point

    def matchMultiState(self, sentence):
        new_index = 0
        while new_index < len(sentence):
            temp_char = sentence[new_index]
            temp_node_list = self.allMatchCharInNodes(self.roots, temp_char)
            new_index += 1
            if temp_node_list:
                break
        self.matchMulti(sentence, new_index, temp_node_list)

    def matchMulti(self, sentence, index, nodes):
        if index >= len(sentence):
            return 
        char = sentence[index]
        for p in nodes:
            temp_nodes = p.childs
            while True:
                node_list = self.allMatchCharInNodes(temp_nodes, char)
                # print index, char.encode('utf-8'), node == None
                if node_list == [] and p != None: # p != None表示p不为根节点，此时的None表示根节点
                    p = p.fail_point
                    if p == None:
                        break
                    temp_nodes = p.childs  # 需要判断p不为None
                else:
                    break
            if node_list != []:
                for node in node_list:
                    self.askFailPoint(index, node)
                self.matchMulti(sentence, index+1, node_list)
            if p == None:
                new_index = index + 1
                temp_node_list = []
                while new_index < len(sentence):
                    temp_char = sentence[new_index]
                    temp_node_list = self.allMatchCharInNodes(self.roots, temp_char)
                    if temp_node_list:
                        break
                    new_index += 1
                self.matchMulti(sentence, new_index, temp_node_list)
 
    def askFailPoint(self, index, node):
        temp = copy.copy(node) 
        while temp != None:
            if temp.is_leaf:
                print "index:", index, "   match:", temp.chars
            temp = temp.fail_point

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
    dict_tree.match(u'羊绵公闪详肉山公站立重配弹夹不足')
    dict_tree.matchMultiState(u'羊绵公闪详肉山公站立重配弹夹不足')
                
