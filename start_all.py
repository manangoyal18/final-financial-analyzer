"""
Start all system components for development
Usage: python start_all.py
"""
import subprocess
import sys
import os
import time
import signal

def check_redis():
    """Check if Redis is running"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return True
    except Exception:
        return False

def start_component(name, command, cwd=None):
    """Start a system component"""
    print(f"🚀 Starting {name}...")
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd or os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    """Start all system components"""
    print("🏁 Starting Financial Document Analyzer System")
    print("=" * 50)
    
    processes = []
    
    try:
        # Check Redis
        print("🔍 Checking Redis connection...")
        if not check_redis():
            print("❌ Redis not available. Please start Redis first:")
            print("   - Using Docker: docker-compose up -d")
            print("   - Manual: redis-server")
            return 1
        print("✅ Redis is running")
        
        # Start Celery worker
        worker_process = start_component(
            "Celery Worker",
            f"{sys.executable} start_worker.py"
        )
        if worker_process:
            processes.append(("Celery Worker", worker_process))
            print("✅ Celery worker started")
            time.sleep(3)  # Give worker time to initialize
        else:
            print("❌ Failed to start Celery worker")
            return 1
        
        # Start FastAPI server
        server_process = start_component(
            "FastAPI Server",
            f"{sys.executable} main.py"
        )
        if server_process:
            processes.append(("FastAPI Server", server_process))
            print("✅ FastAPI server started")
            time.sleep(2)  # Give server time to start
        else:
            print("❌ Failed to start FastAPI server")
            return 1
        
        print("\n🎉 All components started successfully!")
        print("=" * 50)
        print("📊 System URLs:")
        print("   • API Documentation: http://localhost:8000/docs")
        print("   • Health Check: http://localhost:8000/health")
        print("   • Analysis History: http://localhost:8000/analyses")
        print("\n🧪 Test the system:")
        print("   python test_system.py")
        print("\n⏹️  Press Ctrl+C to stop all services")
        
        # Wait for interrupt
        try:
            while True:
                time.sleep(1)
                # Check if processes are still running
                for name, process in processes:
                    if process.poll() is not None:
                        print(f"⚠️  {name} has stopped unexpectedly")
        except KeyboardInterrupt:
            print("\n🛑 Stopping all services...")
    
    finally:
        # Cleanup processes
        for name, process in processes:
            if process and process.poll() is None:
                print(f"🛑 Stopping {name}...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception as e:
                    print(f"⚠️  Error stopping {name}: {e}")
        
        print("✅ All services stopped")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())