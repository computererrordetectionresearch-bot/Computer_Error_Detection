// FILE: app/installation/page.tsx
'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function InstallationPage() {
  const [software, setSoftware] = useState('Adobe Photoshop');
  const [os, setOs] = useState('Windows 11');
  const [loading, setLoading] = useState(false);
  const [steps, setSteps] = useState<string[] | null>(null);
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
    setSteps(null);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
      const res = await fetch(`${apiUrl}/api/installation/steps`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ software, os }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      if (data.success && data.steps) {
        setSteps(data.steps);
      } else {
        setError('No installation steps found for this software and OS combination.');
      }
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

  return (
    <div className="container">
      <div className="header">
        <h1>Installation Steps Guide</h1>
        <nav className="nav-links">
          <Link href="/" className="nav-link">Home</Link>
          <Link href="/installation" className="nav-link active">Installation</Link>
          <Link href="/error-fix" className="nav-link">Error Fix</Link>
        </nav>
      </div>
      
      <form onSubmit={handleSubmit} className="form">
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
          {loading ? 'Loading Steps...' : 'Get Installation Steps'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <p>❌ {error}</p>
        </div>
      )}

      {steps && (
        <div className="response">
          <h2>Installation Steps for {software} on {os}</h2>
          <ol className="steps-list">
            {steps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

