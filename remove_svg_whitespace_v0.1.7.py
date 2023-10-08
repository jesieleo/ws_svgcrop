import xml.etree.ElementTree as ET
from PIL import Image
from io import BytesIO
import cairosvg
import numpy as np
from joblib import Parallel, delayed
import os

def get_svg_files(folder_path):
    # 获取文件夹中的所有文件
    all_files = os.listdir(folder_path)

    # 过滤以 'out.svg' 结尾的文件
    svg_files = [file.split('.')[0] for file in all_files if file.endswith('.svg') and not file.endswith('-out.svg')]

    return svg_files

def remove_svg_whitespace(filename_in, filename_out):
    #获取视图区间
    tree = ET.parse(filename_in)
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
        
    # SVG 文件路径
    svg_file_path = filename_in

    # 使用 cairosvg 将 SVG 转为 PNG
    png_data = cairosvg.svg2png(url=svg_file_path)

    # 使用 Pillow 打开 PNG 数据
    image = Image.open(BytesIO(png_data))

    data = np.array(image)
    x,y=np.where(~np.isin(data[:,:,0],[0,255]))
    limits = f"{x.min()}, {y.min()}, {x.max()}, {y.max()}"


    # 解析 SVG 文件，判断白边位置
    tree = ET.parse(filename_in)
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

    tree.write(filename_out)

# 设置工作目录
os.chdir(os.path.dirname(os.path.realpath(__file__)))

filename = get_svg_files(os.path.dirname(os.path.realpath(__file__)))
filename_in = [i+'.svg' for i in filename] #r'页面 1.svg'
filename_out = [i+'-out.svg' for i in filename] #r'outfile_2________3.svg'

Parallel(n_jobs=-1,max_nbytes=None)(delayed(remove_svg_whitespace)(filename_in[i], filename_out[i]) for i in range(len(filename_in)))