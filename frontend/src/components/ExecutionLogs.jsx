
const ExecutionLogs = ({ logs }) => {
  if (!logs || logs.length === 0) {
    return <p className="empty-state">No activity logs available.</p>;
  }

  return (
    <div className="logs-container">
      {logs.map((log) => (
        <div className="log-item" key={log.log_id}>
          <div className="log-marker" />

          <div className="log-content">
            <div className="log-heading">
              <strong>{log.event_type.replaceAll("_", " ")}</strong>
              <span className={`status ${log.status}`}>
                {log.status}
              </span>
            </div>

            <p>
              {log.agent_name || "System"}
              {log.action_name ? ` · ${log.action_name}` : ""}
            </p>

            {log.details && (
              <pre>{JSON.stringify(log.details, null, 2)}</pre>
            )}

            <small>
              {log.timestamp
                ? new Date(log.timestamp).toLocaleString()
                : "Time unavailable"}
              {log.duration_ms != null
                ? ` · ${log.duration_ms} ms`
                : ""}
            </small>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ExecutionLogs;
