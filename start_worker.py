"""
Celery worker startup script
Usage: python start_worker.py
"""
import os
import sys
from celery_app import celery_app

def main():
    """Start Celery worker with optimal configuration"""
    print("Starting Financial Document Analyzer Celery Worker...")
    print("Worker will process tasks from the 'analysis' queue")
    print("Press Ctrl+C to stop")
    
    # Configure worker arguments
    worker_args = [
        'worker',
        '--loglevel=info',
        '--queues=analysis',
        '--concurrency=1',  # Process one document at a time to avoid memory issues
        '--max-tasks-per-child=10',  # Restart worker after 10 tasks to prevent memory leaks
        '--task-events',  # Enable task events for monitoring
    ]
    
    # Start worker
    try:
        celery_app.worker_main(worker_args)
    except KeyboardInterrupt:
        print("\nShutting down worker...")
        sys.exit(0)

if __name__ == "__main__":
    main()