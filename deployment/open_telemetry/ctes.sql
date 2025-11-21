-- Duration from PR creation to merge (seconds)
SELECT 
    vcs_repository_name,
    vcs_owner_name,
    avg(value) as "avg_time_to_merge",
    approx_percentile_cont(value, 0.95) as "percentile_time_to_merge",
    count(value) as "num_merges"
FROM "vcs_change_time_to_merge"
GROUP BY vcs_repository_name, vcs_owner_name

-- Duration from PR creation to approval (seconds)
SELECT 
    vcs_repository_name,
    vcs_owner_name,
    avg(value) as "avg_time_to_approve",
    approx_percentile_cont(value, 0.95) as "percentile_time_to_approve",
    count(value) as "num_approves"
FROM "vcs_change_time_to_approval"
GROUP BY vcs_repository_name, vcs_owner_name

-- Time PRs remain in open state (seconds)
SELECT 
    vcs_repository_name,
    vcs_owner_name,
    avg(value) as "avg_change_duration",
    approx_percentile_cont(value, 0.95) as "percentile_change_duration",
    count(value) as "num_changes"
FROM "vcs_change_duration"
GROUP BY vcs_repository_name, vcs_owner_name


-- Pull request counts by open state
SELECT 
    vcs_repository_name,
    vcs_owner_name,
    sum(value) as "num_open"
FROM "vcs_change_count"
WHERE vcs_change_state = 'open'
GROUP BY 
    vcs_repository_name,
    vcs_owner_name

-- Pull request counts by merged state
SELECT 
    vcs_repository_name,
    vcs_owner_name,
    sum(value) as "num_merged"
FROM "vcs_change_count"
WHERE vcs_change_state = 'merged'
GROUP BY 
    vcs_repository_name,
    vcs_owner_name

-- Branch/tag counts per repository
SELECT
    vcs_repository_name,
    vcs_owner_name,
sum(value) AS 'branch_count'
FROM vcs_ref_count
GROUP BY
    vcs_repository_name,
    vcs_owner_name

-- Branch lifespan from creation (seconds)
SELECT 
    vcs_repository_name,
    vcs_owner_name,
    avg(value) as "avg_branch_lifespan",
    approx_percentile_cont(value, 0.95) as "percentile_branch_lifespan",
    count(value) as "num_branch"
FROM "vcs_ref_time"
GROUP BY vcs_repository_name, vcs_owner_name

-- Code churn (lines added/removed) vs. trunk
SELECT 
avg(value) as 'avg_loc_churn',
approx_percentile_cont(value, 0.95) as "percentile_loc_churn",
count(value) / 2 as 'num_branch',
    vcs_repository_name,
    vcs_owner_name
FROM "vcs_ref_lines_delta"
GROUP BY
    vcs_repository_name,
    vcs_owner_name

-- Commit count ahead trunk
SELECT 
avg(value) as 'avg_commit_forward',
approx_percentile_cont(value, 0.95) as "percentile_commit_forward",
count(value) as 'num_branch',
    vcs_repository_name,
    vcs_owner_name
FROM "vcs_ref_revisions_delta"
WHERE vcs_revision_delta_direction = 'ahead'
GROUP BY
    vcs_repository_name,
    vcs_owner_name

-- Commit count behind trunk
SELECT 
avg(value) as 'avg_commit_behind',
approx_percentile_cont(value, 0.95) as "percentile_commit_behind",
count(value) as 'num_branch',
    vcs_repository_name,
    vcs_owner_name
FROM "vcs_ref_revisions_delta"
WHERE vcs_revision_delta_direction = 'behind'
GROUP BY
    vcs_repository_name,
    vcs_owner_name