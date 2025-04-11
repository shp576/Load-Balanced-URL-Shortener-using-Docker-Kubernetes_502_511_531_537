# app.py
import os
import string
import random
from flask import Flask, request, redirect, jsonify
import redis

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

# Configuration
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
SHORTCODE_LENGTH = 6

def generate_short_code(length=SHORTCODE_LENGTH):
    """Generate a random short code of specified length."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """API endpoint to shorten a long URL."""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    long_url = data['url']
    
    # Check if URL already exists in our system
    existing_short_code = redis_client.get(f"url:{long_url}")
    if existing_short_code:
        short_code = existing_short_code.decode('utf-8')
    else:
        # Generate a new short code
        short_code = generate_short_code()
        while redis_client.exists(f"code:{short_code}"):
            short_code = generate_short_code()
        
        # Store mappings in both directions for quick lookups
        redis_client.set(f"code:{short_code}", long_url)
        redis_client.set(f"url:{long_url}", short_code)
    
    short_url = f"{BASE_URL}/{short_code}"
    return jsonify({
        'long_url': long_url,
        'short_url': short_url,
        'short_code': short_code
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """Redirect from a short URL to the original long URL."""
    long_url = redis_client.get(f"code:{short_code}")
    
    if long_url:
        return redirect(long_url.decode('utf-8'))
    else:
        return jsonify({'error': 'URL not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes."""
    try:
        # Check Redis connection
        redis_client.ping()
        return jsonify({'status': 'healthy'}), 200
    except:
        return jsonify({'status': 'unhealthy', 'reason': 'Redis connection failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)