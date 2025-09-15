#!/usr/bin/env python3
"""
Script test Microsoft Teams webhook
"""

import requests
import json
import os
from datetime import datetime

def test_simple_message():
    """Test gửi message đơn giản đến Teams"""
    
    # URL webhook
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL", "")
    if not webhook_url:
        print("❌ Missing TEAMS_WEBHOOK_URL in environment")
        return
    
    # Message đơn giản
    simple_message = {
        "text": f"🧪 Test message từ SaleBooks KDP - {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}"
    }
    
    print("🧪 Testing simple message...")
    print(f"URL: {webhook_url}")
    print(f"Message: {json.dumps(simple_message, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(
            webhook_url,
            json=simple_message,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 202]:
            print("✅ Simple message sent successfully!")
        else:
            print("❌ Failed to send simple message")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_card_message():
    """Test gửi message card đến Teams"""
    
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL", "")
    if not webhook_url:
        print("❌ Missing TEAMS_WEBHOOK_URL in environment")
        return
    
    # Message card
    card_message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Test báo cáo từ SaleBooks KDP",
        "sections": [{
            "activityTitle": "🧪 Test Message Card",
            "activitySubtitle": "Kiểm tra format message từ SaleBooks KDP",
            "facts": [
                {
                    "name": "Thời gian test",
                    "value": datetime.now().strftime('%H:%M:%S %d/%m/%Y')
                },
                {
                    "name": "Nguồn",
                    "value": "SaleBooks KDP System"
                },
                {
                    "name": "Trạng thái",
                    "value": "Test thành công"
                }
            ]
        }]
    }
    
    print("\n🧪 Testing card message...")
    print(f"Message: {json.dumps(card_message, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(
            webhook_url,
            json=card_message,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 202]:
            print("✅ Card message sent successfully!")
        else:
            print("❌ Failed to send card message")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("🚀 Testing Microsoft Teams Webhook...")
    print("=" * 50)
    
    # Test 1: Simple message
    test_simple_message()
    
    # Test 2: Card message
    test_card_message()
    
    print("\n✅ Test completed!")
    print("Kiểm tra Microsoft Teams channel để xem thông báo.")
