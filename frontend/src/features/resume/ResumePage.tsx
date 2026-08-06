export function ResumePage() {
  return (
    <div className="space-y-8 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Resume analysis</p>
        <h1 className="mt-3 text-3xl font-bold text-slate-950">Get AI feedback on resume readiness.</h1>
      </div>
      <div className="rounded-3xl border border-slate-200 bg-slate-50 p-8">
        <p className="text-sm text-slate-600">Upload your resume and PrepAI will identify keyword gaps, experience fit, and improvement opportunities aligned to your target role.</p>
        <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center">
          <input type="file" className="rounded-3xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none" aria-label="Upload resume" />
          <button className="rounded-3xl bg-primary px-6 py-3 text-sm font-semibold text-white hover:bg-secondary">Analyze Resume</button>
        </div>
      </div>
    </div>
  );
}
