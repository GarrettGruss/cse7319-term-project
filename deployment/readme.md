## Overview

- Fork a project on github
- Setup otel-collector to scrape metrics from forked project
- Configure self-hosted runners
- Run actions for all tagged releases

Need to review data from scraping and actions to see if DORA metrics can be calculated.

## References

https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/githubreceiver/README.md
https://github.com/open-telemetry/opentelemetry-collector-releases/
https://openobserve.ai/blog/github-monitoring-with-otel/
https://github.com/openobserve/openobserve
https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners
https://github.com/dora-team/fourkeys/blob/main/METRICS.md
https://github.com/dora-team/fourkeys?tab=readme-ov-file

note: auth is not needed if pulling specs annonymously from a project. 