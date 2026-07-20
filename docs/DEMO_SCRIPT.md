# CrisisLoop — Demo Script

## Objective

Demonstrate the complete CrisisLoop learning loop in approximately 2–3 minutes:

**clinical deterioration → deterministic assessment → GPT-5.6 adaptive coaching → replay → quantified improvement**

## Demo preparation

Before recording:

1. Start the FastAPI backend.
2. Start the Vite frontend.
3. Open `http://localhost:5173`.
4. Confirm the application starts with a fresh session.
5. Select Spanish only if the audience or recording will be in Spanish.
6. Keep the browser zoom at a level where the monitor, actions and score panels are readable.
7. Close unrelated windows and disable desktop notifications.

## Recommended demo duration

Target duration: **2 minutes 30 seconds**

Maximum recommended duration: **3 minutes**

---

## 0:00–0:15 — Problem

### Narration

> Clinical simulation often tells learners whether they were right or wrong, but it does not always identify the exact moment their reasoning failed or allow immediate targeted practice.

> CrisisLoop turns a clinical error into a measurable learning loop.

### Screen

Show the CrisisLoop title and the initial patient monitor.

---

## 0:15–0:30 — Product architecture

### Narration

> The patient physiology, intervention effects, safety rules and scoring are deterministic and reproducible.

> GPT-5.6 does not control the patient. It analyzes only the verified decision timeline and deterministic score to generate educational coaching.

### Screen

Point briefly to:

- live patient monitor;
- learner actions;
- elapsed time;
- educational prototype notice.

---

## 0:30–0:55 — Demonstrate clinical deterioration

### Actions

Do not select any clinical action.

Press **Advance 30 seconds** four times until the timer reaches:

`02:00`

### Narration

> In this scenario, the learner delays recognition and treatment of occult postoperative hemorrhagic shock.

> As time passes, the deterministic engine progresses tachycardia, hypotension, hypoperfusion, blood loss and cumulative harm.

### Screen

Allow the judge to see the worsening vital signs and decision timeline.

---

## 0:55–1:10 — Deterministic assessment

### Action

Press **Calculate score**.

### Expected result

- Initial score near `22/100`.
- Critical decision point at `02:00`.
- Low recognition and intervention scores.
- High final harm.
- Critical omissions visible.

### Narration

> CrisisLoop evaluates recognition, intervention timing and safety using deterministic rules.

> The initial attempt scores 22 out of 100 and identifies delayed recognition as the critical failure.

---

## 1:10–1:35 — GPT-5.6 adaptive coaching

### Actions

1. Select the desired language.
2. Press **Generate adaptive debrief**.
3. Wait for the structured response.

### Narration during loading

> GPT-5.6 receives the verified timeline and score. It cannot invent actions, modify physiology or change the grade.

### Narration when the result appears

> The coach explains the dominant reasoning failure, identifies improvement priorities and creates measurable replay objectives.

> It recommends restarting shortly before the critical decision point, at 1 minute 30 seconds.

### Screen

Show:

- performance summary;
- strengths;
- priorities;
- clinical reasoning;
- replay objective;
- success criteria;
- replay checkpoint at `01:30`.

---

## 1:35–1:55 — Adaptive replay

### Action

Press:

**Start replay from 01:30**

### Expected result

- New session identifier.
- Timer returns to `01:30`.
- Replay activation notice appears.
- Failed actions after the checkpoint are removed.
- Learner actions are available again.
- Timeline shows the adaptive replay checkpoint.

### Narration

> CrisisLoop creates a new deterministic session at the pre-failure checkpoint.

> The learner does not restart from the beginning. They immediately practice the decisions that need correction.

---

## 1:55–2:15 — Corrected performance

### Actions

Without advancing time, select:

1. **Call for urgent help**
2. **Start IV fluids**
3. **Activate transfusion**

Then press:

**Calculate score**

### Narration

> During replay, the learner escalates care, begins resuscitation and activates transfusion at the critical moment.

---

## 2:15–2:35 — Quantified learning

### Expected result

The comparison panel should show approximately:

- Initial score: `22/100`
- Replay score: `90/100`
- Score change: `+68`
- Harm reduction: `25 points lower`
- Three corrected omissions
- Zero new omissions
- Outcome: `IMPROVED`

### Narration

> CrisisLoop does not stop at feedback.

> It compares both verified attempts deterministically and demonstrates a 68-point improvement, lower patient harm and correction of all three critical omissions.

---

## 2:35–2:50 — Closing statement

### Narration

> CrisisLoop transforms clinical error into immediate deliberate practice.

> The deterministic engine guarantees reproducibility, while GPT-5.6 converts verified performance data into personalized coaching.

> The result is not just an explanation of what went wrong. It is measurable evidence that the learner improved.

### Final screen

Leave the quantified improvement panel visible.

---

## One-sentence pitch

> CrisisLoop is an adaptive clinical crisis simulator that identifies the moment a learner fails, explains why with GPT-5.6, restarts the scenario before that failure and quantifies whether the learner improved.

## Thirty-second pitch

> CrisisLoop trains clinical decision-making under pressure. A deterministic engine controls patient physiology, interventions, outcomes and scoring. GPT-5.6 analyzes only the verified decision trace to generate structured coaching. The learner then replays the scenario from shortly before the critical error, and CrisisLoop compares both attempts to quantify improvement in score, timing, omissions and patient harm.

## Key differentiators

- Deterministic and reproducible patient simulation.
- GPT-5.6 coaching grounded in verified events.
- Replay from the calculated pre-failure checkpoint.
- Immediate deliberate practice.
- Deterministic pre/post comparison.
- Quantified learning improvement.
- Multilingual educational feedback.
- Clear separation between AI explanation and clinical simulation control.

## Claims to avoid

Do not claim that CrisisLoop:

- is a medical device;
- is validated for real clinical care;
- improves patient outcomes in real hospitals;
- replaces faculty supervision;
- has completed prospective educational validation;
- currently supports multiple production-ready scenarios;
- currently includes user accounts or persistent learner records.

## Safe closing claim

> CrisisLoop is a functional educational prototype demonstrating how deterministic simulation and GPT-5.6 can create an immediate, measurable adaptive learning loop.
