
# Overview

Code quality metrics will be captured in CI/CD workflows using python quality-checking plugins: *Ruff, Mypy, Pytest, Radon, etc*.

Operational quality metrics will be capturing using a combination of *Prometheus* and *Grafana Loki*.

# Functional Domain Mapping

The system will be organized into three core functional domains, each with specific code quality and operational metrics. This breakdown can be used to construct an operational profile-based quality model following Jeff Tian's Unified Markov Model (UMM) approach. Each domain's Defect Rate and Usage Rates can be tracked by Prometheus for usage tracking, and Prometheus, Grafana Loki, and CI/CD for Defect Rates.

## Operational Profile-Based Quality Model (Tian's UMM)

Following Tian's methodology, system quality will be characterized by combining operational profiles (usage patterns) with defect rates across functional domains:

**Quality Metric Formula:**
```
System Quality Score = Σ (Usage_Probability(state) × Defect_Rate(state))
```

Where:
- **Usage_Probability(state)**: Proportion of total operations occurring in each functional domain (from Prometheus usage metrics)
- **Defect_Rate(state)**: Failures per 1000 operations in each functional domain (from error counters and logs)

**Operational States (Functional Domains):**
1. **Reddit Scraping** - Data ingestion from external API
2. **Content Generation** - LLM-based content transformation
3. **User Interface** - Human review and interaction
4. **Database Operations** - Neo4j graph queries and persistence

**Transition Model:**
```
User Request → Reddit Scraping → Database Write → Content Generation → Database Read → UI Display → Human Review → (Approve/Reject)
```

**Metrics Collection for UMM:**
- **Usage Tracking**: Prometheus counters track operation frequency per domain
- **Defect Tracking**: Error rates, failed operations, and exceptions per domain
- **Transition Probabilities**: Derived from API endpoint call patterns and service-to-service communication metrics
- **Reliability Calculation**: System reliability = Π (1 - Defect_Rate(state))^Usage_Count(state)

## Service Breakdown with UMM Quality Metrics

Service | Code Quality Metrics | Operational Metrics | UMM Quality Metrics
--------|---------------------|---------------------|--------------------
Reddit Scraper Service | LOC, Cyclomatic Complexity, Test Coverage, Maintainability Index, Linting Violations, Type Coverage | Reddit API Latency, Error Rates, Scrape Success Rate, Posts Processed/Hour, API Rate Limit Usage | **Usage Rate**: Posts/Hour, **Defect Rate**: Scrape Failures / Total Scrapes
Content Generation Service | LOC, Cyclomatic Complexity, Test Coverage, Maintainability Index, Linting Violations, Type Coverage | LLM API Latency, Token Usage, Generation Success Rate, Cost per Generation, Content Approval Rate | **Usage Rate**: Generations/Hour, **Defect Rate**: (Failed + Rejected) / Total Generations
Streamlit UI Service | LOC, Cyclomatic Complexity, Test Coverage, Maintainability Index, Linting Violations, Type Coverage | User Sessions, Response Time, Page Load Time, User Actions/Session, Error Rate | **Usage Rate**: Sessions/Hour, **Defect Rate**: UI Errors / Total User Actions

**Transition Probabilities (measured via Prometheus):**
- P(Scrape → Content Generation) = Content Generations / Successful Scrapes
- P(Content Generation → UI Review) = UI Review Sessions / Generated Content
- P(UI Review → Approval) = Approved Content / Total Reviews
- P(UI Review → Rejection) = Rejected Content / Total Reviews

# Operational Metrics

Operational and Usage metrics will be tracked by release and separated by functional domain. This usage information will be used to calculate:
1. **Failure rate** per functional domain (defect density)
2. **Mean Time To Failure (MTTF)** per functional domain
3. **Usage-weighted system quality** following Tian's UMM approach
4. **Transition reliability** between operational states

**Per-Domain Quality Calculation:**
- **Domain Quality Score** = (Successful Operations / Total Operations) per time period
- **System-Wide Quality Score** = Σ (Usage_Weight × Domain_Quality) across all domains
- **Reliability Growth** = Track quality score improvements across releases
-   Performance metrics (response time, throughput, resource utilization) from Prometheus
-   API endpoint usage and error rates from Prometheus
-   Application-specific metrics (user sessions, external API latency, cache hit rates) from Prometheus
-   Database performance metrics (Neo4j Enterprise query time, transaction throughput, connection pool usage) from Neo4j built-in Prometheus endpoint
-   Log data and defect data from Grafana Loki
-   Uptime and availability monitoring from Prometheus Alertmanager


# Metrics Stack Architecture

## Quality Tracking System Architecture

```mermaid
classDiagram
    class SoftwareQualitySystem {
        <<abstract>>
        +release_version: SemVer
        +quality_score: float
        +defect_rate: float
        +usage_profile: dict
        +calculate_system_quality()
        +generate_quality_report()
        +track_reliability_growth()
        +aggregate_metrics()
    }

    class CICDQualityTracker {
        <<implementation>>
        +build_status: bool
        +deployment_metrics: dict
        +radon_loc: int
        +radon_complexity: float
        +radon_maintainability_index: float
        +pytest_coverage: float
        +pytest_tests_passed: int
        +pytest_tests_failed: int
        +ruff_violations: int
        +ruff_style_issues: []
        +mypy_type_coverage: float
        +mypy_type_errors: int
        +semver_current_version: SemVer
        +semver_changelog: string
        +analyze_codebase_with_radon()
        +run_tests_with_pytest()
        +check_code_style_with_ruff()
        +check_types_with_mypy()
        +analyze_commits_for_semver()
        +bump_version_and_release()
        +track_deployment_success()
    }

    class PrometheusMetricsCollector {
        <<implementation>>
        +scrape_interval: duration
        +operational_metrics: timeseries
        +usage_rates: dict
        +error_counters: dict
        +service_metrics_endpoints: []
        +neo4j_query_time: histogram
        +neo4j_transaction_throughput: gauge
        +neo4j_connection_pool: gauge
        +alert_rules: []
        +uptime_target: float
        +scrape_service_metrics()
        +scrape_neo4j_metrics()
        +collect_usage_data()
        +track_defect_rates()
        +measure_latencies()
        +calculate_transition_probabilities()
        +monitor_resource_utilization()
        +compute_umm_quality_score()
        +send_alerts()
        +monitor_sla()
    }

    class GrafanaLokiLogAggregator {
        <<implementation>>
        +log_streams: []
        +error_logs: []
        +defect_data: dict
        +aggregate_logs()
        +parse_error_patterns()
        +identify_defects()
        +correlate_failures()
        +track_exception_rates()
        +analyze_log_trends()
        +provide_defect_context()
        +generate_dashboards()
    }

    SoftwareQualitySystem <|.. CICDQualityTracker : implements
    SoftwareQualitySystem <|.. PrometheusMetricsCollector : implements
    SoftwareQualitySystem <|.. GrafanaLokiLogAggregator : implements

    SoftwareQualitySystem ..> CICDQualityTracker : aggregates
    SoftwareQualitySystem ..> PrometheusMetricsCollector : aggregates
    SoftwareQualitySystem ..> GrafanaLokiLogAggregator : aggregates

    note for SoftwareQualitySystem "Computes UMM Quality Score:\nΣ(Usage_Rate × Defect_Rate)\nper functional domain"

    note for CICDQualityTracker "Uses: Radon, Pytest, Ruff,\nMypy, python-semantic-release"

    note for PrometheusMetricsCollector "Scrapes: Service metrics,\nNeo4j metrics, AlertManager"

    note for GrafanaLokiLogAggregator "Provides defect context\nthrough log correlation"
```

## Component Relationships

```mermaid
graph TB
    RSS[RedditScraperService]
    CGS[ContentGenerationService]
    SUI[StreamlitUIService]
    NEO[Neo4jEnterpriseDB]
    PROM[PrometheusServer]
    LOKI[GrafanaLoki]
    GRAF[GrafanaDashboard]
    ALERT[PrometheusAlertmanager]
    CQT[CodeQualityTools]
    SEM[SemanticRelease]

    RSS -->|expose_metrics<br/>:8001/metrics| PROM
    CGS -->|expose_metrics<br/>:8002/metrics| PROM
    SUI -->|expose_metrics<br/>:8003/metrics| PROM
    NEO -->|expose_metrics<br/>:2004/metrics| PROM

    RSS -->|send_logs| LOKI
    CGS -->|send_logs| LOKI
    SUI -->|send_logs| LOKI

    PROM -->|data_source| GRAF
    LOKI -->|data_source| GRAF
    PROM -->|alert_rules| ALERT

    CQT -->|analyze_code| RSS
    CQT -->|analyze_code| CGS
    CQT -->|analyze_code| SUI

    SEM -->|version_tracking| RSS
    SEM -->|version_tracking| CGS
    SEM -->|version_tracking| SUI

    style RSS fill:#c92a2a,stroke:#fa5252,stroke-width:2px,color:#000
    style CGS fill:#0b7285,stroke:#3bc9db,stroke-width:2px,color:#000
    style SUI fill:#1864ab,stroke:#4dabf7,stroke-width:2px,color:#000
    style NEO fill:#2b8a3e,stroke:#51cf66,stroke-width:2px,color:#000
    style PROM fill:#e67700,stroke:#ff922b,stroke-width:2px,color:#000
    style LOKI fill:#495057,stroke:#adb5bd,stroke-width:2px,color:#000
    style GRAF fill:#1971c2,stroke:#74c0fc,stroke-width:2px,color:#000
    style ALERT fill:#d9480f,stroke:#ff8787,stroke-width:2px,color:#000
    style CQT fill:#5f3dc4,stroke:#9775fa,stroke-width:2px,color:#000
    style SEM fill:#a61e4d,stroke:#f06595,stroke-width:2px,color:#000
```

# Summary

## CI/CD Metrics

The following metrics will be implemented in CI/CD jobs.

### Code Quality
- Test Coverage: **Pytest**
- Lines of Code (LOC): **Radon**
- Cyclomatic Complexity: **Radon**
- Maintainability Index: **Radon**

### Code Style & Consistency
- Linting Violations: **Ruff**
- Type Hint Coverage: **Mypy**
- Code Duplication: **Ruff**

### Semantic Versioning
- Version Tracking: **python-semantic-release**
- Changelog Generation: **python-semantic-release**
- Git Tag Creation: **python-semantic-release**
- Deployment Success Rate: **CI/CD Pipeline**

## Operational Metrics

Prometheus will be deployed as a microservice to track the following metrics for the Streamlit App, Reddit Scrapper Service, and Neo4j Database

### Reddit Scrapper Service Metrics

- Reddit API Latency: **Prometheus** (histogram)
- Scrape Error Rate: **Prometheus** (counter)
- Scrape Success Rate: **Prometheus** (gauge)
- Posts Processed Per Hour: **Prometheus** (counter)
- API Rate Limit Usage: **Prometheus** (gauge)
- Service Uptime: **Prometheus** (gauge)


### Content Generation Service Metrics

- LLM API Latency: **Prometheus** (histogram)
- Token Usage Total: **Prometheus** (counter)
- Generation Success Rate: **Prometheus** (gauge)
- Cost Per Generation: **Prometheus** (gauge)
- Content Approval Rate: **Prometheus** (gauge)
- Service Uptime: **Prometheus** (gauge)


### Streamlit UI Service Metrics

- User Sessions Active: **Prometheus/Custom Middleware** (gauge)
- Response Time: **Prometheus** (histogram)
- Page Load Time: **Prometheus** (histogram)
- User Actions Per Session: **Prometheus** (counter)
- UI Error Rate: **Prometheus** (counter)
- Service Uptime: **Prometheus** (gauge)


### Neo4j Enterprise Database Metrics

Neo4j Enterprise is deployed as a containerized service with built-in Prometheus metrics endpoint enabled via:
- `server.metrics.prometheus.enabled=true`
- `server.metrics.prometheus.endpoint=0.0.0.0:2004`


- Query Execution Time (P50, P95, P99): **Neo4j Prometheus Endpoint** (histogram)
- Transaction Throughput: **Neo4j Prometheus Endpoint** (gauge)
- Connection Pool Utilization: **Neo4j Prometheus Endpoint** (gauge)
- Cypher Query Performance: **Neo4j Prometheus Endpoint** (histogram)
- Graph Traversal Depth: **Neo4j Prometheus Endpoint** (histogram)
- Database Storage Usage: **Neo4j Prometheus Endpoint** (gauge)
- Node/Relationship Counts: **Neo4j Prometheus Endpoint** (gauge)
- Page Cache Hit Ratio: **Neo4j Prometheus Endpoint** (gauge)
- GC Pause Time (JVM): **Neo4j Prometheus Endpoint** (histogram)
- Container Health Status: **Container Metrics** (gauge)

## Infrastructure & Monitoring Metrics

The Prometheus service and Grafana Loki will passively monitor system performance and capture the following metrics about the kubernetes cluster.

### Performance & Reliability
- Response Time (P50, P95, P99): **Prometheus**
- Throughput (Requests/sec): **Prometheus**
- Error Rates by Endpoint: **Prometheus**
- Resource Utilization (CPU, Memory, Disk I/O): **Prometheus**
- Uptime/Availability: **Prometheus Alertmanager**

### Application-Specific
- API Endpoint Usage: **Prometheus**
- External API Latency (Reddit, LangChain/Gemini): **Prometheus**
- Cache Hit Rates: **Prometheus**
- Queue Depths: **Prometheus**

### Logging & Monitoring
- Log Data: **Grafana Loki**
- Defect/Error Data: **Grafana**
