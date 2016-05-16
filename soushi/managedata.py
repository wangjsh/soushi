#coding=utf-8
import re

#formatProName 函数，将抓取的原始电视节目名字进行处理
def _formatProName(str):
    pattern = re.compile(u".+[:|：].+[:|：](.+)(（.+）)")
    match = pattern.match(str)
    if match:
        #print 1
        return match.group(1)
    pattern = re.compile(u"(.+)(：|:)(.+)(\d+-\d+)$")
    match = pattern.match(str)
    if match:
        #print 2
        result, number = re.subn(u"\d+$","",match.group(3))
        return result
    pattern = re.compile(u"(.+)(：|:)(.+)(\s+)(\d+)$")
    match = pattern.match(str)
    if match:
        #print 3
        #result, number = re.subn(u"[\d+\/\d+|\d+]+$","",match.group(3))
        result = match.group(3)
        return result
    pattern = re.compile(u"(.+)(:|：)(.+)([\(|（].+[\)|）])$")
    match = pattern.match(str)
    if match:
        #print 4
        return match.group(3)
    pattern = re.compile(u"(.+)[：|:](.+)")
    match = pattern.match(str)
    if match:
        #print 5
        return match.group(2)
    pattern = re.compile(u"(.+)([\(|（].+[\)|）])")
    match = pattern.match(str)
    if match:
        #print 6
        return match.group(1)
    pattern = re.compile(u"(.+)(\d+-\d+)")
    match = pattern.match(str)
    if match:
        #print 7
        return match.group(1)
    pattern = re.compile(u"(.+)(-\d+)")
    match = pattern.match(str)
    if match:
        #print 8
        return match.group(1)
        '''
    pattern = re.compile(u".+\d+$")
    match = pattern.match(str)
    if match:
        print 8
        result, number = re.subn(u"-*\d+$","",str)
        return result
        '''
    return str
def formatProName(str):
    str = _formatProName(str)
    #print str
    pattern = re.compile(u"([^\d]+)(\d+)$")
    match = pattern.match(str)
    if match:
        #print 21
        return match.group(1)
    pattern = re.compile(u"(.+)([\(|（])(.+)([\)|）])")
    match = pattern.match(str)
    if match:
        #print 22
        return match.group(1)
    pattern = re.compile(u"(.+)(第.+季)")
    match = pattern.match(str)
    if match:
        #print 23
        return match.group(1)
    pattern = re.compile(u"(.+)([Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ|Ⅺ])")
    match = pattern.match(str)
    if match:
        #print 24
        return match.group(1)
    return str
'''
s0 = unicode("动画片：果宝特攻Ⅲ",'utf-8')
s = formatProName(s0)
print s
'''
