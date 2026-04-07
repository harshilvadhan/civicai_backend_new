-- ============================================================
-- CivicAI Database Schema
-- Run this in your Supabase SQL Editor (once)
-- ============================================================

-- 1. COMPLAINTS TABLE
create table if not exists complaints (
    id                  uuid primary key default gen_random_uuid(),
    ticket_id           text unique not null,
    raw_input           text not null,
    image_url           text,
    location            text not null,

    -- AI fields (filled by Person 3's engine, passed through by frontend)
    category            text not null check (category in ('Road','Garbage','Water','Electricity','Drainage','Park','Public Safety','Other')),
    urgency             text not null check (urgency in ('Low','Medium','High')),
    formal_complaint    text not null,
    department          text not null,
    reasoning           text not null,

    -- Status
    status              text not null default 'Pending'
                            check (status in ('Pending','Assigned','In Progress','Resolved')),

    created_at          timestamptz default now()
);

-- 2. STATUS UPDATES TABLE (powers citizen timeline)
create table if not exists status_updates (
    id              uuid primary key default gen_random_uuid(),
    complaint_id    uuid not null references complaints(id) on delete cascade,
    status          text not null,
    note            text default '',
    updated_at      timestamptz default now()
);

-- 3. INDEXES (speed up officer dashboard filters)
create index if not exists idx_complaints_urgency   on complaints(urgency);
create index if not exists idx_complaints_category  on complaints(category);
create index if not exists idx_complaints_status    on complaints(status);
create index if not exists idx_status_complaint_id  on status_updates(complaint_id);

-- 4. STORAGE BUCKET (run separately in Supabase dashboard > Storage)
-- Create a bucket named: complaint-images
-- Set it to PUBLIC so image URLs work without auth tokens
