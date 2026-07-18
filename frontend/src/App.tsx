import "./App.css";

const vitalSigns = [
  { label: "Heart rate", value: "108", unit: "bpm" },
  { label: "Blood pressure", value: "104/68", unit: "mmHg" },
  { label: "Respiratory rate", value: "22", unit: "/min" },
  { label: "Oxygen saturation", value: "96", unit: "%" },
];

function App() {
  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">OPENAI BUILD WEEK 2026</p>
          <h1>CrisisLoop</h1>
          <p className="subtitle">Adaptive Clinical Crisis Simulator</p>
        </div>

        <div className="prototype-badge">
          Educational prototype
        </div>
      </header>

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
          <strong>00:00</strong>
        </div>
      </section>

      <section className="dashboard-grid">
        <article className="panel monitor-panel">
          <div className="panel-heading">
            <div>
              <p className="section-label">Live patient monitor</p>
              <h3>Compensated phase</h3>
            </div>
            <span className="status-pill">Active</span>
          </div>

          <div className="vitals-grid">
            {vitalSigns.map((vital) => (
              <div className="vital-card" key={vital.label}>
                <span>{vital.label}</span>
                <strong>{vital.value}</strong>
                <small>{vital.unit}</small>
              </div>
            ))}
          </div>

          <div className="clinical-summary">
            <div>
              <span>Mental status</span>
              <strong>Alert but anxious</strong>
            </div>
            <div>
              <span>Skin perfusion</span>
              <strong>Cool extremities</strong>
            </div>
            <div>
              <span>Estimated blood loss</span>
              <strong>750 ml</strong>
            </div>
            <div>
              <span>Cumulative harm</span>
              <strong>5 / 100</strong>
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
            <button type="button">Call for urgent help</button>
            <button type="button">Start IV fluids</button>
            <button type="button">Activate transfusion</button>
          </div>

          <button className="advance-button" type="button">
            Advance 30 seconds
          </button>
        </aside>
      </section>

      <section className="panel timeline-panel">
        <div className="panel-heading">
          <div>
            <p className="section-label">Decision timeline</p>
            <h3>Session events</h3>
          </div>
        </div>

        <div className="empty-state">
          No events recorded yet. Start the simulation to generate the
          learner decision trace.
        </div>
      </section>

      <footer>
        CrisisLoop is an educational simulation prototype and must not
        be used for real patient care.
      </footer>
    </main>
  );
}

export default App;
