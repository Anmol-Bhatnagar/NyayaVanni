# Contributing to NyayaVanni ⚖️

Thank you for your interest in contributing to NyayaVanni!  
We welcome contributors of all experience levels, including first-time open-source contributors and GSSoC participants.

Please follow the guidelines below to ensure a smooth and organized contribution process.

---

# 📌 Project Structure

NyayaVanni follows a full-stack architecture:

- `backend/` → Python backend services and API logic
- `frontend/` → React + Vite frontend application
- `.env.example` → Environment variable reference
- `CONTRIBUTING.md` → Contribution guidelines

Before contributing, it is recommended to explore the repository structure and understand how the frontend and backend interact.

---

# 🚀 Contribution Workflow

## 1. Fork the Repository

Click the **Fork** button on GitHub to create your own copy of the repository.

---

## 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/NyayaVanni.git
cd NyayaVanni
```

---

## 3. Add Upstream Remote

Adding the original repository as an upstream remote helps keep your fork updated with the latest changes.

```bash
git remote add upstream https://github.com/choudharyms/NyayaVanni.git
```

Verify remotes:

```bash
git remote -v
```

---

## 4. Create a New Branch

Always create a separate branch before making any changes.

### Branch Naming Conventions

| Type | Format |
|---|---|
| Feature | `feat/feature-name` |
| Bug Fix | `fix/bug-description` |
| Documentation | `docs/topic-name` |

Example:

```bash
git checkout -b docs/update-contributing-guide
```

Avoid committing directly to the `main` branch.

---

## 5. Make Your Changes

After creating your branch:

- Implement your feature or fix
- Follow the existing project structure
- Test changes locally before committing

---

## 6. Stage and Commit Changes

Stage your changes:

```bash
git add .
```

Commit with a descriptive message:

```bash
git commit -m "docs: improve contributing guidelines"
```

---

## 7. Push Changes to Your Fork

```bash
git push origin docs/update-contributing-guide
```

---

## 8. Open a Pull Request

- Go to your forked repository on GitHub
- Click **Compare & Pull Request**
- Add a proper title and description
- Link the related issue number

Example:

```text
Closes #12
```

- Submit the pull request for review

# 🛠️ Local Environment Setup
# **Backend Setup (Python)**
## 1. Navigate to the backend folder:

```bash
cd backend
```

## 2.Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

## 3.Install required dependencies:

```bash
pip install -r requirements.txt
```

## 4.Configure environment variables:

- Copy .env.example to .env.
- Update GEMINI_API_KEY with your valid credential.

# **Frontend Setup (Vite / React)**
## 1.Navigate to the frontend folder:

```bash
cd frontend
```

## 2.Install dependencies:

```bash
npm install
```

## 3.Start the local development server:

```bash
npm run dev
```
# **📥 Pull Request (PR) Guidelines**
- **Always link your issue:** Ensure your PR description contains Closes #IssueNumber.

- **One PR per issue:** Do not bundle multiple unrelated fixes into a single pull request.

- **Self-Review:** Test your code locally before submitting to ensure it compiles without errors.

# ❤️ Contributors
Thank you to everyone contributing to NyayaVanni!

**Core Contributors**
- **Madhusudan** - GitHub: @choudharyms

- **Siddhi Sharma** - GitHub: @sidbyte07

## ✨ All Contributors

This project is made possible by all the amazing people who contribute! 

[![NyayaVanni Contributors](https://contrib.rocks/image?repo=choudharyms/NyayaVanni)](https://github.com/choudharyms/NyayaVanni/graphs/contributors)

