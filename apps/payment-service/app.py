import time
import random
import logging
from flask import Flask, jsonify, request
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

resource = Resource.create({ResourceAttributes.SERVICE_NAME: "payment-service"})

trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/process-payment")
def process_payment():
    order_id = request.args.get("order_id")
    logger.info(f"Processing payment for order {order_id}")
    time.sleep(random.uniform(0.1, 0.3))
    if random.random() < 0.2:
        logger.warning(f"Payment failed for order {order_id}")
        return jsonify({"status": "Failed"}), 402
    return jsonify({"status": "Success", "transaction_id": random.randint(100000, 999999)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
