-- Approved Numbers Store — Schema
--
-- This is the dynamic benchmark store used by the Validation Agent.
-- It stores analyst-verified, finance-approved result values for known metrics.
--
-- KEY DISTINCTION vs. Snowflake VQR / Databricks Trusted Answers:
--   VQR stores verified *queries* (static SQL templates).
--   This store stores verified *results* (actual numbers a human has signed off on).
--   A verified query can still produce the wrong answer if data changes.
--   A verified result is the ground truth the Validation Agent checks against.
--
-- Maintained by: Analytics team / Finance / Data Engineering
-- Updated: After each financial close, board presentation, or analyst sign-off.

CREATE TABLE approved_numbers (
    id                BIGSERIAL PRIMARY KEY,

    -- What metric and slice does this cover?
    metric_name       VARCHAR(255)   NOT NULL,   -- matches metrics.yaml name
    entity            VARCHAR(255)   NOT NULL,   -- e.g., 'global', 'north_america', 'product_a'
    granularity       VARCHAR(50)    NOT NULL,   -- 'daily', 'weekly', 'monthly', 'quarterly', 'annual'
    period            DATE           NOT NULL,   -- start date of the period

    -- The approved value
    approved_value    DECIMAL(22,4)  NOT NULL,
    currency          VARCHAR(10)    DEFAULT NULL,

    -- Tolerance: how far can a result deviate before the Validation Agent flags it?
    tolerance_pct     DECIMAL(5,2)   NOT NULL    DEFAULT 5.0,  -- 5% variance allowed by default

    -- Provenance: who approved this, when, and from what source?
    approved_by       VARCHAR(255)   NOT NULL,
    approval_date     TIMESTAMP      NOT NULL    DEFAULT NOW(),
    source            VARCHAR(100)   NOT NULL,   -- 'board_deck', 'finance_close', 'analyst_sign_off', 'audit'
    notes             TEXT           DEFAULT NULL,

    -- Soft delete: don't delete rows, just mark superseded
    is_active         BOOLEAN        NOT NULL    DEFAULT TRUE,
    superseded_at     TIMESTAMP      DEFAULT NULL,
    superseded_by     BIGINT         REFERENCES approved_numbers(id)
);

-- Index for fast lookup by metric + entity + period (the Validation Agent's primary query pattern)
CREATE INDEX idx_approved_numbers_lookup
    ON approved_numbers (metric_name, entity, granularity, period)
    WHERE is_active = TRUE;

-- Sample data for demo and testing
INSERT INTO approved_numbers
    (metric_name, entity, granularity, period, approved_value, tolerance_pct, approved_by, source)
VALUES
    ('revenue',   'global',        'monthly',   '2026-01-01', 12450000.00, 5.0,  'finance_close', 'finance_close'),
    ('revenue',   'global',        'monthly',   '2026-02-01', 11980000.00, 5.0,  'finance_close', 'finance_close'),
    ('revenue',   'north_america', 'quarterly', '2026-01-01', 34200000.00, 3.0,  'board_deck_q1', 'board_deck'),
    ('order_count','global',       'monthly',   '2026-01-01', 48320,       8.0,  'analytics_lead','analyst_sign_off'),
    ('churn_rate', 'global',       'monthly',   '2026-01-01', 0.023,       10.0, 'product_analytics', 'analyst_sign_off');
