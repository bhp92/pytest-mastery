# 🧪 Pytest Mastery — From Zero to Senior in 6 Weeks

> **40 minutes a day. 6 weeks. Interview-ready pytest skills.**

This course takes you from `pip install pytest` to writing production-grade test suites with fixtures, mocking, CI integration, and async testing — the kind of depth that reads as 6 years of experience in a technical interview.

---

## 📦 What's Inside

```
pytest-mastery/
├── week1/          # Foundations — setup, assertions, discovery
├── week2/          # Fixtures — scopes, conftest, yield, params
├── week3/          # Parametrize & Marks
├── week4/          # Mocking & Patching
├── week5/          # Advanced — plugins, coverage, async, hooks
├── week6/          # Real-world — Django/Flask, CI, capstone
├── exercises/      # Standalone exercises with solutions
├── interview_prep/ # 12 senior-level Q&A with code examples
├── docs/           # Extended notes and cheat sheets
├── index.html      # Interactive course dashboard (open in browser)
└── CLAUDE_PROMPT.md # How to use Claude AI as your study tutor
```

---

## 🚀 Quick Start (VM / Local)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/pytest-mastery.git
cd pytest-mastery
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
```

### 3. Install all dependencies
```bash
pip install -r requirements.txt
```

### 4. Open the interactive dashboard
```bash
# Option A: Just open in browser
open index.html                  # Mac
xdg-open index.html              # Linux

# Option B: Serve from VM (access via browser on any device)
python3 -m http.server 8080
# Then visit: http://YOUR_VM_IP:8080
```

### 5. Start Week 1
```bash
cd week1
pytest -v                        # Run the example tests
```

---

## 📅 Study Schedule

| Week | Topic | Key Skills |
|------|-------|-----------|
| 1 | Foundations | Test discovery, assertions, pytest -v/k/m/x |
| 2 | Fixtures | Scopes, conftest.py, yield, params |
| 3 | Parametrize & Marks | DRY tests, xfail, custom marks |
| 4 | Mocking & Patching | mocker, monkeypatch, where to patch |
| 5 | Advanced Patterns | Coverage, async, custom plugins |
| 6 | Real-World & CI | Django/Flask, GitHub Actions, capstone |

**Each day:** Read the README in that week's folder → Run the examples → Do the exercise → Check your solution.

---

## 🤖 Study with Claude AI

See [`CLAUDE_PROMPT.md`](./CLAUDE_PROMPT.md) for exact prompts to use Claude as your personal pytest tutor — explaining concepts, reviewing your code, generating practice problems, and running mock interviews.

---

## 🎯 Interview Prep

See the [`interview_prep/`](./interview_prep/) folder for:
- 12 senior-level questions with full answers
- Code examples for every answer
- How to frame answers to sound experienced

---

## ✅ Running All Tests

```bash
# Run everything
pytest --tb=short -v

# Run with coverage
pytest --cov=. --cov-report=html
open htmlcov/index.html

# Run a specific week
pytest week2/ -v

# Run only fast tests (skip slow)
pytest -m "not slow"
```

---

## 🛠 Requirements

- Python 3.9+
- See `requirements.txt` for all packages

---

## 🤝 Contributing

Students and teachers are welcome to:
- Add exercises (open a PR to `exercises/`)
- Improve explanations
- Add real-world examples (Django, FastAPI, etc.)

---

## 📄 License

MIT — free to use, share, and teach with.
