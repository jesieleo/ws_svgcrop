import tkinter as tk
from tkinter import filedialog,ttk
from os.path import exists
from xml.etree.ElementTree import parse
from PIL import Image
from io import BytesIO
from cairosvg import svg2png
from numpy import array, where, isin
import subprocess
from os import listdir, chdir
from multiprocessing import Pool, freeze_support, cpu_count


class SvgCutterApp:
    def __init__(self, master):
        self.master = master
        master.title("svg_cutter Work Folder Selector")

        # 创建按钮命令
        self.label_instruction = tk.Label(master, text="Select a working folder for svg_cutter:")
        self.entry_path = tk.Entry(master, width=30)
        self.button_browse = tk.Button(master, text="Browse", command=self.select_folder)
        self.button_run_svg_cutter = tk.Button(master, text="Run svg_cutter", command=self.run_svg_cutter)
        self.button_run_pdf_to_svg = tk.Button(master, text="Run pdf_to_svg", command=self.run_pdf_to_svg)

        # 自动排列按钮
        self.label_instruction.pack(pady=10)
        self.entry_path.pack(pady=10)
        self.button_browse.pack(pady=10)
        self.button_run_pdf_to_svg.pack(pady=10)
        self.button_run_svg_cutter.pack(pady=10)

    def get_svg_files(self, folder_path):
        # 获取文件夹中的所有文件
        all_files = listdir(folder_path)

        # 过滤以 'out.svg' 结尾的文件
        svg_files = [file.split('.')[0] for file in all_files if file.endswith('.svg') and not file.endswith('-out.svg')]

        return svg_files

    def get_pdf_files(self, folder_path):
        # 获取文件夹中的所有文件
        all_files = listdir(folder_path)

        # 过滤以 'out.svg' 结尾的文件
        svg_files = [file for file in all_files if file.endswith('.pdf')]

        return svg_files

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder_path)

    def run_svg_cutter(self):
        folder_path = self.entry_path.get()
        if folder_path and exists(folder_path):
            chdir(folder_path)
            filename = self.get_svg_files(folder_path)
            filename_in = [i+'.svg' for i in filename]
            filename_out = [i+'-out.svg' for i in filename]
            with Pool(cpu_count()) as pool:
                pool.starmap(remove_svg_whitespace, zip(filename_in, filename_out))



    def run_pdf_to_svg(self):
        folder_path = self.entry_path.get()
        if folder_path and exists(folder_path):
            chdir(folder_path)
            filename = self.get_pdf_files(folder_path)
            with Pool(cpu_count()) as pool:
                pool.map(inkscape_pdf_to_svg, filename)

def remove_svg_whitespace(filename_in, filename_out):
    #获取视图区间
    tree = parse(filename_in)
    root = tree.getroot()
    viewbox_str_ = root.attrib['viewBox']
    viewbox_str_ = [int(float(v)) for v in viewbox_str_.split()]
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
    png_data = svg2png(url=svg_file_path)

    # 使用 Pillow 打开 PNG 数据
    image = Image.open(BytesIO(png_data))

    data = array(image)
    x,y=where(~isin(data[:,:,0],[0,255]))
    limits = f"{x.min()}, {y.min()}, {x.max()}, {y.max()}"


    # 解析 SVG 文件，判断白边位置
    tree = parse(filename_in)
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

def inkscape_pdf_to_svg(filename):
    subprocess.call(['inkscape', '--export-type=svg', filename])


def main():
    root = tk.Tk()
    app = SvgCutterApp(root)

    root.mainloop()


if __name__ == '__main__':
    freeze_support()
    main()
