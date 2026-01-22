import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Upload,
  FileText,
  CheckCircle2,
  AlertCircle,
  Loader2
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";

export default function ResumeParser() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("Please upload a valid PDF file.");
    }
  };

  const submit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/resume/parse", {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error("Failed to parse resume");
      const data = await res.json();
      setResult(data.entities || data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen w-full bg-background text-foreground font-sans ${theme}`}>
      <div className="fixed inset-0 pointer-events-none opacity-20">
        <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px]" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-500/10 blur-[120px]" />
      </div>

      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-xl">
        <div className="container flex h-16 items-center px-6">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/dashboard")}
            className="rounded-full absolute left-6"
          >
            <ArrowLeft size={20} />
          </Button>
          <div className="flex flex-col items-center flex-1">
            <h1 className="text-xl font-bold tracking-tight">Resume Intelligence</h1>
            <span className="text-[10px] text-muted-foreground uppercase tracking-widest font-bold">Analysis Engine</span>
          </div>
        </div>
      </header>

      <main className="container max-w-4xl mx-auto px-6 py-12 relative z-10">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-3 tracking-tight">Extract Career Data</h2>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Upload your resume to identify key entities, skills, and experience markers.
          </p>
        </div>

        <div className="grid gap-8">
          <div className={`border-2 border-dashed rounded-3xl p-12 text-center transition-all ${file ? 'border-primary/50 bg-primary/5' : 'border-border/60 hover:border-primary/30'}`}>
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              accept="application/pdf"
              onChange={handleFileChange}
            />

            {!file ? (
              <div className="flex flex-col items-center gap-4 cursor-pointer" onClick={() => fileInputRef.current.click()}>
                <div className="w-16 h-16 rounded-2xl bg-secondary flex items-center justify-center text-primary">
                  <Upload size={32} />
                </div>
                <div>
                  <p className="text-lg font-semibold">Drop your resume here</p>
                  <p className="text-sm text-muted-foreground">or click to browse from your computer (PDF only)</p>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center gap-6">
                <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
                  <FileText size={32} />
                </div>
                <div className="text-left">
                  <p className="text-lg font-semibold uppercase tracking-tight">{file.name}</p>
                  <p className="text-sm text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB • Ready</p>
                </div>
                <Button variant="outline" size="sm" onClick={() => setFile(null)} className="ml-4 rounded-xl">Replace</Button>
              </div>
            )}
          </div>

          <div className="flex justify-center">
            <Button
              size="lg"
              onClick={submit}
              disabled={!file || loading}
              className="px-12 rounded-2xl h-14 text-base font-semibold transition-all hover:scale-105 active:scale-95"
            >
              {loading ? (
                <div className="flex items-center gap-3">
                  <Loader2 size={20} className="animate-spin" />
                  Processing...
                </div>
              ) : "Start Analysis"}
            </Button>
          </div>

          {error && (
            <div className="bg-destructive/10 border border-destructive/20 text-destructive p-4 rounded-2xl flex items-center gap-3">
              <AlertCircle size={20} />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          {result && (
            <div className="bg-card border border-border/50 rounded-3xl p-8 shadow-xl shadow-black/5">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center">
                  <CheckCircle2 size={24} />
                </div>
                <h3 className="text-xl font-bold tracking-tight">Extracted Information</h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(result).map(([key, value]) => (
                  <div key={key} className="p-4 rounded-2xl bg-secondary/30 border border-border/30">
                    <p className="text-[10px] uppercase tracking-widest text-muted-foreground font-bold mb-1">{key}</p>
                    <p className="text-sm font-semibold">{Array.isArray(value) ? value.join(", ") : String(value)}</p>
                  </div>
                ))}
              </div>

              <div className="mt-8 p-4 rounded-2xl bg-primary/5 border border-primary/10">
                <p className="text-xs text-muted-foreground leading-relaxed">
                  These entities were identified from your document. You can use these insights to refine your career roadmap or professional profile.
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
