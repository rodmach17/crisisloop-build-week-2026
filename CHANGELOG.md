# Changelog

All notable changes to CrisisLoop will be documented in this file.

The format follows a simplified chronological log for OpenAI Build Week 2026.

## [Unreleased]

### Added

- Independent repository for CrisisLoop.
- Initial project directory structure.
- Build Week scope documentation.
- Project status tracking.
- Architecture and product decision log.
- Educational safety boundaries.
- Separation between deterministic simulation logic and GPT-5.6 coaching responsibilities.

### Planned

- React and TypeScript frontend.
- FastAPI backend.
- Deterministic postoperative hemorrhagic shock scenario.
- Vital-sign progression engine.
- Learner action system.
- Event and decision timeline.
- Deterministic scoring.
- Critical decision detection.
- Structured GPT-5.6 debrief.
- Adaptive replay.
- Pre/post comparison.
- Automated tests.
- Public deployment.
- Submission video.

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
