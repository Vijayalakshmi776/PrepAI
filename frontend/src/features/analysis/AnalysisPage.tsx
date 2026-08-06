export function AnalysisPage() {
  return (
    <div className="space-y-8 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">AI analysis</p>
        <h1 className="mt-3 text-3xl font-bold text-slate-950">Understand your strengths and improvement priorities.</h1>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <p className="text-sm text-slate-500">Placement readiness by category</p>
          <div className="mt-6 space-y-5">
            {[
              { label: 'Aptitude', score: 72 },
              { label: 'Coding', score: 48 },
              { label: 'Technical', score: 61 },
              { label: 'Communication', score: 75 },
            ].map((item) => (
              <div key={item.label} className="space-y-2">
                <div className="flex items-center justify-between text-sm font-semibold text-slate-800">
                  <span>{item.label}</span>
                  <span>{item.score}%</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-slate-200">
                  <div className="h-full rounded-full bg-primary" style={{ width: `${item.score}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <p className="text-sm text-slate-500">AI summary</p>
          <div className="mt-6 space-y-5 text-sm leading-6 text-slate-700">
            <div>
              <p className="font-semibold text-slate-900">Strengths</p>
              <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
                <li>Communication</li>
                <li>Basic Python</li>
              </ul>
            </div>
            <div>
              <p className="font-semibold text-slate-900">Needs improvement</p>
              <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
                <li>Data Structures</li>
                <li>SQL</li>
                <li>Coding problem solving</li>
              </ul>
            </div>
            <div className="rounded-3xl bg-white p-4 text-sm text-slate-700 shadow-sm">
              <p className="font-semibold text-slate-900">Why it matters</p>
              <p className="mt-2">Data Structures and SQL frequently appear in TCS and Infosys selection rounds, and strengthening them will improve both aptitude and technical interview performance.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
