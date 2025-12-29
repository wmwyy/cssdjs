"""
冲刷深度计算器 - Web版本
基于规范 D.2.1 和 D.2.2
使用 Streamlit 框架
"""

import streamlit as st
import tempfile
import os
from datetime import datetime
from scour_calc import (
    calc_d21, calc_d22, k1_from_type,
    K1Type, UcMethod
)
from word_export import export_d21_docx, export_d22_docx

# 页面配置
st.set_page_config(
    page_title="冲刷深度计算器",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .result-box {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .param-box {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
        color: #663c00;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .warning-box strong {
        color: #e65100;
        font-weight: 600;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        padding: 1rem 0;
    }
    h2 {
        color: #34495e;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.5rem;
    }
    h3 {
        color: #546e7a;
    }
    </style>
    """, unsafe_allow_html=True)

# 标题
st.title("🌊 冲刷深度计算器")
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.header("📖 使用说明")
    st.markdown("""
    **计算依据：**
    - D.2.1 丁坝一般冲刷
    - D.2.2 护岸局部冲刷
    
    **使用步骤：**
    1. 选择计算类型标签页
    2. 输入相关参数
    3. 点击计算按钮
    4. 查看结果并可导出Word
    
    **注意事项：**
    - 确保输入参数在合理范围内
    - 单位请按照说明填写
    - 导出的Word包含完整计算过程
    """)
    
    st.markdown("---")
    st.markdown(f"**当前时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 创建标签页
tab1, tab2 = st.tabs(["📐 D.2.1 丁坝一般冲刷", "🏗️ D.2.2 护岸局部冲刷"])

# ============== D.2.1 丁坝一般冲刷 ==============
with tab1:
    st.header("D.2.1 丁坝一般冲刷深度计算")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 输入参数")
        
        # 项目名称
        name_d21 = st.text_input("项目名称（可选）", key="name_d21", placeholder="例如：XX河道丁坝工程")
        
        st.markdown("#### 基本参数")
        H0_d21 = st.number_input("H0 - 冲刷处水深 (m)", min_value=0.01, value=3.0, step=0.1, 
                                  format="%.2f", key="H0_d21")
        d50_d21 = st.number_input("d50 - 床沙中值粒径 (m)", min_value=0.0001, value=0.02, 
                                   step=0.001, format="%.4f", key="d50_d21")
        U_d21 = st.number_input("U - 行近流速 (m/s)", min_value=0.01, value=1.5, 
                                step=0.1, format="%.2f", key="U_d21")
        L0_d21 = st.number_input("L0 - 丁坝有效长度 (m)", min_value=0.1, value=30.0, 
                                 step=1.0, format="%.1f", key="L0_d21")
        B_d21 = st.number_input("B - 河宽 (m)", min_value=0.1, value=120.0, 
                                step=1.0, format="%.1f", key="B_d21")
        
        st.markdown("#### 丁坝参数")
        theta_d21 = st.number_input("θ - 丁坝与水流方向夹角 (°)", min_value=0.1, max_value=90.0, 
                                     value=30.0, step=1.0, format="%.1f", key="theta_d21")
        m_d21 = st.number_input("m - 丁坝头坡率", min_value=0.1, value=2.0, 
                                step=0.1, format="%.1f", key="m_d21")
        k1_type_d21 = st.selectbox("k1 类型", 
                                    options=["弯曲河段凹岸单丁坝(k1=1.34)", "过渡段/顺直段单丁坝(k1=1.00)"],
                                    key="k1_type_d21")
        
        st.markdown("#### 起动流速 Uc")
        uc_method_d21 = st.selectbox("Uc 取值方法", 
                                      options=["张瑞瑾公式(D.2.1-5)", "卵石起动流速(D.2.1-6)", "手动输入"],
                                      key="uc_method_d21")
        
        if uc_method_d21 == "手动输入":
            uc_manual_d21 = st.number_input("Uc - 手动输入值 (m/s)", min_value=0.01, value=1.5, 
                                             step=0.1, format="%.2f", key="uc_manual_d21")
            gamma_s_d21, gamma_w_d21 = None, None
        else:
            gamma_s_d21 = st.number_input("γs - 泥沙容重 (kN/m³)", min_value=1.0, value=26.0, 
                                          step=0.1, format="%.2f", key="gamma_s_d21")
            gamma_w_d21 = st.number_input("γ - 水容重 (kN/m³)", min_value=1.0, value=9.81, 
                                          step=0.01, format="%.2f", key="gamma_w_d21")
            uc_manual_d21 = None
    
    with col2:
        st.subheader("📊 计算结果")
        
        if st.button("🚀 开始计算", type="primary", use_container_width=True, key="calc_d21_btn"):
            try:
                # 准备输入参数
                inputs_d21 = {
                    "H0": H0_d21,
                    "d50": d50_d21,
                    "U": U_d21,
                    "L0": L0_d21,
                    "B": B_d21,
                    "theta_deg": theta_d21,
                    "m": m_d21,
                    "k1_type": k1_type_d21,
                    "uc_method": uc_method_d21,
                }
                
                if uc_method_d21 == "手动输入":
                    inputs_d21["uc_manual"] = uc_manual_d21
                else:
                    inputs_d21["gamma_s"] = gamma_s_d21
                    inputs_d21["gamma_w"] = gamma_w_d21
                
                # 执行计算
                result_d21 = calc_d21(**inputs_d21)
                
                # 保存到session_state（不保存name_d21，因为它已经被widget管理）
                st.session_state.result_d21 = result_d21
                st.session_state.inputs_d21 = inputs_d21
                st.session_state.project_name_d21 = name_d21  # 使用不同的key保存项目名称
                
                st.success("✅ 计算完成！")
            except Exception as e:
                st.error(f"❌ 计算错误：{str(e)}")
        
        # 显示结果
        if "result_d21" in st.session_state:
            result = st.session_state.result_d21
            
            st.markdown("### 💡 主要结果")
            st.latex(r"h_s = " + f"{result.hs:.6f}" + r"\text{ m}")
            st.latex(r"\frac{h_s}{H_0} = " + f"{result.hs_over_H0:.6f}")
            
            st.markdown("#### 📋 中间计算结果")
            with st.expander("展开查看详细参数", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("k₁（位置系数）", f"{result.k1:.6f}")
                    st.metric("k₂（角度系数）", f"{result.k2:.6f}")
                    st.metric("k₃（坡率系数）", f"{result.k3:.6f}")
                with col_b:
                    st.metric("Uₘ（挑流流速）", f"{result.Um:.6f} m/s")
                    st.metric("Uᴄ（起动流速）", f"{result.Uc:.6f} m/s")
                
                # 显示关键计算公式
                st.markdown("##### 🔢 关键公式")
                
                # 计算速度项
                try:
                    import math
                    v_term = (float(result.Um) - float(result.Uc)) / math.sqrt(9.81 * float(st.session_state.inputs_d21.get("d50")))
                    
                    st.latex(r"v = \frac{U_m - U_c}{\sqrt{g \cdot d_{50}}} = " + f"{v_term:.6f}")
                    st.latex(r"\frac{h_s}{H_0} = k_1 \cdot k_2 \cdot k_3 \cdot v^a = " + f"{result.hs_over_H0:.6f}")
                    st.latex(r"h_s = H_0 \cdot \frac{h_s}{H_0} = " + f"{result.hs:.6f}" + r"\text{ m}")
                except:
                    pass
            
            # 导出Word
            st.markdown("#### 📄 导出计算书")
            if st.button("📥 下载 Word 计算书", type="secondary", use_container_width=True, key="export_d21_btn"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                        export_path = export_d21_docx(
                            path=tmp.name,
                            name=st.session_state.get("project_name_d21", name_d21),
                            inputs=st.session_state.inputs_d21,
                            result=result
                        )
                        
                        with open(export_path, "rb") as f:
                            st.download_button(
                                label="💾 点击下载",
                                data=f.read(),
                                file_name=f"冲刷计算书_D21_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                        
                        os.unlink(export_path)
                except Exception as e:
                    st.error(f"❌ 导出错误：{str(e)}")

# ============== D.2.2 护岸局部冲刷 ==============
with tab2:
    st.header("D.2.2 护岸局部冲刷深度计算")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 输入参数")
        
        # 项目名称
        name_d22 = st.text_input("项目名称（可选）", key="name_d22", placeholder="例如：XX河道护岸工程")
        
        st.markdown("#### 基本参数")
        H0_d22 = st.number_input("H0 - 护岸前水深 (m)", min_value=0.01, value=5.0, 
                                  step=0.1, format="%.2f", key="H0_d22")
        U_d22 = st.number_input("U - 行近流速 (m/s)", min_value=0.01, value=2.0, 
                                step=0.1, format="%.2f", key="U_d22")
        Uc_d22 = st.number_input("Uc - 泥沙起动流速 (m/s)", min_value=0.01, value=1.0, 
                                 step=0.1, format="%.2f", key="Uc_d22")
        
        st.markdown("#### 护岸参数")
        alpha_d22 = st.number_input("α - 护岸边壁与水流夹角 (°)", min_value=0.0, max_value=90.0, 
                                     value=15.0, step=1.0, format="%.1f", key="alpha_d22")
        n_d22 = st.number_input("n - 指数（经验值）", min_value=0.1, value=2.0, 
                                step=0.1, format="%.1f", key="n_d22")
        
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ 参数说明：</strong><br>
            • α = 0° 表示顺直护岸<br>
            • α > 0° 表示凸岸或挑流角度<br>
            • n 值通常在 1.5~2.5 之间
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 计算结果")
        
        if st.button("🚀 开始计算", type="primary", use_container_width=True, key="calc_d22_btn"):
            try:
                # 准备输入参数
                inputs_d22 = {
                    "H0": H0_d22,
                    "U": U_d22,
                    "Uc": Uc_d22,
                    "alpha_deg": alpha_d22,
                    "n": n_d22,
                }
                
                # 执行计算
                result_d22 = calc_d22(**inputs_d22)
                
                # 保存到session_state（不保存name_d22，因为它已经被widget管理）
                st.session_state.result_d22 = result_d22
                st.session_state.inputs_d22 = inputs_d22
                st.session_state.project_name_d22 = name_d22  # 使用不同的key保存项目名称
                
                st.success("✅ 计算完成！")
            except Exception as e:
                st.error(f"❌ 计算错误：{str(e)}")
        
        # 显示结果
        if "result_d22" in st.session_state:
            result = st.session_state.result_d22
            
            st.markdown("### 💡 主要结果")
            st.latex(r"h_s\text{(局部)} = " + f"{result.hs_local:.6f}" + r"\text{ m}")
            
            st.markdown("#### 📋 中间计算结果")
            with st.expander("展开查看详细参数", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("η（表 D.2.2）", f"{result.eta:.6f}")
                with col_b:
                    st.metric("Uₑₚ（边壁流速）", f"{result.Uep:.6f} m/s")
                
                # 显示关键计算公式
                st.markdown("##### 🔢 关键公式")
                
                try:
                    inputs = st.session_state.inputs_d22
                    
                    st.latex(r"U_{ep} = U \cdot \frac{2\eta}{1+\eta} = " + f"{result.Uep:.6f}" + r"\text{ m/s}")
                    st.latex(r"h_s = H_0 \cdot \left[\left(\frac{U_{ep}}{U_c}\right)^n - 1\right] = " + f"{result.hs_local:.6f}" + r"\text{ m}")
                except:
                    pass
            
            # 导出Word
            st.markdown("#### 📄 导出计算书")
            if st.button("📥 下载 Word 计算书", type="secondary", use_container_width=True, key="export_d22_btn"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                        export_path = export_d22_docx(
                            path=tmp.name,
                            name=st.session_state.get("project_name_d22", name_d22),
                            inputs=st.session_state.inputs_d22,
                            result=result
                        )
                        
                        with open(export_path, "rb") as f:
                            st.download_button(
                                label="💾 点击下载",
                                data=f.read(),
                                file_name=f"冲刷计算书_D22_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                        
                        os.unlink(export_path)
                except Exception as e:
                    st.error(f"❌ 导出错误：{str(e)}")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>冲刷深度计算器 v1.0 | 基于规范 D.2.1 和 D.2.2 | 
    <a href='https://github.com/wmwyy/cssdjs' target='_blank'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
