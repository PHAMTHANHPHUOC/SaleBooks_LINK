#!/usr/bin/env python3
"""
Script test để kiểm tra chức năng báo cáo Teams
"""

import os
import sys
import django
import requests
import json

# Thêm đường dẫn Django project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Thiết lập Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_api_endpoints():
    """Test các API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Teams Report API endpoints...")
    print("=" * 50)
    
    # Test 1: Test endpoint
    print("1. Testing /api/teams/test/")
    try:
        response = requests.get(f"{base_url}/api/teams/test/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Preview endpoint
    print("2. Testing /api/teams/preview-report/")
    try:
        response = requests.get(f"{base_url}/api/teams/preview-report/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('status')}")
            if 'data' in data:
                stats = data['data'].get('stats', {})
                print(f"   Date: {stats.get('date')}")
                print(f"   Total visits: {stats.get('visit_stats', {}).get('total_visits', 0)}")
                print(f"   Countries: {len(stats.get('country_stats', []))}")
                print(f"   Products: {len(stats.get('top_products', []))}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Send report (test mode)
    print("3. Testing /api/teams/send-report/ (sending actual report)")
    try:
        response = requests.post(f"{base_url}/api/teams/send-report/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

def test_django_commands():
    """Test Django management commands"""
    print("\n" + "=" * 50)
    print("🧪 Testing Django Management Commands...")
    print("=" * 50)
    
    from django.core.management import call_command
    from io import StringIO
    
    # Test send_daily_report command
    print("1. Testing send_daily_report command (test mode)")
    try:
        output = StringIO()
        call_command('send_daily_report', '--test', stdout=output)
        print("   Command executed successfully")
        print("   Output:")
        print(output.getvalue())
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == '__main__':
    print("🚀 Starting Teams Report Test...")
    print("Make sure Django server is running on localhost:8000")
    print()
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test Django commands
    test_django_commands()
    
    print("\n✅ Test completed!")
