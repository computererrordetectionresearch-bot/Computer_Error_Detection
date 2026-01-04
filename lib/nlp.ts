// FILE: lib/nlp.ts
import * as natural from 'natural';

const tokenizer = new natural.WordTokenizer();

export function calculateSimilarity(text1: string, text2: string): number {
  const tokens1 = tokenizer.tokenize(text1.toLowerCase()) || [];
  const tokens2 = tokenizer.tokenize(text2.toLowerCase()) || [];
  
  if (tokens1.length === 0 || tokens2.length === 0) {
    return 0;
  }
  
  // Calculate term frequency for each document
  const tf1 = calculateTermFrequency(tokens1);
  const tf2 = calculateTermFrequency(tokens2);
  
  // Get all unique terms
  const allTerms = new Set([...tokens1, ...tokens2]);
  
  // Calculate TF-IDF vectors
  const vector1: number[] = [];
  const vector2: number[] = [];
  
  allTerms.forEach(term => {
    const tf1Value = tf1.get(term) || 0;
    const tf2Value = tf2.get(term) || 0;
    
    // Simple TF-IDF: TF * IDF (where IDF = log(N/df))
    // For simplicity, we'll use TF for now since we only have 2 documents
    const idf = Math.log(2 / (Number(tf1Value > 0) + Number(tf2Value > 0)));
    vector1.push(tf1Value * idf);
    vector2.push(tf2Value * idf);
  });
  
  return cosineSimilarity(vector1, vector2);
}

function calculateTermFrequency(tokens: string[]): Map<string, number> {
  const tf = new Map<string, number>();
  const total = tokens.length;
  
  tokens.forEach(token => {
    tf.set(token, (tf.get(token) || 0) + 1 / total);
  });
  
  return tf;
}

function cosineSimilarity(vecA: number[], vecB: number[]): number {
  if (vecA.length !== vecB.length) return 0;
  
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  
  if (normA === 0 || normB === 0) return 0;
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

export function extractKeywords(text: string): string[] {
  const tokens = tokenizer.tokenize(text.toLowerCase()) || [];
  const stopwords = natural.stopwords;
  return tokens.filter(token => 
    token.length > 2 && 
    !stopwords.includes(token) &&
    /^[a-z]+$/.test(token)
  );
}

