"""
Test script for the enhanced financial document analyzer system
Usage: python test_system.py
"""
import requests
import time
import sys
import os

API_BASE = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        result = response.json()
        print(f"   Status: {result.get('status')}")
        print(f"   Database: {result.get('database')}")
        print(f"   Celery: {result.get('celery')}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False

def test_document_analysis():
    """Test document analysis with sample file"""
    print("📄 Testing document analysis...")
    
    # Check if sample document exists
    sample_file = "data/TSLA-Q2-2025-Update.pdf"
    if not os.path.exists(sample_file):
        print(f"   ❌ Sample file not found: {sample_file}")
        return False
    
    try:
        # Submit analysis
        print("   📤 Submitting document for analysis...")
        with open(sample_file, 'rb') as f:
            response = requests.post(
                f"{API_BASE}/analyze",
                files={'file': f},
                data={'query': 'Analyze this Tesla financial document for key insights'}
            )
        
        if response.status_code != 200:
            print(f"   ❌ Submit failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        submission = response.json()
        analysis_id = submission.get('analysis_id')
        
        print(f"   ✅ Analysis submitted (ID: {analysis_id})")
        print(f"   Task ID: {submission.get('task_id')}")
        
        # Poll for completion
        print("   ⏳ Polling for completion...")
        max_attempts = 30  # 5 minutes max
        attempt = 0
        
        while attempt < max_attempts:
            time.sleep(10)  # Wait 10 seconds between polls
            attempt += 1
            
            status_response = requests.get(f"{API_BASE}/status/{analysis_id}")
            if status_response.status_code != 200:
                print(f"   ❌ Status check failed: {status_response.status_code}")
                continue
                
            status_data = status_response.json()
            current_status = status_data.get('status')
            
            print(f"   Status (attempt {attempt}): {current_status}")
            
            if current_status == 'completed':
                print("   ✅ Analysis completed successfully!")
                result_length = len(status_data.get('result', ''))
                print(f"   Result length: {result_length} characters")
                print(f"   Duration: {status_data.get('duration_seconds', 0):.1f} seconds")
                return True
            elif current_status == 'failed':
                print(f"   ❌ Analysis failed: {status_data.get('error_message')}")
                return False
        
        print(f"   ❌ Analysis timed out after {max_attempts} attempts")
        return False
        
    except Exception as e:
        print(f"   ❌ Analysis test failed: {e}")
        return False

def test_analysis_history():
    """Test the analysis history endpoint"""
    print("📊 Testing analysis history...")
    try:
        response = requests.get(f"{API_BASE}/analyses?limit=5")
        if response.status_code != 200:
            print(f"   ❌ History request failed: {response.status_code}")
            return False
            
        data = response.json()
        analyses = data.get('analyses', [])
        print(f"   ✅ Found {len(analyses)} recent analyses")
        
        for analysis in analyses[:3]:  # Show first 3
            status = analysis.get('status')
            query = analysis.get('query', '')[:50] + '...'
            duration = analysis.get('duration_seconds', 0)
            print(f"   - ID {analysis.get('analysis_id')}: {status} ({duration:.1f}s) - {query}")
        
        return True
    except Exception as e:
        print(f"   ❌ History test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Financial Document Analyzer - System Test")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Document Analysis", test_document_analysis),
        ("Analysis History", test_analysis_history)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print(f"\n📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the system components:")
        print("   1. Is Redis running?")
        print("   2. Is the Celery worker running?")
        print("   3. Is the FastAPI server running?")
        print("   4. Are all dependencies installed?")
        return 1

if __name__ == "__main__":
    sys.exit(main())