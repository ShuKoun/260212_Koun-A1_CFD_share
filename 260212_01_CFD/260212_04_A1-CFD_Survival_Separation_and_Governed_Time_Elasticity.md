
---

# 檔案名稱

`A1-CFD_Survival_Separation_and_Governed_Time_Elasticity.md`

# 中文標題

A1-CFD 中之生存分離現象與時間彈性治理機制

# 英文標題

Survival Separation and Governed Temporal Elasticity in A1-CFD

---

## 1. 問題背景：顯式格式與 CFL 死亡區

對於不可壓縮 Navier–Stokes 方程之顯式時間離散格式，穩定性受到 CFL 條件限制。對於 MAC 網格上的離散速度場 $u, v$，定義

$$
CFL = \left( \frac{\max |u|}{\Delta x} + \frac{\max |v|}{\Delta y} \right)\Delta t
$$

當 $CFL$ 超過某一臨界值時，顯式對流項會導致數值解爆炸，即所謂 CFL Blowup。

在固定時間步長 $\Delta t$ 的 Baseline 模式中，一旦進入所謂「死亡區」（Kill Zone），數值解將不可逆崩潰。

本節目的在於展示：在完全相同的物理模型與離散算子下，A1 模式透過治理機制可在同一死亡區中存活，形成可重現的生存分離現象。

---

## 2. 對照實驗設計

### 2.1 物理與數值設定

* 雷諾數：$Re = 1000$
* 初始時間步長：$\Delta t_0 = 0.04$
* 網格：$40 \times 40$ MAC Staggered Grid
* 壓力求解器：Matrix-Free PCG
* 散度誤差度量：

$$
|\nabla_h \cdot \mathbf{u}|_2
$$

### 2.2 兩種模式

#### Baseline 模式

* 固定時間步長 $\Delta t = \Delta t_0$
* 無任何治理或回滾機制
* 若 $CFL > 1.5$ 則判定為死亡

#### A1_Governor 模式

* 初始 $\Delta t = \Delta t_0$
* 若偵測到

$$
CFL > C_{\text{safe}}
$$

其中 $C_{\text{safe}} = 1.0$，則：

1. 回滾至上一時間步狀態
2. 更新

$$
\Delta t \leftarrow 0.5 \Delta t
$$

3. 重新計算當前時間步

---

## 3. 實驗結果

### 3.1 Baseline 行為

在 $Re=1000, \Delta t_0=0.04$ 下，數值過程顯示：

* 前數步 $CFL$ 單調上升
* 於第 10 步出現

$$
CFL = 1.54
$$

* 系統觸發 CFL Blowup，計算終止

因此：

$$
\text{Baseline 在有限步數內死亡}
$$

---

### 3.2 A1_Governor 行為

同一組初始條件下，A1 模式出現如下治理事件：

1. 第 5 步：
   $$
   CFL > 1.0
   $$
   觸發回滾，$\Delta t$ 降至 $0.02$

2. 第 46 步：
   再次觸發治理，$\Delta t$ 降至 $0.01$

3. 之後全程穩定至第 200 步

在整個過程中：

$$
|\nabla_h \cdot \mathbf{u}|_2 \approx 10^{-9}
$$

壓力泊松方程之殘差保持在容差內，PCG 迭代次數穩定。

因此：

$$
\text{A1 模式在同一死亡區中完成完整模擬}
$$

---

## 4. 生存分離現象（Survival Separation）

定義：

若在相同物理模型、相同空間離散、相同初始條件下，存在

$$
\text{Baseline 死亡} \quad \text{且} \quad \text{A1 存活}
$$

則稱發生「生存分離現象」。

本實驗明確滿足此條件。

---

## 5. 時間彈性（Temporal Elasticity）

A1 模式的核心差異不在於更高階離散，也不在於更強算子，而在於時間治理：

$$
\Delta t_{n+1} = \alpha \Delta t_n
$$

其中 $0 < \alpha < 1$，並由數值風險指標觸發。

此機制賦予系統一種「時間彈性」：

* 當進入高風險區域時，自動縮小時間尺度
* 當遠離風險時，可保持穩定運行

這種彈性使得系統在同一相空間中避免數值崩潰，而非僅僅延後崩潰。

---

## 6. 幾何守恆未受破壞

值得注意的是，在整個治理過程中：

$$
|\nabla_h \cdot \mathbf{u}|_2 \sim 10^{-9}
$$

表明：

* 投影算子之離散共軛性未受影響
* 幾何約束（不可壓縮條件）始終成立
* 治理機制未破壞結構穩定性

---

## 7. 結論

本節證明：

1. 在顯式對流主導之死亡區內，固定步長 Baseline 會發生不可逆崩潰。
2. A1 模式透過回滾與時間步長治理，在完全相同條件下成功存活。
3. 此存活並非以幾何守恆為代價，而是在保持散度誤差極小的前提下完成。

因此，A1-CFD 在此案例中展示了：

$$
\text{Survival Superiority under Identical Physics}
$$

此結果與 A1-GR 中所觀察到的「高壓走廊存活能力」在結構上完全一致，表明 A1 母算法具備跨領域的一致性治理能力。

---

