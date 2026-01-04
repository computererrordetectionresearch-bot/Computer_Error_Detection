# FILE: models/update_feedback.py
import pandas as pd
import sys
import os
import json
from datetime import datetime

def add_feedback(fix_id, success, error_text, software, os_name, category=None):
    """Add feedback to CSV. fix_id can be -1 if no fix was found."""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'feedback.csv')
    
    # Load existing feedback
    try:
        df = pd.read_csv(csv_path)
    except:
        df = pd.DataFrame(columns=['feedback_id', 'error_text', 'software', 'os', 'fix_id', 'success', 'category', 'timestamp'])
    
    # Generate new feedback_id
    if df.empty:
        new_id = 1
    else:
        new_id = int(df['feedback_id'].max()) + 1 if 'feedback_id' in df.columns else 1
    
    # Handle null fix_id (use -1 as placeholder for "no fix found")
    fix_id_value = int(fix_id) if fix_id is not None and fix_id != -1 else -1
    
    # Add new feedback
    feedback_data = {
        'feedback_id': new_id,
        'error_text': error_text,
        'software': software,
        'os': os_name,
        'fix_id': fix_id_value,
        'success': 'true' if success else 'false',
        'timestamp': datetime.now().isoformat()
    }
    
    # Add category if provided
    if category:
        feedback_data['category'] = category
    
    new_feedback = pd.DataFrame([feedback_data])
    
    df = pd.concat([df, new_feedback], ignore_index=True)
    df.to_csv(csv_path, index=False)
    
    return new_id

if __name__ == '__main__':
    # Command line interface
    if len(sys.argv) < 6:
        print("Usage: python update_feedback.py <fix_id> <success> <error_text> <software> <os>")
        sys.exit(1)
    
    fix_id = int(sys.argv[1])
    success = sys.argv[2].lower() in ['true', '1', 'yes']
    error_text = sys.argv[3]
    software = sys.argv[4]
    os_name = sys.argv[5]
    
    feedback_id = add_feedback(fix_id, success, error_text, software, os_name)
    print(json.dumps({'feedback_id': feedback_id, 'success': True}))

