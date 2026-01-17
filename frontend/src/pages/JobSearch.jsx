import { useState } from "react";

export default function JobSearch() {
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [cv, setCv] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!role || !location || !cv) return;

    setLoading(true);
    setJobs([]);

    const formData = new FormData();
    formData.append("role", role);
    formData.append("location", location);
    formData.append("cv", cv);

    const res = await fetch("http://localhost:8000/jobs/match", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: formData,
    });

    const data = await res.json();
    setJobs(data.jobs || []);
    setLoading(false);
  };

  return (
    <div className="jobs-page">
      <h2>AI Job Matcher</h2>

      <input
        placeholder="Job title (e.g. Data Scientist)"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      />

      <input
        placeholder="Location (e.g. Bangalore)"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setCv(e.target.files[0])}
      />

      <button onClick={submit} disabled={loading}>
        {loading ? "Matching jobs..." : "Find Jobs"}
      </button>

      {jobs.length > 0 && (
        <div className="jobs-results">
          <h3>Top Matches</h3>

          {jobs.map((job, i) => (
            <div key={i} className="job-card">
              <h4>{job.title}</h4>
              <p><b>{job.company}</b> • {job.source}</p>
              <p>{job.desc}</p>

              <a href={job.link} target="_blank" rel="noreferrer">
                View Job →
              </a>

              <span className="score">
                Match Score: {(job.score * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
