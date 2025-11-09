## Purpose

This file gives an AI coding agent focused, actionable guidance for making safe, useful changes in this repository. Keep suggestions specific to the project's layout, naming, and run workflows.

## Big picture (architecture & data flow)

- Data lives under `data/` with raw datasets in `data/storage/raw/` and cleaned/derived outputs in `data/storage/processed/`.
- Ingestion and import scripts live in `scripts/` and often call repo-layer classes in `data/repo/` which in turn use low-level clients in `data/database/`.
  - Example chain: `scripts/Import_csv_to_mongo.py` -> `data/repo/MongoDbRepo.py` -> `data/database/MongoDbClient.py`.
- Notebooks for exploration and feature work are in `notebooks/` and `src/` (models, features, ingestion experiments). Treat notebooks as documentation and experiments — changes to core code should be reflected outside notebooks.

## Key files & directories to inspect when changing behavior

- Database clients: `data/database/MongoDbClient.py`, `data/database/Neo4jClient.py` (always update both repo wrappers and clients together).
- Repo abstraction: `data/repo/MongoDbRepo.py`, `data/repo/Neo4jRepo.py` (public methods like `insert_one`, `insert_many`, `find_many` are used across scripts).
- Ingestion scripts: `scripts/Import_csv_to_mongo.py` (shows how Last.fm files are parsed using `|` delimiter and mapped to fields).
- Raw datasets: `data/storage/raw/Last.fm Multigraph/` — use these paths exactly in scripts and notebooks.
- Logging initializer: `logs/init_logger.py` (project uses `logging.getLogger(__name__)` convention).

## Project-specific conventions and patterns

- Relative imports are used inside the `data` package (e.g. `from .. import MongoDbClient` in `data/repo/*`). Preserve this style when moving files.
- Logging: modules obtain loggers with `logger = logging.getLogger(__name__)`. Use that pattern instead of print statements.
- Error handling: DB code tends to wrap operations in try/except and log exceptions via `logger.exception(...)`. Follow the same approach.
- Type hints are present in many repo files (e.g. typing in `MongoDbRepo`). Keep and prefer type annotations where reasonable.

## Integration and run workflows (concrete examples)

- Import a Last.fm anonymized file into MongoDB (example):

  python scripts/Import_csv_to_mongo.py --uri mongodb://localhost --port 27017 --db mydb --input "data/storage/raw/Last.fm Multigraph/events/randomwalk-4_anonymized" --collection users

  Notes:
  - The import script expects `|` delimited rows of the form `user_id|relation_type|target_id` (see `scripts/Import_csv_to_mongo.py`).
  - On Windows PowerShell, use double quotes for paths with spaces.

- Typical dev iteration when editing DB code:
  1. Edit `data/database/*.py` or `data/repo/*.py`.
  2. Run a small import against a local Mongo (or a single-file test script) to validate behavior.
  3. Ensure logs show expected operations (the code relies on logger messages for progress reporting).

## Integration points & external dependencies

- MongoDB: code uses `pymongo` (`MongoDbClient`, `MongoDbRepo`). Caller scripts assume a running Mongo instance.
- Neo4j: graph functionality is encapsulated under `data/database/Neo4jClient.py` and `data/repo/Neo4jRepo.py`.
- Data science stack: notebooks and `src/` rely on numpy/pandas/networkx/scikit-learn/tensorflow. Confirm environment before running heavy notebooks.

## Discovered gotchas and conservative guidance

- Small inconsistencies found; prefer small, low-risk fixes and add tests or quick scripts to validate:
  - `MongoDbClient.close()` references `self.driver.close()` but the client stores `_driver` (prefer minimal fix and tests). See `data/database/MongoDbClient.py`.
  - Port types in constructors sometimes vary (int vs str). Keep existing parameter names and types consistent with callers.
- Avoid sweeping refactors across `data/` without running a few ingestion scripts and checking notebooks for breakages.

## What agents should do when editing code here

1. Read the chain of responsibility for the change (script -> repo -> client). Update all touched layers.
2. Preserve relative imports and logging style.
3. Add or update a tiny smoke script (or reuse `scripts/Import_csv_to_mongo.py`) to validate DB changes locally.
4. When in doubt, prefer non-breaking changes and ask the maintainer for credentials or environment details (Mongo/Neo4j endpoints).

## Where to look for more context

- Top-level `Readme.md` (project purpose and datasets).
- Notebooks under `notebooks/exploratory/` and `src/` for usage examples and expected data shapes.

If anything in these instructions is unclear or you want more examples (e.g., a small test harness or Docker commands to run Mongo locally), tell me which part you want expanded and I will iterate.
