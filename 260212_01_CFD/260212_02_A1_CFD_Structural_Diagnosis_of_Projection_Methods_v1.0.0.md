
---

# 論文資訊

**英文檔名：**
`A1_CFD_Structural_Diagnosis_of_Projection_Methods_v1.0.0.md`

**中文標題：**
《A1-CFD 結構診斷：不可壓縮投影法的離散共軛性與邊界注入機制》

**英文標題：**
A1-CFD Structural Diagnosis: Discrete Conjugacy and Boundary Injection Mechanisms in Incompressible Projection Methods

---

# A1-CFD 結構診斷：

## 不可壓縮投影法的離散共軛性與邊界注入機制

---

## 一、研究問題與核心命題

不可壓縮流體的投影法（Projection Method）在理論上基於如下關係：

$$
\mathbf{u}^{n+1} = \mathbf{u}^* - \frac{\Delta t}{\rho} \nabla p
$$

其中壓力 $p$ 由壓力泊松方程決定：

$$
\nabla^2 p = \frac{\rho}{\Delta t} \nabla \cdot \mathbf{u}^*
$$

若壓力方程被精確求解，則應有：

$$
\nabla \cdot \mathbf{u}^{n+1} = 0
$$

然而在實際數值實現中，常出現以下現象：

* 壓力泊松方程殘差已達 $10^{-8}$ 或更低；
* 但修正後速度場散度仍停留於 $10^{-3}$ 等級；
* 增加線性迭代次數無法消除該誤差地板。

本章旨在回答以下結構性問題：

1. 此誤差是否來自線性求解器不足？
2. 是否源於可解性條件違反？
3. 是否來自離散算子不共軛？
4. 是否為邊界條件在投影後重新注入散度？

---

## 二、結構診斷指標體系

為區分上述可能來源，我們引入四項結構指標。

### 1. 壓力方程誠實度

$$
\mathrm{ID_Used} = | \Delta_h p - b |
$$

檢驗壓力泊松方程是否真正被解開。

---

### 2. 投影後散度

$$
\mathrm{Div_After} = | \nabla_h \cdot \mathbf{u}^{n+1} |
$$

衡量投影是否成功消除散度。

---

### 3. 算子縫隙

$$
\mathrm{Op_Gap} =
\left|
\nabla_h \cdot \mathbf{u}^*_{\mathrm{mean-free}}
------------------------------------------------

\frac{\Delta t}{\rho}
\nabla_h \cdot \nabla_h p
\right|
$$

若離散算子滿足共軛性，則：

$$
\nabla_h \cdot \nabla_h p = \Delta_h p
$$

此時 $\mathrm{Op_Gap}$ 應接近機器精度。

---

### 4. 可解性條件

$$
\int_{\Omega} b , d\Omega = 0
$$

若不滿足此條件，純 Neumann 邊界下泊松方程無解。

---

## 三、Case A：Collocated Grid

在同位網格（Collocated Grid）下，採用矩陣自由 PCG 將壓力泊松方程殘差壓至：

$$
\mathrm{ID_Used} \approx 10^{-8}
$$

然而觀察到：

$$
\mathrm{Div_After} \approx 10^{-3}
$$

同時：

$$
\mathrm{Op_Gap} \sim 10^{-3}
$$

此結果說明：

* 線性子問題已收斂；
* 可解性條件已滿足；
* 但離散 div–grad–lap 鏈條不共軛。

即使 $\Delta_h p \approx b$ 成立，仍無法保證：

$$
\nabla_h \cdot \mathbf{u}^{n+1} = 0
$$

此即結構性誤差地板。

---

## 四、Case B：MAC Staggered Grid

改用 MAC 交錯網格，在保持相同 PCG 求解器條件下，觀察到：

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

此證明：

$$
\nabla_h \cdot \nabla_h p = \Delta_h p
$$

在離散層面上成立。

因此 MAC 網格確保離散共軛性。

---

## 五、邊界注入機制驗證

在 MAC 結構下進一步進行邊界操作對照實驗。

### 情況一：投影後不重設邊界

對任意強擾動場（人工製造）：

$$
\mathrm{Div_Star} \approx 4.82 \times 10^{-1}
$$

投影後：

$$
\mathrm{Div_Proj} \approx 10^{-13}
$$

若不重新設定邊界：

$$
\mathrm{Div_After} = \mathrm{Div_Proj}
$$

證明投影鏈條完整且無散度回注。

---

### 情況二：投影後強制重設邊界

若在投影後手動重設部分速度分量，則觀察到：

$$
\mathrm{Div_After} \gg \mathrm{Div_Proj}
$$

此證明：

散度誤差可由邊界條件重設重新注入。

---

## 六、結構性結論

本章得到三項關鍵結論：

1. 壓力方程線性收斂不足以保證物理收斂；
2. Collocated 網格存在離散算子不共軛問題；
3. MAC 網格可在離散層面實現算子共軛性；
4. 邊界條件施加策略可重新注入散度。

因此，不可壓縮投影法的精度取決於：

$$
\text{離散共軛性} + \text{邊界一致性}
$$

而非僅僅線性求解器強度。

---

## 七、A1-CFD 框架的意義

本研究顯示 A1-CFD 可：

* 區分線性收斂與物理收斂；
* 定位離散算子不一致；
* 檢測邊界散度注入；
* 驗證結構重構效果。

A1 在 CFD 中的價值不在於提供新型數值技巧，而在於：

$$
\text{建立可遷移的結構診斷框架}
$$

此框架可跨物理場應用於：

* 半導體泊松–漂移系統；
* 相對論約束方程；
* 多場耦合問題。

---

## 八、章節總結

本章完成以下閉環驗證：

1. 定位 Collocated 結構地板；
2. 證明 MAC 離散共軛性；
3. 驗證邊界注入機制；
4. 建立 A1 結構診斷體系。

此結果構成 A1-CFD 的第一個完整實證章節。

---

