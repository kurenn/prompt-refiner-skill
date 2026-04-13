# Prompt Refiner Skill

A Claude skill that translates casual, non-technical application requests into detailed technical specifications that AI coding assistants can execute faithfully.

## What It Does

When a non-technical user says *"I want an app to track expenses"*, an AI assistant will build something — but it'll silently guess about authentication, data relationships, validation, error handling, responsive design, and dozens of other things. Most of those guesses will be wrong or incomplete.

**Prompt Refiner** bridges that gap. It takes what someone *wants*, described in their own words, and produces a structured, complete specification where nothing important is left to chance.

## Three Modes

| Mode | Best For | How It Works |
|------|----------|--------------|
| **One-Shot** | Clear requests that just need technical translation | Produces the full spec immediately, flags assumptions |
| **Interactive** | Vague or complex requests | Asks targeted questions in small batches, builds spec from answers |
| **Hybrid** | Most cases (recommended) | Produces a draft spec, asks follow-up questions, then finalizes |

## What Gets Translated

The skill expands casual language into complete technical specifications covering:

- **User authentication** — "users can sign up" becomes registration flow, verification, session management, password reset, validation rules
- **Data display** — "show a list" becomes pagination, search, sorting, empty states, loading states, responsive layout
- **UI patterns** — "I want the sidebar to hide and show" becomes collapsible sidebar with hamburger toggle, responsive breakpoints, animation, accessibility
- **File uploads** — "upload a photo" becomes file type validation, size limits, storage strategy, image processing, fallback avatars
- **Search & filtering** — "add a search bar" becomes scope, ranking, debounce, indexing, filter persistence
- **Roles & permissions** — "admin vs. regular user" becomes role definitions, authorization checks, UI differences
- **Real-time features** — "live updates" becomes WebSocket vs. polling, conflict resolution, connection loss handling
- And more (data entry, notifications, user-generated content)

## Key Features

- **Self-assessment loop** — Rates every spec on 5 dimensions (completeness, specificity, consistency, proportionality, translation quality), catches gaps, and fixes them before presenting to the user
- **Feature request vs. greenfield detection** — Different approach for new apps vs. adding to existing codebases
- **Security woven in** — Input sanitization, auth boundaries, rate limiting, CSRF — integrated naturally, not as a scary separate section
- **Revision handling** — Guidance for iterating on specs when the user wants changes
- **Worked examples** — Concrete before/after showing how casual requests expand into full specifications

## Installation

### Claude Desktop (Cowork)

1. Download `prompt-refiner.skill` from the [Releases](../../releases) page
2. Open Claude Desktop
3. Drag the `.skill` file into a conversation, or place it in your skills directory

### Manual Installation

Copy the `SKILL.md` file into your Claude skills directory:

```
~/.claude/skills/prompt-refiner/SKILL.md
```

## Benchmarks

Tested across 6 diverse scenarios (greenfield apps + feature requests):

| Metric | With Skill | Without Skill |
|--------|-----------|---------------|
| Assertion pass rate | **97.5%** | 54.4% |
| Mode compliance | 100% | ~33% |
| Structural completeness | 100% | ~50% |

The skill's biggest advantages are in mode compliance (baseline ignores interactive/hybrid instructions entirely) and structural completeness (assumptions sections, validation rules, empty/loading states, self-assessment).

## Example

**User says:**
> "I want a page where my team can submit expense reports and I can approve or reject them."

**Prompt Refiner produces** a spec covering:
- 3 data entities (User with roles, ExpenseReport with status lifecycle, LineItem with receipt attachment)
- 2 detailed user flows (submission + approval)
- Hidden requirements surfaced (rejected report resubmission, spending limits, partial approval, locking after submission)
- UI patterns named (confirmation dialogs for approve/reject, dynamic line item forms, drag-and-drop receipt upload)
- Validation rules, error handling, security considerations, accessibility
- Self-assessment with ratings and issues caught

## Contributing

Issues and PRs welcome. If you find a common phrase that the skill doesn't translate well, open an issue with the phrase and what you expected.

## License

MIT
