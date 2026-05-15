import time
import random
import requests
import logging
from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Resource setup
resource = Resource.create({ResourceAttributes.SERVICE_NAME: "order-service"})

# Tracing setup
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/create-order")
def create_order():
    order_id = random.randint(1000, 9999)
    logger.info(f"Processing order {order_id}")
    try:
        resp = requests.get("http://payment-service:5001/process-payment", params={"order_id": order_id})
        return jsonify({"status": "Order Created", "order_id": order_id, "payment_status": resp.json()})
    except Exception as e:
        logger.error(f"Failed to reach payment service: {e}")
        return jsonify({"error": "Payment service unavailable"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
