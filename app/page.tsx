'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Solution {
  error_name: string;
  category: string;
  confidence: number;
  steps: string[];
  symptoms: string;
  cause: string;
  risk: string;
  verification: string;
  estimated_time?: string;
  issue_type?: string;
}

interface StepAnalysis {
  difficulty: 'easy' | 'medium' | 'advanced';
  commands: string[];
  warning: string;
}

export default function Home() {
  const [errorText, setErrorText] = useState('');
  const [loading, setLoading] = useState(false);
  const [solution, setSolution] = useState<Solution | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);
  const [isSupported, setIsSupported] = useState(false);
  const [showMultiSolutions, setShowMultiSolutions] = useState(false);
  const [multiSolutions, setMultiSolutions] = useState<Solution[]>([]);
  const [eli5Mode, setEli5Mode] = useState(false);
  const [showFollowUp, setShowFollowUp] = useState(false);
  const [userHistory, setUserHistory] = useState<Array<{error: string, solution: string, date: string}>>([]);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const originalError = console.error;
      console.error = (...args: any[]) => {
        const msg = args.join(' ');
        if (
          msg.includes('MetaMask') ||
          msg.includes('chrome-extension://') ||
          msg.includes('moz-extension://')
        ) {
          return;
        }
        originalError.apply(console, args);
      };

      const handleRejection = (event: PromiseRejectionEvent) => {
        const reason = String(event.reason || '');
        if (
          reason.includes('MetaMask') ||
          reason.includes('chrome-extension://') ||
          reason.includes('moz-extension://')
        ) {
          event.preventDefault();
        }
      };

      window.addEventListener('unhandledrejection', handleRejection);

      // Initialize Speech Recognition
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        setIsSupported(true);
        const recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = false;
        recognitionInstance.interimResults = false;
        recognitionInstance.lang = 'en-US';

        recognitionInstance.onstart = () => {
          setIsListening(true);
        };

        recognitionInstance.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setErrorText(prev => prev + (prev ? ' ' : '') + transcript);
          setIsListening(false);
        };

        recognitionInstance.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error);
          setIsListening(false);
          if (event.error === 'no-speech') {
            setError('No speech detected. Please try again.');
          } else if (event.error === 'not-allowed') {
            setError('Microphone permission denied. Please allow microphone access.');
          } else {
            setError('Speech recognition error. Please try typing instead.');
          }
        };

        recognitionInstance.onend = () => {
          setIsListening(false);
        };

        setRecognition(recognitionInstance);
      }

      return () => {
        console.error = originalError;
        window.removeEventListener('unhandledrejection', handleRejection);
        if (recognition) {
          recognition.stop();
        }
      };
    }
  }, []);

  // Load user history from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('errorHistory');
    if (saved) {
      try {
        setUserHistory(JSON.parse(saved));
      } catch (e) {
        console.error('Error loading history:', e);
      }
    }
  }, []);

  // Save to history when solution is found
  useEffect(() => {
    if (solution) {
      const newEntry = {
        error: errorText,
        solution: solution.error_name,
        date: new Date().toISOString()
      };
      const updated = [newEntry, ...userHistory.slice(0, 9)]; // Keep last 10
      setUserHistory(updated);
      localStorage.setItem('errorHistory', JSON.stringify(updated));
    }
  }, [solution]);

  const getStepDifficulty = (stepText: string, stepNum: number): 'easy' | 'medium' | 'advanced' => {
    const stepLower = stepText.toLowerCase();
    const advanced = ['command', 'cmd', 'powershell', 'registry', 'bios', 'chkdsk', 'sfc', 'dism', 'replace', 'hardware'];
    const medium = ['update', 'driver', 'settings', 'recovery', 'safe mode', 'uninstall'];
    const easy = ['restart', 'reboot', 'click', 'select', 'unplug', 'connect'];
    
    if (advanced.some(k => stepLower.includes(k))) return 'advanced';
    if (medium.some(k => stepLower.includes(k))) return 'medium';
    if (easy.some(k => stepLower.includes(k))) return 'easy';
    
    return stepNum <= 2 ? 'easy' : stepNum <= 4 ? 'medium' : 'advanced';
  };

  const extractCommands = (stepText: string): string[] => {
    const commands: string[] = [];
    const patterns = [
      /chkdsk[^\s]*\s+[^\n]+/gi,
      /sfc\s+[^\n]+/gi,
      /dism\s+[^\n]+/gi,
      /netsh\s+[^\n]+/gi,
      /bootrec\s+[^\n]+/gi,
      /`([^`]+)`/g,
    ];
    
    patterns.forEach(pattern => {
      const matches = stepText.match(pattern);
      if (matches) {
        commands.push(...matches.map(m => m.replace(/`/g, '').trim()));
      }
    });
    
    return Array.from(new Set(commands)).slice(0, 3);
  };

  const getRiskWarning = (stepText: string, difficulty: string, risk: string): string => {
    const stepLower = stepText.toLowerCase();
    if (stepLower.includes('format') || stepLower.includes('delete data')) {
      return "⚠️ WARNING: This step may delete data. Backup important files first.";
    }
    if (stepLower.includes('registry') || stepLower.includes('regedit')) {
      return "⚠️ WARNING: Modifying registry can damage your system. Follow instructions carefully.";
    }
    if (stepLower.includes('bios') || stepLower.includes('uefi')) {
      return "⚠️ WARNING: Incorrect BIOS settings can prevent booting. Only change if you're confident.";
    }
    if (difficulty === 'advanced' && risk === 'high') {
      return "⚠️ CAUTION: This is an advanced step. Proceed carefully or seek help.";
    }
    return "";
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      // Show temporary success message
      const btn = document.activeElement as HTMLElement;
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => {
        if (btn) btn.textContent = original;
      }, 2000);
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!errorText.trim()) {
      setError('Please enter an error description');
      return;
    }

    setLoading(true);
    setError(null);
    setSolution(null);
    setMultiSolutions([]);
    setShowMultiSolutions(false);

    try {
      const response = await axios.post('/api/ml/detect-error', {
        user_error: errorText,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setSolution(response.data);
      setShowFollowUp(true);
      
      // Also fetch top 3 solutions
      try {
        const multiResponse = await axios.post('/api/ml/detect-error-multi?limit=3', {
          user_error: errorText,
        });
        if (multiResponse.data.solutions && multiResponse.data.solutions.length > 1) {
          setMultiSolutions(multiResponse.data.solutions);
        }
      } catch (e) {
        // Multi-solution is optional, don't fail if it doesn't work
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Failed to detect error. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const startListening = () => {
    if (recognition && !isListening) {
      setError(null);
      try {
        recognition.start();
      } catch (err) {
        console.error('Error starting recognition:', err);
        setError('Unable to start voice recognition. Please try again.');
      }
    }
  };

  const stopListening = () => {
    if (recognition && isListening) {
      recognition.stop();
      setIsListening(false);
    }
  };

  return (
    <main className="min-h-screen bg-white relative overflow-hidden">
      <div className="relative z-10 max-w-5xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center mb-6">
            <div className="relative">
              <div className="relative bg-gradient-to-r from-blue-500 to-purple-600 p-4 rounded-full shadow-lg">
                <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
            </div>
          </div>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            AI Error Detection
          </h1>
          <p className="text-xl text-gray-700 mb-2">
            Intelligent Computer Error Solutions
          </p>
          <p className="text-sm text-gray-500">
            Powered by Advanced Machine Learning & Semantic Analysis
          </p>
        </div>

        <div className="bg-white rounded-3xl p-8 mb-8 shadow-xl border-2 border-gray-200">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="error-input"
                className="flex items-center text-sm font-semibold text-gray-800 mb-3"
              >
                <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Describe Your Computer Error
                {isSupported && (
                  <span className="ml-2 text-xs text-green-600 flex items-center">
                    <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    Voice enabled
                  </span>
                )}
              </label>
              <div className="relative">
                <textarea
                  id="error-input"
                  rows={5}
                  value={errorText}
                  onChange={(e) => setErrorText(e.target.value)}
                  placeholder={isSupported ? "Type or click microphone to speak your error..." : "Example: I get Black screen on boot when using my PC..."}
                  className="w-full px-5 py-4 pr-16 bg-gray-50 border-2 border-gray-300 rounded-xl text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-all"
                />
                {isSupported && (
                  <button
                    type="button"
                    onClick={isListening ? stopListening : startListening}
                    className={`absolute right-3 top-3 p-3 rounded-lg transition-all duration-300 ${
                      isListening
                        ? 'bg-red-500 hover:bg-red-600 animate-pulse text-white'
                        : 'bg-blue-100 hover:bg-blue-200 border-2 border-blue-300 text-blue-600'
                    }`}
                    title={isListening ? 'Stop listening' : 'Start voice input'}
                  >
                    {isListening ? (
                      <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 012 0v4a1 1 0 11-2 0V7zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V7a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg className="w-6 h-6 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                      </svg>
                    )}
                  </button>
                )}
              </div>
              {isListening && (
                <div className="mt-2 flex items-center space-x-2 text-sm text-blue-400">
                  <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                  <span>Listening... Speak your error description</span>
                </div>
              )}
              {!isSupported && (
                <div className="mt-2 text-xs text-gray-500">
                  Voice input not supported in this browser. Please use Chrome, Edge, or Safari.
                </div>
              )}
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white font-bold py-4 px-8 rounded-xl hover:from-blue-500 hover:via-purple-500 hover:to-pink-500 focus:outline-none focus:ring-4 focus:ring-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-purple-500/50 pulse-glow"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg
                    className="animate-spin -ml-1 mr-3 h-6 w-6 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  <span className="text-lg">Analyzing with AI...</span>
                </span>
              ) : (
                <span className="flex items-center justify-center text-lg">
                  <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Detect Error & Generate Solution
                </span>
              )}
            </button>
          </form>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-xl mb-8 shadow-md">
            <div className="flex items-start">
              <svg className="h-6 w-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="text-red-600 font-semibold mb-1">Error</h3>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {solution && (
          <div className="bg-white rounded-3xl p-8 space-y-8 animate-fade-in border-2 border-gray-200 shadow-xl">
            {/* Header with Confidence and Controls */}
            <div className="border-b-2 border-gray-200 pb-6">
              <div className="flex items-center justify-between mb-4 flex-wrap gap-4">
                <h2 className="text-3xl font-bold text-gray-900">
                  {solution.error_name}
                </h2>
                <div className="flex items-center gap-3 flex-wrap">
                  <div className="flex items-center gap-2">
                    <span className="px-4 py-2 bg-blue-100 border-2 border-blue-300 text-blue-700 rounded-full text-sm font-bold">
                      {Math.round(solution.confidence * 100)}% Confident
                    </span>
                    {solution.confidence > 0.8 && (
                      <span className="text-xs text-green-700 flex items-center font-semibold">
                        <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        High Confidence
                      </span>
                    )}
                  </div>
                  <button
                    onClick={() => setEli5Mode(!eli5Mode)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border-2 ${
                      eli5Mode
                        ? 'bg-yellow-100 border-yellow-400 text-yellow-700'
                        : 'bg-gray-100 border-gray-300 text-gray-700 hover:bg-gray-200'
                    }`}
                    title="Toggle beginner-friendly explanations"
                  >
                    {eli5Mode ? '🧒 Beginner Mode' : '👤 Normal Mode'}
                  </button>
                </div>
              </div>
              <div className="flex items-center gap-4 text-sm flex-wrap">
                <span className="flex items-center px-3 py-1.5 bg-purple-100 border-2 border-purple-300 rounded-lg text-purple-700 font-semibold">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  {solution.category}
                </span>
                <span
                  className={`px-3 py-1.5 rounded-lg border-2 font-semibold ${
                    solution.risk === 'high'
                      ? 'bg-red-100 border-red-400 text-red-700'
                      : solution.risk === 'medium'
                      ? 'bg-yellow-100 border-yellow-400 text-yellow-700'
                      : 'bg-green-100 border-green-400 text-green-700'
                  }`}
                >
                  {solution.risk.toUpperCase()} RISK
                </span>
                {solution.issue_type && (
                  <span className="px-3 py-1.5 bg-blue-100 border-2 border-blue-300 rounded-lg text-blue-700 font-semibold">
                    {solution.issue_type.charAt(0).toUpperCase() + solution.issue_type.slice(1)} Issue
                  </span>
                )}
                {solution.estimated_time && (
                  <span className="px-3 py-1.5 bg-indigo-100 border-2 border-indigo-300 rounded-lg text-indigo-700 flex items-center font-semibold">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {solution.estimated_time}
                  </span>
                )}
              </div>
              {solution.confidence < 0.6 && (
                <div className="mt-4 p-3 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
                  <p className="text-yellow-800 text-sm font-medium">
                    ⚠️ Lower confidence match. Consider trying alternative solutions below or providing more details about your error.
                  </p>
                </div>
              )}
            </div>

            {solution.symptoms && (
              <div className="bg-blue-50 p-6 rounded-xl border-2 border-blue-200 shadow-md">
                <h3 className="text-lg font-bold text-blue-700 mb-3 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Symptoms
                </h3>
                <p className="text-gray-800 leading-relaxed">
                  {solution.symptoms}
                </p>
              </div>
            )}

            {solution.cause && (
              <div className="bg-purple-50 p-6 rounded-xl border-2 border-purple-200 shadow-md">
                <h3 className="text-lg font-bold text-purple-700 mb-3 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Likely Cause
                </h3>
                <p className="text-gray-800 leading-relaxed">
                  {solution.cause}
                </p>
              </div>
            )}

            {/* Solution Steps */}
            <div>
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bold text-gray-900 flex items-center">
                  <svg className="w-6 h-6 mr-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Step-by-Step Solution
                </h3>
                {multiSolutions.length > 1 && (
                  <button
                    onClick={() => setShowMultiSolutions(!showMultiSolutions)}
                    className="px-4 py-2 bg-purple-100 border-2 border-purple-300 rounded-lg text-purple-700 text-sm font-semibold hover:bg-purple-200 transition-all shadow-sm"
                  >
                    {showMultiSolutions ? 'Hide' : 'Show'} Alternative Solutions ({multiSolutions.length - 1})
                  </button>
                )}
              </div>
              <div className="space-y-6">
                {solution.steps.map((step, index) => {
                  const lines = step.split('\n').filter(l => l.trim());
                  // const stepHeader = lines[0] || `Step ${index + 1}`;
                  
                  // Extract sub-steps that start with numbers
                  let subSteps = lines.slice(1).filter(l => l.trim() && /^\d+\./.test(l.trim()));
                  
                  // Check if first sub-step contains "Option" or checkmark to treat as header
                  let optionHeader = '';
                  const firstSubStep = subSteps[0];
                  
                  if (firstSubStep && (firstSubStep.includes('Option') || firstSubStep.includes('✅') || firstSubStep.includes('✔️'))) {
                    // Extract option header from the first sub-step
                    optionHeader = firstSubStep.replace(/^\d+\.\s*/, '').trim();
                    // Remove this from subSteps array since we'll display it separately
                    subSteps.shift();
                  }
                  
                  const difficulty = getStepDifficulty(step, index + 1);
                  const commands = extractCommands(step);
                  const warning = getRiskWarning(step, difficulty, solution.risk);
                  
                  return (
                    <div
                      key={index}
                      className="bg-white p-6 rounded-xl border-2 border-gray-200 shadow-lg hover:shadow-xl transition-all duration-300 group"
                      style={{ borderLeftColor: '#3b82f6', borderLeftWidth: '4px' }}
                    >
                      <div className="flex items-start gap-4">
                        <div className="flex-shrink-0">
                          <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex flex-col items-center justify-center font-bold text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                            <span className="text-[10px] font-light uppercase tracking-wider">Solution</span>
                            <span className="text-2xl leading-none mt-1">{String(index + 1).padStart(2, '0')}</span>
                          </div>
                        </div>
                        <div className="flex-1">
                          {/* Step Header */}
                          {/* <h4 className="text-lg font-bold text-gray-900 mb-2">
                            {stepHeader}
                          </h4> */}
                          
                          {/* Option Header if exists */}
                          {optionHeader && (
                            <div className="mb-3 p-3 bg-blue-50 border-2 border-blue-200 rounded-lg">
                              <h5 className="text-blue-700 font-semibold flex items-center">
                                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                                {optionHeader}
                              </h5>
                            </div>
                          )}
                          
                          {/* Difficulty and Warning badges */}
                          <div className="flex items-center gap-3 mb-4 flex-wrap">
                            <span className={`px-3 py-1 rounded-lg text-xs font-semibold border-2 ${
                              difficulty === 'easy'
                                ? 'bg-green-100 text-green-700 border-green-300'
                                : difficulty === 'medium'
                                ? 'bg-yellow-100 text-yellow-700 border-yellow-300'
                                : 'bg-red-100 text-red-700 border-red-300'
                            }`}>
                              {difficulty === 'easy' ? '🟢 Easy' : difficulty === 'medium' ? '🟡 Medium' : '🔴 Advanced'}
                            </span>
                            
                            {warning && (
                              <span className="px-3 py-1 rounded-lg text-xs font-semibold border-2 border-yellow-300 bg-yellow-100 text-yellow-700">
                                ⚠️ Warning
                              </span>
                            )}
                          </div>
                          
                          {/* Warning message */}
                          {warning && (
                            <div className="mb-4 p-3 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
                              <p className="text-yellow-800 text-sm font-medium">{warning}</p>
                            </div>
                          )}
                          
                          {/* Sub-steps */}
                          {subSteps.length > 0 ? (
                            <ol className="space-y-3">
                              {subSteps.map((subStep, subIndex) => {
                                let stepText = subStep.replace(/^\d+\.\s*/, '').trim();
                                stepText = stepText.replace(/^[→\-—]\s*/, '').trim();
                                
                                const isCheckmarkStep = stepText.startsWith('✔️') || stepText.startsWith('✅');
                                const command = commands.find(c => stepText.includes(c));
                                
                                return (
                                  <li key={subIndex} className="text-gray-800 leading-relaxed text-base">
                                    <span className="text-blue-600 font-bold mr-2">
                                      {subIndex + 1}.
                                    </span>
                                    <span className={isCheckmarkStep ? 'text-green-700 font-semibold' : ''}>
                                      {stepText}
                                    </span>
                                    {command && (
                                      <button
                                        onClick={() => copyToClipboard(command)}
                                        className="ml-3 px-2 py-1 bg-blue-100 border-2 border-blue-300 rounded text-xs text-blue-700 hover:bg-blue-200 transition-all font-semibold"
                                        title="Copy command"
                                      >
                                        📋 Copy
                                      </button>
                                    )}
                                  </li>
                                );
                              })}
                            </ol>
                          ) : (
                            <p className="text-gray-800 leading-relaxed text-base">
                              {lines.slice(1).join(' ')}
                            </p>
                          )}
                          
                          {/* Commands section */}
                          {commands.length > 0 && (
                            <div className="mt-4 p-3 bg-gray-50 rounded-lg border-2 border-gray-300">
                              <p className="text-xs text-gray-600 mb-2 font-semibold">Commands found:</p>
                              <div className="space-y-2">
                                {commands.map((cmd, cmdIdx) => (
                                  <div key={cmdIdx} className="flex items-center justify-between bg-white p-2 rounded border border-gray-300">
                                    <code className="text-green-700 text-sm font-mono font-semibold">{cmd}</code>
                                    <button
                                      onClick={() => copyToClipboard(cmd)}
                                      className="px-2 py-1 bg-green-100 border-2 border-green-300 rounded text-xs text-green-700 hover:bg-green-200 transition-all font-semibold"
                                    >
                                      Copy
                                    </button>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {solution.verification && (
              <div className="bg-green-50 p-6 rounded-xl border-2 border-green-200 shadow-md"
                style={{ borderLeftColor: '#10b981', borderLeftWidth: '4px' }}
              >
                <h3 className="text-lg font-bold text-green-700 mb-3 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Verification
                </h3>
                <p className="text-gray-800 leading-relaxed font-medium">{solution.verification}</p>
              </div>
            )}

            {/* Follow-Up Questions */}
            {showFollowUp && (
              <div className="bg-purple-50 p-6 rounded-xl border-2 border-purple-200 shadow-md">
                <h3 className="text-lg font-bold text-purple-700 mb-4 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Did This Help?
                </h3>
                <div className="space-y-3">
                  <p className="text-gray-800 text-sm mb-4 font-medium">
                    {solution.confidence > 0.8 
                      ? "Did this solution fix your problem, or do you see a new error code?"
                      : "This might not be the exact issue. Did you try the steps? What happened?"}
                  </p>
                  <div className="flex gap-3 flex-wrap">
                    <button
                      onClick={() => {
                        setShowFollowUp(false);
                        setErrorText('');
                        setSolution(null);
                      }}
                      className="px-4 py-2 bg-green-100 border-2 border-green-300 rounded-lg text-green-700 hover:bg-green-200 transition-all text-sm font-semibold shadow-sm"
                    >
                      ✅ Yes, it worked!
                    </button>
                    <button
                      onClick={() => {
                        if (multiSolutions.length > 1) {
                          setShowMultiSolutions(true);
                        } else {
                          setErrorText(errorText + ' - First solution did not work');
                          handleSubmit({ preventDefault: () => {} } as React.FormEvent);
                        }
                      }}
                      className="px-4 py-2 bg-yellow-100 border-2 border-yellow-300 rounded-lg text-yellow-700 hover:bg-yellow-200 transition-all text-sm font-semibold shadow-sm"
                    >
                      ⚠️ No, try alternative
                    </button>
                    <button
                      onClick={() => {
                        setShowFollowUp(false);
                        setErrorText('');
                        setSolution(null);
                      }}
                      className="px-4 py-2 bg-gray-100 border-2 border-gray-300 rounded-lg text-gray-700 hover:bg-gray-200 transition-all text-sm font-semibold shadow-sm"
                    >
                      🔄 Search again
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* When to Stop Warning */}
            {solution.risk === 'high' && solution.steps.length >= 4 && (
              <div className="bg-red-50 p-6 rounded-xl border-2 border-red-200 shadow-md"
                style={{ borderLeftColor: '#ef4444', borderLeftWidth: '4px' }}
              >
                <h3 className="text-lg font-bold text-red-700 mb-3 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  When to Stop
                </h3>
                <p className="text-red-800 leading-relaxed font-medium">
                  If these steps don't resolve the issue after trying all of them, stop and consider:
                  {solution.issue_type === 'hardware' 
                    ? " professional hardware repair or component replacement."
                    : solution.issue_type === 'driver'
                    ? " contacting your device manufacturer for updated drivers."
                    : " seeking professional IT support or system reinstallation."}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Alternative Solutions */}
        {showMultiSolutions && multiSolutions.length > 1 && (
          <div className="bg-white rounded-3xl p-8 space-y-6 mt-8 border-2 border-gray-200 shadow-xl">
            <h3 className="text-2xl font-bold text-gray-900">
              Alternative Solutions
            </h3>
            <div className="space-y-4">
              {multiSolutions.slice(1).map((altSolution, idx) => (
                <div key={idx} className="bg-purple-50 p-6 rounded-xl border-2 border-purple-200 shadow-md">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h4 className="text-lg font-bold text-purple-700 mb-2">
                        Solution {idx + 2} (Alternative)
                      </h4>
                      <p className="text-gray-800 font-medium">{altSolution.error_name}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-3 py-1 bg-purple-100 border-2 border-purple-300 rounded text-xs text-purple-700 font-semibold">
                        {Math.round(altSolution.confidence * 100)}% Match
                      </span>
                      <span className="text-xs text-gray-600 font-medium">
                        {altSolution.estimated_time || '10-15 min'}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      setSolution(altSolution);
                      setShowMultiSolutions(false);
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                    className="px-4 py-2 bg-purple-100 border-2 border-purple-300 rounded-lg text-purple-700 hover:bg-purple-200 transition-all text-sm font-semibold shadow-sm"
                  >
                    View This Solution →
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* User History */}
        {userHistory.length > 0 && (
          <div className="bg-white rounded-3xl p-8 mt-8 border-2 border-gray-200 shadow-xl">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Recent Searches
            </h3>
            <div className="space-y-2">
              {userHistory.slice(0, 5).map((entry, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setErrorText(entry.error);
                    handleSubmit({ preventDefault: () => {} } as React.FormEvent);
                  }}
                  className="w-full text-left p-3 bg-gray-50 border-2 border-gray-200 rounded-lg hover:bg-gray-100 transition-all text-sm shadow-sm"
                >
                  <p className="text-gray-900 font-medium">{entry.error}</p>
                  <p className="text-gray-600 text-xs mt-1">→ {entry.solution}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="text-center mt-12 text-gray-600 text-sm">
          <p className="flex items-center justify-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Powered by Advanced Machine Learning & Semantic Search
          </p>
        </div>
      </div>
    </main>
  );
}