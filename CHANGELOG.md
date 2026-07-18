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
