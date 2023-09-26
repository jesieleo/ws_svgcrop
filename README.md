# ws_svgcrop
通过python代码，将PDF转为SVG后，自动裁剪SVG图片

对于 debian/ubuntu 用户:
首先安装 inkscape & imagemagick
```
sudo apt install inkscape
sudo apt install imagemagick
sudo apt install parallel
```
之后安装conda环境 （Tsinghua source: https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/）
```
pip install wand
```
将同一个文件夹下的所有SVG转为PDF
```
bash parallel_pdf_to_svg.bash 
```
自动裁剪PDF图片白边
```
bash Parallel_remove_whitespace.bash
```

# ws_svgcrop
A bash &amp; python code to convert PDF to SVG, and remove SVG whitespace automaticly.

for debian/ubuntu users:
First install inkscape & imagemagick
```
sudo apt install inkscape
sudo apt install imagemagick
sudo apt install parallel
```
After install conda environment （Tsinghua source: https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/）
```
pip install wand
```
Now convert all PDFs in the same folder to SVG
```
bash parallel_pdf_to_svg.bash 
```
Automatic cropping SVG whitespace
```
bash Parallel_remove_whitespace.bash
```
