# CrisisLoop — Project Status

## Current status

CrisisLoop has a functional end-to-end browser MVP for OpenAI Build Week 2026.

The implemented learning loop is:

**deterministic simulation → verified timeline → deterministic assessment → GPT-5.6 adaptive debrief → replay from the critical decision point**

The current scenario is:

**Occult postoperative hemorrhagic shock**

## Current objective

Complete the competition-facing layer:

1. Polish the judge-facing demo flow.
2. Finalize competition documentation.
3. Prepare deployment.
4. Record the submission video.
5. Package the final Build Week submission.

## Completed

### Product and scope

- Build Week category defined as Education.
- Initial learner defined as medical student or resident.
- Single-scenario MVP scope frozen.
- Educational and safety boundaries documented.
- Deterministic and GPT responsibilities explicitly separated.

### Backend

- FastAPI application.
- Session creation endpoint.
- Deterministic patient state.
- Time-based physiological progression.
- Clinical action system.
- Deterministic intervention effects.
- Session timeline and event logging.
- Deterministic scoring.
- Critical omission detection.
- Critical decision point calculation.
- Structured GPT-5.6 coaching service.
- Multilingual debrief request.
- Adaptive replay engine.
- Replay API endpoint.
- Controlled HTTP error handling.

### Frontend

- React and TypeScript application.
- Live patient monitor.
- Learner action controls.
- Scenario time advancement.
- Decision timeline.
- Deterministic score display.
- Critical decision display.
- GPT-5.6 adaptive debrief interface.
- English and Spanish coach interface labels.
- English, Spanish, Portuguese, French and custom output languages.
- Visible coach loading timer.
- 75-second request timeout.
- Functional replay button.
- Replay activation notice.
- Automatic return to the scenario checkpoint.
- Correct replay timeline labeling.
- Automatic comparison between initial attempt and replay.
- Initial and replay score display.
- Deterministic score delta.
- Deterministic harm reduction.
- Corrected omission detection.
- New omission detection.
- Per-action timing comparison.
- Automatic scrolling to the improvement panel.

### Validation

- Full simulation flow tested in the browser.
- GPT-5.6 API authentication verified.
- Real GPT-5.6 structured response verified.
- Replay verified at 01:30.
- Deterministic checkpoint physiology verified.
- Backend automated tests passing.
- Frontend production build passing.
- Git working tree clean after completed units.

## In progress

- Competition-focused documentation.
- Demo narrative.
- Judge-facing product explanation.
- Visual and usability polish.
- Submission preparation.

## Not yet implemented

- Persistent replay history beyond the current browser session.
- Persistent session storage.
- Authentication or learner accounts.
- Scenario authoring interface.
- Additional clinical scenarios.
- Production deployment.
- Submission video.
- Final Build Week submission package.

## Current blockers

None.

## Next exact action

Finalize the competition demo narrative and submission package, then prepare public deployment.

## Current repository path

`/home/rodmach17/proyectos/crisisloop-build-week-2026`

## Current branch

`main`

## Current HEAD

`f751b4c fix: clarify harm reduction display`

## Current validated baseline

- `40 passed, 1 non-blocking warning`
- Frontend production build successful
- Complete simulation, debrief, replay and quantified-improvement workflow verified in browser
- Demonstrated score improvement from `22/100` to `90/100`
- Demonstrated deterministic score delta of `+68`
- Demonstrated correction of three critical omissions
