# Architecture Decisions

## Bronze
Purpose: durable representation of source data.

Allowed:
- source metadata
- ingestion metadata
- minimal technical parsing

Avoid:
- business calculations
- destructive deduplication
- dimensional modeling

## Silver
Purpose: trusted, conformed domain data.

Responsibilities:
- typing
- validation
- deduplication
- CDC
- standardization
- referential integrity
- canonical entities

## Gold
Purpose: consumption-specific business models.

Responsibilities:
- dimensional models
- aggregates
- KPIs
- customer 360
- reporting marts

## Core principle
Bronze optimizes for recoverability.
Silver optimizes for correctness and reuse.
Gold optimizes for consumption and business meaning.
