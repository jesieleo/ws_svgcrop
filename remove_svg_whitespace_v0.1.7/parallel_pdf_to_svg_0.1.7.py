# 设置并行任务的最大数量（根据系统性能进行调整）
# max_jobs=-1

# 使用 parallel 命令处理 PDF 文件
# ls *.pdf | parallel -j $max_jobs 'inkscape --export-type=svg {.}.pdf'

# 使用python多进程实现上述功能

import joblib
import subprocess
from pathlib import Path
import os

def convert_pdf_to_svg(pdf_file):
    svg_file = pdf_file.with_suffix('.svg')
    command = ['inkscape', '--export-type=svg', str(pdf_file)]
    subprocess.run(command)

# 设置工作目录
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Specify the directory where your PDF files are located
pdf_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# Get a list of PDF files
pdf_files = list(pdf_directory.glob('*.pdf'))

# Set the number of parallel jobs
max_jobs = 4  # Adjust this based on your system's capacity

# Use joblib to parallelize the conversion
joblib.Parallel(n_jobs=max_jobs)(joblib.delayed(convert_pdf_to_svg)(pdf_file) for pdf_file in pdf_files)
