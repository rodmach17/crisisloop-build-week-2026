# CrisisLoop — Submission Summary

## Project name

**CrisisLoop**

## Tagline

**Adaptive Clinical Crisis Simulator**

## Category

**Education**

## One-sentence description

CrisisLoop is an adaptive clinical crisis simulator that identifies the moment a learner fails, explains why with GPT-5.6, restarts the scenario before that failure and deterministically quantifies whether the learner improved.

## Problem

Clinical learners often receive feedback only after a scenario or examination is complete.

Traditional assessment may identify that an answer or action was incorrect, but it often does not:

- isolate the exact critical decision point;
- explain the dominant reasoning failure;
- create a targeted practice objective;
- restart the scenario immediately before the failure;
- quantify whether the learner corrected the error.

This limits immediate deliberate practice.

## Solution

CrisisLoop combines:

1. a deterministic clinical simulation engine;
2. a verified decision timeline;
3. deterministic assessment and scoring;
4. structured GPT-5.6 adaptive coaching;
5. replay from the calculated pre-failure checkpoint;
6. deterministic comparison between the initial attempt and replay.

The learner receives feedback grounded only in verified events and then immediately retries the scenario from the moment where improved decision-making matters most.

## Build Week scenario

The MVP contains one focused clinical crisis:

**Occult postoperative hemorrhagic shock**

The learner must recognize progressive deterioration and perform timely escalation and resuscitation.

## User flow

1. The learner enters the clinical scenario.
2. Patient physiology deteriorates deterministically over time.
3. Every action, omission and delay is recorded.
4. CrisisLoop calculates a deterministic score.
5. The system identifies the critical decision point.
6. GPT-5.6 generates structured adaptive coaching.
7. CrisisLoop calculates a replay checkpoint shortly before the failure.
8. The learner retries from that checkpoint.
9. The system compares both attempts and quantifies improvement.

## Role of GPT-5.6

GPT-5.6 analyzes:

- verified timeline events;
- actions taken;
- omitted actions;
- deterministic score;
- critical decision point;
- deterministic replay checkpoint.

GPT-5.6 generates:

- a concise performance summary;
- evidence-based strengths;
- improvement priorities;
- a clinical reasoning explanation;
- a replay objective;
- measurable replay success criteria.

GPT-5.6 does not control:

- patient physiology;
- vital signs;
- clinical progression;
- intervention effects;
- safety rules;
- outcomes;
- scores;
- replay timing;
- pre/post comparison.

## Why the architecture matters

The deterministic simulation layer preserves:

- reproducibility;
- testability;
- score consistency;
- clinical scenario control;
- separation between educational explanation and simulation logic.

GPT-5.6 adds adaptive explanation without becoming the source of truth for physiology or assessment.

## Key innovation

CrisisLoop does not stop after generating feedback.

It converts feedback into immediate deliberate practice by restarting the scenario shortly before the learner's critical failure and then measuring whether performance improved.

The complete learning loop is:

**fail → explain → replay → measure**

## Demonstrated result

In the validated MVP demo:

- initial score: `22/100`;
- replay score: `90/100`;
- deterministic score delta: `+68`;
- harm reduction: `25 points lower`;
- corrected omissions: `3`;
- new omissions: `0`;
- outcome: `IMPROVED`.

These values are calculated by deterministic comparison of the two verified simulation sessions.

## Current capabilities

- Browser-based React and TypeScript interface.
- FastAPI backend.
- Deterministic patient progression.
- Learner action system.
- Intervention effects.
- Decision timeline.
- Deterministic scoring.
- Critical decision detection.
- Structured GPT-5.6 coaching.
- Multilingual debrief generation.
- Adaptive replay.
- Deterministic pre/post comparison.
- Quantified score improvement.
- Harm reduction comparison.
- Corrected omission detection.
- Action timing comparison.
- Automated backend and API testing.
- Responsive interface.
- Visible educational safety boundaries.

## Technical stack

### Frontend

- React
- TypeScript
- Vite
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- OpenAI API
- Pytest

## Validation status

- `40` automated backend and API tests passing.
- Frontend production build successful.
- Real GPT-5.6 structured output verified.
- Full browser workflow verified:
  simulation → score → debrief → replay → comparison.
- Replay checkpoint verified at `01:30`.
- Automatic scrolling to score, debrief and comparison panels verified.

## Safety

CrisisLoop is an educational simulation prototype.

It is not:

- a medical device;
- a diagnostic tool;
- a clinical decision support system;
- a substitute for faculty supervision;
- intended for real patient care.

## Current limitations

- One clinical scenario.
- Three learner actions.
- Local execution.
- No authentication.
- No persistent database.
- No persistent learner history.
- No production deployment yet.
- No prospective educational validation yet.

## Expansion potential

The same architecture can support:

- additional clinical emergencies;
- procedural training;
- nursing education;
- emergency response;
- anesthesia crisis management;
- surgical decision-making;
- team communication scenarios;
- adaptive difficulty;
- faculty-authored scenarios;
- institutional learning analytics.

## Competitive differentiation

CrisisLoop combines four capabilities in one loop:

1. deterministic simulation;
2. GPT-5.6 grounded coaching;
3. replay from the critical decision point;
4. quantified evidence of improvement.

The core value is not simply that the AI explains the error.

The core value is that the learner can immediately practice the correction and demonstrate measurable improvement.

## Final pitch

CrisisLoop transforms clinical error into an adaptive learning loop.

A deterministic engine controls the patient and scoring. GPT-5.6 explains the verified failure. The learner then replays the scenario from shortly before the critical mistake, and CrisisLoop measures whether the learner improved.

The result is immediate deliberate practice with objective evidence of learning.
