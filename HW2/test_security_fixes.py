#!/usr/bin/env python3
"""
Test script to verify security fixes in the Django application.
This script demonstrates that the vulnerabilities have been properly fixed.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Add the Django project to Python path
sys.path.append('/Users/showkothossain/Desktop/sse-fa25/HW2/website')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

# Setup Django
django.setup()

from tasktracker.models import Task

def test_sql_injection_fix():
    """Test that SQL injection is prevented"""
    print("Testing SQL Injection Fix...")
    
    # Create test user
    user = User.objects.create_user(username='testuser', password='testpass')
    client = Client()
    client.login(username='testuser', password='testpass')
    
    # Attempt SQL injection through task title
    malicious_title = "'; DROP TABLE tasktracker_task; --"
    
    response = client.post('/tasktracker/add/', {
        'title': malicious_title,
        'due_date': '2024-12-31',
        'status': 'N'
    })
    
    # Check that task was created safely (not executed as SQL)
    task = Task.objects.filter(user=user, title=malicious_title).first()
    if task:
        print("✅ SQL Injection prevented - malicious input stored safely as text")
        print(f"   Task title: {task.title}")
    else:
        print("❌ SQL Injection test failed")
    
    # Cleanup
    user.delete()

def test_xss_fix():
    """Test that XSS is prevented"""
    print("\nTesting XSS Fix...")
    
    # Create test user and task with potential XSS
    user = User.objects.create_user(username='testuser2', password='testpass')
    
    xss_title = "<script>alert('XSS')</script>"
    task = Task.objects.create(
        user=user,
        title=xss_title,
        due_date='2024-12-31',
        status='N'
    )
    
    client = Client()
    client.login(username='testuser2', password='testpass')
    
    # Get the index page
    response = client.get('/tasktracker/')
    
    # Check that script tags are escaped in the response
    if '&lt;script&gt;' in response.content.decode() or xss_title not in response.content.decode():
        print("✅ XSS prevented - script tags are escaped in HTML output")
    else:
        print("❌ XSS test failed - script tags not escaped")
    
    # Cleanup
    user.delete()

def test_idor_fix():
    """Test that IDOR is prevented"""
    print("\nTesting IDOR Fix...")
    
    # Create two users with tasks
    user1 = User.objects.create_user(username='user1', password='testpass')
    user2 = User.objects.create_user(username='user2', password='testpass')
    
    task1 = Task.objects.create(user=user1, title="User1's task", due_date='2024-12-31', status='N')
    task2 = Task.objects.create(user=user2, title="User2's task", due_date='2024-12-31', status='N')
    
    # User1 tries to delete User2's task
    client = Client()
    client.login(username='user1', password='testpass')
    
    response = client.post(f'/tasktracker/delete/{task2.id}/')
    
    # Check that User2's task still exists
    if Task.objects.filter(id=task2.id).exists():
        print("✅ IDOR prevented - User1 cannot delete User2's task")
    else:
        print("❌ IDOR test failed - unauthorized deletion occurred")
    
    # Cleanup
    user1.delete()
    user2.delete()

def test_secret_key_fix():
    """Test that secret key is not hard-coded"""
    print("\nTesting Secret Key Fix...")
    
    from website import settings
    
    # Check if secret key uses environment variable
    if hasattr(settings, 'SECRET_KEY'):
        # Read the actual settings.py file to check implementation
        with open('/Users/showkothossain/Desktop/sse-fa25/HW2/website/website/settings.py', 'r') as f:
            content = f.read()
            
        if 'os.environ.get' in content and 'DJANGO_SECRET_KEY' in content:
            print("✅ Secret key fix implemented - using environment variable")
        else:
            print("❌ Secret key still hard-coded")
    else:
        print("❌ Secret key not found")

if __name__ == '__main__':
    print("Security Fixes Verification Test")
    print("=" * 40)
    
    try:
        test_sql_injection_fix()
        test_xss_fix()
        test_idor_fix()
        test_secret_key_fix()
        
        print("\n" + "=" * 40)
        print("All security fix tests completed!")
        print("See VULNERABILITY_FIXES.md for detailed explanations.")
        
    except Exception as e:
        print(f"Test error: {e}")
        print("Note: This test requires Django to be properly configured.")