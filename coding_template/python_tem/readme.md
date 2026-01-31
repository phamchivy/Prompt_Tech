# Knowledge Graph Pipeline Service

Processes markdown knowledge files and populates Neo4j graph database.

## Quick Start

1. **Setup environment**:
```bash
cp .env.example .env
# Edit .env with your Neo4j credentials
```

2. **Add knowledge files**:
Place markdown files in `data/knowledge/` following the template in `schemas/markdown_template.md`

3. **Validate markdown** (dry run):
```bash
python scripts/validate_markdown.py
```

4. **Run pipeline**:
```bash
python scripts/run_pipeline.py
```

## Scalability

### Adding New Entity Types
Edit `schemas/entity_types.yaml`:
```yaml
NewEntityType:
  required_properties: [prop1, prop2]
  optional_properties: [prop3]
  property_types:
    prop1: string
  constraints:
    prop1:
      allowed_values: [value1, value2]
```

### Adding New Relation Types
Edit `schemas/relation_types.yaml`:
```yaml
NEW_RELATION:
  valid_pairs:
    - [EntityA, EntityB]
  required_properties: []
```

### Adding Knowledge
Drop markdown files into `data/knowledge/<category>/` → Run pipeline

## Directory Structure
```
├── config/          # Service configuration
├── data/            # Knowledge files (user-editable)
├── schemas/         # Schema definitions (user-editable)
├── src/             # Application logic
├── scripts/         # Pipeline executables
└── tests/           # Test suite
```