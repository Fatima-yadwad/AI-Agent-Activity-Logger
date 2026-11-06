
const Statistics = ({ statistics }) => {
  const cards = [
    {
      title: "Total Executions",
      value: statistics.total_executions ?? 0,
      icon: "📊",
    },
    {
      title: "Successful",
      value: statistics.successful_executions ?? 0,
      icon: "✅",
    },
    {
      title: "Failed",
      value: statistics.failed_executions ?? 0,
      icon: "❌",
    },
    {
      title: "Agent Actions",
      value: statistics.total_agent_actions ?? 0,
      icon: "🤖",
    },
    {
      title: "Tool Calls",
      value: statistics.total_tool_calls ?? 0,
      icon: "🛠️",
    },
  ];

  return (
    <div className="statistics-grid">
      {cards.map((card) => (
        <div className="stat-card" key={card.title}>
          <div className="stat-icon">{card.icon}</div>
          <p>{card.title}</p>
          <h2>{card.value}</h2>
        </div>
      ))}
    </div>
  );
};

export default Statistics;
