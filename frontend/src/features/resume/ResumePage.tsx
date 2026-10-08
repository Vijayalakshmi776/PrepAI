import { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText,
  UploadCloud,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  RefreshCw,
  Trash2,
  History,
  Award,
  Target,
  Briefcase,
  Clock,
  ArrowRight,
  ShieldCheck,
  FileCheck,
  Layers,
  TrendingUp,
  Zap,
  Check,
  AlertCircle,
  X,
  Plus,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { resumeApi } from '../../services/api';
import type { ResumeAnalysisDetail, ResumeSummaryItem } from '../../types/resume';

export function ResumePage() {
  const [currentAnalysis, setCurrentAnalysis] = useState<ResumeAnalysisDetail | null>(null);
  const [history, setHistory] = useState<ResumeSummaryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [selectedTargetRole, setSelectedTargetRole] = useState<string>('Frontend Developer');

  const SUPPORTED_ROLES = [
    'Frontend Developer',
    'Backend Developer',
    'Full Stack Developer',
    'Software Engineer',
    'AI/ML Engineer',
  ];

  // Fetch latest analysis and history on mount
  const loadData = async () => {
    try {
      setLoading(true);
      setUploadError(null);
      const [histData, latestData] = await Promise.allSettled([
        resumeApi.getHistory(),
        resumeApi.getLatestAnalysis(),
      ]);

      if (histData.status === 'fulfilled') {
        setHistory(histData.value);
      }
      if (latestData.status === 'fulfilled') {
        setCurrentAnalysis(latestData.value);
        if (latestData.value.target_role) {
          setSelectedTargetRole(latestData.value.target_role);
        }
      } else {
        setCurrentAnalysis(null);
      }
    } catch {
      // Handled cleanly
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleFileChange = (file: File | undefined) => {
    setUploadError(null);
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf') && file.type !== 'application/pdf') {
      setUploadError('Invalid file format. Please upload a PDF file (.pdf).');
      setSelectedFile(null);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setUploadError('File size exceeds the 10MB limit. Please upload a smaller PDF.');
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) return;

    try {
      setAnalyzing(true);
      setUploadError(null);
      const result = await resumeApi.analyzeResume(selectedFile, selectedTargetRole);
      setCurrentAnalysis(result);
      if (result.target_role) {
        setSelectedTargetRole(result.target_role);
      }
      setSelectedFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';

      // Refresh history list
      const updatedHistory = await resumeApi.getHistory();
      setHistory(updatedHistory);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Resume analysis failed. Please try again.';
      setUploadError(msg);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSelectHistoryItem = async (resumeId: string) => {
    try {
      setLoading(true);
      setUploadError(null);
      const detail = await resumeApi.getAnalysis(resumeId);
      setCurrentAnalysis(detail);
      if (detail.target_role) {
        setSelectedTargetRole(detail.target_role);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to load analysis.';
      setUploadError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteResume = async (resumeId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this resume analysis?')) return;

    try {
      setDeletingId(resumeId);
      await resumeApi.deleteResume(resumeId);
      const updatedHistory = history.filter((item) => item.resume_id !== resumeId);
      setHistory(updatedHistory);

      if (currentAnalysis?.resume_id === resumeId) {
        if (updatedHistory.length > 0) {
          const next = await resumeApi.getAnalysis(updatedHistory[0].resume_id);
          setCurrentAnalysis(next);
        } else {
          setCurrentAnalysis(null);
        }
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to delete resume.';
      setUploadError(msg);
    } finally {
      setDeletingId(null);
    }
  };

  // Loading skeleton
  if (loading) {
    return (
      <div className="space-y-8 animate-pulse">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
          <div className="h-4 w-32 rounded-full bg-slate-200" />
          <div className="mt-4 h-8 w-2/3 rounded-xl bg-slate-200" />
          <div className="mt-2 h-4 w-1/2 rounded-md bg-slate-100" />
          <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-24 rounded-2xl bg-slate-100" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header & Hero */}
      <section className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-3.5 py-1 text-xs font-bold uppercase tracking-wider text-primary">
                <Sparkles className="h-3.5 w-3.5" />
                AI Resume Intelligence
              </span>
              <div className="flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700 border border-slate-200">
                <Target className="h-3.5 w-3.5 text-primary shrink-0" />
                <span>Target Role:</span>
                <select
                  value={selectedTargetRole}
                  onChange={(e) => setSelectedTargetRole(e.target.value)}
                  className="bg-transparent font-bold text-slate-900 focus:outline-none cursor-pointer pr-1"
                >
                  {SUPPORTED_ROLES.map((role) => (
                    <option key={role} value={role}>
                      {role}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <h1 className="mt-3 text-2xl font-black text-slate-950 sm:text-3xl lg:text-4xl">
              ATS Score & Resume Diagnostics
            </h1>
            <p className="mt-2 max-w-3xl text-sm text-slate-600 sm:text-base">
              Upload your PDF resume to extract verified skills, evaluate suitability for your selected target role, get evidence-based job recommendations, and boost your callback rate.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              as={Link}
              to="/roadmap"
              variant="outline"
              className="border-slate-300 hover:bg-slate-50"
            >
              <Layers className="h-4 w-4 mr-1.5" /> View Roadmap
            </Button>
            <Button as={Link} to="/interview" className="inline-flex items-center gap-2">
              <Sparkles className="h-4 w-4" /> Practice Interview
            </Button>
          </div>
        </div>
      </section>

      {/* Upload Zone & History Bar */}
      <div className="grid gap-8 lg:grid-cols-[1.3fr_0.7fr]">
        {/* Upload Card */}
        <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-950">Upload Your Resume (PDF)</h2>
              <p className="mt-1 text-xs text-slate-500">Evaluating against: <strong className="text-primary">{selectedTargetRole}</strong></p>
            </div>
            <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-bold text-primary">
              PDF up to 10MB
            </span>
          </div>

          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`mt-5 flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed p-8 text-center transition-all ${
              dragActive
                ? 'border-primary bg-primary/5 scale-[1.01]'
                : 'border-slate-300 bg-slate-50/60 hover:border-primary hover:bg-slate-50'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              className="hidden"
              aria-label="Upload resume PDF"
              onChange={(e) => handleFileChange(e.target.files?.[0])}
            />

            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary">
              <UploadCloud className="h-7 w-7" />
            </div>

            <p className="mt-4 text-sm font-semibold text-slate-900">
              {selectedFile ? selectedFile.name : 'Click to upload or drag and drop your PDF resume'}
            </p>
            <p className="mt-1 text-xs text-slate-500">
              {selectedFile
                ? `${(selectedFile.size / 1024).toFixed(1)} KB — Ready to evaluate for ${selectedTargetRole}`
                : 'PDF format with selectable text (single or multi-page)'}
            </p>
          </div>

          {uploadError && (
            <div className="mt-4 flex items-center gap-2 rounded-xl bg-rose-50 p-3 text-xs font-medium text-rose-700 border border-rose-200">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{uploadError}</span>
            </div>
          )}

          <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
            {selectedFile && (
              <button
                type="button"
                onClick={() => {
                  setSelectedFile(null);
                  if (fileInputRef.current) fileInputRef.current.value = '';
                }}
                className="text-xs font-medium text-slate-500 hover:text-slate-900"
              >
                Clear file
              </button>
            )}

            <Button
              onClick={handleUploadAndAnalyze}
              disabled={!selectedFile || analyzing}
              className="ml-auto min-w-[160px] inline-flex items-center justify-center gap-2"
            >
              {analyzing ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" /> Evaluating with AI...
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4" /> Run Role Analysis
                </>
              )}
            </Button>
          </div>
        </section>

        {/* History Sidebar */}
        <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <History className="h-5 w-5 text-slate-500" />
              <h2 className="text-lg font-bold text-slate-950">Previous Analyses</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-bold text-slate-700">
              {history.length}
            </span>
          </div>

          <div className="mt-4 space-y-2.5 max-h-[280px] overflow-y-auto pr-1">
            {history.length === 0 ? (
              <p className="text-xs text-slate-500 py-6 text-center">No resumes analyzed yet. Upload one on the left to start.</p>
            ) : (
              history.map((item) => {
                const isSelected = currentAnalysis?.resume_id === item.resume_id;
                return (
                  <div
                    key={item.id}
                    onClick={() => handleSelectHistoryItem(item.resume_id)}
                    className={`group flex items-center justify-between rounded-xl border p-3 cursor-pointer transition ${
                      isSelected
                        ? 'border-primary bg-primary/5 shadow-sm'
                        : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-slate-300'
                    }`}
                  >
                    <div className="min-w-0 flex-1 pr-2">
                      <p className="truncate text-xs font-semibold text-slate-900">{item.title}</p>
                      <p className="mt-0.5 text-[11px] text-slate-500">
                        {new Date(item.created_at).toLocaleDateString(undefined, {
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </p>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-white px-2 py-0.5 text-xs font-bold text-primary shadow-xs border border-slate-200">
                        {item.ats_score}% ATS
                      </span>
                      <button
                        type="button"
                        onClick={(e) => handleDeleteResume(item.resume_id, e)}
                        disabled={deletingId === item.resume_id}
                        className="rounded-lg p-1 text-slate-400 opacity-0 group-hover:opacity-100 hover:bg-rose-50 hover:text-rose-600 transition"
                        aria-label="Delete analysis"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </section>
      </div>

      {/* Analysis Results Display */}
      {currentAnalysis ? (
        <div className="space-y-8">
          {/* Key Score Indicators */}
          <section className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            {/* Overall Score */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Overall Readiness</span>
                <Award className="h-4 w-4 text-primary" />
              </div>
              <p className="mt-2 text-3xl font-black text-slate-950 sm:text-4xl">{currentAnalysis.readiness_score}%</p>
              <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
                <motion.div
                  className="h-full rounded-full bg-gradient-to-r from-primary to-indigo-600"
                  initial={{ width: 0 }}
                  animate={{ width: `${currentAnalysis.readiness_score}%` }}
                  transition={{ duration: 0.6 }}
                />
              </div>
              <p className="mt-2 text-[11px] text-slate-500">Weighted candidate score</p>
            </div>

            {/* ATS Score */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">PrepAI ATS Compatibility Score</span>
                <ShieldCheck className="h-4 w-4 text-emerald-600" />
              </div>
              <p className="mt-2 text-3xl font-black text-emerald-600 sm:text-4xl">{currentAnalysis.ats_score}%</p>
              <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
                <motion.div
                  className="h-full rounded-full bg-emerald-500"
                  initial={{ width: 0 }}
                  animate={{ width: `${currentAnalysis.ats_score}%` }}
                  transition={{ duration: 0.6 }}
                />
              </div>
              <p className="mt-2 text-[11px] text-slate-500">Role-aware ATS score</p>
            </div>

            {/* Role Suitability Score */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Role Suitability</span>
                <Target className="h-4 w-4 text-indigo-600" />
              </div>
              <p className="mt-2 text-3xl font-black text-indigo-600 sm:text-4xl">
                {currentAnalysis.role_suitability_score ?? currentAnalysis.readiness_score}%
              </p>
              <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
                <motion.div
                  className="h-full rounded-full bg-indigo-500"
                  initial={{ width: 0 }}
                  animate={{ width: `${currentAnalysis.role_suitability_score ?? currentAnalysis.readiness_score}%` }}
                  transition={{ duration: 0.6 }}
                />
              </div>
              <p className="mt-2 text-[11px] text-slate-500">{currentAnalysis.target_role} fit</p>
            </div>

            {/* Impact & Action Verbs */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Impact & Metrics</span>
                <TrendingUp className="h-4 w-4 text-amber-500" />
              </div>
              <p className="mt-2 text-3xl font-black text-amber-600 sm:text-4xl">{currentAnalysis.impact_score}%</p>
              <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
                <motion.div
                  className="h-full rounded-full bg-amber-500"
                  initial={{ width: 0 }}
                  animate={{ width: `${currentAnalysis.impact_score}%` }}
                  transition={{ duration: 0.6 }}
                />
              </div>
              <p className="mt-2 text-[11px] text-slate-500">Measurable achievements</p>
            </div>
          </section>

            {/* Role Suitability Section */}
          <section className="rounded-[2rem] border border-primary/20 bg-gradient-to-br from-primary/5 via-white to-indigo-50/30 p-6 shadow-soft sm:p-8">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200/80 pb-5">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-white shadow-sm">
                  <Target className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-slate-950">Target Role Suitability</h2>
                  <p className="text-xs text-slate-500">
                    Evaluated for: <strong className="text-slate-900">{currentAnalysis.target_role}</strong>
                    {currentAnalysis.target_company && currentAnalysis.target_company !== 'Tech Company' && (
                      <span> at <strong className="text-slate-900">{currentAnalysis.target_company}</strong> (Role/Company Alignment)</span>
                    )}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 self-start sm:self-auto">
                <span className="rounded-2xl bg-white px-3.5 py-1.5 text-xs font-black uppercase tracking-wider text-slate-700 shadow-xs border border-slate-200">
                  Status: <strong className="text-primary">{currentAnalysis.role_suitability_status || (currentAnalysis.role_suitability_score && currentAnalysis.role_suitability_score >= 80 ? 'Strong Match' : currentAnalysis.role_suitability_score && currentAnalysis.role_suitability_score >= 70 ? 'Good Match' : 'Partial Match')}</strong>
                </span>
                <span className="rounded-2xl bg-primary px-4 py-2 text-sm font-black text-white shadow-sm">
                  {currentAnalysis.role_suitability_score ?? currentAnalysis.readiness_score}% Fit
                </span>
              </div>
            </div>

            {/* Explanation box */}
            <div className="mt-5 rounded-2xl bg-white p-4 sm:p-5 border border-slate-200/80 shadow-xs">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1">Evidence-Based Assessment</span>
              <p className="text-sm font-medium leading-relaxed text-slate-800">
                "{currentAnalysis.role_suitability_explanation || `Your resume matches ${roundScore(currentAnalysis.skills_score)}% of the core competencies for ${currentAnalysis.target_role}.`}"
              </p>
            </div>

            {/* Matching & Missing Skills breakdown for Selected Role */}
            <div className="mt-5 grid gap-4 sm:grid-cols-2">
              {/* Matching Skills */}
              <div className="rounded-2xl bg-emerald-50/60 p-4 border border-emerald-200/80">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 flex items-center gap-1.5">
                    <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                    Matching Skills ({currentAnalysis.matching_skills.length})
                  </span>
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {currentAnalysis.matching_skills.length === 0 ? (
                    <span className="text-xs text-slate-500 italic">No direct matching core skills found in resume.</span>
                  ) : (
                    currentAnalysis.matching_skills.map((skill) => (
                      <span key={skill} className="inline-flex items-center gap-1 rounded-lg bg-white px-2.5 py-1 text-xs font-bold text-emerald-700 border border-emerald-200 shadow-xs">
                        <Check className="h-3 w-3 stroke-[3]" />
                        {skill}
                      </span>
                    ))
                  )}
                </div>
              </div>

              {/* Missing / Weak Skills */}
              <div className="rounded-2xl bg-amber-50/60 p-4 border border-amber-200/80">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-amber-900 flex items-center gap-1.5">
                    <AlertTriangle className="h-4 w-4 text-amber-600" />
                    Missing / Weak Skills ({currentAnalysis.missing_skills.length})
                  </span>
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {currentAnalysis.missing_skills.length === 0 ? (
                    <span className="text-xs text-emerald-700 font-bold">✓ All core role skills present!</span>
                  ) : (
                    currentAnalysis.missing_skills.map((skill) => (
                      <span key={skill} className="inline-flex items-center gap-1 rounded-lg bg-white px-2.5 py-1 text-xs font-bold text-amber-800 border border-amber-200 shadow-xs">
                        <AlertCircle className="h-3 w-3" />
                        {skill}
                      </span>
                    ))
                  )}
                </div>
              </div>
            </div>
          </section>

          {/* Recommended Job Roles (Evidence-Based Grounded Recommendations) */}
          <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <Briefcase className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-950">Recommended Roles</h2>
                  <p className="text-xs text-slate-500">Realistic role targets based ONLY on extracted resume evidence (&ge; 55% match threshold)</p>
                </div>
              </div>
              <span className="self-start sm:self-auto rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-700 border border-slate-200">
                {currentAnalysis.job_role_recommendations?.length || 0} Grounded Options
              </span>
            </div>

            <div className="mt-5 space-y-4">
              {!currentAnalysis.job_role_recommendations || currentAnalysis.job_role_recommendations.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-amber-200 bg-amber-50/40 p-6 text-center">
                  <AlertTriangle className="h-6 w-6 text-amber-500 mx-auto" />
                  <p className="mt-2 text-sm font-semibold text-slate-800">
                    Your current resume does not strongly match the available roles. Consider improving the highlighted skills first.
                  </p>
                </div>
              ) : (
                currentAnalysis.job_role_recommendations.map((job, idx) => (
                  <div key={idx} className="rounded-2xl border border-slate-200/90 bg-slate-50/50 p-5 hover:bg-slate-50 transition shadow-xs">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <h3 className="text-base font-black text-slate-900">{job.role}</h3>
                        <span className="rounded-lg bg-emerald-100 px-2.5 py-1 text-xs font-black text-emerald-800 border border-emerald-200">
                          {job.match_percentage}% Match
                        </span>
                      </div>
                    </div>

                    <div className="mt-3 space-y-2 text-xs">
                      <div>
                        <strong className="text-slate-900 font-bold">Why this role? </strong>
                        <span className="text-slate-700">{job.reason}</span>
                      </div>
                      
                      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 pt-1">
                        {job.matching_skills && job.matching_skills.length > 0 && (
                          <div className="flex flex-wrap items-center gap-1">
                            <span className="font-semibold text-slate-500">Matching:</span>
                            {job.matching_skills.map((s) => (
                              <span key={s} className="rounded bg-emerald-50 px-2 py-0.5 text-[11px] font-bold text-emerald-700 border border-emerald-200">
                                ✓ {s}
                              </span>
                            ))}
                          </div>
                        )}
                        {job.missing_skills && job.missing_skills.length > 0 && (
                          <div className="flex flex-wrap items-center gap-1">
                            <span className="font-semibold text-slate-500">Missing:</span>
                            {job.missing_skills.map((s) => (
                              <span key={s} className="rounded bg-amber-50 px-2 py-0.5 text-[11px] font-bold text-amber-800 border border-amber-200">
                                ⚠ {s}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Roles Requiring More Preparation */}
            {currentAnalysis.roles_requiring_preparation && currentAnalysis.roles_requiring_preparation.length > 0 && (
              <div className="mt-8 border-t border-slate-100 pt-6">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xs font-black uppercase tracking-wider text-slate-500">Roles Requiring More Preparation</span>
                </div>
                <div className="grid gap-3 sm:grid-cols-2">
                  {currentAnalysis.roles_requiring_preparation.map((prep, idx) => (
                    <div key={idx} className="rounded-xl border border-slate-200 bg-white p-4 text-xs shadow-xs">
                      <div className="flex items-center justify-between font-bold text-slate-900">
                        <span>{prep.role}</span>
                        <span className="rounded bg-slate-100 px-2 py-0.5 text-[11px] text-slate-700">{prep.match_percentage}%</span>
                      </div>
                      <p className="mt-1.5 text-slate-600 text-[11px]">{prep.reason}</p>
                      {prep.missing_skills && prep.missing_skills.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          <span className="text-[10px] text-slate-400 font-semibold">Missing:</span>
                          {prep.missing_skills.map((s) => (
                            <span key={s} className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] text-slate-600">
                              • {s}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>

          {/* Executive Assessment Card */}
          <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                <FileCheck className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-slate-950">AI Executive Assessment</h2>
                <p className="text-xs text-slate-500">Evaluation for {currentAnalysis.title} ({currentAnalysis.word_count} words)</p>
              </div>
            </div>
            <p className="mt-4 text-sm leading-relaxed text-slate-700 sm:text-base">
              {currentAnalysis.summary}
            </p>
          </section>

          {/* Skills Grid: Detected vs Missing */}
          <div className="grid gap-8 lg:grid-cols-2">
            {/* Detected Skills */}
            <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                  <h2 className="text-lg font-bold text-slate-950">Detected Technical Skills</h2>
                </div>
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-bold text-emerald-800">
                  {currentAnalysis.detected_skills.length} Found
                </span>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {currentAnalysis.detected_skills.length === 0 ? (
                  <p className="text-xs text-slate-500">No core technical keywords detected in the resume text.</p>
                ) : (
                  currentAnalysis.detected_skills.map((skill) => (
                    <span
                      key={skill}
                      className="inline-flex items-center gap-1 rounded-xl border border-emerald-200 bg-emerald-50/70 px-3 py-1 text-xs font-semibold text-emerald-800"
                    >
                      <Check className="h-3 w-3 stroke-[3]" />
                      {skill}
                    </span>
                  ))
                )}
              </div>
            </section>

            {/* Missing / Recommended Skills */}
            <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-amber-500" />
                  <h2 className="text-lg font-bold text-slate-950">Target Role Skill Gaps</h2>
                </div>
                <span className="rounded-full bg-amber-100 px-2.5 py-0.5 text-xs font-bold text-amber-800">
                  {currentAnalysis.missing_skills.length} Missing
                </span>
              </div>

              <p className="mt-1 text-xs text-slate-500">
                Skills highly valued for {currentAnalysis.target_company} ({currentAnalysis.target_role}) not found on your resume.
              </p>

              <div className="mt-4 flex flex-wrap gap-2">
                {currentAnalysis.missing_skills.length === 0 ? (
                  <p className="text-xs text-emerald-600 font-medium">All core target competencies are present on your resume!</p>
                ) : (
                  currentAnalysis.missing_skills.map((skill) => (
                    <span
                      key={skill}
                      className="inline-flex items-center gap-1 rounded-xl border border-amber-200 bg-amber-50/80 px-3 py-1 text-xs font-semibold text-amber-900"
                    >
                      <Plus className="h-3 w-3" />
                      {skill}
                    </span>
                  ))
                )}
              </div>
            </section>
          </div>

          {/* Strengths & Weaknesses Matrix */}
          <div className="grid gap-8 lg:grid-cols-2">
            {/* Strengths */}
            <section className="rounded-[2rem] border border-emerald-100 bg-gradient-to-br from-emerald-50/40 via-white to-slate-50 p-6 shadow-soft sm:p-7">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700">
                  <CheckCircle2 className="h-4 w-4" />
                </div>
                <h2 className="text-lg font-bold text-slate-950">Resume Strengths</h2>
              </div>

              <ul className="mt-4 space-y-3">
                {currentAnalysis.strengths.map((str, idx) => (
                  <li key={idx} className="flex items-start gap-3 rounded-2xl bg-white p-3.5 shadow-xs border border-emerald-100/80">
                    <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-xs font-bold text-emerald-800">
                      ✓
                    </span>
                    <p className="text-xs sm:text-sm font-medium text-slate-800 leading-relaxed">{str}</p>
                  </li>
                ))}
              </ul>
            </section>

            {/* Weaknesses */}
            <section className="rounded-[2rem] border border-rose-100 bg-gradient-to-br from-rose-50/40 via-white to-slate-50 p-6 shadow-soft sm:p-7">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-rose-100 text-rose-700">
                  <AlertCircle className="h-4 w-4" />
                </div>
                <h2 className="text-lg font-bold text-slate-950">Areas for Improvement</h2>
              </div>

              <ul className="mt-4 space-y-3">
                {currentAnalysis.weaknesses.map((weak, idx) => (
                  <li key={idx} className="flex items-start gap-3 rounded-2xl bg-white p-3.5 shadow-xs border border-rose-100/80">
                    <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-rose-100 text-xs font-bold text-rose-800">
                      !
                    </span>
                    <p className="text-xs sm:text-sm font-medium text-slate-800 leading-relaxed">{weak}</p>
                  </li>
                ))}
              </ul>
            </section>
          </div>

          {/* Actionable Improvement Recommendations */}
          <section className="rounded-[2rem] border border-indigo-100 bg-gradient-to-br from-indigo-50/40 via-white to-slate-50 p-6 shadow-soft sm:p-8">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                <Sparkles className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-slate-950">Actionable Recommendations</h2>
                <p className="text-xs text-slate-500">Targeted advice tailored to your uploaded resume and selected role</p>
              </div>
            </div>

            <div className="mt-5 space-y-3">
              {currentAnalysis.recommendations.map((rec, idx) => (
                <div key={idx} className="flex items-start gap-3 rounded-2xl bg-white p-4 shadow-sm border border-slate-100">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-xs font-bold text-white">
                    {idx + 1}
                  </span>
                  <p className="text-xs sm:text-sm font-semibold text-slate-900 leading-relaxed">{rec}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Before and After Bullet Improvements */}
          {currentAnalysis.before_after_suggestions && currentAnalysis.before_after_suggestions.length > 0 && (
            <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <FileText className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-950">AI Bullet Point Optimization</h2>
                  <p className="text-xs text-slate-500">Rewrite your experience points for maximum impact</p>
                </div>
              </div>
              
              <div className="mt-5 grid gap-4 lg:grid-cols-2">
                {currentAnalysis.before_after_suggestions.map((suggestion: any, idx: number) => {
                  const original = suggestion.original_text || suggestion.before || "";
                  const improved = suggestion.improved_text || suggestion.after || "";
                  return (
                    <div key={idx} className="flex flex-col rounded-2xl border border-slate-200 bg-slate-50 overflow-hidden shadow-sm">
                      <div className="flex-1 p-4 bg-white border-b border-slate-100">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-rose-500 mb-1 block">Original (Weak)</span>
                        <p className="text-xs text-slate-600 italic">"{original}"</p>
                      </div>
                      <div className="flex-1 p-4 bg-emerald-50/30">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600 mb-1 block">Improved (Strong)</span>
                        <p className="text-sm font-medium text-slate-900">"{improved}"</p>
                        {suggestion.reason && (
                          <div className="mt-2 text-[10px] text-slate-500 bg-white px-2 py-1 inline-block rounded-md border border-slate-100">
                            <span className="font-semibold">Reason:</span> {suggestion.reason}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>
          )}
        </div>
      ) : (
        /* Empty State */
        <div className="rounded-[2rem] border border-dashed border-slate-200 bg-slate-50/50 p-12 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary">
            <FileText className="h-7 w-7" />
          </div>
          <h3 className="mt-4 text-lg font-bold text-slate-950">No Resume Analysis Yet</h3>
          <p className="mt-1 text-sm text-slate-600 max-w-md mx-auto">
            Upload your PDF resume above to receive a full breakdown of ATS parseability, role suitability, missing skills, and recommended roles.
          </p>
        </div>
      )}
    </div>
  );
}

function roundScore(val: number | undefined): number {
  if (!val) return 0;
  return Math.round(val);
}
