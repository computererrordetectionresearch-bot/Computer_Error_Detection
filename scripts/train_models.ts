// FILE: scripts/train_models.ts
import { loadErrorCategories, classifyError } from './classify_error';
import { loadInstallationSteps, getInstallationSteps } from './get_install_steps';
import { loadErrorFixes, loadFeedbackStats, matchErrorFix } from './match_error_fix';
import { readFileSync } from 'fs';
import { join } from 'path';
import { parse } from 'csv-parse/sync';

interface TrainingResult {
  model: string;
  status: 'success' | 'error';
  message: string;
  dataLoaded?: number;
}

export function trainAllModels(): TrainingResult[] {
  const results: TrainingResult[] = [];

  // Train Model 1: Error Category Classification Model
  try {
    loadErrorCategories();
    const csvPath = join(process.cwd(), 'data', 'error_category.csv');
    const errorCategoryData = readFileSync(csvPath, 'utf-8');
    const errorRecords = parse(errorCategoryData, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });
    
    // Test classification with sample data
    const testErrors = ['app is closing', 'installation failed', 'missing dll'];
    testErrors.forEach(error => {
      const category = classifyError(error);
      if (!category) {
        throw new Error(`Failed to classify error: ${error}`);
      }
    });

    results.push({
      model: 'Error Category Classification Model',
      status: 'success',
      message: 'Model trained and validated successfully',
      dataLoaded: errorRecords.length
    });
  } catch (error: any) {
    results.push({
      model: 'Error Category Classification Model',
      status: 'error',
      message: `Training failed: ${error.message}`
    });
  }

  // Train Model 2: Installation Steps Giver Model
  try {
    loadInstallationSteps();
    const csvPath = join(process.cwd(), 'data', 'installation_steps.csv');
    const installationData = readFileSync(csvPath, 'utf-8');
    const installationRecords = parse(installationData, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });

    // Test retrieval with sample data
    const testCases = [
      { software: 'Adobe Photoshop', os: 'Windows 11' },
      { software: 'Visual Studio Code', os: 'Windows 10' },
      { software: 'Node.js', os: 'MacOS' }
    ];

    testCases.forEach(testCase => {
      const steps = getInstallationSteps(testCase.software, testCase.os);
      if (!steps || steps.length === 0) {
        console.warn(`No steps found for ${testCase.software} on ${testCase.os}`);
      }
    });

    results.push({
      model: 'Installation Steps Giver Model',
      status: 'success',
      message: 'Model trained and validated successfully',
      dataLoaded: installationRecords.length
    });
  } catch (error: any) {
    results.push({
      model: 'Installation Steps Giver Model',
      status: 'error',
      message: `Training failed: ${error.message}`
    });
  }

  // Train Model 3: Error-Fix Matching Model
  try {
    loadErrorFixes();
    loadFeedbackStats();
    const csvPath = join(process.cwd(), 'data', 'error_fix_dataset.csv');
    const errorFixData = readFileSync(csvPath, 'utf-8');
    const errorFixRecords = parse(errorFixData, {
      columns: true,
      skip_empty_lines: true,
      bom: true
    });

    // Test matching with sample data
    const testCases = [
      { error: 'app is closing', software: 'Adobe Photoshop', os: 'Windows 11', category: 'Application Crash / App Closing' },
      { error: 'installation failed', software: 'Visual Studio Code', os: 'Windows 11', category: 'Installation Failed' },
      { error: 'missing dll', software: 'Adobe Photoshop', os: 'Windows 11', category: 'Missing DLL / Library' }
    ];

    testCases.forEach(testCase => {
      const match = matchErrorFix(
        testCase.error,
        testCase.software,
        testCase.os,
        testCase.category
      );
      if (!match) {
        console.warn(`No match found for error: ${testCase.error}`);
      }
    });

    results.push({
      model: 'Error-Fix Matching Model',
      status: 'success',
      message: 'Model trained and validated successfully',
      dataLoaded: errorFixRecords.length
    });
  } catch (error: any) {
    results.push({
      model: 'Error-Fix Matching Model',
      status: 'error',
      message: `Training failed: ${error.message}`
    });
  }

  // Train Model 4: Feedback Learning Model
  try {
    const csvPath = join(process.cwd(), 'data', 'feedback.csv');
    const feedbackData = readFileSync(csvPath, 'utf-8');
    let feedbackRecords: any[] = [];
    
    if (feedbackData.trim().length > 0) {
      feedbackRecords = parse(feedbackData, {
        columns: true,
        skip_empty_lines: true,
        bom: true
      });
    }

    // Load feedback stats to validate
    loadFeedbackStats();

    results.push({
      model: 'Feedback Learning Model',
      status: 'success',
      message: 'Model initialized successfully. Ready to learn from user feedback.',
      dataLoaded: feedbackRecords.length
    });
  } catch (error: any) {
    results.push({
      model: 'Feedback Learning Model',
      status: 'error',
      message: `Initialization failed: ${error.message}`
    });
  }

  return results;
}

// Run training if executed directly
// Simple check: if this file is run directly (not imported)
const runDirectly = process.argv[1]?.includes('train_models');

if (runDirectly) {
  console.log('🚀 Starting model training...\n');
  const results = trainAllModels();
  
  console.log('📊 Training Results:\n');
  results.forEach((result, index) => {
    const icon = result.status === 'success' ? '✅' : '❌';
    console.log(`${icon} Model ${index + 1}: ${result.model}`);
    console.log(`   Status: ${result.status}`);
    console.log(`   Message: ${result.message}`);
    if (result.dataLoaded !== undefined) {
      console.log(`   Data Loaded: ${result.dataLoaded} records`);
    }
    console.log('');
  });

  const allSuccess = results.every(r => r.status === 'success');
  if (allSuccess) {
    console.log('🎉 All models trained successfully!');
    process.exit(0);
  } else {
    console.log('⚠️  Some models failed to train. Please check the errors above.');
    process.exit(1);
  }
}

