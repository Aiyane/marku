#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'

tokenClass = {
    "strongClass":      "",
    "emClass":          "",
    "codeClass":        "",
    "delClass":         "",
    "imgClass":         "",
    "aClass":           "",
    "hClass":           "",
    "blockquoteClass":  "",
    "preClass":         "",
    "tableClass":       "",
    "pClass":           ""
}


def addClass(cls_dict=None):
    if cls_dict is not None and not isinstance(cls_dict, dict):
        raise TypeError('%r 必须是字典类型', cls_dict)
    elif cls_dict is None:
        return tokenClass

    for k, v in cls_dict.items():
        if k in tokenClass:
            tokenClass[k] = v
    return tokenClass


def getClass(name):
    return tokenClass[name]
