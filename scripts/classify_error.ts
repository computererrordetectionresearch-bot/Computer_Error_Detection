// FILE: scripts/classify_error.ts
import { readFileSync } from 'fs';
import { join } from 'path';
import { parse } from 'csv-parse/sync';
import { calculateSimilarity, extractKeywords } from '../lib/nlp';

interface ErrorCategory {
  error_text: string;
  category: string;
}

let errorCategories: ErrorCategory[] = [];

export function loadErrorCategories(): void {
  try {
    const csvPath = join(process.cwd(), 'data', 'error_category.csv');
    const fileContent = readFileSync(csvPath, 'utf-8');
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });
    errorCategories = records as ErrorCategory[];
  } catch (error) {
    console.error('Error loading error categories:', error);
    errorCategories = [];
  }
}

export function classifyError(errorText: string): string | null {
  if (errorCategories.length === 0) {
    loadErrorCategories();
  }
  
  if (!errorText || errorText.trim().length === 0) {
    return null;
  }
  
  const normalizedInput = errorText.toLowerCase().trim();
  const inputKeywords = extractKeywords(errorText);
  
  let bestMatch: { category: string; score: number } | null = null;
  
  for (const category of errorCategories) {
    const categoryText = category.error_text.toLowerCase();
    
    let score = 0;
    
    if (normalizedInput.includes(categoryText) || categoryText.includes(normalizedInput)) {
      score += 0.5;
    }
    
    const similarity = calculateSimilarity(errorText, category.error_text);
    score += similarity * 0.5;
    
    const categoryKeywords = extractKeywords(category.error_text);
    const commonKeywords = inputKeywords.filter(kw => categoryKeywords.includes(kw));
    score += (commonKeywords.length / Math.max(inputKeywords.length, categoryKeywords.length)) * 0.3;
    
    if (!bestMatch || score > bestMatch.score) {
      bestMatch = { category: category.category, score };
    }
  }
  
  if (bestMatch && bestMatch.score > 0.2) {
    return bestMatch.category;
  }
  
  return 'Application Crash / App Closing';
}

export function isErrorRequest(text: string): boolean {
  const errorKeywords = [
    'error', 'failed', 'crash', 'closing', 'missing', 'denied',
    'permission', 'dll', 'library', 'network', 'license', 'activation',
    'problem', 'issue', 'bug', 'broken', 'not working'
  ];
  
  const normalizedText = text.toLowerCase();
  return errorKeywords.some(keyword => normalizedText.includes(keyword));
}

