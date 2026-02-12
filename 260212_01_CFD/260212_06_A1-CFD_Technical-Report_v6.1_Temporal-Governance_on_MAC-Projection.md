

---

# 英文文件名

```
A1-CFD_v6.1_Technical_Report_Survival-Separation_on_MAC-PCG.md
```

---

# 中文标题

A1-CFD 技术报告：基于 MAC-PCG 框架的生存分离与时间步治理机制

# 英文标题

A1-CFD Technical Report: Survival Separation and Governed Time-Stepping on a MAC-PCG Framework

---

# 1. 报告目的

本报告记录 A1-CFD 在高雷诺数与大时间步长条件下的数值行为，并验证以下问题：

在不修改物理算子与离散结构的前提下，是否可以仅通过时间步治理机制，使系统在已知不稳定参数区域内保持稳定运行？

---

# 2. 数值框架概述

## 2.1 控制方程

二维不可压缩 Navier–Stokes 方程：

$$
\frac{\partial \mathbf{u}}{\partial t}
+
(\mathbf{u}\cdot\nabla)\mathbf{u}
==

-\nabla p
+
\nu \nabla^2 \mathbf{u}
$$

$$
\nabla \cdot \mathbf{u} = 0
$$

---

## 2.2 空间离散

采用 MAC (Marker-And-Cell) 交错网格：

* 压力 $p$ 定义在单元中心
* 速度 $u$ 定义在垂直面
* 速度 $v$ 定义在水平面

离散算子满足：

$$
\nabla_h \cdot \nabla_h p = \Delta_h p
$$

该结构保证投影步骤在离散层面具有几何一致性。

---

## 2.3 时间推进

预测步：

$$
\mathbf{u}^*
=

\mathbf{u}^n
+
\Delta t
\left(
-\mathbf{A}(\mathbf{u}^n)
+
\nu \Delta_h \mathbf{u}^n
\right)
$$

压力泊松方程：

$$
\Delta_h p^{n+1}
=

\frac{\rho}{\Delta t}
\nabla_h \cdot \mathbf{u}^*
$$

投影更新：

$$
\mathbf{u}^{n+1}
=

## \mathbf{u}^*

\frac{\Delta t}{\rho}
\nabla_h p^{n+1}
$$

压力方程使用矩阵自由 PCG 求解，并施加零均值约束。

---

# 3. 实验设置

## 3.1 参数

* 网格：$40 \times 40$
* 雷诺数：$Re = 1000$
* 初始时间步长：$\Delta t = 0.04$
* 模拟步数：200

扫描实验表明，在该参数下：

固定时间步 Baseline 在 CFL 超限后必然失稳。

---

# 4. 对照实验设计

## 4.1 Baseline 模式

时间步固定：

$$
\Delta t = 0.04
$$

若：

$$
CFL > 1.5
$$

则视为数值失稳。

---

## 4.2 A1_Governor 模式

当预测步得到：

$$
CFL > 1.0
$$

执行：

1. 回滚至上一步状态
2. 更新：

$$
\Delta t \leftarrow \frac{\Delta t}{2}
$$

3. 重算当前时间步

治理层不改变物理算子，仅调整时间步。

---

# 5. 实验结果

## 5.1 Baseline

| Step | CFL  | Div                |
| ---- | ---- | ------------------ |
| 1    | 0.30 | $1.8\times10^{-9}$ |
| 4    | 0.98 | $3.4\times10^{-9}$ |
| 10   | 1.54 | 数值失稳               |

Baseline 在第 10 步因 CFL 超限终止。

---

## 5.2 A1_Governor

| Step | $\Delta t$ | CFL  | Div                |
| ---- | ---------- | ---- | ------------------ |
| 5    | 0.04       | 1.12 | $4.8\times10^{-9}$ |
| 5    | 0.02       | 0.52 | $2.4\times10^{-9}$ |
| 46   | 0.02       | 1.00 | $4.3\times10^{-9}$ |
| 46   | 0.01       | 0.50 | $2.1\times10^{-9}$ |
| 200  | 0.01       | 0.54 | $2.1\times10^{-9}$ |

A1 模式完成 200 步，未发生失稳。

---

# 6. 关键观察

## 6.1 几何守恒

整个模拟过程中：

$$
|\nabla_h \cdot \mathbf{u}| \approx 10^{-9}
$$

说明：

* 投影结构未被破坏
* 回滚机制未引入散度污染

---

## 6.2 求解器行为

PCG 迭代次数：

* Baseline 早期：136–154
* A1 后期：129–139

时间步缩减改善了压力方程条件数，求解效率未降低。

---

# 7. 生存分离定义

定义：

若存在参数 $(Re, \Delta t)$ 使得

$$
\text{Baseline} \to \text{Failure}
$$

而

$$
\text{Governed Mode} \to \text{Stable}
$$

则称该现象为：

Survival Separation

本报告在 $(Re=1000, \Delta t=0.04)$ 下验证该现象。

---

# 8. 计算代价

时间步由

$$
0.04 \rightarrow 0.02 \rightarrow 0.01
$$

若需达到相同物理时间，计算步数约增加 4 倍。

该代价换取了在死亡区内的可计算性。

---

# 9. 结论

1. MAC-PCG 结构保证离散几何守恒。
2. 固定时间步在高 CFL 区域必然失稳。
3. 引入治理层的时间步回滚机制后，可实现参数区间内的稳定运行。
4. 该结果构成明确的生存分离案例。

本技术报告验证了 A1 框架在 CFD 中的结构有效性。

---

