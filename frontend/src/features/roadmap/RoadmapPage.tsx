export function RoadmapPage() {
  return (
    <div className="space-y-8 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Personalized roadmap</p>
        <h1 className="mt-3 text-3xl font-bold text-slate-950">Preparation plan tailored to your target company and role.</h1>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        {[
          { week: 'Week 1', focus: 'Python fundamentals' },
          { week: 'Week 2', focus: 'Arrays & Strings practice' },
          { week: 'Week 3', focus: 'Hashing & data structures' },
          { week: 'Week 4', focus: 'SQL + database concepts' },
          { week: 'Week 5', focus: 'Technical interview drills' },
          { week: 'Week 6', focus: 'Company-specific mock interview' },
        ].map((item) => (
          <article key={item.week} className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-semibold text-slate-700">{item.week}</p>
            <p className="mt-3 text-base font-semibold text-slate-950">{item.focus}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
