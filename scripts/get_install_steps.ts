// FILE: scripts/get_install_steps.ts
import { readFileSync } from 'fs';
import { join } from 'path';
import { parse } from 'csv-parse/sync';

interface InstallationStep {
  software: string;
  os: string;
  installation_steps: string;
  source: string;
}

let installationSteps: InstallationStep[] = [];

export function loadInstallationSteps(): void {
  try {
    const csvPath = join(process.cwd(), 'data', 'installation_steps.csv');
    const fileContent = readFileSync(csvPath, 'utf-8');
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });
    installationSteps = records as InstallationStep[];
  } catch (error) {
    console.error('Error loading installation steps:', error);
    installationSteps = [];
  }
}

export function getInstallationSteps(software: string, os: string): string[] | null {
  if (installationSteps.length === 0) {
    loadInstallationSteps();
  }
  
  const normalizedSoftware = software.trim();
  const normalizedOS = os.trim();
  
  const match = installationSteps.find(
    step => 
      step.software.toLowerCase() === normalizedSoftware.toLowerCase() &&
      step.os.toLowerCase() === normalizedOS.toLowerCase()
  );
  
  if (!match) {
    return null;
  }
  
  return match.installation_steps.split(' || ').filter(step => step.trim().length > 0);
}

