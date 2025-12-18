# 一、日常开发

## ✨ 1. 开始一个新的功能
### 切换到 dev 并从远程更新

```bash
git checkout develop
git pull
```

### 从 dev 创建功能分支(仅在本地有)
```bash
git checkout -b feature/user-login
```
命名建议：
- feature/xxx
- 用动词或模块名

---

## 🧑‍💻 2. 写代码 & 提交
```bash
git add .
git commit -m "feat: 实现用户登录功能"
```
> 建议从现在开始就养成规范提交习惯

---

## 🔀 3. 功能完成 -> 合并回 develop

```bash
git checkout develop
git pull

git merge feature/user-login
git push
```

### 删除功能分支(根据自己的需要)
```bash
git branch -d feature/user-login
```
---

## 🚀 4. 发布一个版本（dev → main）

当你觉得：
> “这个版本可以发布了”

### 切到 main
```bash
git checkout main
git pull
```

### 合并 dev
```
git merge develop
git push
```

### 打 Tag
```bash
git tag v1.0.0
git push origin v1.0.0
```
---

## 🛠️ 五、线上 Bug 修复流程
场景：
- main 已上线
- 发现严重 bug

### 从 main 拉修复分支
```bash
git checkout main
git pull
git checkout -b fix/login-crash
```

### 修复 & 提交
```bash
git commit -am "fix: 修复登录时崩溃问题"
```

### 合并回 main 并发布
```bash
git checkout main
git merge fix/login-crash
git push
```

### ⚠️ 同步回 develop（非常重要）
```bash
git checkout develop
git merge main
git push
```

---