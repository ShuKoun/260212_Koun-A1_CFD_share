
---

# 論文資訊

**英文檔名：**
`A1_CFD_Structural_Diagnosis_of_Projection_Methods_MAC_vs_Collocated_v1.0.0.md`

**中文標題：**
《不可壓縮投影法的結構診斷：從同位網格到 MAC 網格的幾何重構實證》

**英文標題：**
Structural Diagnosis of Incompressible Projection Methods: A Geometric Reconstruction from Collocated to MAC Grids

---

# 不可壓縮投影法的結構診斷：

## 從同位網格到 MAC 網格的幾何重構實證

---

## 一、研究動機：線性收斂與物理收斂的分離

不可壓縮流體數值模擬中，投影法是一種廣泛使用的時間離散框架。其基本步驟如下：

1. 計算暫態速度場 $ \mathbf{u}^* $；
2. 解壓力泊松方程；
3. 透過壓力梯度修正速度，使其滿足離散不可壓縮條件。

在理論上，若壓力泊松方程被精確求解，則修正後速度場應滿足：

$$
\nabla \cdot \mathbf{u}^{n+1} = 0.
$$

然而在實務計算中，常觀察到如下現象：

* 壓力泊松方程的殘差已降至 $10^{-8}$ 或更低；
* 修正後速度散度仍停留在 $10^{-3}$ 等級；
* 增加線性迭代次數或提升求解器精度，無法進一步降低散度。

此現象顯示，問題未必來自線性收斂不足，而可能來自離散結構本身。

本章目標為建立一套結構診斷流程，區分以下四類可能來源：

1. 可解性違反，即 $ \int_\Omega b , d\Omega \neq 0 $；
2. 線性子問題未充分收斂；
3. 離散算子不一致，即 $ \nabla_h \cdot \nabla_h \neq \Delta_h $；
4. 網格拓撲所導致的結構性誤差地板。

---

## 二、數值實驗設計

為避免非線性對流項干擾，本研究採用 Stokes 模式，即凍結對流項，只保留擴散與投影步驟。

實驗條件如下：

* 二維 Lid-Driven Cavity；
* Reynolds 數 $ Re = 100 $；
* 相同時間步長 $ \Delta t $；
* 相同壓力泊松求解器：矩陣自由 PCG；
* 僅改變網格幾何結構。

對照組設定如下：

| Case | 網格型式               | 變數配置                       |
| ---- | ------------------ | -------------------------- |
| A    | Collocated Grid    | $u, v, p$ 皆定義於 cell center |
| B    | MAC Staggered Grid | $p$ 定義於中心，$u, v$ 定義於面      |

---

## 三、結構診斷指標

為避免主觀推測，本研究引入以下量化指標。

### 1. 壓力方程誠實度指標

定義為：

$$
\mathrm{ID_Used} = | \Delta_h p - b |.
$$

此指標衡量壓力泊松方程是否被真正解開。

---

### 2. 投影後散度指標

定義為：

$$
\mathrm{Div_After} = | \nabla_h \cdot \mathbf{u}^{n+1} |.
$$

衡量投影是否成功消除散度。

---

### 3. 算子縫隙指標

定義為：

$$
\mathrm{Op_Gap} = \left| \nabla_h \cdot \mathbf{u}^*_{\text{mean-free}} - \frac{\Delta t}{\rho} \nabla_h \cdot \nabla_h p \right|.
$$

此量直接衡量離散 div–grad–lap 是否形成共軛鏈條。

---

### 4. 可解性檢驗

檢查：

$$
\int_\Omega b , d\Omega.
$$

若該值不為零，則壓力方程在純 Neumann 邊界下不可解。

---

## 四、Case A：Collocated Grid 結果

在 Collocated 結構下，PCG 將壓力泊松方程誤差壓至：

$$
\mathrm{ID_Used} \approx 10^{-8}.
$$

然而同時觀察到：

$$
\mathrm{Div_After} \approx 10^{-3},
$$

且

$$
\mathrm{Op_Gap} \sim 10^{-3}.
$$

此結果顯示：

* 線性子問題已充分收斂；
* 可解性條件已滿足；
* 但離散算子鏈條存在結構性不一致。

即使 $ \Delta_h p \approx b $ 成立，仍無法保證

$$
\nabla_h \cdot \mathbf{u}^{n+1} = 0.
$$

---

## 五、Case B：MAC Staggered Grid 結果

在 MAC 網格下，保持相同 PCG 求解器，觀察到：

$$
\mathrm{ID_Used} \approx 10^{-10},
$$

$$
\mathrm{Div_After} \approx 10^{-13},
$$

$$
\mathrm{Op_Gap} \approx 10^{-13}.
$$

三個指標同時降至機器精度量級。

此結果證明：

在 MAC 網格上，離散算子滿足

$$
\nabla_h \cdot \nabla_h p = \Delta_h p,
$$

因此投影步驟在離散層面保持共軛一致性。

---

## 六、結構性結論

本研究顯示：

* 提升線性求解器強度不足以消除 Collocated 網格上的散度地板；
* 問題來源於離散幾何結構；
* 透過幾何重構（MAC 網格）可使散度降至機器精度。

因此，投影誤差地板並非單純數值收斂問題，而是離散算子結構問題。

---

## 七、對 A1-CFD 框架的意義

本章實驗表明：

1. A1 框架可區分數學不可解與線性未收斂；
2. 可量化離散算子不一致；
3. 可透過結構對照實驗定位誤差來源；
4. 結構重構可消除投影誤差地板。

這說明 A1-CFD 不僅是一個數值求解工具，而是一套可跨域遷移的結構診斷方法。

---

