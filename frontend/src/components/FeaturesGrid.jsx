import { Share2, BookOpen, UserCheck, BarChart3, Radio, Github, Code2, Briefcase, FileText, Brain, Music, Users, GraduationCap, Search } from 'lucide-react';
export default function FeaturesGrid() {
  return (
    <section id="features" className="py-24 bg-secondary/30">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-12">
          <span className="text-primary font-semibold tracking-wider text-sm uppercase">Features</span>
          <h2 className="text-3xl md:text-5xl font-bold mt-2">Everything you need to grow</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 md:grid-rows-2 gap-4 h-auto md:h-[500px]">
          <div className="md:col-span-2 md:row-span-2 bg-card rounded-3xl p-6 border border-border shadow-sm hover:shadow-xl transition-all relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
              <Code2 size={160} />
            </div>
            <div className="relative z-10 h-full flex flex-col justify-between">
              <div>
                <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary mb-3">
                  <BookOpen size={20} />
                </div>
                <h3 className="text-xl font-bold mb-2">AI Career Roadmap</h3>
                <p className="text-sm text-muted-foreground max-w-md">
                  Generate a personalized, step-by-step career path tailored to your skills and goals. 
                  Our AI analyzes market trends to keep you relevant.
                </p>
              </div>
              <div className="w-full bg-secondary/50 rounded-xl p-3 mt-6 border border-border/50">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-xs font-mono text-muted-foreground">AI ANALYZING SKILLS...</span>
                </div>
                <div className="space-y-2">
                  <div className="h-2 w-3/4 bg-primary/10 rounded-full" />
                  <div className="h-2 w-1/2 bg-primary/10 rounded-full" />
                </div>
              </div>
            </div>
          </div>
          <div className="md:col-span-1 bg-card rounded-3xl p-6 border border-border shadow-sm hover:shadow-xl transition-all group">
            <div className="w-10 h-10 bg-purple-500/10 text-purple-600 rounded-xl flex items-center justify-center mb-3">
              <UserCheck size={20} />
            </div>
            <h3 className="text-lg font-bold mb-2">LinkedIn Assistant</h3>
            <p className="text-xs text-muted-foreground">
              Optimize your profile with AI suggestions to rank higher in recruiter searches.
            </p>
          </div>
          <div className="md:col-span-1 bg-card rounded-3xl p-6 border border-border shadow-sm hover:shadow-xl transition-all group">
            <div className="w-10 h-10 bg-pink-500/10 text-pink-600 rounded-xl flex items-center justify-center mb-3">
              <Brain size={20} />
            </div>
            <h3 className="text-lg font-bold mb-2">Emily - Emotional Support</h3>
            <p className="text-xs text-muted-foreground">
              Your AI companion for mental wellness, providing guidance and support through your career journey.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-6">
           <FeatureCards 
             icon={<Search />} 
             title="Job Search" 
             desc="Find opportunities." 
           />
           <FeatureCards 
             icon={<Brain />} 
             title="AI Tutor" 
             desc="Learn smarter." 
           />
           <FeatureCards 
             icon={<Music />} 
             title="Music Therapy" 
             desc="Stay focused." 
           />
           <FeatureCards 
             icon={<Users />} 
             title="Networking Events" 
             desc="Connect & grow." 
           />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-6">
           <FeatureCards 
             icon={<FileText />} 
             title="Resume Parser" 
             desc="Analyze CVs." 
           />
           <FeatureCards 
             icon={<Briefcase />} 
             title="CV Generator" 
             desc="Build resumes." 
           />
           <FeatureCards 
             icon={<GraduationCap />} 
             title="Quiz Section" 
             desc="Test knowledge." 
           />
           <FeatureCards 
             icon={<Radio />} 
             title="Tech News" 
             desc="Stay updated." 
             className="bg-foreground text-background border border-background/20"
             iconClassName="text-background"
             descClassName="text-background/70"
           />
        </div>
      </div>
    </section>
  );
}
function FeatureCards({ icon, title, desc, className = "bg-card", iconClassName = "text-primary", descClassName = "text-muted-foreground" }) {
  return (
    <div className={`p-6 rounded-2xl border border-border shadow-sm flex flex-col justify-center gap-2 hover:-translate-y-1 transition-transform cursor-default ${className}`}>
      <div className={`${iconClassName} mb-2`}>{icon}</div>
      <h4 className={`font-bold ${iconClassName}`}>{title}</h4>
      <p className={`text-sm ${descClassName}`}>{desc}</p>
    </div>
  )
}


