
import { useState } from "react";

const modes = [
  {
    id: "conversation",
    name: "Conversation",
    icon: "◉",
    description: "A conversational agent workflow",
  },
  {
    id: "round_robin",
    name: "Round Robin",
    icon: "⟳",
    description: "Agents take turns processing tasks",
  },
  {
    id: "selector",
    name: "Selector",
    icon: "⌘",
    description: "Selects the most suitable agent",
  },
];

const sampleLogs = [
  {
    time: "09:30:01",
    type: "USER INPUT",
    description: "User submitted a task.",
    icon: "↗",
    color: "blue",
  },
  {
    time: "09:30:02",
    type: "AGENT ACTION",
    description: "Agent analyzed the task.",
    icon: "✳",
    color: "green",
  },
  {
    time: "09:30:03",
    type: "TOOL CALL",
    description: "Calculation tool executed successfully.",
    icon: "⌘",
    color: "orange",
  },
  {
    time: "09:30:04",
    type: "FINAL RESPONSE",
    description: "Agent prepared a response.",
    icon: "✓",
    color: "green",
  },
];

const sampleMetrics = [
  { label: "Response time", value: "2.4s", icon: "◷" },
  { label: "Agent actions", value: "3", icon: "✳" },
  { label: "Tool calls", value: "2", icon: "⌘" },
  { label: "Tokens used", value: "450", icon: "▤" },
];

function Dashboard() {
  const [mode, setMode] = useState("conversation");
  const [task, setTask] = useState("");
  const [response, setResponse] = useState("");
  const [hasRun, setHasRun] = useState(false);
  const [activeSection, setActiveSection] = useState("workspace");

  const currentMode = modes.find((item) => item.id === mode);

  const runPreview = () => {
    if (!task.trim()) return;

    setResponse(
      `This is a frontend demonstration of the ${currentMode.name} execution mode.\n\nYour task:\n"${task.trim()}"\n\nThe interface is ready to display the actual AI agent response, agent actions, tool results and token usage once the backend is connected.`
    );

    setHasRun(true);
    setActiveSection("workspace");
  };

  const navigateTo = (section) => {
    setActiveSection(section);

    document.getElementById(section)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  return (
    <div className="app-shell">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-mark">✳</div>

          <div>
            <h2>Agent Monitor</h2>
            <p>Multi-Agent Platform</p>
          </div>
        </div>

        <div className="sidebar-status">
          <span className="status-dot"></span>
          <span>System Ready</span>
        </div>

        <div className="nav-section">
          <p className="nav-label">NAVIGATION</p>

          {modes.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${
                mode === item.id && activeSection === "workspace"
                  ? "active"
                  : ""
              }`}
              onClick={() => {
                setMode(item.id);
                setActiveSection("workspace");
                document.getElementById("workspace")?.scrollIntoView({
                  behavior: "smooth",
                });
              }}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.name}</span>
            </button>
          ))}
        </div>

        <div className="nav-section observability-nav">
          <p className="nav-label">OBSERVABILITY</p>

          <button
            className={`nav-item ${
              activeSection === "logs" ? "active" : ""
            }`}
            onClick={() => navigateTo("logs")}
          >
            <span className="nav-icon">☷</span>
            <span>Execution Logs</span>
          </button>

          <button
            className={`nav-item ${
              activeSection === "statistics" ? "active" : ""
            }`}
            onClick={() => navigateTo("statistics")}
          >
            <span className="nav-icon">▥</span>
            <span>Statistics</span>
          </button>
        </div>

        <div className="sidebar-bottom">
          <div className="sidebar-avatar">AI</div>
          <div>
            <strong>AI Activity Logger</strong>
            <p>Execution & Observability</p>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">

        {/* TOP HEADER */}
        <header className="topbar">
          <div className="breadcrumb">
            <span>Workspace</span>
            <span className="breadcrumb-divider">/</span>
            <strong>Activity Monitor</strong>
          </div>

          <div className="topbar-right">
            <span className="preview-label">
              FRONTEND PREVIEW
            </span>

            <div className="user-avatar">U</div>
          </div>
        </header>

        <div className="content-container">

          {/* PAGE HEADING */}
          <section className="page-heading" id="workspace">
            <div>
              <p className="eyebrow">MULTI-AGENT EXECUTION & OBSERVABILITY</p>

              <h1>AI Agent Activity Monitor</h1>

              <p className="page-description">
                Monitor agent execution, inspect tool activity and
                understand every step of your AI workflow.
              </p>
            </div>

            <div className="system-ready">
              <span className="status-dot"></span>
              System Ready
            </div>
          </section>

          {/* WORKSPACE */}
          <section className="workspace-card">

            <div className="section-heading">
              <div>
                <p className="section-kicker">AGENT WORKSPACE</p>
                <h2>Start a new execution</h2>
              </div>

              <span className="mode-badge">
                {currentMode.name}
              </span>
            </div>

            <div className="mode-description">
              <span className="mode-description-icon">
                {currentMode.icon}
              </span>
              <span>{currentMode.description}</span>
            </div>

            <label className="input-label" htmlFor="task-input">
              Enter your task
            </label>

            <textarea
              id="task-input"
              className="task-input"
              placeholder="Ask the AI agent to perform a task..."
              value={task}
              onChange={(event) => setTask(event.target.value)}
              rows={5}
            />

            <div className="input-footer">
              <span>Describe your task in natural language.</span>

              <span>{task.length} characters</span>
            </div>

            <div className="workspace-actions">
              <button
                className="run-button"
                onClick={runPreview}
                disabled={!task.trim()}
              >
                <span>▶</span>
                Run Agent
              </button>

              <span className="preview-note">
                Preview mode · Backend integration pending
              </span>
            </div>
          </section>

          {/* AGENT RESPONSE */}
          <section className="response-card">
            <div className="section-heading">
              <div>
                <p className="section-kicker">OUTPUT</p>
                <h2>Agent Response</h2>
              </div>

              <span className="response-status">
                {hasRun ? "Preview generated" : "Awaiting execution"}
              </span>
            </div>

            {response ? (
              <div className="response-content">
                <div className="response-icon">✳</div>
                <p>{response}</p>
              </div>
            ) : (
              <div className="response-placeholder">
                <div className="placeholder-icon">✧</div>
                <p>
                  The final response will appear here after execution.
                </p>
                <span>
                  Enter a task above to preview the workspace.
                </span>
              </div>
            )}
          </section>

          {/* STATISTICS */}
          <section className="statistics-section" id="statistics">

            <div className="section-heading statistics-heading">
              <div>
                <p className="section-kicker">PERFORMANCE OVERVIEW</p>
                <h2>Execution Statistics</h2>
              </div>

              <span className="illustrative-tag">
                Illustrative values
              </span>
            </div>

            <div className="metrics-grid">
              {sampleMetrics.map((metric, index) => (
                <div className="metric-card" key={metric.label}>
                  <div className={`metric-icon metric-icon-${index}`}>
                    {metric.icon}
                  </div>

                  <div>
                    <p>{metric.label}</p>
                    <h3>{metric.value}</h3>
                  </div>

                  <span className="metric-index">
                    0{index + 1}
                  </span>
                </div>
              ))}
            </div>

            <p className="statistics-caption">
              Sample values for interface demonstration only.
              Actual metrics will be calculated from backend execution data.
            </p>
          </section>

          {/* EXECUTION LOGS */}
          <section className="logs-section" id="logs">

            <div className="section-heading">
              <div>
                <p className="section-kicker">EXECUTION TRACE</p>
                <h2>Execution Logs</h2>
                <p className="logs-subtitle">
                  A chronological view of agent and tool activity.
                </p>
              </div>

              <span className="illustrative-tag">
                Sample events
              </span>
            </div>

            <div className="logs-table">

              <div className="logs-table-header">
                <span>EVENT</span>
                <span>ACTIVITY DESCRIPTION</span>
                <span>TIME</span>
              </div>

              {sampleLogs.map((log, index) => (
                <div className="log-row" key={index}>

                  <div className="log-event">
                    <span className={`log-icon ${log.color}`}>
                      {log.icon}
                    </span>

                    <strong>{log.type}</strong>
                  </div>

                  <p className="log-description">
                    {log.description}
                  </p>

                  <span className="log-time">
                    {log.time}
                  </span>
                </div>
              ))}
            </div>

            <div className="logs-footer">
              <span className="status-dot"></span>
              Sample timeline · Live logging will be enabled after integration.
            </div>
          </section>

          {/* FOOTER */}
          <footer className="page-footer">
            <span>AI Agent Activity Logger</span>
            <span>Multi-Agent Execution & Observability Platform</span>
          </footer>

        </div>
      </main>
    </div>
  );
}

export default Dashboard;
