// FILE: app/page.tsx
'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="container">
      <div className="header">
        <h1>Installation Error Fixer</h1>
        <nav className="nav-links">
          <Link href="/" className="nav-link active">Home</Link>
          <Link href="/installation" className="nav-link">Installation</Link>
          <Link href="/error-fix" className="nav-link">Error Fix</Link>
        </nav>
      </div>
      
      <div className="home-content">
        <div className="welcome-section">
          <h2>Welcome!</h2>
          <p>Choose what you need help with:</p>
        </div>

        <div className="action-cards">
          <Link href="/installation" className="action-card">
            <div className="card-icon">📥</div>
            <h3>Installation Steps</h3>
            <p>Get step-by-step installation guides for software</p>
            <div className="card-arrow">→</div>
          </Link>

          <Link href="/error-fix" className="action-card">
            <div className="card-icon">🔧</div>
            <h3>Error Fix</h3>
            <p>Fix installation errors and troubleshoot issues</p>
            <div className="card-arrow">→</div>
          </Link>
        </div>

      </div>
    </div>
  );
}

