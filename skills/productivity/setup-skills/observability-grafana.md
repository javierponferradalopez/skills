# Observability: Grafana

Grafana is this repo's window onto **metrics, logs, and traces** in production — dashboards, and the datasources behind them.

## Scope

- **Instance**: `<grafana-url>`
- **Datasources**: `<datasources>` — e.g. Loki (logs), Prometheus (metrics), Tempo (traces). Record which ones this repo actually uses.

Queries target this instance and these datasources unless the user points elsewhere.

## Connection

Operations go through the **Grafana MCP server** (`mcp__claude_ai_Grafana__*`), discovered on demand: run `ToolSearch` with a query like `grafana query` to load the schemas, authenticate first if prompted, then call the tools.

## Conventions

- **Query metrics** (Prometheus): run a PromQL query over a time window to read a metric, or to establish a before/after baseline for a regression.
- **Query logs** (Loki): run a LogQL query filtered by service/label over a time window to pull the log lines around an incident.
- **Query traces** (Tempo): fetch a trace by id, or search traces by service/operation, to see where latency accumulates.
- **Read a dashboard/panel**: resolve a dashboard or panel reference to the panel's query and read its current values.

## Referencing a Grafana panel

The user may pass a dashboard or panel **URL** (`<grafana-url>/d/<dashboard-uid>/...` with a `?panelId=` and `?from=/&to=` range). Normalise it:

- Extract the dashboard `<uid>`, the `panelId`, and the `from`/`to` time range.
- Read that panel's underlying query against its datasource over that range.

## When a skill needs production signal

Establish a baseline over a known-good window, then compare against the incident window — metrics for regressions, logs for the error trail, traces for latency. Return the concrete numbers, not a link.
