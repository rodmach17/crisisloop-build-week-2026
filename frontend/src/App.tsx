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

type ImprovementOutcome =
  | "improved"
  | "unchanged"
  | "worsened";

type ActionTimingComparison = {
  action: string;
  initial_time_seconds: number | null;
  replay_time_seconds: number | null;
  seconds_faster: number | null;
  omission_corrected: boolean;
};

type SessionComparison = {
  initial_score: SessionScore;
  replay_score: SessionScore;
  score_delta: number;
  harm_reduction: number;
  corrected_omissions: string[];
  new_omissions: string[];
  action_timings: ActionTimingComparison[];
  outcome: ImprovementOutcome;
};

type AdaptiveDebrief = {
  performance_summary: string;
  strengths: string[];
  improvement_priorities: string[];
  clinical_reasoning_explanation: string;
  replay_objective: string;
  replay_success_criteria: string[];
};

type CoachDebriefResponse = {
  session_id: string;
  model: string;
  language: string;
  score: SessionScore;
  replay_from_seconds: number;
  debrief: AdaptiveDebrief;
  educational_use_only: boolean;
};

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const coachUiCopy = {
  en: {
    languageLabel: "Debrief language",
    otherOption: "Other…",
    customPlaceholder: "Example: Deutsch, 日本語, Italiano",
    generate: "Generate adaptive debrief",
    generating: "Generating adaptive debrief...",
    eyebrow: "GPT-5.6 adaptive coach",
    title: "Personalized debrief",
    performanceSummary: "Performance summary",
    strengths: "Strengths",
    improvementPriorities: "Improvement priorities",
    clinicalReasoning: "Clinical reasoning",
    replayFrom: "Replay from",
    replayObjective: "Replay objective",
    successCriteria: "Success criteria",
    disclaimer:
      "AI-generated educational feedback based only on the verified deterministic timeline and score.",
  },
  es: {
    languageLabel: "Idioma del informe",
    otherOption: "Otro…",
    customPlaceholder: "Ejemplo: Deutsch, 日本語, Italiano",
    generate: "Generar informe adaptativo",
    generating: "Generando informe adaptativo...",
    eyebrow: "Entrenador adaptativo GPT-5.6",
    title: "Informe personalizado",
    performanceSummary: "Resumen de rendimiento",
    strengths: "Fortalezas",
    improvementPriorities: "Prioridades de mejora",
    clinicalReasoning: "Razonamiento clínico",
    replayFrom: "Repetición desde",
    replayObjective: "Objetivo de repetición",
    successCriteria: "Criterios de éxito",
    disclaimer:
      "Retroalimentación educativa generada por IA basada únicamente en la cronología determinista verificada y la puntuación obtenida.",
  },
} as const;

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
  const [coachResult, setCoachResult] =
    useState<CoachDebriefResponse | null>(null);
  const [initialAttempt, setInitialAttempt] =
    useState<SimulationSession | null>(null);
  const [comparison, setComparison] =
    useState<SessionComparison | null>(null);
  const [coachLanguageOption, setCoachLanguageOption] =
    useState("English");
  const [customCoachLanguage, setCustomCoachLanguage] =
    useState("");
  const [loading, setLoading] = useState(true);
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [coachElapsedSeconds, setCoachElapsedSeconds] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [replayNotice, setReplayNotice] = useState<string | null>(null);
  const scenarioSectionRef = useRef<HTMLElement | null>(null);
  const scoreSectionRef = useRef<HTMLElement | null>(null);
  const comparisonSectionRef = useRef<HTMLElement | null>(null);
  const coachSectionRef = useRef<HTMLElement | null>(null);

  async function createSession() {
    setLoading(true);
    setError(null);
    setReplayNotice(null);
    setScore(null);
    setCoachResult(null);
    setInitialAttempt(null);
    setComparison(null);

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

  useEffect(() => {
    if (busyAction !== "coach") {
      setCoachElapsedSeconds(0);
      return;
    }

    const intervalId = window.setInterval(() => {
      setCoachElapsedSeconds((current) => current + 1);
    }, 1000);

    return () => {
      window.clearInterval(intervalId);
    };
  }, [busyAction]);

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
      setCoachResult(null);
      setComparison(null);
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
      setCoachResult(null);
      setComparison(null);
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
    setComparison(null);

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

      const data: {
        session: SimulationSession;
        score: SessionScore;
      } = await response.json();

      setSession(data.session);
      setScore(data.score);

      if (initialAttempt) {
        const compareResponse = await fetch(
          `${API_BASE_URL}/session/compare`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              initial_session: initialAttempt,
              replay_session: data.session,
            }),
          },
        );

        if (!compareResponse.ok) {
          const errorPayload = await compareResponse
            .json()
            .catch(() => null);

          throw new Error(
            errorPayload?.detail ??
              `Session comparison failed: ${compareResponse.status}`,
          );
        }

        const comparisonData: SessionComparison =
          await compareResponse.json();

        setComparison(comparisonData);

        window.setTimeout(() => {
          comparisonSectionRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }, 100);
      } else {
        window.setTimeout(() => {
          scoreSectionRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }, 100);
      }
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

  async function generateAdaptiveDebrief() {
    if (!session) return;

    const selectedLanguage =
      coachLanguageOption === "Other"
        ? customCoachLanguage.trim()
        : coachLanguageOption;

    if (!selectedLanguage) {
      setError("Please enter a valid debrief language.");
      return;
    }

    setBusyAction("coach");
    setCoachElapsedSeconds(0);
    setError(null);

    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => {
      controller.abort();
    }, 75_000);

    try {
      const response = await fetch(`${API_BASE_URL}/coach/debrief`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session,
          language: selectedLanguage,
        }),
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(
          `Adaptive debrief failed: ${response.status}`,
        );
      }

      const data: CoachDebriefResponse = await response.json();
      setScore(data.score);
      setCoachResult(data);

      window.setTimeout(() => {
        coachSectionRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    } catch (requestError) {
      if (
        requestError instanceof DOMException &&
        requestError.name === "AbortError"
      ) {
        setError(
          coachUiLanguage === "es"
            ? "La generación excedió 75 segundos. Intenta nuevamente."
            : "Generation exceeded 75 seconds. Please try again.",
        );
      } else {
        setError(
          requestError instanceof Error
            ? requestError.message
            : "Unable to generate the adaptive debrief.",
        );
      }
    } finally {
      window.clearTimeout(timeoutId);
      setBusyAction(null);
    }
  }

  async function startAdaptiveReplay() {
    if (!session || !coachResult) return;

    const replayFromSeconds = coachResult.replay_from_seconds;

    setBusyAction("replay");
    setError(null);
    setReplayNotice(null);

    try {
      const response = await fetch(`${API_BASE_URL}/session/replay`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session,
          replay_from_seconds: replayFromSeconds,
        }),
      });

      if (!response.ok) {
        const errorPayload = await response
          .json()
          .catch(() => null);

        throw new Error(
          errorPayload?.detail ??
            `Replay creation failed: ${response.status}`,
        );
      }

      const replaySession: SimulationSession = await response.json();

      setInitialAttempt(session);
      setComparison(null);
      setSession(replaySession);
      setScore(null);
      setCoachResult(null);
      setReplayNotice(
        coachLanguageOption === "Español"
          ? `Repetición activa desde ${formatElapsedTime(replayFromSeconds)}. Intenta corregir las decisiones críticas.`
          : `Replay active from ${formatElapsedTime(replayFromSeconds)}. Try to correct the critical decisions.`,
      );

      window.setTimeout(() => {
        scenarioSectionRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to start the adaptive replay.",
      );
    } finally {
      setBusyAction(null);
    }
  }

  const coachUiLanguage =
    coachLanguageOption === "Español" ? "es" : "en";
  const coachCopy = coachUiCopy[coachUiLanguage];

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

      {replayNotice ? (
        <div className="replay-notice" role="status">
          {replayNotice}
        </div>
      ) : null}

      <section
        ref={scenarioSectionRef}
        className="scenario-header"
      >
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

          <div className="coach-controls">
            <label htmlFor="coach-language">
              {coachCopy.languageLabel}
            </label>

            <select
              id="coach-language"
              value={coachLanguageOption}
              disabled={busyAction !== null}
              onChange={(event) => {
                setCoachLanguageOption(event.target.value);
                setCoachResult(null);
              }}
            >
              <option value="English">English</option>
              <option value="Español">Español</option>
              <option value="Português">Português</option>
              <option value="Français">Français</option>
              <option value="Other">
                {coachCopy.otherOption}
              </option>
            </select>

            {coachLanguageOption === "Other" ? (
              <input
                type="text"
                maxLength={40}
                value={customCoachLanguage}
                disabled={busyAction !== null}
                placeholder={coachCopy.customPlaceholder}
                onChange={(event) => {
                  setCustomCoachLanguage(event.target.value);
                  setCoachResult(null);
                }}
              />
            ) : null}
          </div>

          {busyAction === "coach" ? (
            <div className="coach-loading-status" role="status">
              <strong>
                {coachUiLanguage === "es"
                  ? "Analizando la cronología verificada con GPT-5.6"
                  : "Analyzing the verified timeline with GPT-5.6"}
              </strong>
              <span>
                {coachUiLanguage === "es"
                  ? `Tiempo transcurrido: ${coachElapsedSeconds} s`
                  : `Elapsed time: ${coachElapsedSeconds} s`}
              </span>
              <small>
                {coachUiLanguage === "es"
                  ? "La generación puede tardar hasta un minuto."
                  : "Generation may take up to one minute."}
              </small>
            </div>
          ) : null}

          <button
            className="coach-button"
            type="button"
            disabled={
              busyAction !== null ||
              score === null ||
              (coachLanguageOption === "Other" &&
                customCoachLanguage.trim().length < 2)
            }
            onClick={() => void generateAdaptiveDebrief()}
          >
            {busyAction === "coach"
              ? coachCopy.generating
              : coachCopy.generate}
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
                        : event.event_type === "replay_checkpoint"
                          ? "Adaptive replay checkpoint"
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

      {comparison ? (
        <section
          ref={comparisonSectionRef}
          className={`panel comparison-panel comparison-${comparison.outcome}`}
        >
          <div className="comparison-heading">
            <div>
              <p className="section-label">
                Deterministic learning comparison
              </p>
              <h3>
                {comparison.outcome === "improved"
                  ? "Performance improved"
                  : comparison.outcome === "worsened"
                    ? "Performance worsened"
                    : "Performance unchanged"}
              </h3>
            </div>

            <span className="comparison-outcome">
              {comparison.outcome}
            </span>
          </div>

          <div className="comparison-score-grid">
            <article>
              <span>Initial score</span>
              <strong>
                {comparison.initial_score.total_score}
                <small>/100</small>
              </strong>
            </article>

            <article>
              <span>Replay score</span>
              <strong>
                {comparison.replay_score.total_score}
                <small>/100</small>
              </strong>
            </article>

            <article>
              <span>Score change</span>
              <strong>
                {comparison.score_delta > 0 ? "+" : ""}
                {comparison.score_delta}
              </strong>
            </article>

            <article>
              <span>Harm reduction</span>
              <strong>
                {comparison.harm_reduction > 0 ? "-" : ""}
                {Math.abs(comparison.harm_reduction)}
                <small> points</small>
              </strong>
            </article>
          </div>

          <div className="comparison-details-grid">
            <article>
              <span>Corrected omissions</span>
              {comparison.corrected_omissions.length > 0 ? (
                <ul>
                  {comparison.corrected_omissions.map((action) => (
                    <li key={action}>
                      {action.replaceAll("_", " ")}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>None corrected.</p>
              )}
            </article>

            <article>
              <span>New omissions</span>
              {comparison.new_omissions.length > 0 ? (
                <ul>
                  {comparison.new_omissions.map((action) => (
                    <li key={action}>
                      {action.replaceAll("_", " ")}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No new omissions.</p>
              )}
            </article>
          </div>

          <div className="comparison-timings">
            <span>Action timing</span>

            <div className="comparison-timing-list">
              {comparison.action_timings.map((timing) => (
                <article key={timing.action}>
                  <strong>
                    {timing.action.replaceAll("_", " ")}
                  </strong>

                  <p>
                    Initial:{" "}
                    {timing.initial_time_seconds === null
                      ? "omitted"
                      : formatElapsedTime(
                          timing.initial_time_seconds,
                        )}
                    {" · "}
                    Replay:{" "}
                    {timing.replay_time_seconds === null
                      ? "omitted"
                      : formatElapsedTime(
                          timing.replay_time_seconds,
                        )}
                  </p>

                  {timing.omission_corrected ? (
                    <small>Omission corrected during replay</small>
                  ) : timing.seconds_faster !== null ? (
                    <small>
                      {timing.seconds_faster > 0
                        ? `${timing.seconds_faster} seconds faster`
                        : timing.seconds_faster < 0
                          ? `${Math.abs(
                              timing.seconds_faster,
                            )} seconds slower`
                          : "Same action time"}
                    </small>
                  ) : null}
                </article>
              ))}
            </div>
          </div>

          <p className="comparison-disclaimer">
            Improvement values are calculated deterministically from
            the two verified simulation sessions.
          </p>
        </section>
      ) : null}

      {coachResult ? (
        <section
          ref={coachSectionRef}
          className="panel coach-panel"
        >
          <div className="coach-heading">
            <div>
              <p className="section-label">{coachCopy.eyebrow}</p>
              <h3>{coachCopy.title}</h3>
            </div>
            <span className="coach-model">
              {coachResult.model} · {coachResult.language}
            </span>
          </div>

          <div className="coach-summary">
            <span>{coachCopy.performanceSummary}</span>
            <p>{coachResult.debrief.performance_summary}</p>
          </div>

          <div className="coach-grid">
            <article>
              <span>{coachCopy.strengths}</span>
              <ul>
                {coachResult.debrief.strengths.map((strength) => (
                  <li key={strength}>{strength}</li>
                ))}
              </ul>
            </article>

            <article>
              <span>{coachCopy.improvementPriorities}</span>
              <ul>
                {coachResult.debrief.improvement_priorities.map(
                  (priority) => (
                    <li key={priority}>{priority}</li>
                  ),
                )}
              </ul>
            </article>
          </div>

          <div className="coach-reasoning">
            <span>{coachCopy.clinicalReasoning}</span>
            <p>
              {coachResult.debrief.clinical_reasoning_explanation}
            </p>
          </div>

          <div className="replay-card">
            <div>
              <span>{coachCopy.replayFrom}</span>
              <strong>
                {formatElapsedTime(
                  coachResult.replay_from_seconds,
                )}
              </strong>
            </div>

            <div>
              <span>{coachCopy.replayObjective}</span>
              <p>{coachResult.debrief.replay_objective}</p>
            </div>

            <div>
              <span>{coachCopy.successCriteria}</span>
              <ul>
                {coachResult.debrief.replay_success_criteria.map(
                  (criterion) => (
                    <li key={criterion}>{criterion}</li>
                  ),
                )}
              </ul>
            </div>

            <button
              className="coach-button"
              type="button"
              disabled={busyAction !== null}
              onClick={() => void startAdaptiveReplay()}
            >
              {busyAction === "replay"
                ? coachUiLanguage === "es"
                  ? "Iniciando repetición..."
                  : "Starting replay..."
                : coachUiLanguage === "es"
                  ? `Iniciar repetición desde ${formatElapsedTime(
                      coachResult.replay_from_seconds,
                    )}`
                  : `Start replay from ${formatElapsedTime(
                      coachResult.replay_from_seconds,
                    )}`}
            </button>
          </div>

          <p className="coach-disclaimer">
            {coachCopy.disclaimer}
          </p>
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
