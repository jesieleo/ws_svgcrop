# ws_svgcrop
A bash &amp; python code to convert PDF to SVG, and remove SVG whitespace automaticly.

for debian/ubuntu users:
First install inkscape & imagemagick
```
sudo apt install inkscape
sudo apt install imagemagick
```
After install conda environment （Tsinghua source: https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/）
```
pip install wand
```
Now convert all pdfs in the same folder to SVG
```
bash parallel_pdf_to_svg.bash 
```
Automatic cropping SVG whitespace
```
bash Parallel_remove_whitespace.bash
```
