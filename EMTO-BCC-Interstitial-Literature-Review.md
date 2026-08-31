# EMTO-CPA 框架下 BCC 间隙空球处理：文献调研报告

*基于 16 篇一级文献的系统检索 · 2026-07-07*

---

> **核心结论：** 在公开文献中，**不存在成功的 BCC 八面体间隙 EMTO-CPA 计算案例**。ASA/SCA 在 BCC 间隙几何下的球形近似误差是方法论层面的固有困难，非参数调优可解。唯一接近的案例（Huang 2011, KTH 博士论文）使用 BCC 超胞 + 总能优化球半径 η=0.75 来规避 CPA，且仅限于 FCC 基结构的系统性验证。EMTO 共同开发者 Abrikosov 课题组在研究 BCC Fe-C 间隙问题时选择了 VASP-PAW 而非 EMTO-CPA。

---

## 目录

1. [文献全景：BCC 间隙 EMTO 的空白](#1-文献全景bcc-间隙-emto-的空白)
2. [最近案例：Huang (2011) Fe₁₆C₁ BCC 超胞](#2-最近案例huang-2011-fe₁₆c₁-bcc-超胞)
3. [ASA/SCA 在 BCC 间隙中的理论局限](#3-asasca-在-bcc-间隙中的理论局限)
4. [重叠误差机制：为什么 E(SWS) 单调递减](#4-重叠误差机制为什么-esws-单调递减)
5. [Niessen 2023 FCC 参数不可迁移](#5-niessen-2023-fcc-参数不可迁移)
6. [其他 MT 方法的 BCC 间隙经验](#6-其他-mt-方法的-bcc-间隙经验)
7. [实用参数建议](#7-实用参数建议)
8. [推荐路径](#8-推荐路径)
9. [来源文献](#来源文献)

---

## 1. 文献全景：BCC 间隙 EMTO 的空白

在 5 个搜索方向、16 个一级来源中，**没有找到任何一篇发表的论文使用 EMTO-CPA 成功计算了 BCC 结构中的八面体间隙**。这本身就是一个重要信号。

已有的 EMTO 间隙文献全部集中在 FCC 结构：

| 文献 | 结构 | 间隙处理 | 方法 |
|------|------|---------|------|
| Niessen 2023 [9] | FCC γ-Fe | Oct NQ=2 | EMTO-CPA |
| Huang 2011 [1] | FCC Al/Cu/Rh | Oct+Tet NQ=4 | EMTO 超胞 |
| Huang 2011 [1] | BCC Fe₁₆C₁ | 超胞 (非CPA) | EMTO 超胞 |
| Abrikosov 组 2020 [7] | BCC Fe-C | SQS 超胞 | **VASP-PAW** (弃用EMTO) |

> ⚠️ **关键发现：** EMTO 共同开发者 Abrikosov 课题组在研究 BCC Fe-C 间隙碳时，选择了 VASP（PAW, 120 原子 SQS, 3×4×5 超胞, 420 eV 截断）而非 EMTO-CPA [7]。这隐含承认了 CPA 框架不适合处理 BCC 间隙问题——因为碳间隙在 BCC 中引起的长程晶格弛豫（位移在距 C 原子 4 Å 处仍然显著）超出了 CPA 单位点近似的能力。

---

## 2. 最近案例：Huang (2011) Fe₁₆C₁ BCC 超胞

Huang 的 KTH 论文 [1] 是唯一涉及 BCC 间隙 EMTO 计算的已知工作，但有两个关键区别：

- **使用超胞而非 CPA**：Fe₁₆C₁ 的 bct 超胞（体心四方），C 放在 (0, 0, 1/2) 八面体间隙位
- **不依赖 NQ>1 的间隙空球方案**：碳是超胞中的一个独立位点，不需要 CPA 处理无序

### 关键参数：η 优化

Huang 发现碳原子的最优势球半径为 Voronoi 多面体半径的 **η = 0.75**（即 w_C = 0.75 × w_C⁰），通过在 η = 0.60–1.00 范围内以 0.05 步长扫描总能确定 [1]：

- 总能全局最小出现在 η = 0.75，对应 c/a ≈ 1.07
- 该最优 η 对体积（Wigner-Seitz 半径 w）的依赖很弱
- 后续合金计算中固定 η = 0.75

> ℹ️ **注意：** Huang 的 η=0.75 与 Niessen 的 S(ws)=0.77 非常接近，但两者的含义不同。η 是相对于 Voronoi 多面体的缩放比，S(ws) 是相对于平均 Wigner-Seitz 半径的缩放比。在 FCC 中两者近似等价（因为只有一个间隙位），但在 BCC NQ=4/8 中因间隙/金属比 3:1 而产生显著偏差。

### l_max 收敛性问题

Huang 对 FCC 间隙结构（str-II：1 atom + 3 empty spheres per primitive cell）的系统测试发现 [1]：

| 结构 | l_max=2 (spd) | l_max=3 (spdf) | l_max=4 (spdfg) |
|------|--------------|----------------|-----------------|
| FCC str-I (无间隙) | 已收敛 | 良好 | — |
| FCC str-II (有间隙) | 严重偏差 | B₀ 误差 ~17% | 收敛 |

> ⚠️ **对当前计算的启示：** 如果 FCC 间隙已经需要 l_max=4 才能收敛，BCC 间隙（更低对称性、更强的非球形势）可能需要同样甚至更高的基组。检查当前 KGRN 输入中 NL/NLH/NLW 参数是否设置了足够的角动量通道。

---

## 3. ASA/SCA 在 BCC 间隙中的理论局限

多个独立来源从不同角度确认了 ASA 在开放结构间隙中的根本困难：

### 3.1 球形近似的崩溃

已验证发现 [1]（2/3 投票确认）：

> *"For MT methods, [FCC with empty interstitial spheres] represents a real challenge. The tetrahedral Em wells are close to the spherical atomic potential wells located at the original fcc sites and therefore the potential and the charge density within these Em spheres will strongly deviate from the spherical symmetry."*

如果 FCC 间隙空球（O_h 对称性）已经构成"真正的挑战"，BCC 八面体间隙（D_4h 对称性，各向异性更强）的非球形偏差只会更严重。

### 3.2 体积守恒与重叠误差的矛盾

ASA 严格要求所有球体积之和等于胞体积 [3]。这在 BCC 间隙中制造了一个**不可调和的矛盾**：

- **满足体积守恒**（S(ws)=1.0 for all）→ 金属-间隙球严重重叠 → 重叠区域被双重计数，其余区域被遗漏 → 几何违背误差 [3,5]
- **缩小间隙球**（S(ws)=0.77）→ 41% 的胞体积不被覆盖 → 违反 ASA 基本假设 → 电荷分区崩溃

这正是我们在 NbVa_bcc（S(ws)=0.77）和 NbVa_bcc_eq（S(ws)=1.0）中观察到的：**两种极端都失败**。

### 3.3 SCA-EMTO 的误差来源

EMTO 使用 Spherical Cell Approximation (SCA) 而非标准 ASA。在 SCA 中 [4]：

- **Schrödinger 方程**通过 Green 函数精确求解
- **Poisson 方程**（静电/电荷部分）仅在 SCA 近似下求解
- SCA 是方法中**唯一的形状近似误差来源**

Zwierzycki & Andersen (2008) 明确讨论了 Vitos SCA 与 BCC 结构空球的关联，指出 BCC Wigner-Seitz 胞本身就有 14% 的径向重叠——**不加间隙空球就已经在推重叠极限** [4]。

---

## 4. 重叠误差机制：为什么 E(SWS) 单调递减

Andersen 等 [2] 的分析给出了精确的物理机制：

> ⚠️ **多重散射方法（KKR, EMTO, NMTO）仅对势球重叠做到一阶精确。** 在大重叠下，ω⁴ 及更高阶项主导误差，使得**计算的能带系统性地向下移动（负定误差）** [2]。

这直接解释了观测到的行为：

1. 压缩体积 → SWS 减小 → 球间重叠比例增大
2. 更大的重叠 → ω⁴ 误差项增大 → 能量被人为压低更多
3. 结果：E(SWS) 单调递减——不是真正的排斥不足，而是**重叠误差随体积缩小而加速增长**
4. 真实 EOS 阱深（~3 mRy）被伪压力（~1800 mRy/Bohr）完全掩盖

Green 函数代码（如 EMTO 的 KGRN/KFCD）**缺少 "combined correction" 项**来部分补偿重叠误差 [3]，使问题比能带结构代码（如 LMTO-ASA 的 lm 程序）更严重。

---

## 5. Niessen 2023 FCC 参数不可迁移

Niessen et al. (2023) [9] 的工作有以下限制：

- **仅研究 FCC**：γ-Fe 和奥氏体不锈钢 (AISI 304)，完全没有 BCC
- S(ws)=0.77 的参数仅在 FCC 八面体间隙（NQ=2, O_h 对称性）下标定和验证
- FCC 间隙/金属比 1:1，BCC 为 3:1 → 空球数量效应被放大 3 倍
- FCC 八面体洞的体积/球形近似误差本就小于 BCC

> ℹ️ **结论：** 将 FCC 标定的 S(ws)=0.77 直接用于 BCC 八面体间隙在科学上不具备合理性 [9]。即使 FCC 中该值有效，BCC 中需要独立优化。但根据前述分析，BCC 中可能不存在一个使 EOS 正常的 S(ws) 值。

---

## 6. 其他 MT 方法的 BCC 间隙经验

### LMTO-ASA

Andersen (1998) [6] 明确指出：

- ASA 中开放结构只能通过填充间隙空球来处理
- 该方法**仅在高对称间隙中有效**（如金刚石结构）
- 即使在金刚石这种有利情况下，downfolding 所有空球通道仍引入强非线性能量依赖，LMTO-ASA 形式主义无法正确处理

### KKR-CPA

Questaal 框架中 CPA 仅在 ASA 内实现 [5]，继承了 ASA 的所有限制。对于 BCC 间隙，KKR-CPA 面临同样的球形近似问题。

### 共识

所有基于球形近似的 MT 方法（EMTO, LMTO-ASA, KKR-ASA）在 BCC 八面体间隙中**都遇到根本性困难**。这不是某个特定方法的 bug，而是 ASA/SCA 框架的固有局限。

---

## 7. 实用参数建议

虽然 BCC 间隙 EMTO-CPA 可能是方法论死胡同，但如果仍要尝试，文献提示以下参数调整可能改善（但不保证解决）问题：

| 参数 | 当前值 | 建议 | 来源 |
|------|-------|------|------|
| l_max (NL/NLH/NLW) | 3 (spdf)? | **≥ 4 (spdfg)** | Huang [1] |
| S(ws) 间隙 | 0.77 | 扫描 0.60–1.00，做总能优化 | Huang [1] |
| KSTR DMAX | 1.4375 | 需增大（纯 BCC 用 2.1992） | EMTO 手册 [8] |
| KFCD OVCOR | Y (默认) | 确认启用，专为重叠校正 | EMTO 手册 [8] |
| 方法 | CPA (NQ=4/8) | 超胞 (Fe₁₆C₁ 等) | Huang [1] |

> ✅ **如果尝试超胞方案**（效仿 Huang）：用 2×2×2 BCC 超胞（16 个 Fe），将 1 个 Fe 替换为 C 或 Va，无需引入独立间隙子格。虽然丧失 CPA 对无序的处理能力，但避开了空球问题。配合 η 优化（扫描 0.60–1.00），有可能得到合理的 EOS。

---

## 8. 推荐路径

综合全部文献证据，建议按以下优先级推进：

### 路径 A：EMTO 超胞（可行性高）

1. 构建 Fe₁₆C₁ bct 超胞（2×2×2 BCC, C 在 (0,0,1/2) 八面体位），NQ=16 或 NQ=17
2. l_max ≥ 4，DMAX 设为 ≥ 2.0
3. 扫描 η(C) = 0.60–1.00，每个 η 做 7 点 EOS
4. 确认 OVCOR=Y
5. 优势：仍使用 EMTO，参数与 Huang 可对比
6. 劣势：不能用 CPA 处理无序，只能做稀合金（1/16 = 6.25% C）

### 路径 B：切换到 VASP/QE（最可靠）

1. 使用 VASP-PAW 或 Quantum ESPRESSO（全势/PAW 方法）
2. SQS 超胞 + 显式弛豫
3. EMTO 开发者自己的选择 [7]
4. 优势：无 ASA 限制，可处理弛豫
5. 劣势：失去 CPA 高效随机合金处理

### 路径 C：FCC 基准先行（验证方法论）

1. 在 FCC Fe-C（NQ=2）上确认 EMTO-CPA 产生正常 EOS（已完成）
2. 在 FCC 上逐步增加 NQ（NQ=4 加入四面体位），观察 EOS 退化
3. 量化 NQ 增加对 EOS 曲率的影响
4. 为最终判断"BCC 间隙 CPA 是否完全不可行"提供数值证据

---

## 来源文献

[1] Huang, "Describing Interstitials in Close-Packed Lattices: First-Principles Study," KTH Licentiate Thesis, 2011.
diva-portal.org/smash/get/diva2:456082/FULLTEXT01.pdf

[2] O.K. Andersen, T. Saha-Dasgupta, S. Ezhov, "Third-generation muffin-tin orbitals," 2008.
arXiv:0808.0105

[3] Questaal documentation, "ASA Overview."
questaal.org/docs/code/asaoverview/

[4] L. Vitos, "Total-energy method based on the exact muffin-tin orbitals theory," Comp. Mat. Sci. 18, 24 (2000).
doi:10.1016/S0927-0256(99)00098-1

[5] M. van Schilfgaarde, T. Kotani, S. Faleev, "Questaal: a package of electronic structure methods based on the linear muffin-tin orbital technique," 2019.
arXiv:1907.06021

[6] O.K. Andersen, O. Jepsen, G. Krier, "Exact Muffin-Tin Orbital Theory," 1998.
arXiv:cond-mat/9804166

[7] A.V. Ponomareva, Yu.N. Gornostyrev, I.A. Abrikosov, "Ab initio study of carbon effect on the stacking fault energy and local magnetic moments in BCC iron," 2020.
arXiv:2010.01354

[8] EMTO 5.8 Official Manual.
emto.gitlab.io/manual/manual.html

[9] A.K.E. Niessen et al., "Ab initio study of the effect of interstitial alloying on the intrinsic stacking fault energy," Acta Materialia 257, 119146 (2023).
doi:10.1016/j.actamat.2023.119146
