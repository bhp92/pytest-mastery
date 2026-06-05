# 🤖 How to Use Claude AI as Your Pytest Tutor

Claude (claude.ai) is the fastest way to go deep on any concept in this course.
Below are exact prompts — copy, paste, and customize.

---

## 🧠 Before Each Day's Study Session

Paste this at the start of every Claude conversation:

```
I am learning pytest from scratch with a goal of being interview-ready at a senior (6-year experience) level.
I am currently on [WEEK X, DAY Y] of my course. Today's topic is: [TOPIC].

Please be my tutor for this session. When I ask questions:
- Give me the "why" behind every concept, not just the "what"
- Show real-world examples, not toy ones
- Point out common mistakes and anti-patterns
- If I write code, review it like a senior engineer doing a code review
- If I seem to misunderstand something, correct me directly

Let's start: can you give me a 5-minute overview of today's topic?
```

---

## 📖 Understanding a Concept

```
Explain [CONCEPT] in pytest.
- Start with a 1-sentence definition
- Then explain WHY it exists (what problem it solves)
- Show a minimal code example
- Then show a realistic production-style example
- Finally, tell me the 2-3 most common mistakes people make with it
```

**Example:**
```
Explain fixture scopes in pytest.
- Start with a 1-sentence definition...
```

---

## 💻 Code Review

Paste your test code and say:

```
Review this pytest code like a senior engineer:
- Is the structure correct?
- Are there any bugs or mistakes?
- Is there a better/more idiomatic way to write this?
- What would you change and why?

[PASTE YOUR CODE HERE]
```

---

## 🏋️ Generate Practice Problems

```
Give me 3 pytest exercises on [TOPIC] at [beginner/intermediate/advanced] level.
For each exercise:
1. A clear problem statement
2. The code I need to write tests for (the "system under test")
3. A list of cases I must cover
Do NOT give me the solution yet. I want to try first.
```

---

## 🎯 Mock Interview Practice

```
You are a senior Python engineer interviewing me for a role that requires strong pytest skills.
Ask me one interview question at a time about pytest.
After I answer, give me feedback:
- What I got right
- What I missed or got wrong
- What a perfect answer would include
- A score out of 10

Start with a medium-difficulty question.
```

---

## 🐛 Debugging Help

```
My pytest test is failing and I don't understand why.
Here is the test: [PASTE TEST]
Here is the error output: [PASTE ERROR]
Here is the code being tested: [PASTE CODE]

Walk me through exactly what is happening and how to fix it.
```

---

## 🔁 End-of-Week Review

```
I just finished Week [X] of my pytest course. Topics covered:
[LIST THE TOPICS]

Quiz me on everything from this week.
Ask me 5 questions — mix of conceptual and "what does this code do".
After all 5, tell me which areas I should review before moving to Week [X+1].
```

---

## 📋 Cheat Sheet Generator

```
Generate a pytest cheat sheet for [TOPIC].
Format it as:
- Key functions/decorators with one-line descriptions
- Most common patterns with minimal code snippets
- Things to avoid (anti-patterns)
Make it dense — this is a reference card, not a tutorial.
```

---

## 💡 Tips for Getting the Most Out of Claude

1. **Always paste your actual code** — vague questions get vague answers
2. **Say your experience level** — "I'm a beginner at mocking but comfortable with fixtures"
3. **Ask for the anti-pattern** — "What's the WRONG way to do this and why?"
4. **Use follow-ups** — "Can you show that example with async code instead?"
5. **Request a deeper explanation** — "You mentioned fixture scope — can you explain what happens to memory when a session-scoped fixture isn't cleaned up?"
