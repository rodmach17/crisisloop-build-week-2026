# CrisisLoop — Final Submission Copy

## Project name

CrisisLoop

## Tagline

Fail. Understand. Replay. Improve.

## Category

Education

## One-line description

CrisisLoop is an adaptive clinical crisis simulator that identifies a learner's critical decision failure, explains it with GPT-5.6, replays the scenario from before the error, and deterministically measures improvement.

## Project overview

Clinical simulation can show whether a learner succeeded or failed, but feedback often arrives after the scenario has ended and rarely allows immediate practice at the exact point where reasoning broke down.

CrisisLoop turns a clinical error into an adaptive learning loop:

**fail → understand → replay → measure**

The learner manages a time-sensitive clinical crisis while a deterministic engine controls physiology, intervention effects, outcomes, and scoring. Every action, omission, and delay is recorded in a verified timeline.

After the attempt, GPT-5.6 analyzes only that verified timeline and deterministic assessment. It generates concise, structured coaching, explains the dominant reasoning failure, and defines measurable replay objectives.

CrisisLoop then reconstructs the patient state shortly before the critical decision point. The learner retries the crisis from that checkpoint, and the platform compares both attempts to quantify whether learning occurred.

## The problem

Traditional clinical assessments commonly answer one question:

**Did the learner choose the correct action?**

They are less effective at answering:

- When did the learner's reasoning fail?
- Which clinical cues were missed?
- Which omission had the greatest consequence?
- Can the learner immediately practice that exact decision again?
- Did performance objectively improve after feedback?

Without immediate targeted repetition, feedback can remain passive rather than becoming deliberate practice.

## The solution

CrisisLoop combines six components:

1. Deterministic clinical simulation.
2. Verified action and decision timeline.
3. Deterministic assessment and critical-failure detection.
4. Structured GPT-5.6 adaptive coaching.
5. Replay from the calculated pre-failure checkpoint.
6. Deterministic comparison between the original and replay attempts.

The result is a closed educational loop where feedback is immediately converted into measurable practice.

## Build Week scenario

The MVP focuses on one polished scenario:

**Occult postoperative hemorrhagic shock**

A postoperative patient develops progressive tachycardia, hypoperfusion, blood loss, and hemodynamic deterioration.

The learner must recognize the crisis and perform timely escalation and resuscitation.

## How GPT-5.6 is used

GPT-5.6 receives:

- the verified simulation timeline;
- actions and omissions;
- deterministic vital-sign progression;
- deterministic score;
- the critical decision point;
- the application-calculated replay checkpoint.

GPT-5.6 generates:

- a concise performance summary;
- demonstrated strengths;
- specific improvement priorities;
- a clinical reasoning explanation;
- a replay objective;
- measurable replay success criteria;
- multilingual educational feedback.

GPT-5.6 does not control:

- patient physiology;
- vital signs;
- intervention effects;
- clinical progression;
- safety rules;
- outcomes;
- scores;
- replay timing;
- pre/post comparison.

This separation keeps the simulation reproducible and makes the AI explanation grounded in verified evidence.

## Demonstrated result

In the validated public workflow:

- Initial score: 22/100
- Replay score: 90/100
- Deterministic improvement: +68 points
- Harm reduction: 25 points
- Corrected critical omissions: 3
- New omissions: 0
- Final classification: IMPROVED

The comparison is calculated deterministically from two verified simulation sessions.

## Key innovation

The main innovation is not simply AI-generated feedback.

CrisisLoop converts feedback into immediate deliberate practice by reconstructing the scenario shortly before the learner's critical error and then objectively measuring whether the correction was successful.

## Technical architecture

### Frontend

- React
- TypeScript
- Vite
- CSS
- Deployed on Vercel

### Backend

- Python
- FastAPI
- Pydantic
- OpenAI API
- Pytest
- Deployed on Render

### Core systems

- Deterministic physiological state machine
- Deterministic intervention rules
- Session event timeline
- Deterministic scoring engine
- Critical decision detector
- Structured GPT-5.6 coaching
- Deterministic replay reconstruction
- Deterministic pre/post comparison

## What we built

- Public browser-based simulation.
- Progressive deterministic patient deterioration.
- Timed clinical actions.
- Intervention consequences.
- Verified decision timeline.
- Recognition, intervention, and safety scoring.
- Critical omission detection.
- Critical decision-point identification.
- Structured GPT-5.6 debrief.
- Multilingual feedback.
- Adaptive replay from the pre-failure checkpoint.
- Quantified score and harm comparison.
- Corrected and new omission detection.
- Per-action timing comparison.
- Automated backend and API tests.
- Public production deployment.

## Validation

- 42 automated backend and API tests passing.
- Frontend production build successful.
- Real GPT-5.6 structured output verified.
- Full public workflow verified:
  simulation → score → debrief → replay → comparison.
- Public frontend and backend communication verified.
- CORS validated.
- Replay checkpoint verified at 01:30.
- Automatic navigation to score, debrief, replay, and comparison panels verified.

## Challenges

### Separating AI from simulation truth

A major design challenge was deciding what GPT-5.6 should and should not control.

Allowing a language model to generate physiology, scores, or patient outcomes would reduce reproducibility and could introduce unsupported clinical behavior.

We therefore designed a strict boundary:

- deterministic code controls simulation and assessment;
- GPT-5.6 explains only verified performance data.

### Reconstructing a meaningful replay

Replay is not a simple reset. CrisisLoop must reconstruct the patient at a prior timestamp, create a new session, remove future failed actions, preserve deterministic physiology, and allow a corrected attempt without contaminating the original result.

### Measuring learning rather than completion

The product needed to distinguish genuine improvement from merely finishing the replay. We therefore compare scores, harm, omissions, and action timing between the two verified sessions.

### Production deployment

The frontend and backend were deployed separately, requiring environment-variable configuration, CORS validation, and public end-to-end testing.

## Accomplishments

- Built a complete end-to-end adaptive learning loop.
- Preserved deterministic clinical control.
- Integrated GPT-5.6 with validated structured output.
- Implemented replay from the learner's critical decision point.
- Quantified improvement across two attempts.
- Deployed a functional public MVP.
- Demonstrated a 68-point improvement in the validated workflow.

## What we learned

Adaptive education becomes more powerful when AI feedback is connected to an immediate opportunity to act differently.

We also learned that trustworthy AI architecture depends on assigning each component a clear responsibility:

- deterministic systems provide reproducibility and evaluation;
- GPT-5.6 provides grounded explanation and personalization.

## Future development

- Additional clinical crisis scenarios.
- Faculty scenario-authoring tools.
- Persistent learner accounts and histories.
- Adaptive difficulty.
- Team-based simulations.
- Institutional analytics.
- Longitudinal competency tracking.
- Prospective educational validation.
- Integration with procedural and sensor-based simulation systems.

## Safety statement

CrisisLoop is an educational simulation prototype.

It is not a medical device, diagnostic system, clinical decision-support system, or substitute for professional supervision. It must not be used for real patient care.

## Public links

### Live application

https://crisisloop-build-week-2026.vercel.app

### Source repository

https://github.com/rodmach17/crisisloop-build-week-2026

### Public API

https://crisisloop-api.onrender.com

### Health check

https://crisisloop-api.onrender.com/health

## Short pitch

CrisisLoop trains clinical decision-making under pressure. A deterministic engine controls the patient, interventions, outcomes, and scoring. GPT-5.6 explains the verified failure and creates a targeted replay objective. The learner then restarts shortly before the critical mistake, and CrisisLoop measures whether performance, timing, omissions, and patient harm improved.

## Final pitch

CrisisLoop transforms clinical error into immediate deliberate practice.

The system identifies when a learner fails, explains why with GPT-5.6, reconstructs the crisis before that failure, and produces objective evidence of whether the learner improved.

The result is not only feedback.

It is a measurable learning loop.
