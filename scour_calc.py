from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal


G = 9.81


# D.2.1 速度项指数（按用户指定固定值）
D21_VELOCITY_EXPONENT = 0.75


K1Type = Literal[
    "弯曲河段凹岸单丁坝(k1=1.34)",
    "过渡段/顺直段单丁坝(k1=1.00)",
]


def k1_from_type(k1_type: K1Type) -> float:
    if k1_type == "弯曲河段凹岸单丁坝(k1=1.34)":
        return 1.34
    if k1_type == "过渡段/顺直段单丁坝(k1=1.00)":
        return 1.00
    raise ValueError("未知 k1 类型")


def k2_from_theta(theta_deg: float) -> float:
    if theta_deg <= 0 or theta_deg > 90:
        raise ValueError("θ 应在 (0, 90]° 范围内")
    return (theta_deg / 90.0) ** 0.26


def k3_from_m(m: float) -> float:
    if m <= 0:
        raise ValueError("m(丁坝头坡率) 必须为正")
    return math.exp(-0.07 * m)


def um_from_u(U: float, L0: float, B: float) -> float:
    if U <= 0 or L0 <= 0 or B <= 0:
        raise ValueError("U、L0、B 必须为正")
    return (1.0 + 4.8 * (L0 / B)) * U


UcMethod = Literal["张瑞瑾公式(D.2.1-5)", "卵石起动流速(D.2.1-6)", "手动输入"]


def uc_zhang(
    *,
    H0: float,
    d50: float,
    gamma_s: float,
    gamma_w: float,
) -> float:
    """D.2.1-5：张瑞瑾公式（用于黏性土/细颗粒河床起动流速）。

    该式来自用户提供的规范截图。输入单位建议：
    - H0, d50: m
    - gamma_s, gamma_w: kN/m^3
    """
    if H0 <= 0 or d50 <= 0:
        raise ValueError("H0 与 d50 必须为正")
    if gamma_s <= gamma_w:
        raise ValueError("γs 应大于 γ")

    # sqrt( 17.6 * ((γs-γ)/γ) * d50 + 6.05e-7 * (10 + H0) / d50^1.72 )
    term1 = 17.6 * ((gamma_s - gamma_w) / gamma_w) * d50
    term2 = 6.05e-7 * (10.0 + H0) / (d50 ** 1.72)
    return (H0 / d50) ** 0.14 * math.sqrt(max(term1 + term2, 0.0))


def uc_rubble(
    *,
    H0: float,
    d50: float,
    gamma_s: float,
    gamma_w: float,
) -> float:
    """D.2.1-6：卵石/砾石起动流速公式（来自规范截图）。"""
    if H0 <= 0 or d50 <= 0:
        raise ValueError("H0 与 d50 必须为正")
    if gamma_s <= gamma_w:
        raise ValueError("γs 应大于 γ")

    base = 1.08 * math.sqrt(G * d50 * ((gamma_s - gamma_w) / gamma_w))
    return base * (H0 / d50) ** (1.0 / 6.0)


@dataclass(frozen=True)
class D21Result:
    hs: float
    hs_over_H0: float
    k1: float
    k2: float
    k3: float
    Um: float
    Uc: float


def calc_d21(
    *,
    H0: float,
    d50: float,
    U: float,
    L0: float,
    B: float,
    theta_deg: float,
    m: float,
    k1_type: K1Type,
    uc_method: UcMethod,
    gamma_s: float | None = None,
    gamma_w: float | None = None,
    uc_manual: float | None = None,
) -> D21Result:
    """D.2.1 丁坝一般冲刷深度（非淹没丁坝）。

    速度项指数按规范固定为 0.75（见常量 `D21_VELOCITY_EXPONENT`）。
    """
    if H0 <= 0 or d50 <= 0:
        raise ValueError("H0 与 d50 必须为正")

    k1 = k1_from_type(k1_type)
    k2 = k2_from_theta(theta_deg)
    k3 = k3_from_m(m)
    Um = um_from_u(U=U, L0=L0, B=B)

    if uc_method == "手动输入":
        if uc_manual is None or uc_manual <= 0:
            raise ValueError("手动 Uc 必须为正")
        Uc = float(uc_manual)
    else:
        if gamma_s is None or gamma_w is None:
            raise ValueError("选择公式计算 Uc 时必须提供 γs 与 γ")
        if uc_method == "张瑞瑾公式(D.2.1-5)":
            Uc = uc_zhang(H0=H0, d50=d50, gamma_s=gamma_s, gamma_w=gamma_w)
        elif uc_method == "卵石起动流速(D.2.1-6)":
            Uc = uc_rubble(H0=H0, d50=d50, gamma_s=gamma_s, gamma_w=gamma_w)
        else:
            raise ValueError("未知 Uc 计算方法")

    if Um <= Uc:
        raise ValueError("Um 必须大于 Uc，否则按该式无法产生冲刷")

    # (Um-Uc)/sqrt(g*d50)
    v_term = (Um - Uc) / math.sqrt(G * d50)
    if v_term <= 0:
        raise ValueError("速度项为非正，检查输入")

    # hs/H0 = 2.80*k1*k2*k3 * v_term^0.75 * (L0/H0)^0.08
    hs_over_H0 = 2.80 * k1 * k2 * k3 * (v_term ** D21_VELOCITY_EXPONENT) * ((L0 / H0) ** 0.08)
    hs = hs_over_H0 * H0

    return D21Result(
        hs=hs,
        hs_over_H0=hs_over_H0,
        k1=k1,
        k2=k2,
        k3=k3,
        Um=Um,
        Uc=Uc,
    )


@dataclass(frozen=True)
class D22Result:
    hs_local: float
    Uep: float
    eta: float


def eta_from_angle(alpha_deg: float) -> float:
    a = abs(float(alpha_deg))
    # 表 D.2.2：按常用角度取值；其他角度线性插值
    pts = [
        (15.0, 1.00),
        (20.0, 1.25),
        (30.0, 1.50),
        (40.0, 1.75),
        (50.0, 2.00),
        (60.0, 2.25),
        (70.0, 2.50),
        (80.0, 2.75),
        (90.0, 3.00),
    ]
    if a <= pts[0][0]:
        return pts[0][1]
    if a >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= a <= x1:
            t = (a - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return pts[-1][1]


def calc_d22(
    *,
    H0: float,
    U: float,
    Uc: float,
    alpha_deg: float,
    n: float,
) -> D22Result:
    """D.2.2 顺坡/平顺护岸局部冲刷深度。"""
    if H0 <= 0:
        raise ValueError("H0 必须为正")
    if U <= 0 or Uc <= 0:
        raise ValueError("U 与 Uc 必须为正")
    if n <= 0:
        raise ValueError("n 必须为正")

    eta = eta_from_angle(alpha_deg)
    Uep = U * (2.0 * eta / (1.0 + eta))

    ratio = Uep / Uc
    hs_local = H0 * ((ratio ** n) - 1.0)
    return D22Result(hs_local=hs_local, Uep=Uep, eta=eta)
