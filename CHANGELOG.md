# Changelog

All notable changes to CrisisLoop will be documented in this file.

The format follows a simplified chronological log for OpenAI Build Week 2026.

## [Unreleased]

### Added

- Structured GPT-5.6 adaptive debrief using verified deterministic session data.
- Multilingual debrief generation with English, Spanish, Portuguese, French and custom language support.
- Concise validated coach output with performance summary, strengths, priorities, reasoning, replay objective and success criteria.
- Visible GPT-5.6 loading state, elapsed timer and 75-second timeout.
- Adaptive replay checkpoint calculated before the critical decision failure.
- Deterministic replay session reconstruction with a new session identifier.
- Replay API endpoint with controlled validation errors.
- Frontend replay button, replay activation notice and automatic navigation to the checkpoint.
- Deterministic comparison between initial attempt and replay attempt.
- Initial and replay score comparison.
- Deterministic score delta and harm-reduction calculation.
- Corrected omission and new omission detection.
- Per-action timing comparison.
- Automatic scrolling to the quantified improvement panel.
- Automated tests for coaching, replay and session comparison.

### Changed

- Updated README to reflect the working MVP.
- Updated project status to reflect the end-to-end simulation, coaching and replay workflow.
- Constrained GPT-5.6 feedback length for concise judge-facing output.
- Hid internal identifiers from the learner-facing interface.
- Improved replay timeline labeling.
- Clarified harm reduction as a positive reduction rather than a negative value.

### Validated

- Real GPT-5.6 API call with structured output.
- Full browser flow:
  simulation → scoring → adaptive debrief → replay → comparison.
- Replay checkpoint at `01:30`.
- Initial score `22/100`.
- Replay score `90/100`.
- Deterministic score improvement `+68`.
- Three corrected omissions.
- Zero new omissions.
- Frontend production build successful.
- Backend and API suite passing with `40 tests`.

### Remaining

- Public deployment.
- Submission video.
- Final competition package.
- Additional visual polish.
- Optional additional scenarios after Build Week.

## 2026-07-18

### Added

- Created repository at:
  `/home/rodmach17/proyectos/crisisloop-build-week-2026`
- Initialized Git.
- Renamed default branch to `main`.
- Created base frontend, backend, scenario, documentation, test, and script directories.
- Defined the initial scenario as occult postoperative hemorrhagic shock.
- Frozen the MVP around a single polished clinical crisis simulation.

### Added

- Created the initial FastAPI backend.
- Added root and health-check endpoints.
- Verified local API responses at `/` and `/health`.
- Added pinned backend dependencies.

### Added

- Added validated patient-state schemas with Pydantic.
- Added clinical phases and structured vital signs.
- Added the deterministic initial state for the postoperative hemorrhagic shock scenario.
- Added the `/scenario/initial` endpoint.
- Verified the structured scenario response locally.

### Added

- Added deterministic physiological progression over time.
- Added the `/scenario/advance` endpoint.
- Added transition from compensated shock to decompensated shock without intervention.
- Added automated tests for deterioration and zero-second state copying.
- Verified deterministic progression with passing pytest tests.

### Added

- Added deterministic clinical action schemas.
- Added actions to call for help, start intravenous fluids, and activate transfusion.
- Added reproducible intervention effects on vital signs, blood loss, and cumulative harm.
- Added the `/scenario/action` endpoint.
- Added automated intervention tests.
- Verified all intervention tests with pytest.

### Added

- Added simulation session schemas.
- Added timeline events for time advancement and clinical actions.
- Added deterministic session creation.
- Added event recording with state before and after each change.
- Added automated tests for session and timeline behavior.
- Verified all session tests with pytest.

### Added

- Added deterministic session scoring.
- Added recognition, intervention, and safety subscores.
- Added critical omission detection.
- Added critical decision-point identification.
- Added automated tests comparing delayed and early management.
- Verified all scoring tests with pytest.

### Added

- Added complete simulation-session API endpoints.
- Added session creation, timed progression, action application, and scoring endpoints.
- Added API schemas for session operations.
- Added end-to-end API tests for the full learner flow.
- Verified the complete session API with passing tests.

### Added

- Created the React and TypeScript frontend with Vite.
- Added the first CrisisLoop clinical simulation interface.
- Added patient vital-sign cards, scenario status, learner actions, timer, and timeline sections.
- Added responsive styling for desktop and mobile layouts.
- Verified the frontend with a successful production build.

### Fixed

- Prevented completed learner actions from being selected repeatedly in the frontend.
- Added visual completion states for executed actions.
- Added automatic scrolling to the score panel.
- Prevented future critical-decision thresholds from being reported before they occur.
- Verified the complete backend test suite with 13 passing tests.
