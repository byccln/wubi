# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import itertools
import unicodedata

import pickle

from _compat import u

__all__ = ['get','data']


# init wubi dict
data = {}
dat = os.path.join(os.path.dirname(__file__), "wubi.pickle")

try :
    with open(dat) as f:
        data = pickle.loads(f.read())
except:
    pass

if len(data)<1:
    from cw import cw
    from wc import wc
    data['cw'] = cw
    data['wc'] = wc


def _wubi_generator(chars):
    """Generate wubi for chars, if char is not chinese character,
    itself will be returned.
    Chars must be unicode list.
    """
    s = []
    flag = ''
    for i, char in enumerate(chars):
        # handle english in chinese
        var =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if char ==' ':
            if len(s)!=0:
                yield ''.join(s)
                s=[]
                flag = ''
        elif char in var or char in digit or (flag in digit and (char == ',' or char == '.')):
            flag = char
            s.append(char)
            if i == len(chars) - 1:
                yield ''.join(s)
        else:
            if len(s)!=0:
                yield ''.join(s)
                s=[]
                flag = ''
            wubi = data['cw'].get(char)
            if wubi == None:
                wubi=char
            yield wubi


def _chinese_generator(chars, delimiter):
    """Generate chinese for chars, if char is not chinese character,
    itself will be returned.
    Chars must be unicode list.
    """
    for char in chars.split(delimiter):
        chinese = data['wc'].get(char)
        if chinese ==None:
                chinese=char
        yield chinese

def get(s,type='',delimiter=' '):
    """Return wubi of string, the string must be unicode
    """
    #pre process input string


    if type=='cw':
        return delimiter.join(_wubi_generator(u(s)))
    elif type =='wc':
        return ''.join(_chinese_generator(u(s),delimiter))
    else:
        return None

if __name__ =='__main__':
    s = "我12岁了， 我有一个apple。 No.1是谁？这儿有3,000元。"
    t = get(s, 'cw')
    print(t)
