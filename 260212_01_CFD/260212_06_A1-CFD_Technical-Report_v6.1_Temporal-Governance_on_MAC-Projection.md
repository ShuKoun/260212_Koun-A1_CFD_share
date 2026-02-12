

---

# 英文文件名

```
A1-CFD_Technical-Report_v6.1_Temporal-Governance_on_MAC-Projection.md
```

# 英文標題

**A1-CFD Technical Report: Temporal Governance on MAC-Based Incompressible Flow Solver**

# 中文標題

**A1-CFD 技術報告：基於 MAC 投影的不可壓縮流時間治理機制**

---

# 1. 目標

本報告記錄 A1-CFD 在高雷諾數與大時間步長條件下的穩定性實驗結果。
重點不在於提出新的流體離散格式，而在於展示：

* 在固定物理算子下
* 僅透過時間治理機制
* 改變系統的可生存參數區域

---

# 2. 數值核心

## 2.1 控制方程

不可壓縮 Navier–Stokes 方程：

$$
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u}
$$

$$
\nabla \cdot \mathbf{u} = 0
$$

## 2.2 離散結構

* 網格：MAC 交錯網格
* 壓力：單元中心
* 速度：面中心
* 對流項：Donor-Cell Upwind
* 擴散項：中心差分
* 壓力方程：矩陣自由 PCG

投影步：

$$
\mathbf{u}^{n+1} = \mathbf{u}^* - \frac{\Delta t}{\rho} \nabla p^{n+1}
$$

泊松方程：

$$
\nabla^2 p^{n+1} = \frac{\rho}{\Delta t} \nabla \cdot \mathbf{u}^*
$$

MAC 網格滿足離散共軛性：

$$
\nabla_h \cdot \nabla_h = \nabla_h^2
$$

因此在數值誤差範圍內應有：

$$
|\nabla \cdot \mathbf{u}^{n+1}|_2 \approx 10^{-9}
$$

---

# 3. 死亡區測試

## 3.1 測試條件

* 網格：$40 \times 40$
* 雷諾數：$Re = 1000$
* 初始時間步長：$\Delta t = 0.04$

CFL 定義：

$$
\text{CFL} = \left( \frac{u_{\max}}{\Delta x} + \frac{v_{\max}}{\Delta y} \right)\Delta t
$$

## 3.2 Baseline 模式

固定時間步長：

$$
\Delta t_{n+1} = \Delta t_n
$$

結果：

* 第 10 步發生
* $\text{CFL} = 1.54$
* 模擬終止

---

# 4. A1 時間治理機制

## 4.1 治理規則

當：

$$
\text{CFL} > 1.0
$$

觸發：

$$
\Delta t \leftarrow \frac{\Delta t}{2}
$$

並回滾至上一步狀態重新計算。

## 4.2 實際運行軌跡

時間步長演化：

$$
0.04 \rightarrow 0.02 \rightarrow 0.01
$$

最終穩定於：

$$
\Delta t = 0.01
$$

成功運行 200 步。

---

# 5. 關鍵數據

| 指標      | Baseline | A1-CFD            |
| ------- | -------- | ----------------- |
| 存活步數    | 10       | 200               |
| 最終時間步長  | 0.04     | 0.01              |
| 散度誤差    | 崩潰       | $\approx 10^{-9}$ |
| PCG 迭代數 | 136–154  | 129–139           |

觀察：

* 散度誤差全程維持機器精度級別
* 壓力求解器穩定
* 未出現幾何漂移

---

# 6. 技術意義

A1-CFD 的價值不在於新的物理離散方法，而在於：

$$
\text{在相同物理核心下，透過治理層改變可生存區域}
$$

此結果構成：

* 對 CFL 牆的動態穿越能力
* 對高 Re 死亡區的可控通行能力
* 與 A1-GR 中高曲率走廊存活機制的結構對應

---

# 7. 結論

A1-CFD 展示了明確的「生存分離」現象：

$$
\exists (Re, \Delta t)
$$

使得：

$$
\text{Baseline 崩潰}
$$

而：

$$
\text{A1-CFD 穩定存活}
$$

且保持：

$$
|\nabla \cdot \mathbf{u}|_2 \approx 10^{-9}
$$

這證明：

時間治理可以在不改變物理算子的前提下，擴展數值方法的穩定運行區域。

---

