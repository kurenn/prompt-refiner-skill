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
- **Payments & billing** — "users can pay" becomes processor choice, plan tiers, trials, failed payment handling, cancellation, refunds
- **Third-party integrations** — "connect to Stripe" becomes API key management, OAuth, webhooks, retry logic, sandbox vs. production
- **Multi-tenancy** — "each team has a workspace" becomes data scoping, org model, invitations, tenant switching
- **Email & messaging** — "send an email when X" becomes delivery service, templates, bounce handling, unsubscribe compliance
- **File uploads** — "upload a photo" becomes file type validation, size limits, storage strategy, image processing
- **Search & filtering** — "add a search bar" becomes scope, ranking, debounce, indexing, filter persistence
- **Roles & permissions** — "admin vs. regular user" becomes role definitions, authorization checks, UI differences
- And more (data entry, notifications, real-time features, settings, user-generated content)

## Key Features

- **Self-assessment loop** — Rates every spec on 6 dimensions (completeness, specificity, consistency, proportionality, translation quality, implementation coverage), catches gaps, and fixes them before presenting to the user
- **Input sophistication detection** — Calibrates expansion depth based on whether the input is non-technical, semi-technical, or technical
- **Compression mechanism** — "Would the user notice on day 1?" test prevents over-engineering, with spec length targets per complexity level
- **Builder Notes** — Distinguishes load-bearing requirements from polish, helping the AI builder prioritize
- **Colocation principle** — Validation, error handling, and edge cases live inline with implementation steps, not in separate sections the builder might skip
- **Feature request vs. greenfield detection** — Different approach for new apps vs. adding to existing codebases
- **Security woven in** — Input sanitization, auth boundaries, rate limiting, CSRF — integrated naturally, not as a scary separate section
- **Complete worked example** — Full invoicing app spec showing the exact output format with all sections

## Installation

### Claude Desktop (Cowork)

1. Download `prompt-refiner.skill` from the [Releases](../../releases) page
2. Open Claude Desktop
3. Drag the `.skill` file into a conversation, or place it in your skills directory

### Manual Installation

```bash
mkdir -p ~/.claude/skills/prompt-refiner && curl -sL https://raw.githubusercontent.com/kurenn/prompt-refiner-skill/main/SKILL.md -o ~/.claude/skills/prompt-refiner/SKILL.md
```

### Update

```bash
curl -sL https://raw.githubusercontent.com/kurenn/prompt-refiner-skill/main/SKILL.md -o ~/.claude/skills/prompt-refiner/SKILL.md
```

## Benchmarks

Tested across 10 diverse scenarios (greenfield, feature requests, multi-turn, over-engineering traps) using programmatic assertions and LLM-as-judge evaluations:

| Metric | Score |
|--------|-------|
| Assertion pass rate | **100%** (76/76) |
| Avg judge score | **4.25/5** |
| Composite score | **94.0%** |

Judges evaluate expansion quality (did it add meaningful depth?), actionability (are requirements in implementation steps?), and builder consumability (is the spec structured for an AI to follow?). The eval harness is in `evals/` — run it yourself with `python evals/run_evals.py`.

## Example

**User says:**
> "I want a simple invoicing app where I can create invoices for clients, mark them as paid, and see which ones are overdue."

**Prompt Refiner produces** a complete spec including:
- **Builder Notes** — load-bearing requirements (status lifecycle, line item math, overdue detection) vs. polish (PDF generation, dashboard charts)
- **3 data entities** (Client, Invoice with status lifecycle, LineItem with computed amounts)
- **User flows** with every step specified (create → add line items → send → mark paid → view overdue)
- **Implementation steps with colocated requirements** — validation, error handling, loading states, and confirmation dialogs appear as sub-steps within the feature that needs them, not in separate sections
- **Compression applied** — Future Considerations captures deferred items (email delivery, tax calculation, recurring invoices) instead of bloating the initial spec
- **Self-assessment** with 6 ratings and issues caught during self-review

## Contributing

Issues and PRs welcome. If you find a common phrase that the skill doesn't translate well, open an issue with the phrase and what you expected.

## License

MIT
