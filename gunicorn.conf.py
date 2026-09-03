import multiprocessing

# Bind to all interfaces on port 8000
bind = "0.0.0.0:8000"

# Worker configuration
workers = 3        # nice and sane
threads = 2        # enough for light concurrency

worker_class = "gthread"

backlog = 2048

timeout = 60
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"

limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

reload = False
