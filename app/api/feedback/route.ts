// FILE: app/api/feedback/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { addFeedback } from '../../../lib/pythonRunner';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { fix_id, success, text, software, os } = body;
    
    if (fix_id === null || fix_id === undefined || success === undefined || !text || !software || !os) {
      return NextResponse.json(
        { error: 'Missing required fields: fix_id, success, text, software, os' },
        { status: 400 }
      );
    }
    
    await addFeedback(parseInt(fix_id.toString()), Boolean(success), text, software, os);
    
    return NextResponse.json({
      success: true,
      message: 'Feedback recorded'
    });
  } catch (error) {
    console.error('Error in feedback route:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

