
# Project Title
**Operational Profile-Based Software Quality Measurement for LinkedIn Content Curation Platform**

# Abstract

This project implements a comprehensive software quality measurement system for a microservices-based LinkedIn content curation platform. The system combines static code analysis (CI/CD metrics) with runtime operational metrics (Prometheus) and log-based defect tracking (Grafana Loki) to provide quantifiable quality assessment. Following Jeff Tian's Unified Markov Model (UMM) methodology, quality is characterized by computing usage-weighted defect rates across functional domains (Reddit scraping, content generation, and user interface services). The measurement system tracks code quality metrics (LOC, complexity, test coverage, linting violations, type coverage) via CI/CD pipelines, operational metrics (API latency, error rates, throughput, resource utilization) via Prometheus, and defect context via Grafana Loki log aggregation. System-wide quality score is calculated as Σ(Usage_Probability × Defect_Rate) per functional domain, enabling prioritization of quality improvements in high-usage components. The project delivers actionable quality insights through automated dashboards, configurable alerts, and reliability growth tracking across semantic-versioned releases.

# Project Schedule

```mermaid
gantt
    title Software Quality Measurement Project Timeline
    dateFormat YYYY-MM-DD

    section Course Milestones
    Presentation Signup           :milestone, m1, 2025-10-10, 0d
    Project Proposal Due          :milestone, m2, 2025-10-24, 0d
    Literature Research Due       :milestone, m3, 2025-11-07, 0d
    Project Progress Report Due   :milestone, m4, 2025-11-21, 0d
    Exam                          :milestone, m5, 2025-11-26, 0d
    Project Report Due            :milestone, m6, 2025-12-05, 0d
    Project Presentation Due      :milestone, m7, 2025-12-05, 0d

    section Project Implementation
    Proposal Development          :done, p1, 2025-10-17, 7d
    CI/CD Metrics Setup           :active, p2, 2025-10-25, 7d
    Prometheus Deployment         :p3, 2025-11-01, 7d
    Grafana Loki Integration      :p4, 2025-11-08, 7d
    UMM Quality Model Implementation :p5, 2025-11-15, 7d
    Dashboard & Alerting Config   :p6, 2025-11-22, 7d
    Data Collection & Analysis    :p7, 2025-11-29, 7d
    Final Report Writing          :p8, 2025-12-01, 5d
    Presentation Preparation      :p9, 2025-12-03, 3d

    section Deliverables
    Literature Research           :crit, d1, 2025-10-31, 7d
    Progress Report               :crit, d2, 2025-11-14, 7d
    Quality Metrics Collection    :crit, d3, 2025-11-22, 7d
    Final Analysis & Report       :crit, d4, 2025-11-28, 8d
```

# Overview

Code quality metrics will be captured in CI/CD workflows using python quality-checking plugins: *Ruff, Mypy, Pytest, Radon, etc*.

Operational quality metrics will be capturing using a combination of *Prometheus* and *Grafana Loki*.

# Functional Domain Mapping

The system will be organized into three core functional domains, each with specific code quality and operational metrics. This breakdown can be used to construct an operational profile-based quality model following Jeff Tian's Unified Markov Model (UMM) approach. Each domain's Defect Rate and Usage Rates can be tracked by Prometheus for usage tracking, and Prometheus, Grafana Loki, and CI/CD for Defect Rates.

```mermaid
graph LR
    RSS["<b>Reddit Scraper Service</b><br/><br/>Usage Rate: Posts/Hour<br/>Defect Rate: Failures/Total Scrapes"]
    CGS["<b>Content Generation Service</b><br/><br/>Usage Rate: Generations/Hour<br/>Defect Rate: (Failed + Rejected)/Total"]
    UIS["<b>Streamlit UI Service</b><br/><br/>Usage Rate: Sessions/Hour<br/>Defect Rate: Errors/Total Actions"]

    RSS ~~~ CGS
    CGS ~~~ UIS

    style RSS fill:#ff6b6b,stroke:#c92a2a,stroke-width:2px,color:#000
    style CGS fill:#4ecdc4,stroke:#0b7285,stroke-width:2px,color:#000
    style UIS fill:#45b7d1,stroke:#1864ab,stroke-width:2px,color:#000
```

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


## Service Breakdown with UMM Quality Metrics

Service | Code Quality Metrics | Operational Metrics | UMM Quality Metrics
--------|---------------------|---------------------|--------------------
Reddit Scraper Service | LOC, Cyclomatic Complexity, Test Coverage, Maintainability Index, Linting Violations, Type Coverage | Reddit API Latency, Error Rates, Scrape Success Rate, Posts Processed/Hour, API Rate Limit Usage | **Usage Rate**: Posts/Hour, **Defect Rate**: Scrape Failures / Total Scrapes
Content Generation Service | LOC, Cyclomatic Complexity, Test Coverage, Maintainability Index, Linting Violations, Type Coverage | LLM API Latency, Token Usage, Generation Success Rate, Cost per Generation, Content Approval Rate | **Usage Rate**: Generations/Hour, **Defect Rate**: (Failed + Rejected) / Total Generations
Streamlit UI Service | LOC, Cyclomatic Complexity, Test Coverage, Maintainability Index, Linting Violations, Type Coverage | User Sessions, Response Time, Page Load Time, User Actions/Session, Error Rate | **Usage Rate**: Sessions/Hour, **Defect Rate**: UI Errors / Total User Actions

# Operational Metrics

Operational and Usage metrics will be tracked by release and separated by functional domain. This usage information will be used to calculate:
1. **Failure rate** per functional domain (defect density)
2. **Mean Time To Failure (MTTF)** per functional domain

**Per-Domain Quality Calculation:**
- **Domain Quality Score** = (Successful Operations / Total Operations) per time period
- **System-Wide Quality Score** = Σ (Usage_Weight × Domain_Quality) across all domains
- **Reliability Growth** = Track quality score improvements across releases

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

# Follow-up Actions & Process Improvement

This section defines the response protocols and continuous improvement processes triggered by quality metrics thresholds and trend analysis.

## Quality Thresholds & Alert Triggers

### CI/CD Quality Gates

**Blocking Conditions (Prevent Merge/Deploy):**
- Test Coverage < 70% (per service)
- Cyclomatic Complexity > 15 (any function)
- Maintainability Index < 50 (any module)
- Linting Violations > 50 (per service)
- Type Coverage < 60% (per service)
- Failed Tests > 0

**Warning Conditions (Allow Merge with Review):**
- Test Coverage 70-80%
- Cyclomatic Complexity 10-15
- Maintainability Index 50-65
- Linting Violations 20-50

**Actions:**
1. **Automated**: CI/CD pipeline blocks merge request
2. **Notification**: Alert developer via GitHub PR comment with specific violations
3. **Required Action**: Developer must refactor code or justify exception
4. **Review**: Team lead approval required for threshold exceptions

### Operational Quality Alerts

**Critical Alerts (Immediate Response Required):**
- Error Rate > 5% (any service)
- API Response Time P95 > 2000ms
- Service Uptime < 99%
- Database Connection Pool Utilization > 90%
- Neo4j Query Time P95 > 500ms
- System-Wide UMM Quality Score > 0.05 (5% defect rate)

**Warning Alerts (Investigation Within 24 Hours):**
- Error Rate 1-5%
- API Response Time P95 1000-2000ms
- Service Uptime 99-99.9%
- Database Connection Pool Utilization 75-90%
- UMM Quality Score 0.02-0.05 (2-5% defect rate)

## UMM Quality Score Response Plan

The UMM quality score (Σ(Usage_Probability × Defect_Rate)) provides usage-weighted quality assessment. When quality degrades, follow this prioritization framework:

### Quality Score Degradation Triggers

**Severity Levels:**
- **Critical**: UMM Score increases by >50% between releases
- **Major**: UMM Score increases by 25-50% between releases
- **Minor**: UMM Score increases by 10-25% between releases
- **Informational**: UMM Score increases by <10% between releases

### Prioritized Response Strategy

**Step 1: Identify High-Impact Domains**
```
Impact Score = Usage_Probability × Defect_Rate × 1000
```

Prioritize domains with highest Impact Score:
- Focus on services with >30% usage probability first
- Example: If Reddit Scraper has 60% usage and 3% defect rate:
  Impact = 0.60 × 0.03 × 1000 = 18 points

**Step 2: Domain-Specific Actions**

**Reddit Scraper Service:**
- **Defect Types**: API failures, rate limiting, parsing errors
- **Actions**:
  - Implement exponential backoff for API retries
  - Add request caching to reduce API calls
  - Improve error handling for malformed posts
  - Add integration tests for edge cases

**Content Generation Service:**
- **Defect Types**: LLM timeouts, token limit exceeded, poor quality output
- **Actions**:
  - Implement timeout handling with fallback strategies
  - Add content validation before returning results
  - Track rejection reasons to improve prompts
  - Implement content quality scoring

**Streamlit UI Service:**
- **Defect Types**: Session errors, rendering failures, slow page loads
- **Actions**:
  - Optimize database queries
  - Implement caching for frequently accessed data
  - Add client-side validation
  - Improve error messages for user clarity

**Neo4j Database:**
- **Defect Types**: Slow queries, connection timeouts, transaction failures
- **Actions**:
  - Add missing indexes on frequently queried properties
  - Optimize Cypher queries with EXPLAIN/PROFILE
  - Increase connection pool size
  - Implement query result caching

**Step 3: Measure Improvement**
- Re-calculate UMM quality score after fixes deployed
- Track reliability growth: `(New_Quality_Score - Old_Quality_Score) / Old_Quality_Score × 100%`
- Target: Reduce defect rate by 20% per iteration