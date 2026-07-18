# CrisisLoop — Decisions Log

## D-001 — Product category

**Decision:** Compete in the Education category.

**Reason:** CrisisLoop is designed as an adaptive learning system for clinical decision-making under pressure. The educational value is clearer and more defensible than positioning it as a clinical tool.

## D-002 — Initial user

**Decision:** The initial user is a medical student or resident training recognition and management of acute deterioration.

**Reason:** This user has a clear learning need, measurable performance variables, and a realistic use case for repeated deliberate practice.

## D-003 — Initial scenario

**Decision:** The MVP will contain one primary scenario: occult postoperative hemorrhagic shock.

**Reason:** It provides visible deterioration, time-sensitive decisions, meaningful distractors, measurable delays, and a strong replay narrative.

## D-004 — Deterministic physiological engine

**Decision:** Vital signs, progression, intervention effects, outcomes, safety rules, and scoring will be deterministic.

**Reason:** The simulation must be reproducible, testable, and safe. GPT-5.6 must not invent physiological consequences.

## D-005 — GPT-5.6 role

**Decision:** GPT-5.6 will interpret the learner's decision trace and generate structured educational coaching and replay adaptation.

**Reason:** This makes the model essential to personalization without delegating critical simulation logic to a generative model.

## D-006 — Structured model output

**Decision:** GPT-5.6 responses will use validated structured output.

**Reason:** The application needs predictable fields for debriefing, learning objectives, difficulty changes, and replay configuration.

## D-007 — Technology stack

**Decision:**

- Frontend: React, Vite, TypeScript.
- Interface styling: Tailwind CSS.
- Charts and vital-sign visualization: Recharts or lightweight custom SVG where necessary.
- Backend: FastAPI and Python.
- Data validation: Pydantic.
- Tests: Pytest for backend and Vitest for frontend.
- AI integration: OpenAI Responses API.
- Version control: Git with small functional commits.

**Reason:** This stack supports rapid development, typed interfaces, deterministic Python logic, testing, and browser-based deployment.

## D-008 — Browser-first delivery

**Decision:** The MVP must work in a browser without specialized hardware or local installation for judges.

**Reason:** Immediate accessibility reduces evaluation friction and allows the full experience to be tested directly.

## D-009 — Single-scenario scope

**Decision:** Build one polished scenario rather than multiple incomplete cases.

**Reason:** The competition demo depends more on clarity, execution quality, and measurable adaptation than content volume.

## D-010 — Replay as the core interaction

**Decision:** The central product interaction is replay from the critical decision point.

**Reason:** Replay creates a clear educational loop:

initial attempt → critical error → adaptive feedback → repeated decision → quantified improvement.

## D-011 — Safety positioning

**Decision:** CrisisLoop will be described only as an educational simulation prototype.

**Reason:** It is not intended for diagnosis, treatment recommendations, real patient care, or autonomous competence certification.

## D-012 — Repository separation

**Decision:** CrisisLoop will remain in an independent repository located at:

`/home/rodmach17/proyectos/crisisloop-build-week-2026`

**Reason:** This preserves provenance, simplifies Build Week documentation, and prevents mixing CrisisLoop with MachDex or other projects.

## D-013 — Development discipline

**Decision:** Each functional unit must end with:

1. implementation;
2. test;
3. review;
4. documentation update;
5. descriptive commit.

**Reason:** Small verified increments reduce errors and create clear evidence of Build Week development.
