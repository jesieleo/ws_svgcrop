# ws_svgcrop
# V0.1.5使用说明：
通过python代码，将PDF转为SVG后，自动裁剪SVG图片

！！！将这些文件与需要转换的PDF文件放在同一个文件夹下！！！

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
# V0.1.7使用说明：
```
python parallel_pdf_to_svg_0.1.7.py
python remove_svg_whitespace_v0.1.7.py
```
# v0.2.0使用说明：
```
直接下载可执行文件，双击无法使用时，右键->属性->权限->允许执行文件
```
# ws_svgcrop
# For V0.1.5:
A bash &amp; python code to convert PDF to SVG, and remove SVG whitespace automaticly.

! ! ! Place these files in the same folder as the PDF files that need to be converted！！！

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
# For V0.1.7：
```
python parallel_pdf_to_svg_0.1.7.py
python remove_svg_whitespace_v0.1.7.py
```
# For V0.2.0：
```
Download the executable file directly, and when double-clicking it does not work, right-click -> Properties -> Permissions -> Allow execution of file
```
