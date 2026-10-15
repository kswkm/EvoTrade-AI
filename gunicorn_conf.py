import multiprocessing

bind = "0.0.0.0:8000"
workers = max(2, multiprocessing.cpu_count() // 2)
worker_class = "uvicorn.workers.UvicornWorker"
threads = 2
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
timeout = 30
graceful_timeout = 30
accesslog = "-"
errorlog = "-"
loglevel = "info"
