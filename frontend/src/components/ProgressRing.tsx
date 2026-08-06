interface ProgressRingProps {
  progress: number;
  label: string;
}

export function ProgressRing({ progress, label }: ProgressRingProps) {
  const normalized = Math.max(0, Math.min(100, progress));
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalized / 100) * circumference;

  return (
    <div className="flex items-center gap-4">
      <svg width="96" height="96" viewBox="0 0 96 96" className="rotate-[-90deg]">
        <circle cx="48" cy="48" r={radius} stroke="#E5E7EB" strokeWidth="10" fill="transparent" />
        <circle
          cx="48"
          cy="48"
          r={radius}
          stroke="#4F46E5"
          strokeWidth="10"
          strokeLinecap="round"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
        />
      </svg>
      <div className="text-sm">
        <p className="text-2xl font-bold text-slate-950">{normalized}%</p>
        <p className="text-slate-500">{label}</p>
      </div>
    </div>
  );
}
