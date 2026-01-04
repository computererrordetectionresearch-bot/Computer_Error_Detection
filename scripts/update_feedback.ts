// FILE: scripts/update_feedback.ts
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { parse } from 'csv-parse/sync';
import { stringify } from 'csv-stringify/sync';

interface FeedbackRecord {
  feedback_id: string;
  error_text: string;
  software: string;
  os: string;
  fix_id: string;
  success: string;
  timestamp: string;
}

let feedbackRecords: FeedbackRecord[] = [];

function loadFeedback(): void {
  try {
    const csvPath = join(process.cwd(), 'data', 'feedback.csv');
    const fileContent = readFileSync(csvPath, 'utf-8');
    if (fileContent.trim().length === 0) {
      feedbackRecords = [];
      return;
    }
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });
    feedbackRecords = records as FeedbackRecord[];
  } catch (error) {
    console.error('Error loading feedback:', error);
    feedbackRecords = [];
  }
}

function saveFeedback(): void {
  try {
    const csvPath = join(process.cwd(), 'data', 'feedback.csv');
    const headers = ['feedback_id', 'error_text', 'software', 'os', 'fix_id', 'success', 'timestamp'];
    const csvContent = stringify(feedbackRecords, {
      header: true,
      columns: headers
    });
    writeFileSync(csvPath, csvContent, 'utf-8');
  } catch (error) {
    console.error('Error saving feedback:', error);
    throw error;
  }
}

export function addFeedback(
  fixId: number,
  success: boolean,
  errorText: string,
  software: string,
  os: string
): void {
  loadFeedback();
  
  const newId = feedbackRecords.length > 0 
    ? (Math.max(...feedbackRecords.map(r => parseInt(r.feedback_id) || 0)) + 1).toString()
    : '1';
  
  const timestamp = new Date().toISOString();
  
  const newRecord: FeedbackRecord = {
    feedback_id: newId,
    error_text: errorText,
    software: software,
    os: os,
    fix_id: fixId.toString(),
    success: success ? 'true' : 'false',
    timestamp: timestamp
  };
  
  feedbackRecords.push(newRecord);
  saveFeedback();
}

export function getFeedbackStats(fixId: number): { success_count: number; total_count: number } {
  loadFeedback();
  
  const relevantFeedback = feedbackRecords.filter(r => parseInt(r.fix_id) === fixId);
  
  const total_count = relevantFeedback.length;
  const success_count = relevantFeedback.filter(r => r.success === 'true' || r.success === '1').length;
  
  return { success_count, total_count };
}

