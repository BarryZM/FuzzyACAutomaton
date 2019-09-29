# -*- coding: utf-8 -*-
# Author: wfh
# Date: 2019/09/29

import os
import sys
import time
import json
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
from utils.dict_tree import *
from utils.utils import *

import numpy as np
from flask import Flask, request, jsonify

id = 0 # 字典树节点id

def setup_logger(logger_name, log_file, level=logging.INFO):
    """
    config logging info
    :param logger_name:
    :param log_file:
    :param level:
    :return:
    """
    log_conf = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    log_conf.setLevel(level)
    log_conf.addHandler(fileHandler)

def setup_all_logger():
    logger_math_name = 'math_logger'
    logger_chemistry_name = 'chemistry_logger'

    setup_logger(logger_math_name, './log/math_log.log')
    setup_logger(logger_chemistry_name, './log/chemistry_log.log')

    math_logger = logging.getLogger('math_logger')
    chemistry_logger = logging.getLogger('chemistry_logger')
    return math_logger, chemistry_logger

if __name__ == "__main__":
    # load config
    config_path = './config/config_json.json' 
    with open(config_path, 'r') as f:
	    config = json.load(f)
    print config['dict_tree']['same_pinyin_path']    
    math_logger, chemistry_logger = setup_all_logger()
    print config['dict_tree']['same_pinyin_path']
    pinyin_dict = load_same_pinyin(config['dict_tree']['same_pinyin_path'])
    stroke_dict = load_same_stroke(config['dict_tree']['same_stroke_path'])
    math_noun = load_subject_noun(config['dict_tree']['math_dict'])
    chem_noun = load_subject_noun(config['dict_tree']['chem_dict'])
    math_dict_tree = DictTreeModel(pinyin_dict, stroke_dict, math_noun)
    math_dict_tree.printInfo()
    chem_dict_tree = DictTreeModel(pinyin_dict, stroke_dict, chem_noun)
    chem_dict_tree.printInfo()

    app = Flask(__name__)
    @app.route('/')
    def index():
        return "please use correct route: eg. /math"

    @app.route(config['server']['route_chemistry'], methods=['GET','POST'])
    def predict_chemistry():
        dict_tree = chem_dict_tree
        logger = chemistry_logger
        if request.method == 'POST':
            start = time.time()
            input_data = request.json
            log_info = [str(input_data["tid"]), json.dumps(input_data)]
            output_data = {
                "match_list": [],
                "text": "",
                "errNum": "1",
                "tid": input_data["tid"]
            }
            text = input_data['text']
            dict_tree.matchMultiNew(text)
            match_pairs, new_text = dict_tree.get_res()
            output_data["match_list"] = match_pairs
            output_data["text"] = new_text
            log_info.append(json.dumps(match_pairs))
            log_info.append(new_text)
            end = time.time()
            print "运行时间：{}".format(end - start)
            logger.info("\t".join(log_info))
            return jsonify(output_data)
        else:
            return "Please use POST method."

    @app.route(config['server']['route_math'], methods=['GET','POST'])
    def predict_math():
        dict_tree = math_dict_tree
        logger = math_logger
        if request.method == 'POST':
            start = time.time()
            input_data = request.json
            log_info = [str(input_data["tid"]), json.dumps(input_data)]
            output_data = {
                "match_list": [],
                "text": "",
                "errNum": "1",
                "tid": input_data["tid"]
            }
            text = input_data['text']
            dict_tree.matchMultiNew(text)
            match_pairs, new_text = dict_tree.get_res()
            output_data["match_list"] = match_pairs
            output_data["text"] = new_text
            log_info.append(json.dumps(match_pairs))
            log_info.append(new_text)
            end = time.time()
            print "运行时间：{}".format(end - start)
            logger.info("\t".join(log_info))
            return jsonify(output_data)
        else:
            return "Please use POST method."

    # HTTP Errors handlers
    @app.errorhandler(404)
    def url_error(e):
        return """Wrong URL!<pre>{}</pre>""".format(e), 404
    @app.errorhandler(500)
    def server_error(e):
        return """ An internal error occurred: <pre>{}</pre> See logs for full stacktrace.""".format(e), 500
    app.run(host=config['server']['host'], port=config['server']['port'], debug=False)

