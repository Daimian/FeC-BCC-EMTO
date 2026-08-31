# FeC-BCC-EMTO

BCC Fe 与 Fe-C 间隙固溶体的 EMTO-CPA 第一性原理计算。

## 主要发现

`EMTO-BCC-Interstitial-EOS-Failure-Analysis.md`（292 行）——
在 EMTO-CPA 框架下，所有含八面体间隙空球（NQ>1）的 BCC 结构都无法产生正常的状态方程极小值：
E(SWS) 曲线单调递减，缺少物理上应有的排斥-吸引平衡点。该文档分析成因。

`EMTO-BCC-Interstitial-Literature-Review.md`（228 行）——
基于 16 篇一级文献的 EMTO-CPA 间隙空球处理调研。

`EMTO-CPA_BCC_Interstitial_Construction_Guide.md` —— 结构构建操作指南。

## 计算目录

`Fe_bcc/`、`FeC_bcc/`、`FeC_bcc_B/`（方案 B）、`FeC_bcc_sc/`（超胞）——
各含 EMTO 的 kgrn/kfcd 输入输出（全库共 392 个计算文件）。

## 脚本

`*_eos.py` 状态方程拟合、`Fe_bcc_fit.py` 拟合、`FeC_bcc_sc_eta.py` 四方畸变。

## 环境

无依赖声明。需要 Python + numpy/scipy，以及外部 EMTO 程序（kgrn/kfcd，不在本仓库）。

> `docs/refs/*.pdf`（AL-ZOUBI 学位论文等）已在 .gitignore 中排除。
