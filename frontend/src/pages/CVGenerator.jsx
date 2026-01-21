import { useState } from "react";

export default function CVGenerator() {
  const [form, setForm] = useState({
    name: "",
    target_role: "",
    self_intro: "",
    skills: "",
    projects: "",
    education: ""
  });

  const [cv, setCv] = useState("");
  const [loading, setLoading] = useState(false);

  const generateCV = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/cv/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name,
        target_role: form.target_role,
        self_intro: form.self_intro,
        skills: form.skills.split(",").map(s => s.trim()),
        projects: form.projects.split(",").map(p => p.trim()),
        education: form.education
      })
    });

    const data = await res.json();
    setCv(data.cv);
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">
        ATS-Optimized CV Generator (LLaMA-3.1)
      </h2>

      <input placeholder="Full Name" onChange={e => setForm({...form, name:e.target.value})} />
      <input placeholder="Target Role" onChange={e => setForm({...form, target_role:e.target.value})} />
      <textarea placeholder="Professional Summary" onChange={e => setForm({...form, self_intro:e.target.value})} />
      <textarea placeholder="Skills (comma separated)" onChange={e => setForm({...form, skills:e.target.value})} />
      <textarea placeholder="Projects / Experience (comma separated)" onChange={e => setForm({...form, projects:e.target.value})} />
      <textarea placeholder="Education" onChange={e => setForm({...form, education:e.target.value})} />

      <button
        onClick={generateCV}
        disabled={loading}
        className="mt-4 bg-black text-white px-4 py-2"
      >
        {loading ? "Generating..." : "Generate CV"}
      </button>

      {cv && (
        <pre className="mt-6 p-4 bg-gray-100 whitespace-pre-wrap">
          {cv}
        </pre>
      )}
    </div>
  );
}
