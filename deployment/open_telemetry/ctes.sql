-- Comprehensive VCS Metrics View
-- All metrics joined by repository and owner
WITH
-- Duration from PR creation to merge (days)
time_to_merge AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        avg(value) / 86400.0 as avg_time_to_merge,
        approx_percentile_cont(value, 0.95) / 86400.0 as percentile_time_to_merge,
        count(value) as num_merges
    FROM vcs_change_time_to_merge
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Duration from PR creation to approval (days)
time_to_approval AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        avg(value) / 86400.0 as avg_time_to_approve,
        approx_percentile_cont(value, 0.95) / 86400.0 as percentile_time_to_approve,
        count(value) as num_approves
    FROM vcs_change_time_to_approval
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Time PRs remain in open state (days)
change_duration AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        avg(value) / 86400.0 as avg_change_duration,
        approx_percentile_cont(value, 0.95) / 86400.0 as percentile_change_duration,
        count(value) as num_changes
    FROM vcs_change_duration
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Pull request counts by state (open and merged)
pr_counts AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        sum(CASE WHEN vcs_change_state = 'open' THEN value ELSE 0 END) as num_open,
        sum(CASE WHEN vcs_change_state = 'merged' THEN value ELSE 0 END) as num_merged
    FROM vcs_change_count
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Branch/tag counts per repository
branch_counts AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        sum(value) AS branch_count
    FROM vcs_ref_count
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Branch lifespan from creation (days)
branch_lifespan AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        avg(value) / 86400.0 as avg_branch_lifespan,
        approx_percentile_cont(value, 0.95) / 86400.0 as percentile_branch_lifespan,
        count(value) as num_branch_lifespan
    FROM vcs_ref_time
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Code churn (lines added/removed) vs. trunk
code_churn AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        avg(value) as avg_loc_churn,
        approx_percentile_cont(value, 0.95) as percentile_loc_churn,
        count(value) / 2 as num_branch_churn
    FROM vcs_ref_lines_delta
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Commit count ahead trunk
commits_ahead AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        avg(value) as avg_commit_forward,
        approx_percentile_cont(value, 0.95) as percentile_commit_forward,
        count(value) as num_branch_ahead
    FROM vcs_ref_revisions_delta
    WHERE vcs_revision_delta_direction = 'ahead'
    GROUP BY vcs_repository_name, vcs_owner_name
),

-- Commit count behind trunk
commits_behind AS (
    SELECT
        vcs_repository_name,
        vcs_owner_name,
        avg(value) as avg_commit_behind,
        approx_percentile_cont(value, 0.95) as percentile_commit_behind,
        count(value) as num_branch_behind
    FROM vcs_ref_revisions_delta
    WHERE vcs_revision_delta_direction = 'behind'
    GROUP BY vcs_repository_name, vcs_owner_name
)

-- Final unified view joining all metrics
SELECT
    COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name, cd.vcs_repository_name,
             pc.vcs_repository_name, bc.vcs_repository_name, bl.vcs_repository_name,
             cc.vcs_repository_name, ca.vcs_repository_name, cb.vcs_repository_name) as vcs_repository_name,
    COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name, cd.vcs_owner_name,
             pc.vcs_owner_name, bc.vcs_owner_name, bl.vcs_owner_name,
             cc.vcs_owner_name, ca.vcs_owner_name, cb.vcs_owner_name) as vcs_owner_name,

    -- PR merge metrics
    ttm.avg_time_to_merge,
    ttm.percentile_time_to_merge,
    ttm.num_merges,

    -- PR approval metrics
    tta.avg_time_to_approve,
    tta.percentile_time_to_approve,
    tta.num_approves,

    -- PR duration metrics
    cd.avg_change_duration,
    cd.percentile_change_duration,
    cd.num_changes,

    -- PR counts
    pc.num_open,
    pc.num_merged,

    -- Branch metrics
    bc.branch_count,
    bl.avg_branch_lifespan,
    bl.percentile_branch_lifespan,
    bl.num_branch_lifespan,

    -- Code churn metrics
    cc.avg_loc_churn,
    cc.percentile_loc_churn,
    cc.num_branch_churn,

    -- Commit delta metrics
    ca.avg_commit_forward,
    ca.percentile_commit_forward,
    ca.num_branch_ahead,
    cb.avg_commit_behind,
    cb.percentile_commit_behind,
    cb.num_branch_behind

FROM time_to_merge ttm
FULL OUTER JOIN time_to_approval tta
    ON ttm.vcs_repository_name = tta.vcs_repository_name
    AND ttm.vcs_owner_name = tta.vcs_owner_name
FULL OUTER JOIN change_duration cd
    ON COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name) = cd.vcs_repository_name
    AND COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name) = cd.vcs_owner_name
FULL OUTER JOIN pr_counts pc
    ON COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name, cd.vcs_repository_name) = pc.vcs_repository_name
    AND COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name, cd.vcs_owner_name) = pc.vcs_owner_name
FULL OUTER JOIN branch_counts bc
    ON COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name, cd.vcs_repository_name, pc.vcs_repository_name) = bc.vcs_repository_name
    AND COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name, cd.vcs_owner_name, pc.vcs_owner_name) = bc.vcs_owner_name
FULL OUTER JOIN branch_lifespan bl
    ON COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name, cd.vcs_repository_name, pc.vcs_repository_name, bc.vcs_repository_name) = bl.vcs_repository_name
    AND COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name, cd.vcs_owner_name, pc.vcs_owner_name, bc.vcs_owner_name) = bl.vcs_owner_name
FULL OUTER JOIN code_churn cc
    ON COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name, cd.vcs_repository_name, pc.vcs_repository_name, bc.vcs_repository_name, bl.vcs_repository_name) = cc.vcs_repository_name
    AND COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name, cd.vcs_owner_name, pc.vcs_owner_name, bc.vcs_owner_name, bl.vcs_owner_name) = cc.vcs_owner_name
FULL OUTER JOIN commits_ahead ca
    ON COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name, cd.vcs_repository_name, pc.vcs_repository_name, bc.vcs_repository_name, bl.vcs_repository_name, cc.vcs_repository_name) = ca.vcs_repository_name
    AND COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name, cd.vcs_owner_name, pc.vcs_owner_name, bc.vcs_owner_name, bl.vcs_owner_name, cc.vcs_owner_name) = ca.vcs_owner_name
FULL OUTER JOIN commits_behind cb
    ON COALESCE(ttm.vcs_repository_name, tta.vcs_repository_name, cd.vcs_repository_name, pc.vcs_repository_name, bc.vcs_repository_name, bl.vcs_repository_name, cc.vcs_repository_name, ca.vcs_repository_name) = cb.vcs_repository_name
    AND COALESCE(ttm.vcs_owner_name, tta.vcs_owner_name, cd.vcs_owner_name, pc.vcs_owner_name, bc.vcs_owner_name, bl.vcs_owner_name, cc.vcs_owner_name, ca.vcs_owner_name) = cb.vcs_owner_name

ORDER BY vcs_owner_name, vcs_repository_name;