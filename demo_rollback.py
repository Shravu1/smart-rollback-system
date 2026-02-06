"""
Smart Rollback System - Demonstration
Shows how the Health API detects when to rollback deployments
"""

import requests
import time
import sys

def test_health_api():
    """Test basic health endpoints"""
    print("🧪 Testing Health API Endpoints...")
    print("-" * 50)
    
    try:
        # 1. Test root endpoint
        print("1. Root endpoint:")
        response = requests.get("http://localhost:8000/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # 2. Test health endpoint
        print("\n2. Health check:")
        response = requests.get("http://localhost:8000/health")
        health_data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Overall: {health_data.get('status', 'N/A')}")
        print(f"   Score: {health_data.get('overall_score', 'N/A')}/100")
        
        # 3. Test metrics endpoint
        print("\n3. Current metrics:")
        response = requests.get("http://localhost:8000/metrics/current")
        metrics = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Healthy metrics: {metrics.get('summary', {}).get('healthy_metrics', 'N/A')}/{metrics.get('summary', {}).get('total_metrics', 'N/A')}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Health API!")
        print("   Make sure server is running: python monitoring/health_api.py")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def demonstrate_rollback_decisions():
    """Show smart rollback decisions in action"""
    print("\n🚀 Smart Rollback Detection Demo")
    print("=" * 60)
    print("Simulating deployment monitoring...")
    print("Thresholds: Error rate >5% = Rollback | Latency >1000ms = Rollback")
    print("-" * 60)
    
    try:
        for i in range(6):
            print(f"\n📊 Check #{i+1}:")
            
            # Get rollback decision from API
            response = requests.get("http://localhost:8000/rollback/check")
            data = response.json()
            
            # Display results
            metrics = data.get("metrics", {})
            
            print(f"   Error Rate: {metrics.get('error_rate', 'N/A')}%")
            print(f"   Latency: {metrics.get('latency_p95', 'N/A')}ms")
            print(f"   Success Rate: {metrics.get('success_rate', 'N/A')}%")
            
            if data.get("should_rollback", False):
                print("   ❌ DECISION: ROLLBACK REQUIRED!")
                for reason in data.get("reasons", []):
                    print(f"      • {reason}")
            else:
                print("   ✅ DECISION: Deployment is HEALTHY")
            
            # Small delay between checks
            if i < 5:
                time.sleep(1.5)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR during rollback demo: {e}")
        return False

def simulate_critical_failure():
    """Simulate a critical failure scenario"""
    print("\n🔥 Simulating Critical Failure Scenario")
    print("-" * 50)
    
    try:
        # Add custom metrics to simulate failure
        print("Injecting high error rate (12%)...")
        response = requests.post(
            "http://localhost:8000/metrics/custom",
            params={"name": "critical_error_rate", "value": 12.0, "unit": "percent"}
        )
        
        print("Checking rollback decision...")
        response = requests.get("http://localhost:8000/rollback/check")
        data = response.json()
        
        if data.get("should_rollback", False):
            print("✅ SUCCESS: System correctly detected critical failure!")
            print(f"   Reasons: {', '.join(data.get('reasons', []))}")
        else:
            print("⚠️ WARNING: System did not detect the critical failure")
            
        return True
        
    except Exception as e:
        print(f"⚠️ Could not simulate failure: {e}")
        return True  # Don't fail demo for this

def main():
    """Main demonstration function"""
    print("=" * 60)
    print("       SMART DEPLOYMENT ROLLBACK SYSTEM")
    print("               Health Monitoring Demo")
    print("=" * 60)
    
    # Check if server is running
    print("\nChecking Health API status...")
    time.sleep(1)
    
    if not test_health_api():
        sys.exit(1)
    
    # Demonstrate rollback decisions
    if not demonstrate_rollback_decisions():
        sys.exit(1)
    
    # Optional: Simulate failure
    simulate_critical_failure()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETE!")
    print("\nWhat you've seen:")
    print("1. ✅ Health API is running and monitoring system")
    print("2. ✅ Real-time rollback decisions based on metrics")
    print("3. ✅ Automatic detection of deployment issues")
    print("4. ✅ Configurable thresholds for rollback triggers")
    print("\nNext: Connect this to the Rollback Engine for automatic recovery!")
    print("=" * 60)

if __name__ == "__main__":
    # Make sure requests module is available
    try:
        import requests
    except ImportError:
        print("❌ Missing 'requests' module. Install it:")
        print("   pip install requests")
        sys.exit(1)
    
    main()