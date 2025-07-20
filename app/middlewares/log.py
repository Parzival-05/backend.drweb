import logging
import time
from flask import current_app as app, g, request


@app.before_request
def start_timer():
    g.start_time = time.time()


@app.after_request
def log_request_info(response):
    total_time = time.time() - g.start_time
    logging.info(
        f"{response.status_code} [{request.method}] {request.path} - Time taken: {total_time:.4f}s."
    )
    return response
