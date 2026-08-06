import { AnimatePresence, motion } from 'framer-motion';
import { Routes, Route, useLocation } from 'react-router-dom';
import { LandingPage } from './features/landing/LandingPage';
import { AuthPage } from './features/auth/AuthPage';
import { OnboardingPage } from './features/onboarding/OnboardingPage';
import { DashboardPage } from './features/dashboard/DashboardPage';
import { MockInterviewPage } from './features/interview/MockInterviewPage';
import { RoadmapPage } from './features/roadmap/RoadmapPage';
import { ResumePage } from './features/resume/ResumePage';
import { AnalysisPage } from './features/analysis/AnalysisPage';
import { Layout } from './layouts/Layout';

function App() {
  const location = useLocation();

  return (
    <Layout>
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/auth/*" element={<AuthPage />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/interview" element={<MockInterviewPage />} />
          <Route path="/roadmap" element={<RoadmapPage />} />
          <Route path="/resume" element={<ResumePage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
        </Routes>
      </AnimatePresence>
    </Layout>
  );
}

export default App;
