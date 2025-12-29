from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

from scour_calc import calc_d21, calc_d22


def _to_float(s: str) -> float:
    ss = str(s).strip()
    if ss == "":
        raise ValueError("输入不能为空")
    try:
        return float(ss.replace(",", ""))
    except Exception as e:
        raise ValueError(f"无法解析为数字：{s}") from e


def _fmt(x: float, nd: int = 6) -> str:
    try:
        if abs(x) >= 1e4 or (abs(x) > 0 and abs(x) < 1e-3):
            return f"{x:.{nd}e}"
        return f"{x:.{nd}f}".rstrip("0").rstrip(".")
    except Exception:
        return str(x)


class ScourApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("冲刷深度计算器（D.2）")
        self.minsize(920, 560)

        self._last_d21: dict | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        nb = ttk.Notebook(self)
        nb.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.tab_d21 = ttk.Frame(nb)
        self.tab_d22 = ttk.Frame(nb)
        nb.add(self.tab_d21, text="D.2.1 丁坝一般冲刷")
        nb.add(self.tab_d22, text="D.2.2 护岸局部冲刷")

        self._build_tab_d21(self.tab_d21)
        self._build_tab_d22(self.tab_d22)

    def _build_tab_d21(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=0)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)

        left = ttk.Frame(parent)
        right = ttk.Frame(parent)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        right.grid(row=0, column=1, sticky="nsew")

        for i in range(25):
            left.rowconfigure(i, weight=0)
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self.d21_vars: dict[str, tk.StringVar] = {}

        def add_row(r: int, label: str, key: str, default: str, hint: str = ""):
            ttk.Label(left, text=label).grid(row=r, column=0, sticky="e", padx=6, pady=4)
            var = tk.StringVar(value=default)
            self.d21_vars[key] = var
            ent = ttk.Entry(left, textvariable=var, width=18)
            ent.grid(row=r, column=1, sticky="w", padx=6, pady=4)
            if hint:
                ttk.Label(left, text=hint, foreground="#666").grid(row=r, column=2, sticky="w", padx=6, pady=4)
            return ent

        r = 0
        ttk.Label(left, text="输入参数", font=("Segoe UI", 10, "bold")).grid(row=r, column=0, columnspan=3, sticky="w", padx=6, pady=(6, 10))
        r += 1

        add_row(r, "H0 (m)：", "H0", "3.0", "冲刷处水深")
        r += 1
        add_row(r, "d50 (m)：", "d50", "0.02", "床沙中值粒径")
        r += 1
        add_row(r, "U (m/s)：", "U", "1.5", "行近流速")
        r += 1
        add_row(r, "L0 (m)：", "L0", "30", "丁坝有效长度")
        r += 1
        add_row(r, "B (m)：", "B", "120", "河宽")
        r += 1
        add_row(r, "θ (°)：", "theta", "30", "丁坝与水流方向夹角")
        r += 1
        add_row(r, "m (-)：", "m", "2.0", "丁坝头坡率")
        r += 1

        ttk.Label(left, text="k1：").grid(row=r, column=0, sticky="e", padx=6, pady=4)
        self.k1_type = tk.StringVar(value="弯曲河段凹岸单丁坝(k1=1.34)")
        self.k1_combo = ttk.Combobox(
            left,
            textvariable=self.k1_type,
            state="readonly",
            width=28,
            values=[
                "弯曲河段凹岸单丁坝(k1=1.34)",
                "过渡段/顺直段单丁坝(k1=1.00)",
            ],
        )
        self.k1_combo.grid(row=r, column=1, columnspan=2, sticky="w", padx=6, pady=4)
        r += 1

        ttk.Separator(left).grid(row=r, column=0, columnspan=3, sticky="ew", padx=6, pady=10)
        r += 1

        ttk.Label(left, text="起动流速 Uc", font=("Segoe UI", 10, "bold")).grid(row=r, column=0, columnspan=3, sticky="w", padx=6, pady=(0, 6))
        r += 1

        ttk.Label(left, text="Uc 取值：").grid(row=r, column=0, sticky="e", padx=6, pady=4)
        self.uc_method = tk.StringVar(value="张瑞瑾公式(D.2.1-5)")
        self.uc_combo = ttk.Combobox(
            left,
            textvariable=self.uc_method,
            state="readonly",
            width=28,
            values=["张瑞瑾公式(D.2.1-5)", "卵石起动流速(D.2.1-6)", "手动输入"],
        )
        self.uc_combo.grid(row=r, column=1, columnspan=2, sticky="w", padx=6, pady=4)
        self.uc_combo.bind("<<ComboboxSelected>>", lambda _e: self._d21_toggle_uc_fields())
        r += 1

        self.ent_gamma_s = add_row(r, "γs (kN/m³)：", "gamma_s", "26", "泥沙容重")
        r += 1
        self.ent_gamma_w = add_row(r, "γ (kN/m³)：", "gamma_w", "9.81", "水容重")
        r += 1
        self.ent_uc_manual = add_row(r, "Uc (m/s)：", "uc_manual", "", "手动输入时启用")
        r += 1

        ttk.Separator(left).grid(row=r, column=0, columnspan=3, sticky="ew", padx=6, pady=10)
        r += 1
        btns = ttk.Frame(left)
        btns.grid(row=r, column=0, columnspan=3, sticky="w", padx=6, pady=(6, 0))
        ttk.Button(btns, text="计算 D.2.1", command=self.on_calc_d21).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btns, text="导出 Word", command=self.on_export_d21_word).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(btns, text="清空结果", command=lambda: self._set_text(self.d21_out, "")).grid(row=0, column=2)

        self.d21_out = tk.Text(right, wrap="word")
        self.d21_out.grid(row=0, column=0, sticky="nsew")

        self._set_text(
            self.d21_out,
            "填写左侧参数，点击“计算 D.2.1”。\n\n"
            "提示：当 Um ≤ Uc 时，按该式无法产生冲刷（程序会提示）。\n",
        )

        self._d21_toggle_uc_fields()

    def _build_tab_d22(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=0)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)

        left = ttk.Frame(parent)
        right = ttk.Frame(parent)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        right.grid(row=0, column=1, sticky="nsew")

        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self.d22_vars: dict[str, tk.StringVar] = {}

        def add_row(r: int, label: str, key: str, default: str, hint: str = ""):
            ttk.Label(left, text=label).grid(row=r, column=0, sticky="e", padx=6, pady=4)
            var = tk.StringVar(value=default)
            self.d22_vars[key] = var
            ent = ttk.Entry(left, textvariable=var, width=18)
            ent.grid(row=r, column=1, sticky="w", padx=6, pady=4)
            if hint:
                ttk.Label(left, text=hint, foreground="#666").grid(row=r, column=2, sticky="w", padx=6, pady=4)
            return ent

        r = 0
        ttk.Label(left, text="输入参数", font=("Segoe UI", 10, "bold")).grid(row=r, column=0, columnspan=3, sticky="w", padx=6, pady=(6, 10))
        r += 1

        add_row(r, "H0 (m)：", "H0", "3.0", "冲刷处水深")
        r += 1
        add_row(r, "U (m/s)：", "U", "1.5", "行近流速")
        r += 1
        add_row(r, "Uc (m/s)：", "Uc", "", "泥沙起动流速")
        r += 1
        add_row(r, "α (°)：", "alpha", "30", "水流方向与岸坡坡交角")
        r += 1
        add_row(r, "n (-)：", "n", "0.25", "取 1/4~1/8")
        r += 1

        btns = ttk.Frame(left)
        btns.grid(row=r, column=0, columnspan=3, sticky="w", padx=6, pady=(10, 0))
        ttk.Button(btns, text="从 D.2.1 带入", command=self.on_fill_from_d21).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btns, text="计算 D.2.2", command=self.on_calc_d22).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(btns, text="导出 Word", command=self.on_export_d22_word).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(btns, text="清空结果", command=lambda: self._set_text(self.d22_out, "")).grid(row=0, column=3)

        self.d22_out = tk.Text(right, wrap="word")
        self.d22_out.grid(row=0, column=0, sticky="nsew")

        self._set_text(
            self.d22_out,
            "填写左侧参数，点击“计算 D.2.2”。\n"
            "也可先在 D.2.1 计算后点击“从 D.2.1 带入”。\n",
        )

    def _d21_toggle_uc_fields(self) -> None:
        method = self.uc_method.get().strip()
        if method == "手动输入":
            self.ent_gamma_s.configure(state="disabled")
            self.ent_gamma_w.configure(state="disabled")
            self.ent_uc_manual.configure(state="normal")
        else:
            self.ent_gamma_s.configure(state="normal")
            self.ent_gamma_w.configure(state="normal")
            self.ent_uc_manual.configure(state="disabled")

    @staticmethod
    def _set_text(widget: tk.Text, text: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="normal")

    def on_calc_d21(self) -> None:
        try:
            inputs, res = self._calc_d21_from_ui()

            self._last_d21 = {
                "H0": inputs["H0"],
                "U": inputs["U"],
                "Uc": res.Uc,
                "d50": inputs["d50"],
                "L0": inputs["L0"],
                "B": inputs["B"],
                "theta": inputs["theta_deg"],
                "m": inputs["m"],
                "k1_type": inputs["k1_type"],
                "uc_method": inputs["uc_method"],
            }

            out = (
                "D.2.1 计算结果\n"
                f"- hs = {_fmt(res.hs, 6)} m\n"
                f"- hs/H0 = {_fmt(res.hs_over_H0, 6)}\n\n"
                "中间量\n"
                f"- k1 = {_fmt(res.k1, 6)}\n"
                f"- k2 = {_fmt(res.k2, 6)}\n"
                f"- k3 = {_fmt(res.k3, 6)}\n"
                f"- Um = {_fmt(res.Um, 6)} m/s\n"
                f"- Uc = {_fmt(res.Uc, 6)} m/s\n"
            )
            self._set_text(self.d21_out, out)
        except Exception as e:
            messagebox.showerror("计算失败", str(e))

    def _calc_d21_from_ui(self):
        H0 = _to_float(self.d21_vars["H0"].get())
        d50 = _to_float(self.d21_vars["d50"].get())
        U = _to_float(self.d21_vars["U"].get())
        L0 = _to_float(self.d21_vars["L0"].get())
        B = _to_float(self.d21_vars["B"].get())
        theta = _to_float(self.d21_vars["theta"].get())
        m = _to_float(self.d21_vars["m"].get())

        k1_type = self.k1_type.get().strip()
        uc_method = self.uc_method.get().strip()

        gamma_s = gamma_w = uc_manual = None
        if uc_method == "手动输入":
            uc_manual = _to_float(self.d21_vars["uc_manual"].get())
        else:
            gamma_s = _to_float(self.d21_vars["gamma_s"].get())
            gamma_w = _to_float(self.d21_vars["gamma_w"].get())

        inputs = {
            "H0": H0,
            "d50": d50,
            "U": U,
            "L0": L0,
            "B": B,
            "theta_deg": theta,
            "m": m,
            "k1_type": k1_type,
            "uc_method": uc_method,
            "gamma_s": gamma_s,
            "gamma_w": gamma_w,
            "uc_manual": uc_manual,
        }

        res = calc_d21(
            H0=H0,
            d50=d50,
            U=U,
            L0=L0,
            B=B,
            theta_deg=theta,
            m=m,
            k1_type=k1_type,  # type: ignore[arg-type]
            uc_method=uc_method,  # type: ignore[arg-type]
            gamma_s=gamma_s,
            gamma_w=gamma_w,
            uc_manual=uc_manual,
        )
        return inputs, res

    def on_export_d21_word(self) -> None:
        try:
            inputs, res = self._calc_d21_from_ui()
            from word_export import export_d21_docx

            path = filedialog.asksaveasfilename(
                title="保存 Word（D.2.1）",
                defaultextension=".docx",
                filetypes=[("Word 文档", "*.docx")],
                initialfile="scour_d21_calcbook.docx",
            )
            if not path:
                return
            out_path = export_d21_docx(path=path, name=None, inputs=inputs, result=res)
            messagebox.showinfo("导出完成", f"已导出 Word: {out_path}")
        except ImportError as e:
            messagebox.showerror("缺少依赖", str(e))
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    def on_fill_from_d21(self) -> None:
        if not self._last_d21:
            messagebox.showinfo("提示", "尚未计算 D.2.1，无法带入。")
            return
        self.d22_vars["H0"].set(str(self._last_d21["H0"]))
        self.d22_vars["U"].set(str(self._last_d21["U"]))
        self.d22_vars["Uc"].set(str(self._last_d21["Uc"]))
        messagebox.showinfo("已带入", "已将 H0/U/Uc 从 D.2.1 结果带入。")

    def on_calc_d22(self) -> None:
        try:
            H0 = _to_float(self.d22_vars["H0"].get())
            U = _to_float(self.d22_vars["U"].get())
            Uc = _to_float(self.d22_vars["Uc"].get())
            alpha = _to_float(self.d22_vars["alpha"].get())
            n = _to_float(self.d22_vars["n"].get())

            res = calc_d22(H0=H0, U=U, Uc=Uc, alpha_deg=alpha, n=n)

            out = (
                "D.2.2 计算结果\n"
                f"- hs(局部) = {_fmt(res.hs_local, 6)} m\n\n"
                "中间量\n"
                f"- η = {_fmt(res.eta, 6)}\n"
                f"- Uep = {_fmt(res.Uep, 6)} m/s\n"
            )
            self._set_text(self.d22_out, out)
        except Exception as e:
            messagebox.showerror("计算失败", str(e))

    def _calc_d22_from_ui(self):
        H0 = _to_float(self.d22_vars["H0"].get())
        U = _to_float(self.d22_vars["U"].get())
        Uc = _to_float(self.d22_vars["Uc"].get())
        alpha = _to_float(self.d22_vars["alpha"].get())
        n = _to_float(self.d22_vars["n"].get())
        inputs = {
            "H0": H0,
            "U": U,
            "Uc": Uc,
            "alpha_deg": alpha,
            "n": n,
        }
        res = calc_d22(H0=H0, U=U, Uc=Uc, alpha_deg=alpha, n=n)
        return inputs, res

    def on_export_d22_word(self) -> None:
        try:
            inputs, res = self._calc_d22_from_ui()
            from word_export import export_d22_docx

            path = filedialog.asksaveasfilename(
                title="保存 Word（D.2.2）",
                defaultextension=".docx",
                filetypes=[("Word 文档", "*.docx")],
                initialfile="scour_d22_calcbook.docx",
            )
            if not path:
                return
            out_path = export_d22_docx(path=path, name=None, inputs=inputs, result=res)
            messagebox.showinfo("导出完成", f"已导出 Word: {out_path}")
        except ImportError as e:
            messagebox.showerror("缺少依赖", str(e))
        except Exception as e:
            messagebox.showerror("导出失败", str(e))


def main() -> None:
    try:
        from tkinter import TclError

        _ = TclError  # silence linters
    except Exception:
        pass

    app = ScourApp()
    try:
        ttk.Style().theme_use("clam")
    except Exception:
        pass
    app.mainloop()


if __name__ == "__main__":
    main()
