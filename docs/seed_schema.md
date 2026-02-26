# Seed File Schema

This project uses a harmonized seed schema for both carbon taxes and emissions trading systems.
The schema is enforced as:

- **Core columns**: strict (missing core columns raise errors).
- **Optional columns**: soft (missing columns produce warnings).

All seed CSVs are also backfilled so that missing columns exist (empty values).

## Core Schema

**acts**
- `act_id`
- `jurisdiction`
- `instrument_name`
- `instrument_type`
- `citation`
- `adoption_date`
- `publication_date`
- `entry_into_force`
- `source_url`
- `source_id`

**provisions**
- `provision_id`
- `act_id`
- `provision_ref`
- `chapter_ref`
- `title`
- `change_type`
- `change_note`

**rates**
- `rate_id`
- `provision_id`
- `pollutant`
- `rate_value`
- `rate_unit`
- `effective_from`
- `effective_to`
- `rate_basis`
- `method`
- `notes`
- `rate_value_tco2e`
- `rate_unit_tco2e`
- `tco2e_method`
- `tco2e_notes`

**coverage**
- `coverage_id`
- `provision_id`
- `scope_type`
- `scope_subject`
- `description_text`
- `start_date`
- `end_date`
- `notes`

**exemptions**
- `exemption_id`
- `provision_id`
- `exemption_type`
- `description_text`
- `details`
- `start_date`
- `end_date`
- `notes`

## Backfill Script

Use the backfill script to add missing core columns across all seed files:

```bash
python3 -m _code._preprocessing.backfill_seed_schema
```

This preserves existing extra columns by appending them after the core columns.
