from fastapi import FastAPI
import time

app = FastAPI(title="Health API")

@app.get("/")
def home():
    return {"message": "Health API is running!"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

# Add after your existing endpoints
@app.get("/rollback/check")
def rollback_check():
    """Check if deployment should be rolled back"""
    import random
    
    # Simulate metrics (in real system, these come from monitoring)
    error_rate = random.uniform(0, 15)  # 0-15% error rate
    latency_p95 = random.uniform(100, 2000)  # 100-2000ms
    success_rate = random.uniform(80, 100)  # 80-100%
    
    # Rollback thresholds
    should_rollback = False
    reasons = []
    
    if error_rate > 5.0:
        should_rollback = True
        reasons.append(f"High error rate: {error_rate:.1f}% > 5%")
    
    if latency_p95 > 1000:
        should_rollback = True
        reasons.append(f"High latency: {latency_p95:.0f}ms > 1000ms")
    
    if success_rate < 95.0:
        should_rollback = True
        reasons.append(f"Low success rate: {success_rate:.1f}% < 95%")
    
    return {
        "should_rollback": should_rollback,
        "reasons": reasons,
        "metrics": {
            "error_rate": round(error_rate, 2),
            "latency_p95": round(latency_p95, 0),
            "success_rate": round(success_rate, 2)
        },
        "thresholds": {
            "max_error_rate": 5.0,
            "max_latency_ms": 1000,
            "min_success_rate": 95.0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)