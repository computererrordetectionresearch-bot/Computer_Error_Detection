// FILE: app/api/detect/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { classifyError, isErrorRequest, getInstallationSteps, matchErrorFix } from '../../../lib/pythonRunner';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { text, software, os } = body;
    
    if (!text || !software || !os) {
      return NextResponse.json(
        { error: 'Missing required fields: text, software, os' },
        { status: 400 }
      );
    }
    
    const isError = await isErrorRequest(text);
    
    if (isError) {
      const category = (await classifyError(text)) || 'Application Crash / App Closing';
      const match = await matchErrorFix(text, software, os, category);
      
      if (match) {
        const fixSteps = match.fix.fix_steps.split(' || ').filter(step => step.trim().length > 0);
        
        return NextResponse.json({
          type: 'error',
          category: category,
          probable_cause: match.fix.probable_cause,
          fix_steps: fixSteps,
          fix_id: match.fix.id
        });
      } else {
        return NextResponse.json({
          type: 'error',
          category: category,
          probable_cause: 'Unknown cause',
          fix_steps: [
            'Check software documentation',
            'Update to latest version',
            'Check system requirements',
            'Contact software support',
            'Review system logs for details'
          ],
          fix_id: null
        });
      }
    } else {
      const steps = await getInstallationSteps(software, os);
      
      if (steps && steps.length > 0) {
        return NextResponse.json({
          type: 'installation',
          steps: steps
        });
      } else {
        return NextResponse.json({
          type: 'installation',
          steps: [
            'Download installer from official website',
            'Run installer as administrator',
            'Follow on-screen instructions',
            'Complete installation',
            'Restart if required'
          ]
        });
      }
    }
  } catch (error) {
    console.error('Error in detect route:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

