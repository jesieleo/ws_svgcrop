# 设置并行任务的最大数量（根据系统性能进行调整）
max_jobs=-1

# 使用 parallel 命令处理 PDF 文件
ls *.svg | parallel -j $max_jobs 'python remove_svg_whitespace_v0.1.5.py --infile {.}.svg --outfile {.}-out.svg'