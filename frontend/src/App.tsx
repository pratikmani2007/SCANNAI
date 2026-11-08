import React, { useState, useEffect, useCallback } from 'react';
import { Navbar } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { AnalysisWorkspace } from './components/AnalysisWorkspace';
import { AnalysisResults } from './components/AnalysisResults';
import { Footer } from './components/Footer';
import { fetchHealth, submitForAnalysis } from './services/api';
import { HealthResponse, AnalysisResponse } from './types/analysis';

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState<boolean>(true);
  const [healthError, setHealthError] = useState<string | null>(null);

  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  const loadHealth = useCallback(async () => {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const data = await fetchHealth();
      setHealth(data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Backend connection unavailable';
      setHealthError(message);
      setHealth(null);
    } finally {
      setHealthLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHealth();
  }, [loadHealth]);

  const handleAnalyze = async (text: string, file: File | null) => {
    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      const result = await submitForAnalysis(text, file);
      setAnalysisResult(result);

      // Smooth scroll to results
      setTimeout(() => {
        const resultsEl = document.getElementById('results-dashboard');
        if (resultsEl) {
          resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Analysis failed. Please check backend connection.';
      setAnalysisError(message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-cyber-bg text-cyber-text overflow-x-hidden">
      {/* Navigation Header */}
      <Navbar
        health={health}
        healthLoading={healthLoading}
        healthError={healthError}
        onRefreshHealth={loadHealth}
      />

      {/* Main Content Area */}
      <main className="flex-1 pb-16">
        <HeroSection />

        <AnalysisWorkspace
          onAnalyze={handleAnalyze}
          isLoading={isAnalyzing}
          error={analysisError}
        />

        {/* Dynamic Analysis Results Container */}
        {analysisResult && (
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <AnalysisResults response={analysisResult} />
          </div>
        )}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default App;
