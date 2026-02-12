
---

# 論文資訊

**英文檔名：**
`A1_CFD_Discrete_Structural_Diagnosis_of_Incompressible_Projection_Methods_v1.0.0.md`

**中文標題：**
《A1-CFD 離散結構診斷：不可壓縮投影法中的共軛性與邊界一致性分析》

**英文標題：**
A1-CFD Discrete Structural Diagnosis: Conjugacy and Boundary Consistency in Incompressible Projection Methods

---

# A1-CFD 離散結構診斷：

## 不可壓縮投影法中的共軛性與邊界一致性分析

---

## 一、研究動機

不可壓縮流體的數值求解通常依賴投影法，其核心步驟為：

$$
\mathbf{u}^{n+1} = \mathbf{u}^* - \frac{\Delta t}{\rho} \nabla p
$$

其中壓力場 $p$ 由壓力泊松方程決定：

$$
\nabla^2 p = \frac{\rho}{\Delta t} \nabla \cdot \mathbf{u}^*
$$

在理論層面，若泊松方程被精確求解，則應有：

$$
\nabla \cdot \mathbf{u}^{n+1} = 0
$$

然而，在實際數值實現中，常觀察到以下現象：

* 壓力泊松方程的殘差已降至 $10^{-8}$ 甚至更低；
* 修正後的速度場散度卻停留在 $10^{-3}$ 等級；
* 提升線性求解器精度無法消除此誤差地板。

本研究旨在回答一個結構性問題：

> 投影法的失效究竟來自線性求解器不足，還是來自離散結構本身？

---

## 二、結構診斷框架

為區分數值收斂與結構一致性，我們建立以下診斷指標。

### 1. 壓力方程一致性指標

$$
\mathrm{ID_Used} = | \Delta_h p - b |
$$

其中 $b = \frac{\rho}{\Delta t} \nabla_h \cdot \mathbf{u}^*$。
此指標衡量泊松方程是否被正確求解。

---

### 2. 投影後散度

$$
\mathrm{Div_After} = | \nabla_h \cdot \mathbf{u}^{n+1} |
$$

此指標衡量物理不可壓縮條件是否實現。

---

### 3. 離散共軛性指標

$$
\mathrm{Op_Gap} =
\left|
\nabla_h \cdot \mathbf{u}^*_{\mathrm{mean-free}}
------------------------------------------------

\frac{\Delta t}{\rho}
\nabla_h \cdot \nabla_h p
\right|
$$

若離散算子滿足共軛性：

$$
\nabla_h \cdot \nabla_h p = \Delta_h p
$$

則 $\mathrm{Op_Gap}$ 應接近機器精度。

---

## 三、Collocated 網格的結構地板

在同位網格上，採用矩陣自由共軛梯度法（PCG）求解壓力泊松方程，得到：

$$
\mathrm{ID_Used} \approx 10^{-8}
$$

然而觀察到：

$$
\mathrm{Div_After} \approx 10^{-3}
$$

同時：

$$
\mathrm{Op_Gap} \approx 10^{-3}
$$

此結果說明：

* 線性子問題已收斂；
* 可解性條件已滿足；
* 但離散 div–grad–lap 鏈條不共軛。

即便 $\Delta_h p \approx b$ 成立，也無法保證：

$$
\nabla_h \cdot \mathbf{u}^{n+1} = 0
$$

此為結構性誤差地板，而非線性求解器問題。

---

## 四、MAC 交錯網格的離散共軛性

改用 MAC 交錯網格，在保持相同 PCG 求解器條件下，得到：

$$
\mathrm{ID_Used} \approx 10^{-10}
$$

$$
\mathrm{Div_After} \approx 10^{-13}
$$

$$
\mathrm{Op_Gap} \approx 10^{-13}
$$

三者同時降至機器精度量級。

此結果證明：

$$
\nabla_h \cdot \nabla_h p = \Delta_h p
$$

在離散層面精確成立。

MAC 網格確保了離散共軛性。

---

## 五、主動擾動驗證實驗

為排除偶然性，我們構造強散度初值場：

$$
\mathrm{Div_Star} \approx 4.82 \times 10^{-1}
$$

投影後得到：

$$
\mathrm{Div_Proj} \approx 10^{-13}
$$

且：

$$
\mathrm{Div_After} = \mathrm{Div_Proj}
$$

此結果說明：

* 投影鏈條可消除任意強散度；
* 在不干涉邊界的情況下，不存在散度回注；
* 結構閉合性在數值上成立。

---

## 六、邊界一致性分析

進一步對比兩種操作：

### 情況 A：投影後不修改邊界

$$
\mathrm{Div_After} \approx 10^{-13}
$$

### 情況 B：投影後重設法向邊界分量

實驗顯示，在 MAC 結構下僅重設法向分量並不導致散度增長。

這說明：

> 散度注入並非由邊界重設本身決定，而是由邊界操作是否破壞離散共軛鏈條決定。

在共軛結構下，只要邊界操作不破壞算子閉合性，散度不會被重新注入。

---

## 七、核心結論

本研究得到以下結論：

1. 線性求解器收斂不等同於物理收斂；
2. Collocated 網格存在離散算子不共軛問題；
3. MAC 網格在離散層面滿足算子共軛性；
4. 散度注入來源於結構破壞，而非單純邊界重設；
5. 投影法的成功條件為：

$$
\text{離散共軛性} + \text{邊界一致性}
$$

---

## 八、A1-CFD 框架的意義

A1-CFD 並非旨在提出新數值技巧，而是建立一套可遷移的結構診斷框架。
此框架能夠：

* 區分線性收斂與結構收斂；
* 檢測離散算子不一致；
* 分離邊界注入與算子地板；
* 為跨物理場問題提供結構性分析工具。

本章構成 A1-CFD 的第一個完整實證模組。

---

