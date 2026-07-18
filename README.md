# CrisisLoop

**Adaptive Clinical Crisis Simulator**

CrisisLoop is an educational simulation prototype built for OpenAI Build Week 2026.

It trains clinical decision-making under pressure by combining a deterministic patient simulation with structured GPT-5.6 adaptive coaching.

## Core learning loop

1. The learner manages a time-sensitive clinical crisis.
2. A deterministic engine advances the patient's physiological state.
3. Every action, omission, and delay is recorded.
4. CrisisLoop identifies the critical decision point.
5. GPT-5.6 analyzes the verified decision trace.
6. The system generates a measurable learning objective.
7. The learner replays the crisis from the critical moment.
8. CrisisLoop compares both attempts and quantifies improvement.

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

GPT-5.6 analyzes the verified simulation trace to:

- identify the dominant reasoning error;
- explain missed clinical cues;
- generate an educational debrief;
- define a measurable learning objective;
- configure an adaptive replay;
- adjust difficulty and distractors;
- recommend progression or repetition.

Model responses will use validated structured output.

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

The repository and Build Week scope are initialized.

Application implementation has not started yet.

## Safety notice

CrisisLoop is an educational simulation prototype.

It is not a medical device, diagnostic tool, clinical decision support system, or substitute for professional supervision. It must not be used for real patient care.

## Build Week objective

Deliver a browser-based MVP in which a judge can:

1. complete a simulated clinical crisis;
2. observe deterministic consequences;
3. review the critical decision timeline;
4. receive structured adaptive coaching;
5. replay the failure point;
6. demonstrate quantified improvement.
