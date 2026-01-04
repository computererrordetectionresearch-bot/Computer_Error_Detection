// FILE: lib/pythonRunner.ts
import { exec } from 'child_process';
import { promisify } from 'util';
import { join } from 'path';

const execAsync = promisify(exec);

export async function runPythonScript(scriptName: string, args: string[]): Promise<string> {
  const scriptPath = join(process.cwd(), 'models', scriptName);
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  
  // Properly escape arguments for cross-platform compatibility
  const escapedArgs = args.map(arg => {
    // Escape quotes and wrap in quotes
    const escaped = arg.replace(/"/g, '\\"').replace(/\$/g, '\\$');
    return `"${escaped}"`;
  });
  
  const command = `${pythonCmd} "${scriptPath}" ${escapedArgs.join(' ')}`;
  
  try {
    const { stdout, stderr } = await execAsync(command, {
      maxBuffer: 10 * 1024 * 1024, // 10MB buffer
      encoding: 'utf8'
    });
    
    if (stderr && !stderr.includes('Warning') && !stderr.includes('DeprecationWarning')) {
      console.error(`Python script stderr: ${stderr}`);
    }
    
    return stdout.trim();
  } catch (error: any) {
    console.error(`Error running Python script ${scriptName}:`, error.message);
    if (error.stdout) console.error('Stdout:', error.stdout);
    if (error.stderr) console.error('Stderr:', error.stderr);
    throw error;
  }
}

export async function classifyError(errorText: string): Promise<string | null> {
  try {
    const result = await runPythonScript('classify_error.py', [errorText]);
    return result === 'null' ? null : result;
  } catch (error) {
    console.error('Error classifying error:', error);
    return null;
  }
}

export async function isErrorRequest(text: string): Promise<boolean> {
  const errorKeywords = [
    'error', 'failed', 'crash', 'closing', 'missing', 'denied',
    'permission', 'dll', 'library', 'network', 'license', 'activation',
    'problem', 'issue', 'bug', 'broken', 'not working'
  ];
  
  const normalizedText = text.toLowerCase();
  return errorKeywords.some(keyword => normalizedText.includes(keyword));
}

export async function getInstallationSteps(software: string, os: string): Promise<string[] | null> {
  try {
    const result = await runPythonScript('get_install_steps.py', [software, os]);
    if (result === 'null') return null;
    return JSON.parse(result);
  } catch (error) {
    console.error('Error getting installation steps:', error);
    return null;
  }
}

export async function matchErrorFix(
  errorText: string,
  software: string,
  os: string,
  category: string
): Promise<{ fix: any; score: number } | null> {
  try {
    const result = await runPythonScript('match_error_fix.py', [errorText, software, os, category]);
    if (result === 'null') return null;
    return JSON.parse(result);
  } catch (error) {
    console.error('Error matching error fix:', error);
    return null;
  }
}

export async function addFeedback(
  fixId: number,
  success: boolean,
  errorText: string,
  software: string,
  os: string
): Promise<void> {
  try {
    await runPythonScript('update_feedback.py', [
      fixId.toString(),
      success ? 'true' : 'false',
      errorText,
      software,
      os
    ]);
  } catch (error) {
    console.error('Error adding feedback:', error);
    throw error;
  }
}

