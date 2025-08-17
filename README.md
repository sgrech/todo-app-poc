# Todo App Proof of Concept: Quality Gates vs No Quality Gates

This repository contains a controlled experiment to measure the effectiveness of quality gates in AI-assisted development.

## Overview

This proof of concept tests the hypothesis that using quality gates from the start of AI-assisted development results in:
1. **Lower total token usage**
2. **More maintainable code**
3. **Easier feature expansion**
4. **Reduced debugging cycles**

## Experiment Design

### Phase 1: Basic Todo CRUD
Two parallel implementations of the same functionality:
- **Track A**: No quality gates (`prompt1_basic_no_gates.md`)
- **Track B**: Quality gates from start (`prompt2_basic_with_gates.md`)

Both implementations must pass identical integration tests (`test_integration_phase1.py`).

### Phase 2: Multi-User Feature Addition
Both Track A and Track B implementations receive the same expansion requirements (`prompt3_multiuser.md`) to add multi-user functionality.

### Phase 3: Remediation Analysis
For Track A (no quality gates), measure the cost of applying quality gates retroactively:
- Run quality gate tools on the Track A codebase
- Count violations and measure token cost to fix them
- Compare total cost (Track A + remediation) vs Track B

## Quality Gates Used

- **Ruff**: Linting and code formatting
- **Pyright**: Static type checking
- **Vulture**: Dead code detection
- **Pytest**: Testing and coverage

## Measurement

Token usage tracked via OpenTelemetry integration with Claude Code:
- Implementation tokens per phase
- Debugging/correction cycles
- Total tokens by approach

## File Structure

```
todo-app-poc/
├── prompts/
│   ├── prompt1_basic_no_gates.md      # Track A: No quality gates
│   ├── prompt2_basic_with_gates.md    # Track B: Quality gates from start
│   └── prompt3_multiuser.md           # Phase 2: Multi-user expansion
├── tests/
│   ├── test_integration_phase1.py     # Phase 1 test specification
│   └── test_integration_phase2.py     # Phase 2 test specification
├── track_a_no_gates/                  # Track A implementation
├── track_b_with_gates/                # Track B implementation
└── analysis/                          # Token usage analysis and results
```

## Integration Tests

The integration tests serve as the specification for both tracks:

### Phase 1 Functions
- `init_db(db_path: str) -> None`
- `create_todo(title: str, description: str, db_path: str) -> int`
- `get_todo(todo_id: int, db_path: str) -> dict | None`
- `update_todo(todo_id: int, db_path: str, **kwargs) -> bool`
- `delete_todo(todo_id: int, db_path: str) -> bool`
- `list_todos(db_path: str, completed: bool = None) -> list[dict]`

### Phase 2 Additions
- `create_user(username: str, email: str, db_path: str) -> int`
- `get_user(user_id: int, db_path: str) -> dict | None`
- `get_user_by_username(username: str, db_path: str) -> dict | None`
- `create_user_todo(user_id: int, title: str, description: str, db_path: str) -> int`
- `get_user_todo(user_id: int, todo_id: int, db_path: str) -> dict | None`
- `update_user_todo(user_id: int, todo_id: int, db_path: str, **kwargs) -> bool`
- `delete_user_todo(user_id: int, todo_id: int, db_path: str) -> bool`
- `list_user_todos(user_id: int, db_path: str, completed: bool = None) -> list[dict]`

## Expected Outcomes

Based on the analysis in the Quality Gates blog series, we expect:

1. **Track B (with quality gates)** will show:
   - More iterations per function initially
   - Fewer correction cycles overall
   - Cleaner architecture for Phase 2 expansion
   - Lower total token usage across all phases

2. **Track A (no quality gates)** will show:
   - Faster initial implementation
   - More correction cycles during debugging
   - Expensive remediation in Phase 3
   - Higher total token usage when including remediation

3. **Phase 3 remediation** will demonstrate:
   - High token cost to fix quality issues retroactively
   - Complex correction spirals due to interconnected problems
   - Validation that prevention is cheaper than cure

## Running the Experiment

1. **Implement Track A**: Use `prompt1_basic_no_gates.md` with Claude Code
   - Initialize: `uv init --python 3.10 && uv add sqlalchemy alembic pytest`
2. **Implement Track B**: Use `prompt2_basic_with_gates.md` with Claude Code  
   - Initialize: `uv init --python 3.10 && uv add sqlalchemy alembic && uv add --dev pytest ruff pyright vulture`
3. **Expand both tracks**: Use `prompt3_multiuser.md` for Phase 2
4. **Analyze Track A**: Run quality gates and measure remediation cost
5. **Compare results**: Total token usage and code quality metrics

## Technology Stack

- **Language**: Python 3.10+
- **Package Manager**: uv (for dependency management and script execution)
- **Database**: SQLite with SQLAlchemy ORM
- **Migrations**: Alembic
- **Testing**: Pytest
- **Quality Gates**: Ruff, Pyright, Vulture
- **Measurement**: OpenTelemetry with Claude Code

## Success Criteria

This experiment succeeds if it provides concrete data supporting or refuting the hypothesis that quality gates reduce total development costs in AI-assisted projects.

The results will inform best practices for AI-assisted development and validate the economic arguments made in the Quality Gates blog series.
