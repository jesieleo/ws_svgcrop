import xml.etree.ElementTree as ET
from wand.image import Image
import numpy as np
from optparse import OptionParser

usage = '''%prog FILE1 [FILE2] [...] [options]

concatenate SVG files

This will concatenate FILE1, FILE2, ... to a new svg file printed to
stdout.

'''
VERSION = '0.1.5'

parser = OptionParser(usage, version=VERSION)


parser.add_option("--infile",type='str',
                  help='size of margin (in any units, px default)',)

parser.add_option("--outfile",type='str',
                  help='size of margin (in any units, px default)',)


(options, args) = parser.parse_args()

infile = options.infile
outfile = options.outfile

if infile is None:
    raise ValueError('未定义输入文件名')

if outfile is None:
    raise ValueError('未定义输出文件名')
'''# 读取 SVG 图像
with Image() as img:
    img.read(filename=r'D:\python\SVG_combine\hello.svg')
    data = np.array(img)
    x,y=np.where(np.sum(np.isin(data,255),axis=4)!=4)
    limits = f"{x.min()}, {y.min()}, {x.max()}, {y.max()}"
    print(limits)
    print(x.max()-x.min())
    print(y.max()-y.min())'''
filename = infile#r'页面 1.svg'
filename_out = outfile#r'outfile_2________3.svg'

#获取视图区间
tree = ET.parse(filename)
root = tree.getroot()
viewbox_str_ = root.attrib['viewBox']
viewbox_str_ = [int(float(v)) for v in viewbox_str_.split()]
#viewbox = [int(float(v)) for v in viewbox_str.split()]
width_ = root.attrib['width']
width_ = [int(float(v)) for v in width_.split()]
height_ = root.attrib['height']
height_ = [int(float(v)) for v in height_.split()]

# 查看viewbox是否覆盖整个图片
if ((viewbox_str_[2]-viewbox_str_[0])==width_[0])&((viewbox_str_[3]-viewbox_str_[1])==height_[0]):
    pass
else:
    print((viewbox_str_[2]-viewbox_str_[0]),width_)
    raise ValueError('viewBox不覆盖整个图片，需要修复viewBox')
with Image() as img:
    img.read(filename=filename)
    #img.resize(width_[0],height_[0])
#    img.resize(viewbox[2]-viewbox[0],
#               viewbox[3]-viewbox[1])
    data = np.array(img)
    x,y=np.where(~np.isin(data[:,:,0],255))
    limits = f"{x.min()}, {y.min()}, {x.max()}, {y.max()}"
    #print(limits)
    #print(x.max()-x.min())
    #print(y.max()-y.min())

# 解析 SVG 文件，判断白边位置
tree = ET.parse(filename)
root = tree.getroot()

# 设置截图后保留白边大小
jianjv = 3
if jianjv:
    root.attrib['viewBox'] = f'{y.min()-jianjv} {x.min()-jianjv} {y.max()-y.min()+2*jianjv} {x.max()-x.min()+2*jianjv}'
    root.attrib['height']=f'{x.max()-x.min()+2*jianjv}'
    root.attrib['width']=f'{y.max()-y.min()+2*jianjv}'
else:
    root.attrib['viewBox'] = f'{y.min()} {x.min()} {y.max()-y.min()} {x.max()-x.min()}'
    root.attrib['height']=f'{x.max()-x.min()}'
    root.attrib['width']=f'{y.max()-y.min()}'

# 打印新的SVG图像参数
#print(y.min()-jianjv)

tree.write(filename_out)


