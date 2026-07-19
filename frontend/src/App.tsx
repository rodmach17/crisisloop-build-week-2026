import { useEffect, useMemo, useRef, useState } from "react";
import "./App.css";

type ClinicalPhase =
  | "compensated"
  | "early_shock"
  | "decompensated"
  | "critical"
  | "stabilized";

type VitalSigns = {
  heart_rate: number;
  systolic_bp: number;
  diastolic_bp: number;
  respiratory_rate: number;
  oxygen_saturation: number;
  temperature_c: number;
};

type PatientState = {
  scenario_id: string;
  elapsed_seconds: number;
  phase: ClinicalPhase;
  mental_status: string;
  skin_perfusion: string;
  estimated_blood_loss_ml: number;
  cumulative_harm: number;
  vital_signs: VitalSigns;
};

type TimelineEvent = {
  elapsed_seconds: number;
  event_type: string;
  action?: string | null;
  description: string;
  state_before: PatientState;
  state_after: PatientState;
};

type SimulationSession = {
  session_id: string;
  initial_state: PatientState;
  current_state: PatientState;
  timeline: TimelineEvent[];
};

type SessionScore = {
  total_score: number;
  recognition_score: number;
  intervention_score: number;
  safety_score: number;
  final_harm: number;
  critical_omissions: string[];
  critical_decision: {
    elapsed_seconds: number;
    reason: string;
    missed_action?: string | null;
  } | null;
};

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const phaseLabels: Record<ClinicalPhase, string> = {
  compensated: "Compensated phase",
  early_shock: "Early shock",
  decompensated: "Decompensated shock",
  critical: "Critical phase",
  stabilized: "Stabilized",
};

function formatElapsedTime(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(
    2,
    "0",
  )}`;
}

function App() {
  const [session, setSession] = useState<SimulationSession | null>(null);
  const [score, setScore] = useState<SessionScore | null>(null);
  const [loading, setLoading] = useState(true);
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const scoreSectionRef = useRef<HTMLElement | null>(null);

  async function createSession() {
    setLoading(true);
    setError(null);
    setScore(null);

    try {
      const response = await fetch(`${API_BASE_URL}/session`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`Session creation failed: ${response.status}`);
      }

      const data: SimulationSession = await response.json();
      setSession(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to create session.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void createSession();
  }, []);

  async function advanceTime(seconds: number) {
    if (!session) return;

    setBusyAction("advance");
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/session/advance`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session,
          seconds,
        }),
      });

      if (!response.ok) {
        throw new Error(`Time advance failed: ${response.status}`);
      }

      const data: SimulationSession = await response.json();
      setSession(data);
      setScore(null);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to advance the scenario.",
      );
    } finally {
      setBusyAction(null);
    }
  }

  async function applyAction(action: string) {
    if (!session) return;

    setBusyAction(action);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/session/action`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session,
          action,
        }),
      });

      if (!response.ok) {
        throw new Error(`Action failed: ${response.status}`);
      }

      const data: SimulationSession = await response.json();
      setSession(data);
      setScore(null);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to apply the action.",
      );
    } finally {
      setBusyAction(null);
    }
  }

  async function calculateScore() {
    if (!session) return;

    setBusyAction("score");
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/session/score`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(session),
      });

      if (!response.ok) {
        throw new Error(`Scoring failed: ${response.status}`);
      }

      const data = await response.json();
      setSession(data.session);
      setScore(data.score);

      window.setTimeout(() => {
        scoreSectionRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to calculate the score.",
      );
    } finally {
      setBusyAction(null);
    }
  }

  const patient = session?.current_state;

  const completedActions = useMemo(
    () =>
      new Set(
        session?.timeline
          .map((event) => event.action)
          .filter((action): action is string => Boolean(action)) ?? [],
      ),
    [session],
  );

  const actionButtons = useMemo(
    () => [
      {
        id: "call_for_help",
        label: "Call for urgent help",
      },
      {
        id: "start_iv_fluids",
        label: "Start IV fluids",
      },
      {
        id: "activate_transfusion",
        label: "Activate transfusion",
      },
    ],
    [],
  );

  if (loading) {
    return (
      <main className="app-shell centered-state">
        <div className="loading-card">
          <p className="eyebrow">CRISISLOOP</p>
          <h1>Starting simulation...</h1>
        </div>
      </main>
    );
  }

  if (!session || !patient) {
    return (
      <main className="app-shell centered-state">
        <div className="loading-card">
          <p className="eyebrow">CONNECTION ERROR</p>
          <h1>Unable to load the simulation</h1>
          <p>{error ?? "The backend did not return a valid session."}</p>
          <button type="button" onClick={() => void createSession()}>
            Retry
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">OPENAI BUILD WEEK 2026</p>
          <h1>CrisisLoop</h1>
          <p className="subtitle">Adaptive Clinical Crisis Simulator</p>
        </div>

        <div className="prototype-badge">Educational prototype</div>
      </header>

      {error ? <div className="error-banner">{error}</div> : null}

      <section className="scenario-header">
        <div>
          <p className="section-label">Scenario</p>
          <h2>Occult postoperative hemorrhagic shock</h2>
          <p>
            A postoperative patient is becoming anxious, tachycardic,
            and progressively hypoperfused.
          </p>
        </div>

        <div className="timer-card">
          <span>Elapsed time</span>
          <strong>{formatElapsedTime(patient.elapsed_seconds)}</strong>
        </div>
      </section>

      <section className="dashboard-grid">
        <article className="panel monitor-panel">
          <div className="panel-heading">
            <div>
              <p className="section-label">Live patient monitor</p>
              <h3>{phaseLabels[patient.phase]}</h3>
            </div>
            <span className="status-pill">Active</span>
          </div>

          <div className="vitals-grid">
            <div className="vital-card">
              <span>Heart rate</span>
              <strong>{patient.vital_signs.heart_rate}</strong>
              <small>bpm</small>
            </div>

            <div className="vital-card">
              <span>Blood pressure</span>
              <strong>
                {patient.vital_signs.systolic_bp}/
                {patient.vital_signs.diastolic_bp}
              </strong>
              <small>mmHg</small>
            </div>

            <div className="vital-card">
              <span>Respiratory rate</span>
              <strong>{patient.vital_signs.respiratory_rate}</strong>
              <small>/min</small>
            </div>

            <div className="vital-card">
              <span>Oxygen saturation</span>
              <strong>{patient.vital_signs.oxygen_saturation}</strong>
              <small>%</small>
            </div>
          </div>

          <div className="clinical-summary">
            <div>
              <span>Mental status</span>
              <strong>{patient.mental_status}</strong>
            </div>
            <div>
              <span>Skin perfusion</span>
              <strong>{patient.skin_perfusion}</strong>
            </div>
            <div>
              <span>Estimated blood loss</span>
              <strong>{patient.estimated_blood_loss_ml} ml</strong>
            </div>
            <div>
              <span>Cumulative harm</span>
              <strong>{patient.cumulative_harm} / 100</strong>
            </div>
          </div>
        </article>

        <aside className="panel actions-panel">
          <div className="panel-heading">
            <div>
              <p className="section-label">Learner actions</p>
              <h3>Choose the next step</h3>
            </div>
          </div>

          <div className="action-stack">
            {actionButtons.map((action) => {
              const isCompleted = completedActions.has(action.id);

              return (
                <button
                  type="button"
                  key={action.id}
                  className={isCompleted ? "completed-action" : ""}
                  disabled={busyAction !== null || isCompleted}
                  onClick={() => void applyAction(action.id)}
                >
                  {busyAction === action.id
                    ? "Applying..."
                    : isCompleted
                      ? `${action.label} — Completed`
                      : action.label}
                </button>
              );
            })}
          </div>

          <button
            className="advance-button"
            type="button"
            disabled={busyAction !== null}
            onClick={() => void advanceTime(30)}
          >
            {busyAction === "advance"
              ? "Advancing..."
              : "Advance 30 seconds"}
          </button>

          <button
            className="score-button"
            type="button"
            disabled={busyAction !== null}
            onClick={() => void calculateScore()}
          >
            {busyAction === "score" ? "Scoring..." : "Calculate score"}
          </button>

          <button
            className="reset-button"
            type="button"
            disabled={busyAction !== null}
            onClick={() => void createSession()}
          >
            Reset session
          </button>
        </aside>
      </section>

      <section className="panel timeline-panel">
        <div className="panel-heading">
          <div>
            <p className="section-label">Decision timeline</p>
            <h3>Session events</h3>
          </div>
          <span>{session.timeline.length} events</span>
        </div>

        {session.timeline.length === 0 ? (
          <div className="empty-state">
            No events recorded yet. Advance time or select an action.
          </div>
        ) : (
          <div className="timeline-list">
            {session.timeline
              .slice()
              .reverse()
              .map((event, index) => (
                <article
                  className="timeline-event"
                  key={`${event.elapsed_seconds}-${event.event_type}-${index}`}
                >
                  <div className="timeline-time">
                    {formatElapsedTime(event.elapsed_seconds)}
                  </div>
                  <div>
                    <strong>
                      {event.action
                        ? event.action.replaceAll("_", " ")
                        : "Time advanced"}
                    </strong>
                    <p>{event.description}</p>
                  </div>
                </article>
              ))}
          </div>
        )}
      </section>

      {score ? (
        <section
          ref={scoreSectionRef}
          className="panel score-panel"
        >
          <div className="score-main">
            <p className="section-label">Deterministic assessment</p>
            <strong>{score.total_score}</strong>
            <span>/ 100</span>
          </div>

          <div className="score-grid">
            <div>
              <span>Recognition</span>
              <strong>{score.recognition_score} / 30</strong>
            </div>
            <div>
              <span>Intervention</span>
              <strong>{score.intervention_score} / 40</strong>
            </div>
            <div>
              <span>Safety</span>
              <strong>{score.safety_score} / 30</strong>
            </div>
            <div>
              <span>Final harm</span>
              <strong>{score.final_harm} / 100</strong>
            </div>
          </div>

          {score.critical_decision ? (
            <div className="critical-decision">
              <span>Critical decision point</span>
              <strong>
                {formatElapsedTime(
                  score.critical_decision.elapsed_seconds,
                )}
              </strong>
              <p>{score.critical_decision.reason}</p>
            </div>
          ) : (
            <div className="success-decision">
              No critical decision failure detected.
            </div>
          )}
        </section>
      ) : null}

      <footer>
        CrisisLoop is an educational simulation prototype and must not
        be used for real patient care.
      </footer>
    </main>
  );
}

export default App;
