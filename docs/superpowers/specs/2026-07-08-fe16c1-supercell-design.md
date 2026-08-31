# Fe₁₆C₁ BCC 超胞 EMTO 计算设计

## 1. 背景与动机

EMTO-CPA 框架下所有包含八面体间隙空球（NQ>1）的 BCC 结构计算均无法产生正常 EOS 极小值（详见 `EMTO-BCC-Interstitial-EOS-Failure-Analysis.md`）。根因是 ASA/SCA 球形近似在 BCC 间隙几何下引入体积依赖的伪能量，掩盖真实 EOS 曲率。

Al-Zoubi et al. (PRB 85, 014112, 2012) 使用 Fe₁₆C₁ 超胞方法成功规避了此问题：不引入间隙空球子格和 CPA，直接将 C 作为超胞中的独立原子位点，并通过 η 优化势球半径。EMTO 结果与 VASP-PAW 吻合良好（(c/a)_eq ≈ 1.07）。

本设计复现 Al-Zoubi 的超胞方案，分三步推进。

## 2. 超胞几何与 Zener 有序

### 2.1 Zener 有序与四方畸变的物理前提

BCC 中有 3 族等价的八面体间隙位，分别沿 x、y、z 轴排列：

```
x 族: (a/2, 0, 0) 及其平移等价位 — 2 个近邻 Fe 沿 x 轴, 距离 a/2
y 族: (0, a/2, 0) 及其平移等价位 — 2 个近邻 Fe 沿 y 轴, 距离 a/2
z 族: (0, 0, a/2) 及其平移等价位 — 2 个近邻 Fe 沿 z 轴, 距离 a/2
```

C 在三族间的分布决定对称性：

| C 分布 | 对称性 | 结构 | 物理场景 |
|--------|--------|------|---------|
| 三族等概率占据 | 立方 O_h | BCC | 高温无序固溶体 |
| 全部占据 z 族 | 四方 D_4h | BCT | 完全 Zener 有序 → 马氏体 |
| 部分偏好 z 族 | 四方（较弱） | BCT | 部分有序，实验常见 |

Fe₁₆C₁ 超胞中 C 放在 z 族八面体位 = 100% Zener 有序，对应完全有序马氏体。碳钢淬火后 C 自发占据单一子格，产生四方畸变。

### 2.2 四方畸变的力学机制

C 坐在 z 族八面体位 (0, 0, a/2) 时：

- 沿 z：C 将两侧 Fe（距离 a/2）推开 → c 增大
- 沿 x, y：Poisson 效应 + 电子重新分布 → a 缩小
- 结果：c/a > 1，BCC → BCT

实验经验公式：c/a ≈ 1 + 0.046 × wt%C。对于 Fe₁₆C₁（≈1.3 wt%C），预期 c/a ≈ 1.06–1.07。Al-Zoubi 的 EMTO 和 VASP 均给出 (c/a)_eq ≈ 1.07。

### 2.3 超胞构造

2×2×2 BCC 常规胞 → 简单四方（ST）超胞，边长 2a × 2a × 2c。

17 个原子的分数坐标（超胞坐标系）：

```
# 8 Fe — (0,0,0) 子格 (常规胞顶点):
Fe1:  (0.00, 0.00, 0.00)    Fe5:  (0.50, 0.50, 0.00)
Fe2:  (0.50, 0.00, 0.00)    Fe6:  (0.50, 0.00, 0.50)
Fe3:  (0.00, 0.50, 0.00)    Fe7:  (0.00, 0.50, 0.50)
Fe4:  (0.00, 0.00, 0.50)    Fe8:  (0.50, 0.50, 0.50)

# 8 Fe — (½,½,½)a 子格 (体心位):
Fe9:  (0.25, 0.25, 0.25)    Fe13: (0.75, 0.75, 0.25)
Fe10: (0.75, 0.25, 0.25)    Fe14: (0.75, 0.25, 0.75)
Fe11: (0.25, 0.75, 0.25)    Fe15: (0.25, 0.75, 0.75)
Fe12: (0.25, 0.25, 0.75)    Fe16: (0.75, 0.75, 0.75)

# 1 C — z 族八面体间隙位 (Zener 有序, 四方轴沿 z):
C1:   (0.00, 0.00, 0.25)    ← Cartesian: (0, 0, a/2)
```

四方轴沿 z → C 在 z 族 → EMTO 的 c/a 参数直接对应物理四方畸变。

NQ=17, NT=2（Fe=IT1, C=IT2）。无 CPA——每个位点 100% 单一元素。

## 3. 势球半径与体积守恒

### 3.1 体积守恒条件

EMTO 中每个原子的势球半径 R_i = SWS × S(ws)_i，体积守恒要求：

```
Σ S(ws)_i³ = NQ = 17
→ 16 × S(ws)_Fe³ + 1 × S(ws)_C³ = 17
→ S(ws)_Fe = ((17 - S(ws)_C³) / 16)^(1/3)
```

### 3.2 S(ws)_C 扫描方案

直接扫描 S(ws)_C，不经过 η-Voronoi 中间步骤（避免 Voronoi 半径的不确定性）：

```python
s_ws_C_values = [0.40, 0.45, 0.50, 0.55, 0.60]
```

对应的 S(ws)_Fe（体积守恒）：

| S(ws)_C | S(ws)_Fe | 注释 |
|---------|----------|------|
| 0.40 | 1.019 | 扫描下界 |
| 0.45 | 1.019 | |
| 0.50 | 1.018 | |
| 0.55 | 1.017 | Al-Zoubi η=0.75 附近 |
| 0.60 | 1.016 | 扫描上界 |

S(ws)_Fe 对 S(ws)_C 几乎不敏感（1 个 C 球 vs 16 个 Fe 球）。

## 4. pyemto 脚本参数

### 4.1 Lattice 生成

```python
basis = np.array([
    [0.00, 0.00, 0.00], [0.50, 0.00, 0.00],
    [0.00, 0.50, 0.00], [0.00, 0.00, 0.50],
    [0.50, 0.50, 0.00], [0.50, 0.00, 0.50],
    [0.00, 0.50, 0.50], [0.50, 0.50, 0.50],
    [0.25, 0.25, 0.25], [0.75, 0.25, 0.25],
    [0.25, 0.75, 0.25], [0.25, 0.25, 0.75],
    [0.75, 0.75, 0.25], [0.75, 0.25, 0.75],
    [0.25, 0.75, 0.75], [0.75, 0.75, 0.75],
    [0.00, 0.00, 0.25],   # C — z-type octahedral
])

sys.lattice.set_values(
    jobname_lat='fe16c1',
    latpath='.',
    lat='sc',
    basis=basis,
    kappaw=[0.0, -0.2],
)
```

c/a=1.0 时用 `lat='sc'`。c/a≠1 的 Step 3 需确认 pyemto 对简单四方的支持方式。

### 4.2 KGRN/KFCD 参数

```python
atoms = np.array(['Fe']*16 + ['C'])
iqs   = np.arange(1, 18, dtype='int32')
its   = np.array([1]*16 + [2], dtype='int32')
itas  = np.array([1]*17, dtype='int32')
concs = np.array([100.0]*17)
splts = np.array([2.0]*16 + [0.0])

s_wss   = np.array([s_ws_Fe]*16 + [s_ws_C])
ws_wsts = np.array([s_ws_Fe]*16 + [s_ws_C])

sys.bulk_new(
    lat='sc',
    jobname='fe16c1',
    latname='fe16c1',
    latpath='.',
    ibz=1,                  # SC Brillouin zone
    atoms=atoms, iqs=iqs, its=its, itas=itas,
    concs=concs, splts=splts,
    sws=sws_val,
    s_wss=s_wss, ws_wsts=ws_wsts,
    afm='F',                # 铁磁
    xc='PBE',
    expan='S',
    sofc='Y',
    niter=500,
    amix=0.02,
    efmix=1.0,
    tole=1.0e-7, tolef=1.0e-7,
    mmom=2.2,
    nkx=9, nky=9, nkz=9,   # ~40 IBZ k-points
    lmaxh=8, lmaxt=4,       # spdfg
    depth=0.6,              # Al-Zoubi 使用 0.6 Ry
    imagz=0.02,
    tfermi=500.0,
    ncpu=4,
)
```

### 4.3 与现有脚本的关键差异

| 参数 | Fe_bcc (NQ=1) | FeC_bcc CPA (NQ=4) | Fe₁₆C₁ 超胞 (NQ=17) |
|------|---------------|---------------------|----------------------|
| lat | 'bcc' | 'bcc' | 'sc' |
| NQ | 1 | 4 | 17 |
| CPA | 无 | Va+C 混合 | 无 |
| ibz | 3 (BCC) | 3 (BCC) | 1 (SC) |
| depth | 1.0 | 1.0 | 0.6 |
| niter | 500 | 100 | 500 |
| k-mesh | 21³ | 21³ | 9³–13³ |
| S(ws) | 全 1.0 | Fe=1.0, Va/C=0.77 | Fe≈1.017, C≈0.50–0.55 |

## 5. 脚本结构与文件组织

### 5.1 目录结构

```
FeC-BCC-EMTO/
├── lattice/
│   └── bcc_sc17/           # Fe₁₆C₁ KSTR/BMDL/SHAPE
├── FeC_bcc_sc/             # 计算主目录
│   ├── bmdl -> ../lattice/bcc_sc17/bmdl
│   ├── kstr -> ../lattice/bcc_sc17/kstr
│   ├── shape -> ../lattice/bcc_sc17/shape
│   ├── kgrn/
│   ├── kfcd/
│   └── fit/
├── FeC_bcc_sc_eta.py       # Step 1: S(ws)_C 扫描 (5 jobs)
├── FeC_bcc_sc_eos.py       # Step 2: EOS, c/a=1 (7 jobs)
└── FeC_bcc_sc_2d.py        # Step 3: 2D (w, c/a) map (42 jobs, 后续)
```

### 5.2 三步计算方案

**Step 1 — S(ws)_C 扫描**
- 固定 w=2.65 Bohr, c/a=1.0
- S(ws)_C = [0.40, 0.45, 0.50, 0.55, 0.60], 共 5 个 KGRN+KFCD job
- 目标：找总能极小对应的最优 S(ws)_C
- Lattice 文件生成一次（c/a=1 固定）

**Step 2 — EOS (c/a=1)**
- 固定 c/a=1.0, 使用 Step 1 的最优 S(ws)_C
- w = linspace(2.60, 2.70, 7), 共 7 个 job
- 目标：确认 E(w) 有抛物线极小值，拟合 w_eq 和 B₀
- 共用 Step 1 的 lattice 文件

**Step 3 — 2D (w, c/a) map**（后续实现）
- 固定最优 S(ws)_C
- w = linspace(2.60, 2.70, 6) × c/a = linspace(0.95, 1.10, 7) = 42 jobs
- 每个 c/a 需独立 lattice 文件
- 目标：找 (w_eq, (c/a)_eq) 二维极小，对标 Al-Zoubi

### 5.3 每步脚本均自包含

每个 .py 脚本完整包含：超胞坐标定义、S(ws) 计算、lattice 生成（或符号链接）、KGRN/KFCD/batch 输出。代码有重复但每个脚本可独立运行，符合现有 repo 惯例。

## 6. 验证与预期结果

### 6.1 Step 1 验证

E(S(ws)_C) 应有单一极小值。预期最优 S(ws)_C ≈ 0.50–0.55（对应 Al-Zoubi η ≈ 0.75 附近）。

### 6.2 Step 2 验证

| 量 | Al-Zoubi (EMTO) | Al-Zoubi (VASP) | 允许范围 |
|---|---|---|---|
| w_eq (Bohr) | 2.646 | 2.639 | 2.63–2.66 |
| E(w) 曲线 | 抛物线 | — | 必须有极小 |

关键验证：E(SWS) 必须有抛物线极小值——这正是 CPA+空球方案失败的地方。

### 6.3 Step 3 验证

| 量 | Al-Zoubi | 允许偏差 |
|---|---|---|
| w_eq | 2.646 Bohr | ±0.02 |
| (c/a)_eq | 1.070 | ±0.01 |
| ΔE(c/a=1.15 vs 1.1) | 0.938 mRy/atom | ±0.3 |

### 6.4 收敛性风险

| 风险 | 应对 |
|------|------|
| NQ=17 SCF 不收敛 | 降 AMIX 至 0.01；增 NITER 至 1000 |
| 计算时间过长 | 先跑单点测试估算 wall time |
| pyemto 对 NQ=17 生成异常 | 检查 KSTR 输出，手动对比坐标 |
| k-mesh 不够密 | 从 9³ 增到 13³ |

### 6.5 建议先跑单点测试

在生成全部扫描前，先跑 1 个 KGRN+KFCD job（w=2.65, S(ws)_C=0.50, c/a=1.0），确认：
1. KSTR/BMDL/SHAPE 正常完成
2. KGRN 收敛
3. KFCD 产出总能量
4. 记录 wall time

## 7. 来源文献

- Al-Zoubi et al., PRB 85, 014112 (2012) — Fe₁₆C₁ 超胞 EMTO+CPA 方法与参数
- Al-Zoubi, KTH Doctoral Thesis (2011) — η 优化详细过程
- 本项目 `EMTO-BCC-Interstitial-EOS-Failure-Analysis.md` — CPA+空球方案失败分析
- 本项目 `EMTO-BCC-Interstitial-Literature-Review.md` — 文献综述
