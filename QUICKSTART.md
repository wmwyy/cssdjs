# 快速开始指南

## 🚀 本地运行

### 方法 1: 运行 Web 版本（推荐）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动应用
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

### 方法 2: 运行桌面版本

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动GUI程序
python scour_gui.py
```

## 📦 部署到云端

### Streamlit Cloud 部署（免费，推荐）

1. **准备 GitHub 仓库**
   ```bash
   git add .
   git commit -m "Add web version"
   git push
   ```

2. **访问 Streamlit Cloud**
   - 打开 https://share.streamlit.io/
   - 使用 GitHub 账号登录
   - 点击 "New app"
   - 选择仓库 `wmwyy/cssdjs`
   - 主文件选择 `app.py`
   - 点击 "Deploy"

3. **等待部署完成**
   - 通常需要 2-5 分钟
   - 部署成功后会得到一个访问链接

### Heroku 部署

创建 `Procfile` 文件：
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

创建 `runtime.txt` 文件：
```
python-3.11.0
```

部署命令：
```bash
heroku create your-app-name
git push heroku main
```

### Docker 部署

创建 `Dockerfile`：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

构建和运行：
```bash
docker build -t cssdjs-app .
docker run -p 8501:8501 cssdjs-app
```

## 🧪 测试功能

### 测试 D.2.1 计算

输入示例参数：
- H0 = 3.0 m
- d50 = 0.02 m
- U = 1.5 m/s
- L0 = 30 m
- B = 120 m
- θ = 30°
- m = 2.0

### 测试 D.2.2 计算

输入示例参数：
- H0 = 5.0 m
- U = 2.0 m/s
- Uc = 1.0 m/s
- α = 15°
- n = 2.0

### 测试 Word 导出

1. 完成计算后
2. 点击"下载 Word 计算书"按钮
3. 检查生成的 .docx 文件
4. 确认包含计算过程和附图

## 🔧 故障排除

### 问题 1: 模块未找到

```bash
pip install -r requirements.txt
```

### 问题 2: Streamlit 命令不存在

```bash
pip install streamlit
# 或使用虚拟环境
python -m streamlit run app.py
```

### 问题 3: Word 导出失败

```bash
pip install python-docx
```

### 问题 4: 端口被占用

```bash
streamlit run app.py --server.port 8502
```

## 📝 开发建议

### 修改样式

编辑 `app.py` 中的 CSS 部分：
```python
st.markdown("""
    <style>
    /* 你的自定义样式 */
    </style>
    """, unsafe_allow_html=True)
```

### 添加新功能

1. 在 `scour_calc.py` 中添加计算函数
2. 在 `app.py` 中添加新的标签页
3. 在 `word_export.py` 中添加导出函数

### 本地测试

```bash
# 开启开发模式（自动重载）
streamlit run app.py --server.runOnSave true
```

## 🌐 访问应用

- **本地**: http://localhost:8501
- **网络**: 查看终端输出的 Network URL
- **云端**: Streamlit Cloud 提供的链接

## 📚 更多资源

- [Streamlit 文档](https://docs.streamlit.io/)
- [Python-docx 文档](https://python-docx.readthedocs.io/)
- [项目 GitHub](https://github.com/wmwyy/cssdjs)

---

💡 **提示**: 首次运行可能需要下载依赖，请耐心等待。
