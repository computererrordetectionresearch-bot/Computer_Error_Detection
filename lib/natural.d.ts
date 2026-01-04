// FILE: lib/natural.d.ts
declare module 'natural' {
  export class WordTokenizer {
    tokenize(text: string): string[] | null;
  }

  export class TfIdf {
    addDocument(document: string): void;
    tfidfs(term: string, documentIndex: number): number;
  }

  export const stopwords: string[];
}

