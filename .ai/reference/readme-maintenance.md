# README Maintenance

**README.md MUST be reviewed and, when affected, updated in the same commit as any change to this repository.** This is the closing step of every task: do it when the in-progress work is finished, before marking the task DONE, moving its progress file to `.ai/completed/`, or sending the final reply. Never leave the update as a follow-up task for the user.

## What Triggers a README Update

| Change Type | Examples |
|-------------|---------|
| Adding/removing files in `.ai/` | New skill, pattern, checklist, template |
| Adding/removing any tracked file | New root-level file, new script, new sample |
| Renaming or moving files | Skill renamed, directory restructured, prompts moved into `.ai/` |
| Adding/removing directories | New top-level folder, new subdirectory |
| Changing the directory layout | Moving templates, reorganizing skills, new junctions |
| Changing scripts or automation | `sync-platforms.py`, `hygiene-lint.py`, hooks, workflows, commands |
| Changing behaviour or setup | New prerequisite, changed default, changed CLI usage |

## Required Actions

1. Update the **File Structure** section of `README.md` to reflect the new layout
2. Update any affected **Skills**, **Pattern Guides**, or **Work-Type Context Mapping** tables
3. Update any affected **Quick Start** or **Customization** instructions
4. Update path references in **Usage Examples** if directories moved
5. Describe changed scripts, commands, junctions or prerequisites wherever the README documents them

Do NOT end a session that included changes without confirming `README.md` reflects the current state. If the change genuinely touches nothing the README describes, say so explicitly in the final reply — a reviewed README is the requirement, not a silent skip.
