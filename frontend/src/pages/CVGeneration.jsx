import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Sparkles, 
  Plus, 
  Trash2, 
  GraduationCap, 
  Briefcase, 
  User, 
  FileText,
  Terminal,
  BrainCircuit,
  Link as LinkIcon,
  Github
} from 'lucide-react';
import { useTheme } from '../components/ThemeProvider';
import { Button } from "../components/ui/button";
import '../styles/cv.css';

export default function CVGeneration() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    fullName: "",
    targetRole: "",
    selfIntro: "",
    skills: [],
    education: [{ school: "", degree: "", year: "" }],
    projects: [{ name: "", tech: "", desc: "", github: "", live: "" }]
  });

  const [skillInput, setSkillInput] = useState("");

  const addSkill = () => {
    if (skillInput.trim() && !formData.skills.includes(skillInput.trim())) {
      setFormData({ ...formData, skills: [...formData.skills, skillInput.trim()] });
      setSkillInput("");
    }
  };

  const removeSkill = (skill) => {
    setFormData({ ...formData, skills: formData.skills.filter(s => s !== skill) });
  };

  const updateEducation = (index, field, value) => {
    const newEdu = [...formData.education];
    newEdu[index][field] = value;
    setFormData({ ...formData, education: newEdu });
  };

  const addEducation = () => {
    setFormData({ ...formData, education: [...formData.education, { school: "", degree: "", year: "" }] });
  };

  const removeEducation = (index) => {
    setFormData({ ...formData, education: formData.education.filter((_, i) => i !== index) });
  };

  const updateProject = (index, field, value) => {
    const newProj = [...formData.projects];
    newProj[index][field] = value;
    setFormData({ ...formData, projects: newProj });
  };

  const addProject = () => {
    setFormData({ ...formData, projects: [...formData.projects, { name: "", tech: "", desc: "", github: "", live: "" }] });
  };

  const removeProject = (index) => {
    setFormData({ ...formData, projects: formData.projects.filter((_, i) => i !== index) });
  };

  const handleGenerate = async () => {
    setLoading(true);

    // ---- transform education ----
    const educationText = formData.education
      .map(
        edu =>
          `${edu.degree} - ${edu.school} (${edu.year || "Year not specified"})`
      )
      .join("\n");

    // ---- transform projects ----
    const projectsText = formData.projects.map(proj => {
      return `${proj.name} | ${proj.tech}
  - ${proj.desc}
  ${proj.github ? "GitHub: " + proj.github : ""}
  ${proj.live ? "Live: " + proj.live : ""}`;
    });

    const payload = {
      name: formData.fullName,
      target_role: formData.targetRole,
      self_intro: formData.selfIntro,
      skills: formData.skills,
      education: educationText,
      projects: projectsText
    };

    try {
      const res = await fetch("http://localhost:8000/cv/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (data.status === "success") {
        alert("CV generated successfully");
        console.log(data.cv); // later show in UI
      } else {
        alert("CV generation failed");
      }
    } catch (err) {
      console.error(err);
      alert("Error connecting to CV service");
    } finally {
      setLoading(false);
    }
  };

  const generateCVPdf = async (download = false) => {
    setLoading(true);

    // ---- same payload as text CV ----
    const educationText = formData.education
      .map(
        edu =>
          `${edu.degree} - ${edu.school} (${edu.year || "Year not specified"})`
      )
      .join("\n");

    const projectsText = formData.projects.map(proj => {
      return `${proj.name} | ${proj.tech}
  - ${proj.desc}
  ${proj.github ? "GitHub: " + proj.github : ""}
  ${proj.live ? "Live: " + proj.live : ""}`;
    });

    const payload = {
      name: formData.fullName,
      target_role: formData.targetRole,
      self_intro: formData.selfIntro,
      skills: formData.skills,
      education: educationText,
      projects: projectsText
    };

    try {
      const endpoint = download
        ? "/cv/generate/pdf/download"
        : "/cv/generate/pdf";

      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      if (download) {
        const a = document.createElement("a");
        a.href = url;
        a.download = "generated_cv.pdf";
        a.click();
      } else {
        window.open(url, "_blank");
      }

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Failed to generate PDF");
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className={`cv-layout ${theme}`}>
      <div className="cv-bg"></div>
      <main className="cv-main">
        <header className="cv-header">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")} className="rounded-full">
              <ArrowLeft size={22} />
            </Button>
            <div className="cv-brand">
              <div className="cv-logo">
                <FileText size={22} />
              </div>
              <div>
                <h1 className="text-xl font-bold leading-none">CV ARCHITECT</h1>
                <span className="text-xs text-muted-foreground">STRATEGIC CAREER ASSET ENGINEERING</span>
              </div>
            </div>
          </div>
        </header>

        <div className="cv-container">
          <div className="cv-form-flow">
            <section className="cv-form-section mb-8">
              <h2 className="section-title">
                <User size={20} />
                PROFESSIONAL SUMMARY
              </h2>
              <div className="form-group">
                <label className="label-box">Full Name</label>
                <input 
                  type="text" 
                  className="cv-input" 
                  placeholder="e.g. Alexander Pierce"
                  value={formData.fullName}
                  onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label className="label-box">Target Role</label>
                <input 
                  type="text"
                  className="cv-input"
                  placeholder="e.g. Machine Learning Engineer, Backend Developer"
                  value={formData.targetRole}
                  onChange={(e) =>
                    setFormData({ ...formData, targetRole: e.target.value })
                  }
                />
              </div>
              <div className="form-group">
                <label className="label-box">Self Introduction</label>
                <textarea 
                  className="cv-textarea" 
                  rows={4} 
                  placeholder="Elevate your profile with a powerful summary of your expertise..."
                  value={formData.selfIntro}
                  onChange={(e) => setFormData({...formData, selfIntro: e.target.value})}
                />
              </div>
            </section>

            <section className="cv-form-section mb-8">
              <h2 className="section-title">
                <BrainCircuit size={20} />
                CORE COMPETENCIES
              </h2>
              <div className="form-group">
                <label className="label-box">Add Expertise</label>
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    className="cv-input" 
                    placeholder="e.g. Distributed Systems, Product Strategy"
                    value={skillInput}
                    onChange={(e) => setSkillInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && addSkill()}
                  />
                  <Button onClick={addSkill} variant="outline" className="rounded-lg h-12 px-6">Add</Button>
                </div>
              </div>
              <div className="tag-container">
                {formData.skills.map(skill => (
                  <div key={skill} className="tag-chip">
                    {skill}
                    <Trash2 size={14} className="tag-remove" onClick={() => removeSkill(skill)} />
                  </div>
                ))}
              </div>
            </section>

            <section className="cv-form-section mb-8">
              <h2 className="section-title">
                <GraduationCap size={20} />
                ACADEMIC BACKGROUND
              </h2>
              {formData.education.map((edu, idx) => (
                <div key={idx} className="item-card">
                  <div className="item-actions">
                    <Button variant="ghost" size="icon" onClick={() => removeEducation(idx)} className="text-muted-foreground hover:text-destructive h-8 w-8">
                      <Trash2 size={16} />
                    </Button>
                  </div>
                  <div className="grid grid-cols-2 gap-6">
                    <div className="form-group mb-0">
                      <label className="label-box">Institution</label>
                      <input 
                        type="text" 
                        className="cv-input" 
                        value={edu.school}
                        onChange={(e) => updateEducation(idx, 'school', e.target.value)}
                      />
                    </div>
                    <div className="form-group mb-0">
                      <label className="label-box">Degree</label>
                      <input 
                        type="text" 
                        className="cv-input" 
                        value={edu.degree}
                        onChange={(e) => updateEducation(idx, 'degree', e.target.value)}
                      />
                    </div>
                  </div>
                </div>
              ))}
              <button className="btn-add" onClick={addEducation}>
                Add Education Item
              </button>
            </section>

            <section className="cv-form-section">
              <h2 className="section-title">
                <Terminal size={20} />
                TECHNICAL PROJECTS
              </h2>
              {formData.projects.map((proj, idx) => (
                <div key={idx} className="item-card">
                  <div className="item-actions">
                    <Button variant="ghost" size="icon" onClick={() => removeProject(idx)} className="text-muted-foreground hover:text-destructive h-8 w-8">
                      <Trash2 size={16} />
                    </Button>
                  </div>
                  <div className="grid grid-cols-2 gap-6 mb-6">
                    <div className="form-group mb-0">
                      <label className="label-box">Project Title</label>
                      <input 
                        type="text" 
                        className="cv-input" 
                        value={proj.name}
                        onChange={(e) => updateProject(idx, 'name', e.target.value)}
                      />
                    </div>
                    <div className="form-group mb-0">
                      <label className="label-box">Primary Tech Stack</label>
                      <input 
                        type="text" 
                        className="cv-input" 
                        placeholder="e.g. React, Node.js, AWS"
                        value={proj.tech}
                        onChange={(e) => updateProject(idx, 'tech', e.target.value)}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-6 mb-6">
                    <div className="form-group mb-0">
                      <label className="label-box">GitHub Repository</label>
                      <div className="relative">
                        <Github size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                        <input 
                          type="text" 
                          className="cv-input pl-10" 
                          placeholder="github.com/your-repo"
                          value={proj.github}
                          onChange={(e) => updateProject(idx, 'github', e.target.value)}
                        />
                      </div>
                    </div>
                    <div className="form-group mb-0">
                      <label className="label-box">Deployment Link</label>
                      <div className="relative">
                        <LinkIcon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                        <input 
                          type="text" 
                          className="cv-input pl-10" 
                          placeholder="live-project.com"
                          value={proj.live}
                          onChange={(e) => updateProject(idx, 'live', e.target.value)}
                        />
                      </div>
                    </div>
                  </div>
                  <div className="form-group mb-0">
                    <label className="label-box">Impact & Contribution</label>
                    <textarea 
                      className="cv-textarea" 
                      rows={3}
                      placeholder="Detail your specific contributions and the project's impact..."
                      value={proj.desc}
                      onChange={(e) => updateProject(idx, 'desc', e.target.value)}
                    />
                  </div>
                </div>
              ))}
              <button className="btn-add" onClick={addProject}>
                Add Project Case Study
              </button>
            </section>
          </div>

          <aside className="cv-preview-sidebar">
            <div className="preview-card">
              <div className="preview-avatar-circle"></div>
              <h3 className="preview-name">{formData.fullName || "Your Identity"}</h3>
              <p className="preview-role">{formData.targetRole || "Target Role"}</p>
              
              <div className="completion-stats">
                <div className="flex justify-between text-xs font-bold mb-3 uppercase tracking-wider">
                  <span className="text-muted-foreground">Dossier Readiness</span>
                  <span>75%</span>
                </div>
                <div className="w-full h-1 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-foreground w-[75%]"></div>
                </div>
              </div>

              <div className="mt-8 pt-8 border-t border-border">
                <p className="text-xs text-muted-foreground leading-relaxed mb-6">
                  Finalize your data entries to enable AI-powered professional asset formatting.
                </p>
                <div className="flex flex-col gap-3">
                  <button
                    className="generate-btn"
                    onClick={handleGenerate}
                    disabled={loading}
                  >
                    {loading ? "PROCESSING..." : "GENERATE TEXT CV"}
                  </button>

                  <button
                    className="generate-btn"
                    onClick={() => generateCVPdf(false)}
                    disabled={loading}
                  >
                    VIEW PDF
                  </button>

                  <button
                    className="generate-btn"
                    onClick={() => generateCVPdf(true)}
                    disabled={loading}
                  >
                    DOWNLOAD PDF
                  </button>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
}
