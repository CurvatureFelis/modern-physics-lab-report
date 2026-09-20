# Modern Physics Lab Report Skill

面向大学本科近代物理实验课程的 Codex Skill。它读取实验原理、操作资料和原始数据，按具体物理模型完成数据检查、拟合、不确定度分析、作图和 LaTeX 实验报告生成。

核心原则是：原始数据真实、分析过程可追溯、计算可以复现、物理模型与实验相符。Skill 不会为接近理论值而修改数据，也不会虚构仪器精度、实验步骤或缺失测量。

## 安装

在 Codex 中调用 `$skill-installer`：

```text
$skill-installer 请从以下仓库安装 Skill：
https://github.com/CurvatureFelis/modern-physics-lab-report
```

也可以将整个仓库复制到以下任一位置：

- 用户级：`%USERPROFILE%/.agents/skills/modern-physics-lab-report`
- 项目级：`<project>/.agents/skills/modern-physics-lab-report`

若安装后未出现，重新启动 Codex。

## 使用

将实验资料和数据放在同一个实验目录，然后输入：

```text
$modern-physics-lab-report 读取这个目录中的实验资料和原始数据，生成可复现的 LaTeX 实验报告。
```

支持 PDF、图片、Word、Markdown、LaTeX、Excel、CSV 和手动输入的数据。图片、手写表格与软件界面中的数值统一通过 `manual_transcription.csv` 转录并保留原图溯源。

## 本地环境

Python 建议使用 3.10 或更高版本：

```text
python -m pip install -r requirements.txt
```

LaTeX 需要 XeLaTeX 和 `latexmk`。TeX Live 或 MiKTeX 应提供：

```text
ctex amsmath amssymb bm physics upgreek siunitx booktabs longtable graphicx hyperref
```

部分文件读取与 PDF 视觉检查由运行环境中的文档、电子表格和 PDF 能力提供。

## 项目骨架

```text
python <skill-dir>/scripts/init_lab_project.py <output-directory>
```

生成的项目包含：

```text
data/raw/                 原始文件，只读保留
data/processed/           转录与派生数据
analysis/analysis.py      可重复运行的分析入口
figures/                  自动生成的图像
report/report.tex         LaTeX 报告
config/experiment.yaml    实验模型和字段配置
```

报告完成并通过检查后，可以先扫描再清理可再生成的临时文件：

```text
python <skill-dir>/scripts/cleanup_lab_project.py <output-directory>
python <skill-dir>/scripts/cleanup_lab_project.py <output-directory> --apply
```

## 许可与数据责任

代码、Skill 指令和模板采用 MIT License。
