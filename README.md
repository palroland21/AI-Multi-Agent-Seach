# AI Multi-Agent Search – Pacman 🟡👻

Multi-agent decision-making for the **UC Berkeley Pacman AI** project using **game trees** and adversarial search.  
Unlike classic single-agent search (BFS/DFS/UCS/A*), this project models **Pacman vs. Ghosts** and chooses actions by looking ahead and evaluating future outcomes.

> Project report/details: see `Multi_Agent_Search.pdf`.

---

## ✅ What’s implemented

### Q1 — Reflex Agent
A simple agent that evaluates **only the current state + 1-step successors**.

Evaluation function logic:
- **Avoid active ghosts:** if an active ghost is closer than distance `< 2` → score = **−∞**
- **Move toward food:** reward closer food using:
  \[
  Score = GameScore + \frac{10}{d_{min}+1}
  \]
- **Avoid STOP:** penalty of **−10** if the action is `STOP`

---

### Q2 — Minimax Agent
Classic **adversarial search**:
- Pacman = **MAX** (tries to maximize score)
- Ghosts = **MIN** (assumed to play optimally to minimize Pacman’s score)

Key points:
- Recursive minimax over `(state, agentIndex, depth)`
- Stop when:
  - depth reaches `self.depth`, or
  - terminal state (`Win` / `Lose`)
- After the last ghost acts, depth increases and Pacman moves again

---

### Q3 — Alpha-Beta Pruning Agent
Optimized Minimax using pruning:
- **α** = best value so far for MAX
- **β** = best value so far for MIN

Pruning rules:
- At MAX node: if `v > β` → prune
- At MIN node: if `v < α` → prune

Result: **same decisions / same score as Minimax**, but significantly faster by exploring fewer branches.

---

## 📁 Project structure (typical)
- `multiAgents.py` – ReflexAgent, MinimaxAgent, AlphaBetaAgent, evaluation functions
- `pacman.py`, `game.py`, `util.py` – framework (Berkeley starter code)
- `layouts/` – maps/layouts
- `autograder.py` – grading script

---

## ▶️ How to run

### Requirements
- Python 3.x
- Berkeley Pacman project files included in the repo

### Example commands

Run Reflex agent:
```bash
python pacman.py -p ReflexAgent -l mediumClassic
python pacman.py -p MinimaxAgent -l mediumClassic -a depth=2
python pacman.py -p AlphaBetaAgent -l mediumClassic -a depth=2
python autograder.py
