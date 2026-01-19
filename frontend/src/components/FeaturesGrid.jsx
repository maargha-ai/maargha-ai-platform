import { Share2, BookOpen, UserCheck, BarChart3, Radio, Github, Code2 } from 'lucide-react';
export default function FeaturesGrid() {
  return (
    <section id="features" className="py-24 bg-secondary/30">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-12">
          <span className="text-primary font-semibold tracking-wider text-sm uppercase">Features</span>
          <h2 className="text-3xl md:text-5xl font-bold mt-2">Everything you need to grow</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 md:grid-rows-2 gap-6 h-auto md:h-[600px]">
          <div className="md:col-span-2 md:row-span-2 bg-card rounded-3xl p-8 border border-border shadow-sm hover:shadow-xl transition-all relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
              <Code2 size={200} />
            </div>
            <div className="relative z-10 h-full flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary mb-4">
                  <BookOpen />
                </div>
                <h3 className="text-2xl font-bold mb-2">AI Career Roadmap</h3>
                <p className="text-muted-foreground max-w-md">
                  Generate a personalized, step-by-step career path tailored to your skills and goals. 
                  Our AI analyzes market trends to keep you relevant.
                </p>
              </div>
              <div className="w-full bg-secondary/50 rounded-xl p-4 mt-8 border border-border/50">
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
          {}
          <div className="md:col-span-1 bg-card rounded-3xl p-8 border border-border shadow-sm hover:shadow-xl transition-all group">
            <div className="w-12 h-12 bg-purple-500/10 text-purple-600 rounded-xl flex items-center justify-center mb-4">
              <UserCheck />
            </div>
            <h3 className="text-xl font-bold mb-2">LinkedIn Audit</h3>
            <p className="text-sm text-muted-foreground">
              Optimize your profile with AI suggestions to rank higher in recruiter searches.
            </p>
          </div>
          <div className="md:col-span-1 bg-card rounded-3xl p-8 border border-border shadow-sm hover:shadow-xl transition-all group">
            <div className="w-12 h-12 bg-amber-500/10 text-amber-600 rounded-xl flex items-center justify-center mb-4">
              <BarChart3 />
            </div>
            <h3 className="text-xl font-bold mb-2">Skill Gap Analysis</h3>
            <p className="text-sm text-muted-foreground">
              Identify missing skills and get recommended courses instantly.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-6">
           <FeatureCards 
             icon={<Share2 />} 
             title="Networking" 
             desc="Find events." 
           />
           <FeatureCards 
             icon={<Radio />} 
             title="Daily News" 
             desc="Stay updated." 
           />
           <FeatureCards 
             icon={<Github />} 
             title="Project Ideas" 
             desc="Build portfolio." 
           />
           <FeatureCards 
             icon={<Code2 />} 
             title="Code Review" 
             desc="Get feedback." 
             className="bg-primary text-primary-foreground"
             iconClassName="text-primary-foreground"
             descClassName="text-primary-foreground/80"
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
      <h4 className="font-bold">{title}</h4>
      <p className={`text-sm ${descClassName}`}>{desc}</p>
    </div>
  )
}


