# CrisisLoop

**Adaptive Clinical Crisis Simulator**

CrisisLoop is an educational simulation prototype built for OpenAI Build Week 2026.

It trains clinical decision-making under pressure by combining a deterministic patient simulation with structured GPT-5.6 adaptive coaching.

## Core learning loop

1. The learner manages a time-sensitive clinical crisis.
2. A deterministic engine advances the patient's physiological state.
3. Every action, omission and delay is recorded.
4. A deterministic scoring engine evaluates performance.
5. CrisisLoop identifies the critical decision point.
6. GPT-5.6 analyzes only the verified timeline and score.
7. The system generates structured adaptive feedback.
8. The learner replays the crisis from shortly before the failure.
9. The learner attempts a corrected sequence of decisions.

## Initial scenario

The Build Week MVP focuses on one scenario:

**Occult postoperative hemorrhagic shock**

The learner must recognize progressive hypoperfusion and initiate timely escalation and resuscitation.

## Why CrisisLoop

Traditional assessments often test whether learners know the correct answer.

CrisisLoop evaluates whether they can:

- recognize deterioration;
- prioritize information;
- act under time pressure;
- avoid diagnostic anchoring;
- recover from a critical error;
- improve during immediate deliberate practice.

## Architecture

- React and TypeScript frontend.
- FastAPI backend.
- Deterministic scenario engine.
- Physiological state machine.
- Timed action and event log.
- Deterministic scoring.
- Critical decision detector.
- GPT-5.6 adaptive coach.

## Deterministic simulation

GPT-5.6 does not control:

- vital signs;
- physiological progression;
- intervention effects;
- safety rules;
- clinical outcomes;
- scores;
- mathematical pre/post comparison.

These components are deterministic, reproducible, and testable.

## GPT-5.6 integration

GPT-5.6 analyzes the verified simulation timeline and deterministic score to:

- summarize performance;
- identify evidence-based strengths;
- explain missed clinical cues;
- define improvement priorities;
- generate a replay objective;
- establish measurable success criteria.

Model responses use validated structured output. GPT-5.6 does not control physiology, intervention effects, safety rules, patient outcomes, scores or replay timing.

## Repository structure

- `frontend/`: browser interface.
- `backend/`: API, simulation engine, scoring, schemas and coaching.
- `scenarios/`: deterministic clinical scenario definitions.
- `docs/`: architecture, validation and submission materials.
- `scripts/`: development and validation utilities.
- `BUILD_WEEK_SCOPE.md`: frozen competition scope.
- `PROJECT_STATUS.md`: current operational state.
- `DECISIONS.md`: product and architecture decisions.
- `CHANGELOG.md`: chronological development history.

## Current status

A functional browser MVP is running locally.

Implemented capabilities include deterministic physiological progression, learner actions, decision timeline, deterministic scoring, critical decision detection, structured GPT-5.6 multilingual coaching and adaptive replay from the calculated pre-failure checkpoint.

Current validation baseline:

- 33 automated backend and API tests passing;
- frontend production build successful;
- complete simulation, debrief and replay workflow verified in the browser.

## Safety notice

CrisisLoop is an educational simulation prototype.

It is not a medical device, diagnostic tool, clinical decision support system, or substitute for professional supervision. It must not be used for real patient care.

## Build Week objective

Deliver a browser-based MVP in which a judge can:

1. complete a simulated clinical crisis;
2. observe deterministic consequences;
3. review the critical decision timeline;
4. receive structured adaptive coaching;
5. replay the crisis from the calculated pre-failure checkpoint;
6. attempt a corrected sequence of decisions.
