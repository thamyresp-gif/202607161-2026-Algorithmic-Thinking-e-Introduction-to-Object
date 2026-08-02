from flask import Flask, jsonify
import psutil
import os

app = Flask(__name__)


@app.route("/health")
def health():
    try:
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)
        disk = psutil.disk_usage("/")
        return jsonify(
            {
                "status": "healthy",
                "uptime_seconds": psutil.boot_time(),
                "memory": {
                    "total": mem.total,
                    "available": mem.available,
                    "percent": mem.percent,
                },
                "cpu": {"percent": cpu},
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "percent": disk.percent,
                },
                "process": {
                    "pid": os.getpid(),
                    "memory_rss": psutil.Process(os.getpid()).memory_info().rss,
                    "cpu_percent": psutil.Process(os.getpid()).cpu_percent(),
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)