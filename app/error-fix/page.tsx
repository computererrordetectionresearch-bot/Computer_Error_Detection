// FILE: app/error-fix/page.tsx
'use client';

import { useState } from 'react';
import Link from 'next/link';

interface ErrorFixResponse {
  success: boolean;
  error_text: string;
  software: string;
  os: string;
  category: string;
  probable_cause: string;
  fix_steps: string[];
  fix_id: number | null;
  confidence_score?: number;
}

export default function ErrorFixPage() {
  const [text, setText] = useState('');
  const [software, setSoftware] = useState('Adobe Photoshop');
  const [os, setOs] = useState('Windows 11');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ErrorFixResponse | null>(null);
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const softwareOptions = [
    'Adobe Photoshop', 'Visual Studio Code', 'Node.js', 'Python', 'Chrome',
    'Firefox', 'Git', 'Docker', 'PostgreSQL', 'MongoDB', 'Microsoft Office',
    'Spotify', 'Discord', 'Zoom', 'Slack', 'WhatsApp', 'Telegram', 'VLC Media Player',
    'WinRAR', '7-Zip', 'Notepad++', 'Sublime Text', 'IntelliJ IDEA', 'Eclipse',
    'Android Studio', 'Xcode', 'MySQL', 'Redis', 'Elasticsearch', 'Kubernetes',
    'Terraform', 'Anaconda', 'Jupyter Notebook', 'TensorFlow', 'PyTorch',
    'Adobe Premiere Pro', 'Adobe Illustrator', 'Figma', 'Sketch', 'OBS Studio',
    'Steam', 'Epic Games Launcher', 'Adobe After Effects', 'Blender', 'Unity',
    'AutoCAD', 'SolidWorks', 'MATLAB', 'Tableau', 'Power BI'
  ];

  const osOptions = [
    'Windows 11',
    'Windows 10',
    'MacOS'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
      const res = await fetch(`${apiUrl}/api/error/fix`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, software, os }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err: any) {
      console.error('Error:', err);
      if (err.message?.includes('Failed to fetch') || err.message?.includes('ERR_CONNECTION_REFUSED')) {
        setError('Cannot connect to backend server. Please make sure the backend is running on http://localhost:5000');
      } else {
        setError(`An error occurred: ${err.message || 'Please try again.'}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (success: boolean) => {
    if (!response) {
      return;
    }

    setSubmittingFeedback(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
      await fetch(`${apiUrl}/api/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fix_id: response.fix_id, // Can be null
          success,
          text,
          software,
          os,
          category: response.category,
        }),
      });

      alert('Thank you for your feedback! This helps us improve our error fixes.');
      setResponse(null);
      setText('');
    } catch (err: any) {
      console.error('Error submitting feedback:', err);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setSubmittingFeedback(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Error Fix Guide</h1>
        <nav className="nav-links">
          <Link href="/" className="nav-link">Home</Link>
          <Link href="/installation" className="nav-link">Installation</Link>
          <Link href="/error-fix" className="nav-link active">Error Fix</Link>
        </nav>
      </div>
      
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="text">Error Message</label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter your error message (e.g., 'app is closing', 'installation failed', 'missing dll')..."
            rows={4}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="software">Software</label>
          <select
            id="software"
            value={software}
            onChange={(e) => setSoftware(e.target.value)}
            required
          >
            {softwareOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="os">Operating System</label>
          <select
            id="os"
            value={os}
            onChange={(e) => setOs(e.target.value)}
            required
          >
            {osOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Finding Fix...' : 'Get Fix Steps'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <p>❌ {error}</p>
        </div>
      )}

      {response && (
        <div className="response">
          <h2>Error Fix Guide</h2>
          <div className="error-info">
            <p><strong>Error:</strong> {response.error_text}</p>
            <p><strong>Category:</strong> {response.category}</p>
            {response.probable_cause && (
              <p><strong>Probable Cause:</strong> {response.probable_cause}</p>
            )}
            {response.confidence_score && (
              <p><strong>Confidence:</strong> {(response.confidence_score * 100).toFixed(1)}%</p>
            )}
          </div>
          <h3>Fix Steps:</h3>
          <ol className="steps-list">
            {response.fix_steps?.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>
          
          <div className="feedback-section">
            <p>Did this fix your issue? Your feedback helps us improve!</p>
            {response.fix_id === null && (
              <p className="feedback-note">⚠️ No specific fix was found, but your feedback will help us learn about this error.</p>
            )}
            <div className="feedback-buttons">
              <button
                onClick={() => handleFeedback(true)}
                disabled={submittingFeedback}
                className="feedback-btn success"
              >
                ✔ Fixed
              </button>
              <button
                onClick={() => handleFeedback(false)}
                disabled={submittingFeedback}
                className="feedback-btn error"
              >
                ✖ Not Fixed
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

