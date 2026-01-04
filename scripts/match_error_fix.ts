// FILE: scripts/match_error_fix.ts
import { readFileSync } from 'fs';
import { join } from 'path';
import { parse } from 'csv-parse/sync';
import { calculateSimilarity } from '../lib/nlp';

interface ErrorFix {
  id: number;
  software: string;
  os: string;
  error_message: string;
  probable_cause: string;
  fix_steps: string;
}

interface FeedbackStats {
  fix_id: number;
  success_count: number;
  total_count: number;
}

let errorFixes: ErrorFix[] = [];
let feedbackStats: Map<number, FeedbackStats> = new Map();

export function loadErrorFixes(): void {
  try {
    const csvPath = join(process.cwd(), 'data', 'error_fix_dataset.csv');
    const fileContent = readFileSync(csvPath, 'utf-8');
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });
    errorFixes = records.map((record: any) => ({
      id: parseInt(record.id),
      software: record.software,
      os: record.os,
      error_message: record.error_message,
      probable_cause: record.probable_cause,
      fix_steps: record.fix_steps
    }));
  } catch (error) {
    console.error('Error loading error fixes:', error);
    errorFixes = [];
  }
}

export function loadFeedbackStats(): void {
  try {
    const csvPath = join(process.cwd(), 'data', 'feedback.csv');
    const fileContent = readFileSync(csvPath, 'utf-8');
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });
    
    feedbackStats.clear();
    
    records.forEach((record: any) => {
      const fixId = parseInt(record.fix_id);
      if (isNaN(fixId)) return;
      
      const success = record.success === 'true' || record.success === '1';
      
      if (!feedbackStats.has(fixId)) {
        feedbackStats.set(fixId, { fix_id: fixId, success_count: 0, total_count: 0 });
      }
      
      const stats = feedbackStats.get(fixId)!;
      stats.total_count++;
      if (success) {
        stats.success_count++;
      }
    });
  } catch (error) {
    console.error('Error loading feedback stats:', error);
  }
}

export function matchErrorFix(
  errorText: string,
  software: string,
  os: string,
  category: string
): { fix: ErrorFix; score: number } | null {
  if (errorFixes.length === 0) {
    loadErrorFixes();
  }
  
  if (feedbackStats.size === 0) {
    loadFeedbackStats();
  }
  
  const normalizedSoftware = software.trim().toLowerCase();
  const normalizedOS = os.trim().toLowerCase();
  const normalizedCategory = category.trim().toLowerCase();
  
  const candidates = errorFixes
    .filter(fix => 
      fix.software.toLowerCase() === normalizedSoftware &&
      fix.os.toLowerCase() === normalizedOS
    )
    .map(fix => {
      let score = 0;
      
      const errorSimilarity = calculateSimilarity(errorText.toLowerCase(), fix.error_message.toLowerCase());
      score += errorSimilarity * 0.6;
      
      const categoryMatch = fix.error_message.toLowerCase().includes(normalizedCategory) ||
                           normalizedCategory.includes(fix.error_message.toLowerCase());
      if (categoryMatch) {
        score += 0.2;
      }
      
      const stats = feedbackStats.get(fix.id);
      if (stats && stats.total_count > 0) {
        const successRate = stats.success_count / stats.total_count;
        score += successRate * 0.2;
      }
      
      return { fix, score };
    })
    .filter(candidate => candidate.score > 0.1)
    .sort((a, b) => b.score - a.score);
  
  if (candidates.length === 0) {
    return null;
  }
  
  return candidates[0];
}

export function getFixSteps(fixId: number): string[] | null {
  if (errorFixes.length === 0) {
    loadErrorFixes();
  }
  
  const fix = errorFixes.find(f => f.id === fixId);
  if (!fix) {
    return null;
  }
  
  return fix.fix_steps.split(' || ').filter(step => step.trim().length > 0);
}

