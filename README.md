# 冲刷深度计算器

🌊 基于规范 D.2.1 和 D.2.2 的冲刷深度在线计算工具

## 功能特性

- ✅ **D.2.1 丁坝一般冲刷计算**：支持非淹没丁坝一般冲刷深度计算
- ✅ **D.2.2 护岸局部冲刷计算**：支持顺坡及平顺护岸局部冲刷深度计算
- 📊 **实时计算**：输入参数后即时获取计算结果
- 📄 **导出计算书**：可将完整计算过程导出为 Word 文档
- 🎨 **美观界面**：现代化的 Web 界面，操作简便直观
- 💻 **双模式**：支持 Web 版和桌面版

## 在线访问

🔗 **Web版本**：访问 Streamlit 部署地址（部署后可用）

💻 **桌面版本**：运行本地 Python GUI 程序

## 本地部署

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/wmwyy/cssdjs.git
cd cssdjs
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行 Web 应用**
```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认地址：http://localhost:8501

4. **运行桌面程序**（可选）
```bash
python scour_gui.py
```

## 使用说明

### Web 版本

1. 访问应用网址或本地运行
2. 在顶部选择计算类型标签页：
   - **D.2.1 丁坝一般冲刷**
   - **D.2.2 护岸局部冲刷**
3. 在左侧输入相关参数
4. 点击"开始计算"按钮
5. 查看右侧计算结果
6. 可选：点击"下载 Word 计算书"导出完整报告

### 桌面版本

1. 运行 `python scour_gui.py`
2. 选择计算类型标签页
3. 填写输入参数
4. 点击"计算"按钮
5. 查看结果并可导出 Word

## 项目结构

```
cssdjs/
├── app.py              # Streamlit Web 应用主文件
├── scour_gui.py        # Tkinter 桌面 GUI 程序
├── scour_calc.py       # 核心计算模块
├── word_export.py      # Word 文档导出模块
├── requirements.txt    # Python 依赖包
├── 1.png              # 附图1（计算书附件）
├── 2.png              # 附图2（计算书附件）
└── README.md          # 项目说明文档
```

## 计算依据

- **D.2.1**：非淹没丁坝一般冲刷深度计算
  - 张瑞瑾公式 (D.2.1-5)：用于黏性土/细颗粒河床
  - 卵石起动流速公式 (D.2.1-6)：用于卵石/砾石河床
  - 速度项指数固定为 0.75
  
- **D.2.2**：顺坡及平顺护岸局部冲刷深度计算
- 默认重力加速度：g = 9.81 m/s²

## Streamlit Cloud 部署

### 方法一：通过 Streamlit Cloud（推荐）

1. Fork 本仓库到你的 GitHub 账号
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 使用 GitHub 账号登录
4. 点击 "New app"
5. 选择你的仓库、分支（main）和主文件（app.py）
6. 点击 "Deploy"
7. 等待部署完成，获取访问链接

### 方法二：其他云平台

本应用也可部署到：
- Heroku
- Railway
- Render
- Google Cloud Run
- AWS

## 开发

### 修改计算逻辑

编辑 `scour_calc.py` 文件中的计算函数。

### 修改界面

- Web 界面：编辑 `app.py`
- 桌面界面：编辑 `scour_gui.py`

### 修改导出格式

编辑 `word_export.py` 文件中的导出函数。

## 技术栈

- **后端**：Python 3.8+
- **Web 框架**：Streamlit
- **桌面 GUI**：Tkinter
- **文档处理**：python-docx
- **计算库**：标准库 math, dataclasses

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License

## 联系方式

- GitHub: [wmwyy/cssdjs](https://github.com/wmwyy/cssdjs)
- Issues: [提交问题](https://github.com/wmwyy/cssdjs/issues)

## 更新日志

### v1.0.0 (2025-12-30)
- ✨ 首次发布 Web 版本
- ✅ 完成 D.2.1 和 D.2.2 计算功能
- 🌐 添加 Streamlit Web 版本
- 💻 保留 Tkinter 桌面版本
- 📄 支持 Word 计算书导出（包含附图）
- 🎨 美化界面设计

---

⭐ 如果这个项目对你有帮助，请给个 Star！
