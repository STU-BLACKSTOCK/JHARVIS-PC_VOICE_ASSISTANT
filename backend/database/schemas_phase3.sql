-- 4. Create Workflows Table
create table workflows (
  id bigint primary key generated always as identity,
  name text not null,
  steps jsonb not null,
  created_at timestamp with time zone default now()
);

-- 5. Create System Logs Table
create table system_logs (
  id bigint primary key generated always as identity,
  cpu_percent float,
  ram_percent float,
  logged_at timestamp with time zone default now()
);
