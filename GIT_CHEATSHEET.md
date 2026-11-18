# Git cheat sheet (BazaarBD workshop)

One-time setup (per computer)
    git config --global user.name  "Your Name"
    git config --global user.email "you@example.com"

Start tracking the project (once, in the BazaarBD_Workshop folder)
    git init
    git add .
    git commit -m "Start: workshop kit"

Every time something works
    git status                  # what changed?
    git add .                   # stage all changes
    git commit -m "Lab 1: clean customers"
    git log --oneline           # history, newest first

Look back
    git diff                    # unstaged changes
    git restore lab1_starter.py # undo uncommitted edits to a file

Optional: publish to GitHub
    (create an empty repository on github.com first)
    git branch -M main
    git remote add origin https://github.com/<you>/<repo>.git
    git push -u origin main

Rules of thumb
- Commit code, SQL and README. Do not commit data/, *.db, *.log or .venv/ (see .gitignore).
- Small commits with clear messages: "Add validate step", not "stuff".
- Commit after each lab step that works.
