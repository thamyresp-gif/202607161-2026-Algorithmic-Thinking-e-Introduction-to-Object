from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Info,
    start_http_server,
)
import threading
import time

REQUEST_DURATION = Histogram(
    "app_request_duration_seconds",
    "Time spent processing requests",
    ["endpoint", "method"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

REQUEST_TOTAL = Counter(
    "app_request_total",
    "Total number of requests",
    ["endpoint", "method", "status"],
)

CALCULATION_DURATION = Histogram(
    "app_calculation_duration_seconds",
    "Time spent calculating budget",
    ["property_type"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)

CSV_EXPORT_TOTAL = Counter(
    "app_csv_export_total",
    "Total number of CSV exports",
    ["property_type"],
)

ERROR_TOTAL = Counter(
    "app_error_total",
    "Total number of errors by type",
    ["error_type"],
)

ACTIVE_USERS = Gauge(
    "app_active_users",
    "Number of active users",
)

HEALTH_STATUS = Gauge(
    "app_health_status",
    "Health status of the application (1=healthy, 0=unhealthy)",
)

CALCULATION_TOTAL = Counter(
    "app_calculation_total",
    "Total number of budget calculations",
    ["property_type", "has_children", "parcelar"],
)

MEMORY_BYTES = Gauge(
    "app_process_memory_bytes",
    "Current memory usage of the process in bytes",
)

CPU_SECONDS = Counter(
    "app_process_cpu_seconds_total",
    "Total CPU seconds used by the process",
)

OPEN_FDS = Gauge(
    "app_process_open_fds",
    "Number of open file descriptors",
)

import os
import psutil

_process = psutil.Process(os.getpid())


def update_process_metrics():
    try:
        MEMORY_BYTES.set(_process.memory_info().rss)
        CPU_SECONDS.inc(_process.cpu_times().user + _process.cpu_times().system)
        OPEN_FDS.set(_process.num_fds())
    except Exception:
        pass


def start_metrics_server(port=9090):
    start_http_server(port)
    threading.Thread(target=_metrics_loop, daemon=True).start()


def _metrics_loop():
    while True:
        update_process_metrics()
        time.sleep(15)


def record_request(endpoint, method, status, duration):
    REQUEST_DURATION.labels(endpoint=endpoint, method=method).observe(duration)
    REQUEST_TOTAL.labels(endpoint=endpoint, method=method, status=status).inc()


def record_calculation(property_type, duration, has_children=False, parcelar=False):
    CALCULATION_DURATION.labels(property_type=property_type).observe(duration)
    CALCULATION_TOTAL.labels(
        property_type=property_type,
        has_children=str(has_children),
        parcelar=str(parcelar),
    ).inc()


def record_csv_export(property_type):
    CSV_EXPORT_TOTAL.labels(property_type=property_type).inc()


def record_error(error_type):
    ERROR_TOTAL.labels(error_type=error_type).inc()


def set_health_status(healthy):
    HEALTH_STATUS.set(1 if healthy else 0)


def set_active_users(count):
    ACTIVE_USERS.set(count)