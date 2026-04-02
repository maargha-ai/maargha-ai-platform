import { Brain, Target, Zap, CheckCircle2, ArrowRight } from 'lucide-react';
export default function ThinkingProcess({ id }) {
  const steps = [
    {
      icon: Target,
      title: "Goal Setting",
      desc: "Define your dream career or skill.",
      color: "text-blue-500",
      bg: "bg-blue-500/10"
    },
    {
      icon: Brain,
      title: "AI Analysis",
      desc: "Deep analysis of market & gaps.",
      color: "text-purple-500",
      bg: "bg-purple-500/10"
    },
    {
      icon: Zap,
      title: "Path Generation",
      desc: "Create a custom roadmap.",
      color: "text-amber-500",
      bg: "bg-amber-500/10"
    },
    {
      icon: CheckCircle2,
      title: "Success",
      desc: "Track progress & achieve.",
      color: "text-emerald-500",
      bg: "bg-emerald-500/10"
    }
  ];
  return (
    <section id={id} className="py-24 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">How Maargha Thinks</h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Our AI engine breaks down complex career ambitions into actionable, logical steps.
          </p>
        </div>
        <div className="relative grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="hidden md:block absolute top-12 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-border to-transparent -z-10" />
          {steps.map((step, index) => (
            <div 
              key={index} 
              className="group relative flex flex-col items-center text-center p-6 bg-card border border-border/50 rounded-2xl shadow-sm hover:shadow-md hover:border-primary/20 transition-all duration-300"
            >
              <div className={`w-16 h-16 rounded-2xl ${step.bg} ${step.color} flex items-center justify-center mb-6 relative z-10 group-hover:scale-110 transition-transform`}>
                <step.icon size={32} />
              </div>
              <h3 className="text-xl font-bold mb-2">{step.title}</h3>
              <p className="text-muted-foreground">{step.desc}</p>
              {index < steps.length - 1 && (
                <ArrowRight className="md:hidden absolute -bottom-6 left-1/2 -translate-x-1/2 text-muted-foreground/30" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}


