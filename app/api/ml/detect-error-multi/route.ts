import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '3');
    
    if (!body.user_error) {
      return NextResponse.json(
        { detail: 'user_error field is required' },
        { status: 400 }
      );
    }
    
    const response = await fetch(`http://localhost:8000/detect-error-multi?limit=${limit}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      let errorDetail = 'Error detection failed';
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch {
        errorDetail = `Backend returned status ${response.status}`;
      }
      return NextResponse.json(
        { detail: errorDetail },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('API route error:', error);
    return NextResponse.json(
      { detail: error.message || 'Failed to connect to ML backend. Make sure the backend is running on port 8000.' },
      { status: 500 }
    );
  }
}



















