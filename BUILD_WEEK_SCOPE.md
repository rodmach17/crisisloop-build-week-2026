# CrisisLoop — Build Week Scope

## Project

**CrisisLoop: Adaptive Clinical Crisis Simulator**

CrisisLoop is an educational clinical simulation prototype designed for OpenAI Build Week 2026.

The system presents a time-sensitive clinical deterioration scenario, records the learner's decisions, applies deterministic physiological consequences, identifies the critical reasoning failure, and uses GPT-5.6 to generate an adaptive debrief and replay experience.

## Build Week objective

Build a functional web-based MVP that demonstrates:

1. A dynamic clinical crisis.
2. Time-dependent physiological deterioration.
3. Learner actions with deterministic consequences.
4. A reproducible scoring system.
5. Identification of a critical decision point.
6. Structured GPT-5.6 educational debriefing.
7. Adaptive replay from the point of failure.
8. Quantified pre/post improvement.

## Initial scenario

The MVP will use one primary scenario:

**Occult postoperative hemorrhagic shock**

The learner must recognize progressive hypoperfusion and initiate appropriate escalation and resuscitation before irreversible deterioration occurs.

## Components built during Build Week

- Web frontend.
- Clinical monitor interface.
- Scenario state machine.
- Deterministic physiological engine.
- Timed decision and event logging.
- Clinical action system.
- Deterministic scoring.
- Critical decision detection.
- Structured GPT-5.6 coaching.
- Adaptive scenario replay.
- Pre/post comparison.
- Demo mode.
- Documentation and tests.
- Public deployment.
- Submission video and materials.

## Deterministic responsibilities

The following functions must not depend on GPT-5.6:

- Vital sign progression.
- Scenario timing.
- Physiological state transitions.
- Intervention effects.
- Critical event detection.
- Outcome calculation.
- Safety rules.
- Score calculation.
- Pre/post mathematical comparison.

## GPT-5.6 responsibilities

GPT-5.6 will be used to:

- Interpret the complete decision trace.
- Identify the dominant reasoning error.
- Explain missed clinical cues.
- Produce a structured educational debrief.
- Define a measurable learning objective.
- Configure an adaptive replay variant.
- Adjust difficulty and distractors.
- Recommend whether the learner should advance, repeat, or reduce difficulty.

GPT-5.6 must not invent metrics, events, interventions, or physiological outcomes.

## Out of scope

The Build Week MVP will not include:

- Real patient care.
- Medical diagnosis for actual patients.
- Clinical decision support.
- Certification of clinical competence.
- Multiple medical specialties.
- A complete drug database.
- Advanced physiological modeling.
- Electronic health record integration.
- Voice interaction.
- Virtual reality.
- Three-dimensional simulation.
- Mobile native applications.
- Institutional analytics.
- Regulatory claims.
- Clinical efficacy claims.

## Safety and positioning

CrisisLoop is an educational prototype for simulated training.

It is not a medical device, clinical decision support system, diagnostic tool, or substitute for professional supervision.

All clinical content is simulated and intended exclusively for education and demonstration.

## Success criteria

The MVP is successful if a judge can:

1. Open the application in a browser.
2. Complete a simulated clinical crisis.
3. See the consequences of delayed or incorrect decisions.
4. Review a structured timeline and score.
5. Receive an adaptive GPT-5.6 debrief.
6. Replay the critical moment.
7. Demonstrate measurable improvement on the second attempt.
