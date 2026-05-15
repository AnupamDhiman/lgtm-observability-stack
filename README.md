# LGTM Observability Stack

A comprehensive project to learn and implement the **LGTM** stack (Loki, Grafana, Tempo, Mimir) for full-stack observability.

## Components
- **Loki**: Log aggregation system.
- **Grafana**: The open observability platform for visualization.
- **Tempo**: High-volume, minimal-dependency distributed tracing backend.
- **Mimir**: Scalable, long-term storage for Prometheus metrics.

## Project Structure
- `docker-compose.yaml`: Orchestrates the stack.
- `config/`: Configuration files for each component.
- `apps/`: Sample applications to demonstrate instrumentation.

## How to Run
1. Ensure Docker Desktop is installed.
2. Run `docker-compose up -d`.
3. Access Grafana at `http://localhost:3000`.
