import "../styles/dashboard.css";

export default function NetworkingEvents() {
  return (
    <div className="dashboard-wrapper">
      <h1 className="dashboard-title">
        Networking & Hackathon Insights
      </h1>

      {/* Power BI Embed */}
      <div className="powerbi-container">
        <iframe
          title="Networking Events Dashboard"
          src="https://app.powerbi.com/view?r=eyJrIjoiOGU2MGZhMzgtYWRhNy00ZDc5LTg5NDctZTk3ZGZlMTIzMjNjIiwidCI6IjM5ZmU4ZmY2LTUwNjMtNGI0NS1hZDI1LWVkNjBlMjAyNjlhNSJ9"
          frameBorder="0"
          allowFullScreen
        />
      </div>
    </div>
  );
}

<button
  className="orchestrator-btn"
  onClick={() => window.history.back()}
>
  ← Back to Dashboard
</button>

