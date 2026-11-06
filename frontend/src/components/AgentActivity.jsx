
const AgentActivity = ({ logs }) => {
  const agentLogs = logs.filter(
    (log) => log.agent_name || log.event_type === "tool_call"
  );

  if (agentLogs.length === 0) {
    return <p className="empty-state">No agent activity recorded yet.</p>;
  }

  return (
    <div className="agent-activity">
      {agentLogs.map((log) => (
        <div className="agent-card" key={log.log_id}>
          <div>
            <strong>{log.agent_name || "Tool"}</strong>
            <p>{log.action_name || log.event_type}</p>
          </div>

          <span className={`status ${log.status}`}>
            {log.status}
          </span>
        </div>
      ))}
    </div>
  );
};

export default AgentActivity;
