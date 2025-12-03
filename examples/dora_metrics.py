"""
DORA Metrics Analysis for LangChain

This script calculates the four key DORA (DevOps Research and Assessment) metrics:
1. Deployment Frequency - How often code is merged/deployed
2. Lead Time for Changes - Time from PR creation to merge
3. Change Failure Rate - Percentage of changes that cause failures
4. Time to Restore Service - Time to recover from failures
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import re
from pathlib import Path

# Set style for visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)


def load_data(data_dir='examples/data/intel'):
    """Load all CSV files"""
    print("Loading data...")
    print(f"Data directory: {data_dir}\n")

    closed_requests = pd.read_csv(f'{data_dir}/closed_requests.csv')
    merged_requests = pd.read_csv(f'{data_dir}/merged_requests.csv')
    opened_requests = pd.read_csv(f'{data_dir}/opened_requests.csv')
    opened_issues = pd.read_csv(f'{data_dir}/opened_issues.csv')

    # Convert date columns to datetime
    for df in [closed_requests, merged_requests, opened_requests, opened_issues]:
        df['date_abs'] = pd.to_datetime(df['date_abs'])

    print(f"Merged PRs: {len(merged_requests)}")
    print(f"Opened PRs: {len(opened_requests)}")
    print(f"Closed PRs: {len(closed_requests)}")
    print(f"Opened Issues: {len(opened_issues)}")
    print(f"\nDate range: {merged_requests['date_abs'].min()} to {merged_requests['date_abs'].max()}")

    return closed_requests, merged_requests, opened_requests, opened_issues


def calculate_deployment_frequency(merged_requests):
    """Calculate deployment frequency metrics"""
    print("\n" + "="*80)
    print("1. DEPLOYMENT FREQUENCY")
    print("="*80)

    merged_requests_sorted = merged_requests.sort_values('date_abs')

    # Get date range
    start_date = merged_requests_sorted['date_abs'].min()
    end_date = merged_requests_sorted['date_abs'].max()
    total_days = (end_date - start_date).days + 1

    # Calculate metrics
    total_deployments = len(merged_requests)
    deployments_per_day = total_deployments / total_days
    deployments_per_week = deployments_per_day * 7

    print(f"Total deployments: {total_deployments}")
    print(f"Time period: {total_days} days")
    print(f"Deployments per day: {deployments_per_day:.2f}")
    print(f"Deployments per week: {deployments_per_week:.2f}")

    # Daily deployment counts
    daily_deployments = merged_requests.groupby(merged_requests['date_abs'].dt.date).size()

    print(f"\nMedian deployments per day: {daily_deployments.median():.1f}")
    print(f"Max deployments in a day: {daily_deployments.max()}")

    # Visualize
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Daily deployments (convert index to datetime for proper plotting)
    daily_dates = pd.to_datetime(daily_deployments.index)
    ax1.plot(daily_dates, daily_deployments.values, color='steelblue', linewidth=2, marker='o', markersize=5)
    ax1.set_title('Deployments per Day', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Deployments')
    ax1.axhline(y=deployments_per_day, color='red', linestyle='--',
                label=f'Average: {deployments_per_day:.2f}')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)

    # Cumulative deployments
    cumulative = range(1, len(merged_requests_sorted) + 1)
    ax2.plot(merged_requests_sorted['date_abs'], cumulative, linewidth=2, color='green')
    ax2.set_title('Cumulative Deployments Over Time', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Cumulative Deployments')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('examples/deployment_frequency.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved to: examples/deployment_frequency.png")

    return {
        'total_deployments': total_deployments,
        'deployments_per_day': deployments_per_day,
        'deployments_per_week': deployments_per_week,
        'total_days': total_days,
        'start_date': start_date,
        'end_date': end_date
    }


def calculate_lead_time(opened_requests, merged_requests):
    """Calculate lead time for changes using temporal proximity matching"""
    print("\n" + "="*80)
    print("2. LEAD TIME FOR CHANGES")
    print("="*80)

    # Try direct hash matching first
    lead_time_data = pd.merge(
        opened_requests[['hash', 'date_abs', 'msg']],
        merged_requests[['hash', 'date_abs']],
        on='hash',
        suffixes=('_opened', '_merged')
    )

    # If no matches found, use temporal statistical approach
    if len(lead_time_data) == 0:
        print("No direct PR matches found between opened and merged datasets.")
        print("Using temporal statistical approach to estimate lead time...\n")

        # Sort both datasets
        opened_sorted = opened_requests.sort_values('date_abs')
        merged_sorted = merged_requests.sort_values('date_abs')

        # For each merged PR, find the closest opened PR before it
        lead_time_estimates = []

        for idx, merged_pr in merged_sorted.iterrows():
            merge_date = merged_pr['date_abs']

            # Find opened PRs before this merge date
            prior_opens = opened_sorted[opened_sorted['date_abs'] < merge_date]

            if len(prior_opens) > 0:
                # Find the closest one
                time_diffs = (merge_date - prior_opens['date_abs']).dt.total_seconds()
                closest_idx = time_diffs.abs().idxmin()
                closest_open = prior_opens.loc[closest_idx]

                lead_time_days = (merge_date - closest_open['date_abs']).total_seconds() / (24 * 3600)
                lead_time_hours = (merge_date - closest_open['date_abs']).total_seconds() / 3600

                # Only include reasonable lead times (< 90 days)
                if 0 <= lead_time_days <= 90:
                    lead_time_estimates.append({
                        'hash_opened': closest_open['hash'],
                        'hash_merged': merged_pr['hash'],
                        'msg': merged_pr['msg'],
                        'date_abs_opened': closest_open['date_abs'],
                        'date_abs_merged': merge_date,
                        'lead_time_days': lead_time_days,
                        'lead_time_hours': lead_time_hours
                    })

        if len(lead_time_estimates) > 0:
            lead_time_data = pd.DataFrame(lead_time_estimates)
            print(f"Estimated lead time for {len(lead_time_data)} PR pairs using temporal proximity")
            print("Note: This is an approximation based on matching nearby open/merge events")
        else:
            print("Could not estimate lead times. Using simplified metric.")
            # Calculate simple average time between events
            avg_gap = (merged_sorted['date_abs'].mean() - opened_sorted['date_abs'].mean()).total_seconds() / (24 * 3600)
            return {
                'mean_days': avg_gap,
                'median_days': avg_gap,
                'p90_days': avg_gap,
                'data': None
            }
    else:
        # Calculate lead time from matched PRs
        lead_time_data['lead_time_days'] = (
            lead_time_data['date_abs_merged'] - lead_time_data['date_abs_opened']
        ).dt.total_seconds() / (24 * 3600)

        lead_time_data['lead_time_hours'] = (
            lead_time_data['date_abs_merged'] - lead_time_data['date_abs_opened']
        ).dt.total_seconds() / 3600

    print(f"\nTotal PRs with lead time data: {len(lead_time_data)}")
    print(f"\nLead Time Statistics (in days):")
    print(f"  Mean: {lead_time_data['lead_time_days'].mean():.2f} days")
    print(f"  Median: {lead_time_data['lead_time_days'].median():.2f} days")
    print(f"  Min: {lead_time_data['lead_time_days'].min():.2f} days")
    print(f"  Max: {lead_time_data['lead_time_days'].max():.2f} days")
    print(f"  Std Dev: {lead_time_data['lead_time_days'].std():.2f} days")

    print(f"\nPercentiles:")
    print(f"  25th: {lead_time_data['lead_time_days'].quantile(0.25):.2f} days")
    print(f"  50th: {lead_time_data['lead_time_days'].quantile(0.50):.2f} days")
    print(f"  75th: {lead_time_data['lead_time_days'].quantile(0.75):.2f} days")
    print(f"  90th: {lead_time_data['lead_time_days'].quantile(0.90):.2f} days")

    # Show fastest merges
    if len(lead_time_data) > 0:
        print(f"\nFastest 5 merges:")
        fastest = lead_time_data.nsmallest(5, 'lead_time_hours')[['msg', 'lead_time_hours']]
        for idx, row in fastest.iterrows():
            print(f"  {row['lead_time_hours']:.1f} hours - {row['msg'][:60]}...")

    print("\n[Visualization skipped - lead time data unreliable without direct PR matching]")

    return {
        'mean_days': lead_time_data['lead_time_days'].mean(),
        'median_days': lead_time_data['lead_time_days'].median(),
        'p90_days': lead_time_data['lead_time_days'].quantile(0.90),
        'data': lead_time_data
    }


def calculate_change_failure_rate(opened_issues, merged_requests):
    """Calculate change failure rate"""
    print("\n" + "="*80)
    print("3. CHANGE FAILURE RATE")
    print("="*80)

    # Bug keywords
    bug_keywords = [
        'bug', 'error', 'fix', 'broken', 'crash', 'fail', 'issue',
        'regression', 'exception', 'typeerror', 'attributeerror',
        'importerror', 'not working', 'does not work', 'doesn\'t work'
    ]

    def is_bug_issue(msg):
        """Check if issue message indicates a bug/failure"""
        if pd.isna(msg):
            return False
        msg_lower = str(msg).lower()
        return any(keyword in msg_lower for keyword in bug_keywords)

    opened_issues['is_bug'] = opened_issues['msg'].apply(is_bug_issue)
    bug_issues = opened_issues[opened_issues['is_bug']].copy()

    total_deployments = len(merged_requests)

    print(f"Total issues: {len(opened_issues)}")
    print(f"Bug-related issues: {len(bug_issues)} ({len(bug_issues)/len(opened_issues)*100:.1f}%)")
    print(f"Total deployments: {total_deployments}")

    # Calculate change failure rate
    change_failure_rate = (len(bug_issues) / total_deployments) * 100

    print(f"\nChange Failure Rate: {change_failure_rate:.2f}%")
    print(f"  ({len(bug_issues)} bugs / {total_deployments} deployments)")
    print(f"\nNote: This is an approximation based on keyword matching.")

    # Show sample bugs
    print("\nSample bug-related issues:")
    print("="*80)
    for idx, row in bug_issues.head(10).iterrows():
        print(f"{row['hash']} ({row['date_abs'].date()}): {row['msg'][:70]}...")

    # Visualize
    fig, ax = plt.subplots(figsize=(14, 6))

    # Group by date (only dates with actual data)
    deployments_by_date = merged_requests.groupby(merged_requests['date_abs'].dt.date).size()
    bugs_by_date = bug_issues.groupby(bug_issues['date_abs'].dt.date).size()

    # Convert index to datetime for proper plotting
    deployments_dates = pd.to_datetime(deployments_by_date.index)
    bugs_dates = pd.to_datetime(bugs_by_date.index)

    # Plot both metrics on the same chart
    ax.plot(deployments_dates, deployments_by_date.values, linewidth=2, marker='o', markersize=5,
            label='Deployments', color='green', alpha=0.8)
    ax.plot(bugs_dates, bugs_by_date.values, linewidth=2, marker='s', markersize=5,
            label='Bug Issues', color='red', alpha=0.8)

    ax.set_title('Deployments vs Bug Issues Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('examples/change_failure_rate.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved to: examples/change_failure_rate.png")

    return {
        'rate': change_failure_rate,
        'total_bugs': len(bug_issues),
        'bug_issues': bug_issues
    }


def calculate_time_to_restore(bug_issues, merged_requests):
    """Calculate time to restore service"""
    print("\n" + "="*80)
    print("4. TIME TO RESTORE SERVICE")
    print("="*80)

    def extract_issue_refs(msg):
        """Extract issue references (#12345) from PR message"""
        if pd.isna(msg):
            return []
        matches = re.findall(r'#(\d+)', str(msg))
        return [f'#{num}' for num in matches]

    # Find fix PRs
    merged_requests['referenced_issues'] = merged_requests['msg'].apply(extract_issue_refs)
    fix_prs = merged_requests[merged_requests['referenced_issues'].apply(len) > 0].copy()

    # Match fix PRs to bug issues
    restoration_times = []

    for idx, fix_pr in fix_prs.iterrows():
        for issue_ref in fix_pr['referenced_issues']:
            matching_bugs = bug_issues[bug_issues['hash'] == issue_ref]
            if len(matching_bugs) > 0:
                bug = matching_bugs.iloc[0]
                restoration_time = (fix_pr['date_abs'] - bug['date_abs']).total_seconds() / 3600
                if restoration_time >= 0:
                    restoration_times.append({
                        'bug_hash': issue_ref,
                        'bug_msg': bug['msg'],
                        'bug_opened': bug['date_abs'],
                        'fix_hash': fix_pr['hash'],
                        'fix_msg': fix_pr['msg'],
                        'fix_merged': fix_pr['date_abs'],
                        'restoration_hours': restoration_time,
                        'restoration_days': restoration_time / 24
                    })

    restoration_df = pd.DataFrame(restoration_times)

    if len(restoration_df) > 0:
        print(f"Bug-fix pairs identified: {len(restoration_df)}")
        print(f"\nRestoration Time Statistics (in hours):")
        print(f"  Mean: {restoration_df['restoration_hours'].mean():.2f} hours ({restoration_df['restoration_days'].mean():.2f} days)")
        print(f"  Median: {restoration_df['restoration_hours'].median():.2f} hours ({restoration_df['restoration_days'].median():.2f} days)")
        print(f"  Min: {restoration_df['restoration_hours'].min():.2f} hours")
        print(f"  Max: {restoration_df['restoration_hours'].max():.2f} hours ({restoration_df['restoration_days'].max():.2f} days)")

        print(f"\nPercentiles:")
        print(f"  25th: {restoration_df['restoration_hours'].quantile(0.25):.2f} hours")
        print(f"  50th: {restoration_df['restoration_hours'].quantile(0.50):.2f} hours")
        print(f"  75th: {restoration_df['restoration_hours'].quantile(0.75):.2f} hours")
        print(f"  90th: {restoration_df['restoration_hours'].quantile(0.90):.2f} hours")

        # Show examples
        print("\nFastest restorations:")
        print("="*80)
        fastest = restoration_df.nsmallest(5, 'restoration_hours')
        for idx, row in fastest.iterrows():
            print(f"\nBug {row['bug_hash']}: {row['bug_msg'][:60]}...")
            print(f"  Fixed by {row['fix_hash']} in {row['restoration_hours']:.1f} hours")
            print(f"  Fix: {row['fix_msg'][:60]}...")

        print("\n" + "="*80)
        print("\nSlowest restorations:")
        print("="*80)
        slowest = restoration_df.nlargest(5, 'restoration_hours')
        for idx, row in slowest.iterrows():
            print(f"\nBug {row['bug_hash']}: {row['bug_msg'][:60]}...")
            print(f"  Fixed by {row['fix_hash']} in {row['restoration_days']:.1f} days")
            print(f"  Fix: {row['fix_msg'][:60]}...")

        print("\n[Visualization skipped - MTTR data unreliable without direct bug-fix matching]")

        return {
            'mean_hours': restoration_df['restoration_hours'].mean(),
            'median_hours': restoration_df['restoration_hours'].median(),
            'count': len(restoration_df),
            'data': restoration_df
        }
    else:
        print("No bug-fix pairs could be identified from the data.")
        print("This requires explicit references from fix PRs to bug issues.")
        return {
            'mean_hours': None,
            'median_hours': None,
            'count': 0,
            'data': None
        }


def classify_metrics(deployment_freq, lead_time, failure_rate, restoration_time):
    """Classify metrics according to DORA performance levels"""

    def classify_deployment_frequency(deploys_per_day):
        if deploys_per_day >= 1:
            return "Elite"
        elif deploys_per_day >= 1/7:
            return "High"
        elif deploys_per_day >= 1/30:
            return "Medium"
        else:
            return "Low"

    def classify_lead_time(days):
        if days < 1:
            return "Elite"
        elif days <= 7:
            return "High"
        elif days <= 30:
            return "Medium"
        else:
            return "Low"

    def classify_failure_rate(rate):
        if rate <= 15:
            return "Elite"
        elif rate <= 30:
            return "High"
        elif rate <= 45:
            return "Medium"
        else:
            return "Low"

    def classify_restoration_time(hours):
        if hours is None:
            return "N/A"
        if hours < 1:
            return "Elite"
        elif hours < 24:
            return "High"
        elif hours < 168:
            return "Medium"
        else:
            return "Low"

    print("\n" + "="*80)
    print(" " * 25 + "PERFORMANCE CLASSIFICATION")
    print("="*80)

    df_class = classify_deployment_frequency(deployment_freq['deployments_per_day'])
    lt_class = classify_lead_time(lead_time['median_days'])
    cfr_class = classify_failure_rate(failure_rate['rate'])
    mttr_class = classify_restoration_time(restoration_time['median_hours'])

    print(f"\nDeployment Frequency: {df_class}")
    print(f"Lead Time for Changes: {lt_class}")
    print(f"Change Failure Rate: {cfr_class}")
    print(f"Time to Restore Service: {mttr_class}")

    # Overall assessment
    classifications = [c for c in [df_class, lt_class, cfr_class, mttr_class] if c != "N/A"]
    elite_count = classifications.count("Elite")
    high_count = classifications.count("High")

    print(f"\nOverall Performance: ", end="")
    if elite_count >= 3:
        print("Elite Performer")
    elif elite_count + high_count >= 3:
        print("High Performer")
    elif "Low" not in classifications:
        print("Medium Performer")
    else:
        print("Needs Improvement")

    print("="*80)


def print_summary(deployment_freq, lead_time, failure_rate, restoration_time):
    """Print summary dashboard"""
    print("\n" + "="*80)
    print(" " * 25 + "DORA METRICS SUMMARY")
    print("="*80)

    print(f"\n1. DEPLOYMENT FREQUENCY")
    print(f"   {deployment_freq['deployments_per_day']:.2f} deployments/day | {deployment_freq['deployments_per_week']:.2f} deployments/week")
    print(f"   Elite: Multiple deploys per day | High: Once per day to once per week")

    print(f"\n2. LEAD TIME FOR CHANGES")
    print(f"   Median: {lead_time['median_days']:.2f} days | Mean: {lead_time['mean_days']:.2f} days")
    print(f"   Elite: Less than 1 day | High: 1 day to 1 week")

    print(f"\n3. CHANGE FAILURE RATE")
    print(f"   {failure_rate['rate']:.2f}% ({failure_rate['total_bugs']} bugs / {deployment_freq['total_deployments']} deployments)")
    print(f"   Elite: 0-15% | High: 16-30%")

    if restoration_time['median_hours'] is not None:
        print(f"\n4. TIME TO RESTORE SERVICE")
        print(f"   Median: {restoration_time['median_hours']:.2f} hours | Mean: {restoration_time['mean_hours']:.2f} hours")
        print(f"   Elite: Less than 1 hour | High: Less than 1 day")
        print(f"   (Based on {restoration_time['count']} identified bug-fix pairs)")
    else:
        print(f"\n4. TIME TO RESTORE SERVICE")
        print(f"   Unable to calculate - no bug-fix pairs identified")

    print("\n" + "="*80)
    print(f"Analysis Period: {deployment_freq['start_date'].date()} to {deployment_freq['end_date'].date()} ({deployment_freq['total_days']} days)")
    print("="*80)


def main():
    """Main function to run all DORA metrics calculations"""
    print("="*80)
    print(" " * 20 + "DORA METRICS ANALYSIS FOR LANGCHAIN")
    print("="*80)

    # Load data
    closed_requests, merged_requests, opened_requests, opened_issues = load_data()

    # Calculate metrics
    deployment_freq = calculate_deployment_frequency(merged_requests)
    lead_time = calculate_lead_time(opened_requests, merged_requests)
    failure_rate = calculate_change_failure_rate(opened_issues, merged_requests)
    restoration_time = calculate_time_to_restore(failure_rate['bug_issues'], merged_requests)

    # Print summary
    print_summary(deployment_freq, lead_time, failure_rate, restoration_time)

    # Classify metrics
    classify_metrics(deployment_freq, lead_time, failure_rate, restoration_time)

    print("\n✓ Analysis complete!")
    print("  Visualizations saved:")
    print("    - examples/deployment_frequency.png")
    print("    - examples/change_failure_rate.png")
    print("  Note: Lead Time and MTTR visualizations skipped due to data matching limitations.")


if __name__ == "__main__":
    main()
