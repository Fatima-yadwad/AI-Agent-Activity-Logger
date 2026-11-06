
import { useEffect, useState } from "react";
import { getExecutions } from "../services/api";

const History = () => {
  const [executions, setExecutions] = useState([]);

  useEffect(() => {
    getExecutions()
      .then(setExecutions)
      .catch((error) => {
        console.error("Unable to load execution history:", error);
      });
  }, []);

  return (
    <main className="history-page">
      <h1>Execution History</h1>
      <p>All previously recorded AI executions.</p>

      {executions.length === 0 ? (
        <p className="empty-state">No executions found.</p>
      ) : (
        <div className="panel">
          {executions.map((execution) => (
            <div className="history-row" key={execution.execution_id}>
              <div>
                <strong>{execution.user_input}</strong>
                <p>
                  {execution.execution_mode} · {execution.status}
                </p>
                <small>
                  {execution.started_at
                    ? new Date(execution.started_at).toLocaleString()
                    : ""}
                </small>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
};

export default History;
