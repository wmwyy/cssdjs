# 部署到 GitHub 和 Streamlit Cloud

本文档介绍如何将冲刷深度计算器部署到 GitHub 仓库并在 Streamlit Cloud 上运行。

## 步骤 1：推送到 GitHub

### 1.1 初始化 Git 仓库（如果还没有）

```bash
cd "d:\1\yy\cssdjs源码"
git init
```

### 1.2 添加远程仓库

```bash
git remote add origin https://github.com/wmwyy/cssdjs.git
```

如果已经添加过，可以查看：
```bash
git remote -v
```

### 1.3 添加所有文件

```bash
git add .
```

### 1.4 提交更改

```bash
git commit -m "Add Streamlit web version with beautiful UI"
```

### 1.5 推送到 GitHub

```bash
git push -u origin main
```

如果是第一次推送，可能需要先创建 main 分支：
```bash
git branch -M main
git push -u origin main
```

## 步骤 2：部署到 Streamlit Cloud

### 2.1 访问 Streamlit Cloud

打开浏览器访问：https://share.streamlit.io/

### 2.2 登录

使用你的 GitHub 账号登录

### 2.3 新建应用

1. 点击 "New app" 按钮
2. 填写以下信息：
   - **Repository**: wmwyy/cssdjs
   - **Branch**: main
   - **Main file path**: app.py
   - **App URL** (可选): 自定义一个网址，如 `cssdjs-calculator`

### 2.4 高级设置（可选）

点击 "Advanced settings" 可以配置：
- Python 版本：建议 3.10 或 3.11
- 其他环境变量

### 2.5 部署

点击 "Deploy!" 按钮

等待几分钟，应用将自动部署。部署完成后会得到一个访问链接，例如：
```
https://cssdjs-calculator.streamlit.app
```

## 步骤 3：验证部署

### 3.1 测试 Web 应用

访问部署后的链接，测试以下功能：
- [ ] D.2.1 计算功能是否正常
- [ ] D.2.2 计算功能是否正常
- [ ] Word 导出功能是否正常
- [ ] 界面是否美观
- [ ] 响应速度是否可接受

### 3.2 监控应用

Streamlit Cloud 提供了：
- 实时日志查看
- 应用状态监控
- 重启应用功能

## 常见问题

### Q1: 推送到 GitHub 时需要认证

**解决方案**：
```bash
# 使用 GitHub Personal Access Token
# 在 GitHub 上生成 Token: Settings > Developer settings > Personal access tokens
git remote set-url origin https://<TOKEN>@github.com/wmwyy/cssdjs.git
```

### Q2: 部署失败

**检查清单**：
1. 确认 `requirements.txt` 文件存在且正确
2. 确认 `app.py` 文件在仓库根目录
3. 查看 Streamlit Cloud 的错误日志
4. 确认 Python 版本兼容性

### Q3: Word 导出功能在云端不工作

**原因**：Streamlit Cloud 的文件系统限制

**解决方案**：代码中已使用 `tempfile` 模块处理临时文件，应该可以正常工作

### Q4: 图片无法显示在 Word 中

**检查**：确认 1.png 和 2.png 文件已推送到 GitHub

```bash
git add 1.png 2.png
git commit -m "Add images for Word export"
git push
```

## 本地测试 Streamlit 应用

在推送到云端之前，建议先在本地测试：

```bash
cd "d:\1\yy\cssdjs源码"
streamlit run app.py
```

访问 http://localhost:8501 进行测试

## 更新应用

当你修改代码后：

```bash
# 添加更改
git add .

# 提交
git commit -m "Update description"

# 推送
git push

# Streamlit Cloud 会自动检测更新并重新部署
```

## 手动重启应用

在 Streamlit Cloud 控制台：
1. 找到你的应用
2. 点击右上角菜单
3. 选择 "Reboot app"

## 删除应用

如果需要删除应用：
1. 在 Streamlit Cloud 控制台找到应用
2. 点击右上角菜单
3. 选择 "Delete app"

---

## 快速命令参考

### 初始化和推送

```bash
cd "d:\1\yy\cssdjs源码"
git init
git add .
git commit -m "Initial commit with Streamlit web app"
git branch -M main
git remote add origin https://github.com/wmwyy/cssdjs.git
git push -u origin main
```

### 后续更新

```bash
cd "d:\1\yy\cssdjs源码"
git add .
git commit -m "Your update message"
git push
```

---

🎉 完成部署后，你的冲刷深度计算器就可以在线访问了！
