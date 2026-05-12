# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-05-12

### Released
- Published **analytics-semantic-layer-publisher** as the semantic publishing artifact in the marketing and analytics cluster.
- Packaged metric definitions, ownership, formula logic, JSON-LD publishing, and catalog views into one public repo.
- Positioned the project around metric explainability for both humans and AI systems.

### Why this mattered
- Many organizations have semantic definitions, but they remain trapped inside BI tooling or dbt project files.
- AI systems and even internal stakeholders often ask the same question: what does this metric actually mean here?
- This release made the repo useful to analytics engineering, BI, and AEO-minded teams.

## [0.1.0] - 2026-02-03

### Shipped
- Locked the first internal pipeline for reading semantic definitions and publishing them as structured artifacts.
- Added the first catalog views that made measures, owners, and formulas easier to inspect.

## [Prototype] - 2025-05-18

### Built
- Built the earliest prototype around exporting metric definitions into machine-readable and human-readable forms.
- Tested whether structured publication could reduce ambiguity around shared business measures.

## [Design Phase] - 2024-02-07

### Designed
- Chose a semantic publishing framing instead of another internal metrics UI.
- Treated measure definition and ownership as public interfaces, not hidden model details.
- Kept the design aligned with both BI consumers and answer-engine use cases.

## [Idea Origin] - 2023-03-25

### Observed
- The idea came from a common analytics problem: teams reuse the same metric names while meaning slightly different things.
- The missing artifact was a way to publish a semantic layer so definitions could travel with the metric.