# Fittslaw-Analyzer
**Fitts law**是人机交互领域很重要的定理之一，主要研究使用指定设备到达并点击一个目标的时间，与当前设备位置和目标距离(A)以及目标大小(W)的关系。Fitts定律用公式表述为：t = a + b log2(A/W + 1)。

Fitts law实验主要有以下步骤：

1. 针对不同用户和不同使用设备（如鼠标、触摸板、手机等）在实验平台(Tsinghua人机交互)：http://39.97.170.246/fitts/进行实验，采集不同宽度、不同距离的目标下用户的点击时间。
2. 对收集到的数据进行处理，并做回归分析和anova方差分析。

## 轮子介绍

这个轮子是在做人机交互作业的时候顺手写的，有问题的地方欢迎指正~

### 一般功能

- 对收集到的数据，生成其散点分布图。
- 对收集到的数据，针对每一种设备(device)，进行线性回归分析，确定Fitts law中a,b的值以及相关系数。这样可以方便用户对于不同设备直观比较他们的a,b值。
- 对收集到的数据，可针对指定变量进行anova方差分析，从而确定某变量是否直接影响用户的点击时间。

### 说明

- 此工具对于同一用户同一设备，将相同A和W的数据取平均，并作为一个数据点存储。
- 此工具采用的是log2(A/W + 1)作为ID值，而不是log2(2A/W)。

## 安装和使用

### 安装依赖

```shell
pip install -r requirements.txt
```

### 使用

把所有数据(.csv)放在一个路径下，比如./data，运行demo.py即可：

```shell
python demo.py ./data [-r] [-a] [-g] [-p]
```

用`-h`查看帮助。

这里`-a`选项为anova方差分析，默认是分析“用户(name)”和“设备(device)”两个因素对时间的影响，如果需要更改可以在`-a`后加入，比如要分析device和width：

```shell
python demo.py ./data -a device width
```

## 关于anova方差分析

使用工具中的方差分析会得到如下一张表：

|          | df   | sum_sq | mean_sq | F    | PR(>F) |
| -------- | ---- | ------ | ------- | ---- | ------ |
| factor_1 |      |        |         |      |        |
| factor_2 |      |        |         |      |        |
| Residual |      |        |         |      |        |

这是一张多因素方差分析表，是`anova_lm`生成的分析结果。第一列`factor_1`、`factor_2`表示参与分析的因素，Residual表示误差。第一行df表示自由度，sum_sq表示离差平方和，mean_sq表示均方离差，F表示F值，PR(>F)表示F值所对应的显著水平α。

实验中一般用PR或者F值判断某个因素对结果的影响程度，PR<0.05认为有影响，否则不能拒绝0假设（认为不同组数据其实是同分布）。