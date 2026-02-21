PRAGMA foreign_keys = ON;

-- Core legal objects
CREATE TABLE IF NOT EXISTS acts (
  act_id            INTEGER PRIMARY KEY,
  jurisdiction      TEXT NOT NULL,
  instrument_name   TEXT NOT NULL,
  instrument_type   TEXT NOT NULL,   -- Act / Regulation / Decree / Directive / etc.
  citation          TEXT,            -- official citation string
  adoption_date     TEXT,            -- YYYY-MM-DD (nullable)
  publication_date  TEXT,            -- YYYY-MM-DD (nullable)
  entry_into_force  TEXT,            -- YYYY-MM-DD (nullable)
  source_url        TEXT             -- canonical link
);

CREATE TABLE IF NOT EXISTS provisions (
  provision_id      INTEGER PRIMARY KEY,
  act_id            INTEGER NOT NULL,
  provision_ref     TEXT NOT NULL,   -- e.g., "§19" or "Article 5"
  chapter_ref       TEXT,            -- optional
  title             TEXT,            -- optional
  change_type       TEXT,            -- inserted/replaced/repealed/renumbered/unknown
  change_note       TEXT,            -- free text
  FOREIGN KEY (act_id) REFERENCES acts(act_id)
);

-- Numeric parameters and schedule
CREATE TABLE IF NOT EXISTS rates (
  rate_id           INTEGER PRIMARY KEY,
  provision_id      INTEGER NOT NULL,
  pollutant         TEXT NOT NULL,   -- CO2, CO2e, etc.
  rate_value        REAL NOT NULL,
  rate_unit         TEXT NOT NULL,   -- e.g., "EUR/tCO2"
  effective_from    TEXT NOT NULL,   -- YYYY-MM-DD
  effective_to      TEXT,            -- YYYY-MM-DD (nullable; open-ended)
  rate_basis        TEXT,            -- e.g., "air pollution charge"
  method            TEXT,            -- statutory table / formula / etc.
  notes             TEXT,
  FOREIGN KEY (provision_id) REFERENCES provisions(provision_id)
);

-- Coverage / liable entities
CREATE TABLE IF NOT EXISTS coverage_rules (
  coverage_id       INTEGER PRIMARY KEY,
  provision_id      INTEGER NOT NULL,
  scope_type        TEXT NOT NULL,   -- sector/facility/activity
  scope_subject     TEXT NOT NULL,   -- e.g., "district heating"
  condition_text    TEXT,            -- verbatim / paraphrase
  effective_from    TEXT,
  effective_to      TEXT,
  notes             TEXT,
  FOREIGN KEY (provision_id) REFERENCES provisions(provision_id)
);

-- Exemptions / reliefs / rebates
CREATE TABLE IF NOT EXISTS exemptions (
  exemption_id      INTEGER PRIMARY KEY,
  provision_id      INTEGER NOT NULL,
  exemption_type    TEXT NOT NULL,   -- exemption/reduction/refund/credit/substitution
  description_text  TEXT NOT NULL,   -- verbatim / paraphrase
  condition_text    TEXT,
  effective_from    TEXT,
  effective_to      TEXT,
  notes             TEXT,
  FOREIGN KEY (provision_id) REFERENCES provisions(provision_id)
);

-- Convenience view: current rates by jurisdiction/pollutant
CREATE VIEW IF NOT EXISTS v_current_rates AS
SELECT
  a.jurisdiction,
  r.pollutant,
  r.rate_value,
  r.rate_unit,
  r.effective_from,
  r.effective_to,
  a.instrument_name,
  a.citation,
  a.source_url
FROM rates r
JOIN provisions p ON p.provision_id = r.provision_id
JOIN acts a ON a.act_id = p.act_id
WHERE r.effective_to IS NULL OR r.effective_to >= date('now');