# FILE: backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add models directory to path (go up from backend/ to root, then into models/)
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
models_path = os.path.join(project_root, 'models')
sys.path.insert(0, models_path)

from classify_error import classify_error, is_error_request
from get_install_steps import get_installation_steps
from match_error_fix import match_error_fix
from update_feedback import add_feedback

app = Flask(__name__)
CORS(app)

# ============================================================================
# INSTALLATION STEPS ENDPOINTS
# ============================================================================

@app.route('/api/installation/steps', methods=['POST'])
def get_installation_steps_endpoint():
    """Get installation steps for a software and OS"""
    try:
        data = request.json
        software = data.get('software')
        os_name = data.get('os')
        
        if not software or not os_name:
            return jsonify({'error': 'Missing required fields: software, os'}), 400
        
        steps = get_installation_steps(software, os_name)
        
        if steps and len(steps) > 0:
            return jsonify({
                'success': True,
                'software': software,
                'os': os_name,
                'steps': steps,
                'count': len(steps)
            })
        else:
            return jsonify({
                'success': False,
                'software': software,
                'os': os_name,
                'steps': [
                    'Download installer from official website',
                    'Run installer as administrator',
                    'Follow on-screen instructions',
                    'Complete installation',
                    'Restart if required'
                ],
                'message': 'No specific steps found, using generic steps'
            })
    except Exception as e:
        print(f'Error in installation steps route: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/installation/list', methods=['GET'])
def list_installations():
    """List all available software installations"""
    try:
        from get_install_steps import load_installation_steps
        import pandas as pd
        
        csv_path = os.path.join(project_root, 'data', 'installation_steps.csv')
        df = pd.read_csv(csv_path)
        
        # Get unique software list
        software_list = sorted(df['software'].unique().tolist())
        
        return jsonify({
            'success': True,
            'count': len(software_list),
            'software': software_list
        })
    except Exception as e:
        print(f'Error in installation list route: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# ERROR FIX ENDPOINTS
# ============================================================================

@app.route('/api/error/classify', methods=['POST'])
def classify_error_endpoint():
    """Classify an error into a category"""
    try:
        data = request.json
        error_text = data.get('text')
        
        if not error_text:
            return jsonify({'error': 'Missing required field: text'}), 400
        
        category = classify_error(error_text) or 'Application Crash / App Closing'
        is_error = is_error_request(error_text)
        
        return jsonify({
            'success': True,
            'is_error': is_error,
            'category': category,
            'text': error_text
        })
    except Exception as e:
        print(f'Error in classify route: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/error/fix', methods=['POST'])
def get_error_fix_endpoint():
    """Get fix steps for an error"""
    try:
        data = request.json
        error_text = data.get('text')
        software = data.get('software')
        os_name = data.get('os')
        category = data.get('category')  # Optional, will classify if not provided
        
        if not error_text or not software or not os_name:
            return jsonify({'error': 'Missing required fields: text, software, os'}), 400
        
        # Classify error if category not provided
        if not category:
            category = classify_error(error_text) or 'Application Crash / App Closing'
        
        match = match_error_fix(error_text, software, os_name, category)
        
        if match:
            fix_steps = [step.strip() for step in match['fix']['fix_steps'].split(' || ') if step.strip()]
            
            return jsonify({
                'success': True,
                'error_text': error_text,
                'software': software,
                'os': os_name,
                'category': category,
                'probable_cause': match['fix']['probable_cause'],
                'fix_steps': fix_steps,
                'fix_id': match['fix']['id'],
                'confidence_score': round(match['score'], 3)
            })
        else:
            return jsonify({
                'success': False,
                'error_text': error_text,
                'software': software,
                'os': os_name,
                'category': category,
                'probable_cause': 'Unknown cause',
                'fix_steps': [
                    'Check software documentation',
                    'Update to latest version',
                    'Check system requirements',
                    'Contact software support',
                    'Review system logs for details'
                ],
                'fix_id': None,
                'message': 'No specific fix found, using generic steps'
            })
    except Exception as e:
        print(f'Error in error fix route: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/error/list', methods=['GET'])
def list_errors():
    """List all error categories"""
    try:
        import pandas as pd
        
        csv_path = os.path.join(project_root, 'data', 'error_category.csv')
        df = pd.read_csv(csv_path)
        
        # Get unique categories
        categories = sorted(df['category'].unique().tolist())
        
        return jsonify({
            'success': True,
            'count': len(categories),
            'categories': categories
        })
    except Exception as e:
        print(f'Error in error list route: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# UNIFIED DETECT ENDPOINT (for backward compatibility)
# ============================================================================

@app.route('/api/detect', methods=['POST'])
def detect():
    """Unified endpoint that detects if request is installation or error"""
    try:
        data = request.json
        text = data.get('text')
        software = data.get('software')
        os_name = data.get('os')
        
        if not text or not software or not os_name:
            return jsonify({'error': 'Missing required fields: text, software, os'}), 400
        
        is_error = is_error_request(text)
        
        if is_error:
            # Route to error fix endpoint
            category = classify_error(text) or 'Application Crash / App Closing'
            match = match_error_fix(text, software, os_name, category)
            
            if match:
                fix_steps = [step.strip() for step in match['fix']['fix_steps'].split(' || ') if step.strip()]
                
                return jsonify({
                    'type': 'error',
                    'category': category,
                    'probable_cause': match['fix']['probable_cause'],
                    'fix_steps': fix_steps,
                    'fix_id': match['fix']['id']
                })
            else:
                return jsonify({
                    'type': 'error',
                    'category': category,
                    'probable_cause': 'Unknown cause',
                    'fix_steps': [
                        'Check software documentation',
                        'Update to latest version',
                        'Check system requirements',
                        'Contact software support',
                        'Review system logs for details'
                    ],
                    'fix_id': None
                })
        else:
            # Route to installation steps endpoint
            steps = get_installation_steps(software, os_name)
            
            if steps and len(steps) > 0:
                return jsonify({
                    'type': 'installation',
                    'steps': steps
                })
            else:
                return jsonify({
                    'type': 'installation',
                    'steps': [
                        'Download installer from official website',
                        'Run installer as administrator',
                        'Follow on-screen instructions',
                        'Complete installation',
                        'Restart if required'
                    ]
                })
    except Exception as e:
        print(f'Error in detect route: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# FEEDBACK ENDPOINT
# ============================================================================

@app.route('/api/feedback', methods=['POST'])
def feedback():
    """Submit feedback about a fix (fix_id can be null if no fix was found)"""
    try:
        data = request.json
        fix_id = data.get('fix_id')  # Can be null
        success = data.get('success')
        text = data.get('text')
        software = data.get('software')
        os_name = data.get('os')
        category = data.get('category')  # Optional
        
        if success is None or not text or not software or not os_name:
            return jsonify({'error': 'Missing required fields: success, text, software, os'}), 400
        
        # Allow null fix_id - use -1 as placeholder for "no fix found"
        fix_id_value = int(fix_id) if fix_id is not None else -1
        
        add_feedback(fix_id_value, bool(success), text, software, os_name, category)
        
        return jsonify({
            'success': True,
            'message': 'Feedback recorded'
        })
    except Exception as e:
        print(f'Error in feedback route: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
