---
description: Strict protocol for developing, validating, and documenting Skills. ENFORCES documentation updates before task completion.
---

# Skill Development & Documentation Protocol

**Goal**: Ensure that **Historical Experience** and **Proven Patterns** are immediately captured in `SKILL.md` after any successful verification.

**Trigger**: When creating a new Skill or adding platform support to an existing Skill.

## Protocol Steps

1.  **Develop & Verify**
    - Create/Update scripts in `scripts/`.
    - Run the scripts to verify functionality (Success/Fail).
    - **CRITICAL**: Note any errors encountered (e.g., missing metadata, login timeouts).

2.  **Refactor Documentation (MANDATORY)**
    - **BEFORE** notifying the user of success:
    - Edit `SKILL.md`.
    - Update "Rocket Start" / "Usage" sections with new commands.
    - **Add/Update a "Historical Experience" section**.
    - Explicitly document the "Why" behind the code (e.g., "Why do we use `ensure_metadata`? Because of crashing.").

3.  **Sync**
    - Copy the `skills/<name>` folder to `.claude/skills/<name>`.

4.  **Notify**
    - Only AFTER Step 2 & 3 are complete, report success to the user.
    - Explicitly mention *what* documentation was updated to reflect the new learnings.

## // turbo-all
