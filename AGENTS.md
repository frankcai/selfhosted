# Repository Guidelines

Welcome to the **selfhosted** automation repository. This file defines guardrails for any work carried out inside this project. Please read it before touching files.

## General expectations
- Prioritise maintainability: keep solutions small, focused, and easy to reason about.
- Apply SOLID principles when adding or refactoring code; favour clear separation of concerns and dependency inversion.
- When you change behaviour or add new features, provide accompanying automated checks (e.g., Molecule scenarios, Ansible syntax checks, or unit tests for Python utilities) whenever feasible.
- Before committing changes run the same automation the CI uses: `ansible-lint`, `ansible-playbook --syntax-check site.yml`, and `python -m pytest`. Remember to create a temporary `vault_pass.txt` (ignored by git) so the commands succeed locally.
- Never commit real secrets or environment-specific credentials. Use sample/default files and document overrides instead.
- Follow existing naming patterns for files, variables, and Ansible roles. If you must diverge, explain why in code comments or commit messages.
- Keep service and role definitions uniform. Inline container configuration (image, name, ports, volumes) inside the service task unless there is a repo-wide pattern to factor it out. Mirroring the surrounding conventions keeps playbooks predictable.
- Prefer declarative, module-driven automation over per-role custom logic. Create shared includes or modules rather than sprinkling ad-hoc shell or templating snippets throughout the codebase.

## Ansible and YAML
- Use two-space indentation in YAML and keep keys alphabetically ordered when the order has no semantic meaning.
- Prefer Ansible modules over raw shell commands. When shell usage is unavoidable, set `creates`, `removes`, or `changed_when` to keep runs idempotent.
- Always validate playbooks and roles with `ansible-playbook --syntax-check` or Molecule before committing, when applicable.
- Place reusable logic inside roles. Reserve playbooks for orchestration and variable wiring.
- Organise `tasks/`, `handlers/`, and `services/` files consistently across roles so contributors can copy and adapt patterns without guesswork.
- Keep handler names consistent (`restart <service>`). If a handler becomes unused, delete it in the same change to avoid drift.

## Python utilities
- Format Python files with an autoformatter compatible with Black's defaults (88 character line length) and run `python -m compileall` or the relevant test suite if modified.
- Avoid introducing hard-coded paths. Derive locations relative to the project root or use environment variables with sensible defaults.
- Provide docstrings for new public functions or classes and include type hints for new code.
- Keep CLI entry points and helper modules cohesive: one module per concern, small functions, and dependency-inverted boundaries so utilities remain testable.

## Documentation
- Update `README.md` or role-specific docs when behaviour changes or new configuration options are introduced.
- Prefer Markdown tables or bullet lists for enumerating configuration options, ports, or services.
- When introducing new conventions, document them here so future contributors keep the repo uniform.

By following these conventions we keep the infrastructure code predictable and safe to operate.
