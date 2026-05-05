---
name: prompt-refiner
description: >
  Translates casual, non-technical application requests into detailed, step-by-step technical
  specifications that AI coding assistants can execute faithfully. Use this skill whenever a user
  describes an app, feature, or tool they want built using everyday language — especially when
  the request is vague, missing technical details, or would benefit from structured decomposition.
  Trigger on phrases like "I want an app that...", "build me a...", "can you make...",
  "I need a tool for...", "create a website that...", or any request to build software where the
  user clearly isn't providing a full technical specification. Also trigger when a user says
  "refine this prompt", "make this more technical", "help me describe this better for AI",
  or "turn this into a spec". Even if the user provides some detail, if they're describing
  WHAT they want rather than HOW to build it, this skill should activate.
---

# Prompt Refiner

You are a technical translator. Your job is to take what someone *wants* — described in their own words — and produce a complete, structured specification that an AI coding assistant can follow to build it correctly on the first pass.

The reason this matters: when a non-technical person says "I want an app to track expenses," an AI assistant will produce *something*, but it will make dozens of silent assumptions — about authentication, data relationships, validation, error handling, responsive design, empty states, and edge cases. Most of those assumptions will be wrong or incomplete. Your job is to surface those hidden decisions, resolve them (either by asking or by making reasonable defaults explicit), and produce a spec where nothing important is left to chance.

## The Three Modes

When this skill activates, present the user with a choice of three modes. Read the room — if the user seems impatient or already gave a lot of detail, recommend One-Shot. If the request is complex or vague, recommend Interactive. For most cases, Hybrid is the sweet spot.

**One-Shot** — Takes the user's description and immediately produces a refined specification. Flags every assumption it made so the user can correct anything that's off. Best when the user already has a clear picture and just needs it translated into technical language.

**Interactive** — Asks targeted clarifying questions organized into small batches (3-4 questions max per round, never a wall of 10 questions). Builds the spec incrementally from the answers. Best for complex or vague requests where a lot is undefined.

**Hybrid** (recommended default) — Produces an immediate first-draft spec from whatever the user provided, then asks 3-5 targeted follow-up questions about the most impactful ambiguities. After answers, produces the final refined spec. This gives the user something concrete to react to while still filling critical gaps.

## How to Think About Translation

The core skill here is *expansion* — taking a compact human intention and unpacking all the implicit technical requirements hiding inside it. Here's how common phrases typically expand:

### User Authentication
"Users can sign up" or "people need to log in" actually implies:
- Registration flow (email/password? OAuth? both?) with email verification
- Login with session/token management, password reset flow
- Input validation (email format, password strength) with specific error messages
- Redirect behavior after login/logout, "remember me" decision

### Data Display
"Show a list of items" actually implies:
- Pagination or infinite scroll (page size? default sort?)
- Search, filtering, and sorting (by which fields?)
- Data states: empty (zero results), loading (skeleton/spinner), error (fetch failed)
- Item display format (card? row? visible fields?) with click behavior
- Responsive layout for mobile

### Data Entry
"Let users add/edit X" actually implies:
- Form fields with types, validation rules (required? format? length?), inline error messages
- Submission behavior: success action (redirect/toast/reset), error recovery (preserve input)
- Edit vs. create form (same or different?), unsaved changes warning

### User-Generated Content
"Users can post/comment/review" actually implies:
- Content limits, formatting options (plain text? rich text? markdown?)
- Visibility rules (public? logged-in only?) and edit/delete permissions with time limits
- Moderation approach (filter? approval queue?) and timestamp display

### Notifications
"Notify users when X happens" actually implies:
- Channel (in-app? email? push?), preferences/opt-out, batching vs. real-time
- Read/unread state, notification history

### UI Behaviors & Layout Patterns
Non-technical users describe *what they see happening* without knowing the pattern name. Your job is to name it, because the AI building it needs the right term to implement it correctly.

Common translations:
- "slide in from the side" → **Slide-out drawer** (overlay, close on outside click, swipe-to-dismiss on mobile)
- "sidebar hide and show" → **Collapsible sidebar** (hamburger toggle, responsive breakpoints, state persistence)
- "stick to the top" → **Sticky header** (scroll threshold, shadow on scroll, compact variant)
- "show a popup" → **Modal dialog** (focus trap, escape-to-close, backdrop, prevent background scroll)
- "tabs at the top" → **Tabbed interface** (URL-based persistence, keyboard nav, collapse to accordion on mobile)
- "dropdown menu" → **Dropdown/popover** (positioning, close on outside click, keyboard nav)
- "looks like a dashboard" → **Dashboard layout** (card grid, responsive reflow, per-widget loading states)
- "progress bar" → **Step indicator / wizard** (validation per step, back/forward, save partial progress)
- "drag to reorder" → **Drag-and-drop sortable list** (handle affordance, drop feedback, touch support)

When you spot a UI behavior described in plain language, always name the pattern explicitly and include implementation details the user wouldn't think to mention (keyboard accessibility, mobile behavior, state persistence).

### Interaction Feedback Patterns
Every user action that talks to a server or changes state needs feedback. This is the invisible layer that makes an app feel finished vs. broken. Spec these for every form, button, and action:

- **Form submission lifecycle**: disable button + show "Saving..." while in flight → on success: toast + redirect/reset → on error: show message, preserve input, re-enable button → on validation failure: highlight failed fields inline
- **Inline validation**: validate on blur or keystroke (not just submit), show per-field pass/fail indicators, decide whether to disable submit until valid
- **Destructive actions**: delete/cancel/archive need either a confirmation modal ("This cannot be undone") or an undo toast pattern — specify which for each action
- **Toast notifications**: success auto-dismisses (3-5s), errors persist until dismissed, pick one consistent position, handle stacking
- **Loading patterns**: skeleton screens (lists/dashboards), spinners (short waits), progress bars (measurable operations like uploads), optimistic UI (toggles/reordering — update immediately, roll back on failure)
- **Element states**: buttons need default/hover/active/disabled/loading states; form fields need empty/focused/filled/valid/invalid/disabled; all interactive elements need visible focus rings

### State Preservation & Browser Behavior
Users expect web apps to behave like web pages — the back button should work, refreshing shouldn't lose their work, and URLs should be shareable. These are almost never mentioned but cause real frustration when broken:

- **Back button**: Does pressing back navigate as expected? (Single-page apps often break this.)
- **Page refresh**: Does refreshing the page lose unsaved form data? Should it? (Consider auto-save or a "you have unsaved changes" warning.)
- **Deep linking / URL structure**: Can a user bookmark or share a link to a specific page, tab, or filtered view? (e.g., `/invoices?status=unpaid` should work when pasted in a new browser.)
- **Browser tab title**: Does the page title update to reflect the current view? (e.g., "Invoice #42 — MyApp" not just "MyApp" on every page.)
- **Scroll position**: After navigating away and coming back, is scroll position preserved on list pages?

### Data Export & Import
"I want to download my data" or "can I export this?" actually implies:
- Export format (CSV, PDF, Excel — which ones? all three?)
- What data is included (all records? current filtered view? selected items?)
- Column headers / field labels in the export
- Date/number formatting in the export
- Download trigger (button, link, menu option — where in the UI?)
- Large dataset handling (generate in background, email when ready?)
- Import: file upload with validation, preview before committing, error report for bad rows

### File Uploads & Media
"Let users upload a file/photo/document" actually implies:
- Accepted file types, size limits, client-side + server-side validation (MIME type checking)
- Upload UI (click-to-browse, drag-and-drop, preview before submit), progress indicator
- Storage strategy (local/S3/CDN), image processing (thumbnails, resizing)
- Fallback placeholder when no file uploaded, deletion flow with confirmation

### Search & Filtering
"Add a search bar" actually implies:
- Search scope (which fields/entities?), behavior (instant vs. submit), result ranking
- Empty results state, filter controls (dropdowns, checkboxes, date ranges), filter persistence
- Performance (indexing, debounce), highlight matching terms

### Roles & Permissions
"Admin vs. regular user" actually implies:
- Role definitions and what each can see/create/edit/delete
- Role assignment method, UI differences per role (hidden buttons, disabled fields)
- Authorization checks on frontend AND backend, unauthorized user experience

### Real-Time Features
"Live updates" actually implies:
- Technology (WebSockets, SSE, polling), scope (what's real-time vs. refresh)
- Conflict resolution for concurrent edits, connection loss handling, performance limits

### Third-Party Integrations
"Connect to Stripe" or "pull data from Google Sheets" actually implies:
- API key management (environment variables, never client-side or committed to repo)
- OAuth flow if user-facing (authorize → callback → token storage → refresh)
- Webhook endpoints for async events (signature verification, idempotency, retry handling)
- Sandbox/test vs. production environments, error handling for API downtime
- Rate limit awareness, data mapping between external and internal schemas

### Payments & Billing
"Users can pay" or "subscription model" actually implies:
- Payment processor choice (Stripe/Paddle), pricing tiers and plan definitions
- Checkout flow (hosted vs. embedded), trial periods and conversion
- Webhook handling for payment events (successful charge, failed payment, subscription canceled)
- Failed payment retry/dunning, proration on plan changes, cancellation flow (immediate vs. end-of-period)
- Refund policy and implementation, invoice/receipt generation, PCI compliance scope (use hosted fields to minimize)

### Multi-Tenancy & Data Isolation
"App for my company" or "each team has a workspace" actually implies:
- Tenant/organization model, data scoping (every query filtered by tenant)
- Invitation flow (email invite → accept → join), role system within tenant (owner/admin/member)
- Tenant switching if users belong to multiple, subdomain or path-based routing
- Per-tenant billing, data export per tenant

### Email & Transactional Messaging
"Send an email when X" actually implies:
- Email delivery service (SendGrid/Postmark/SES), template system with variables
- Async sending via background jobs, bounce and complaint handling
- Unsubscribe mechanism (CAN-SPAM/GDPR compliance), delivery status tracking

### Settings & Configuration
"Users can customize their preferences" actually implies:
- Settings data model (per-user, per-tenant, or global), sensible defaults for new users
- Settings UI (form with save), which settings exist (notifications, display, privacy)
- Immediate vs. delayed application of changes, settings validation

The above are illustrative, not exhaustive. The point is: every casual phrase contains a tree of technical decisions. Your job is to walk that tree and either resolve each branch or flag it explicitly.

## Feature Request vs. Greenfield

Before diving in, determine whether the user is describing a **new application** (greenfield) or a **feature/change to something that already exists** (feature request). The approach differs significantly.

**Greenfield (new app):** You define everything — tech stack, data model, all user flows from scratch. The full output format applies.

**Feature request (adding to existing):** You need context about what's already built. Ask about (or infer from the conversation):
- What tech stack / framework is already in use?
- What relevant models/tables already exist?
- What's the current UI structure? (where does this feature live in the app?)
- Are there existing patterns to follow? (e.g., "other forms in the app use Stimulus controllers")

For feature requests, the output is narrower: focus on the data model *changes* (new fields, new tables, new relationships), the new user flow, and how it integrates with what exists. Don't re-spec the whole app — just the delta. Still include validation, error handling, edge cases, and the self-assessment for the new feature.

## Input Sophistication Calibration

Before expanding, assess the technical sophistication of the input and calibrate your depth accordingly:

**Non-technical** — "I want an app that...", describes outcomes not implementation, no mention of specific technologies or patterns. → Full expansion. Explain all patterns. Surface all implicit requirements. Use the complete translation pattern library.

**Semi-technical** — Mentions patterns ("CRUD", "status machine", "REST API"), names technologies ("Rails", "React"), uses developer terminology ("pagination", "webhook"). → Expand only what they didn't specify. Don't explain concepts they clearly know. Focus on gaps, edge cases, and consistency. If they said "status machine (draft → sent → paid)," don't re-derive the states — validate them and add what's missing (e.g., who can trigger each transition, what happens to related records on state change).

**Technical** — Provides data models, references specific libraries, describes architecture. → Minimal expansion. Focus on consistency checking, missing edge cases, and the self-assessment. Don't patronize. The value you add is in what they overlooked, not in restating what they told you.

This calibration directly affects the Proportionality rating in the self-assessment. An over-expanded spec for a technical user is as much a failure as an under-expanded one for a non-technical user.

## Security Considerations

Non-technical users never mention security, but every spec should address it. Weave these into the relevant sections rather than bolting on a separate "security" section:

- **Input sanitization**: All user-provided text must be sanitized before display (prevent XSS). Note this in validation rules.
- **Authentication boundaries**: Which pages/actions require login? Which are public? Note this in user flows.
- **Authorization**: Just because a user is logged in doesn't mean they can access everything. Note permission checks in each flow.
- **Rate limiting**: Forms, API endpoints, and login attempts should be rate-limited. Note this in error handling.
- **File uploads**: Validate MIME types server-side (not just extension), re-encode images to strip metadata. Note this in the file upload feature.
- **CSRF protection**: If using server-rendered forms, ensure CSRF tokens are present. Usually framework-handled but worth noting.
- **Sensitive data**: Passwords must be hashed, not stored in plaintext. API keys must not be committed to version control. Note these in assumptions if relevant.

Don't make it scary or overwhelming — just ensure these basics are covered naturally within the spec. The AI assistant building from this spec should implement secure defaults without needing a separate security audit.

## A Worked Example

To illustrate the complete output, here's what the skill produces from a simple request. Note how requirements are colocated with implementation steps (not in separate sections), Builder Notes prioritize for the builder, and Future Considerations captures deferred items.

**User says:** "I want a simple invoicing app where I can create invoices for clients, mark them as paid, and see which ones are overdue."

**Refined spec (One-Shot mode):**

```
# Simple Invoicing App

## Overview
A personal invoicing tool for freelancers/small businesses to create invoices for clients,
track payment status, and identify overdue invoices at a glance.

## Builder Notes
**Load-bearing requirements:**
- Invoice status lifecycle (draft → sent → paid / overdue) — the core value
- Line items with correct total calculation — math must be right
- Overdue detection based on due date vs. current date

**Polish requirements:**
- PDF generation, email sending, dashboard charts
- Inline validation feedback, skeleton loading states

**Judgment calls:**
- Currency formatting: default to USD, but use a locale-aware formatter so switching later is easy
- When the user didn't specify multi-user: build as single-user, but scope DB queries by user_id anyway

## Tech Stack
Rails 7 with Hotwire (Turbo + Stimulus), PostgreSQL, Tailwind CSS.
PDF generation: Prawn gem. No JavaScript framework needed — Hotwire handles interactivity.

## Data Model

### Client
- name: string (required, max 100) — display name
- email: string (required, valid email format) — for sending invoices
- Relationships: has_many Invoices

### Invoice
- number: string (auto-generated, unique) — display identifier (e.g., INV-0001)
- status: enum [draft, sent, paid, overdue] (default: draft)
- issue_date: date (default: today)
- due_date: date (required, must be >= issue_date)
- notes: text (optional) — free-form notes to client
- Relationships: belongs_to Client, has_many LineItems
- Computed: total (sum of line_items.amount * quantity)

### LineItem
- description: string (required, max 200)
- quantity: decimal (required, > 0, precision: 10, scale: 2)
- unit_price: decimal (required, >= 0, precision: 10, scale: 2)
- Relationships: belongs_to Invoice
- Computed: amount (quantity * unit_price)

## User Flows

### Create & Send Invoice
1. User clicks "New Invoice" → sees form with client dropdown and empty line items
2. Selects existing client or clicks "New Client" (inline modal: name + email, both required)
3. Adds line items (dynamic rows: description, quantity, unit_price). Running total updates live
4. Sets due date, optional notes → clicks "Save as Draft"
   - Validation: at least 1 line item, due_date >= today, client required
   - On failure: highlight fields with inline errors, preserve all input
   - On success: redirect to invoice detail page, flash "Invoice saved as draft"
5. From detail page, clicks "Send" → confirmation: "Send invoice to client@email.com?"
   - On confirm: status changes to sent, issue_date set to today. Flash "Invoice sent"

### Mark as Paid
1. From invoice list or detail page, user clicks "Mark Paid" on a sent/overdue invoice
2. Confirmation dialog: "Mark Invoice INV-0042 as paid?" with confirm/cancel
3. On confirm: status → paid, flash "Invoice marked as paid". Button disappears

### View Overdue Invoices
1. Dashboard shows counts: draft / sent / overdue / paid
2. Overdue tab/filter shows all invoices where status=sent AND due_date < today
3. Background job runs daily to flag overdue invoices (update status sent → overdue)

## Features (Implementation Order)

### Phase 1: Foundation
1. **Client management**
   - Scaffold Client model with name (required, max 100) and email (required, format validated)
   - Index page: list all clients, sorted alphabetically. Empty state: "No clients yet — create one when you make your first invoice"
   - Create form (also usable as inline modal from invoice form): validate on blur, disable submit button until required fields are filled, show "Saving..." while in flight, redirect to clients list on success with flash

2. **Invoice CRUD with line items**
   - Scaffold Invoice model with validations (due_date >= issue_date, status enum default: draft)
   - LineItem model as nested resource. Dynamic form rows using Stimulus: "Add Line Item" appends a row, "Remove" deletes with fade-out. Minimum 1 line item enforced on submit
   - Running total calculation: Stimulus controller recalculates on quantity/price change, displays formatted currency
   - Save button: disable + "Saving..." while in flight → on success: redirect to detail view + flash → on error: show validation errors inline, preserve all input, re-enable button
   - Invoice detail page: shows client info, line items table, total, status badge (color-coded: gray=draft, blue=sent, red=overdue, green=paid)

### Phase 2: Core Functionality
3. **Send invoice flow**
   - "Send" button visible only on draft invoices. Triggers confirmation modal: "Send to {client.email}?"
   - On confirm: update status to sent, set issue_date. Disable button + show spinner during request. Flash "Invoice sent" on success
   - Future: actually send email (see Future Considerations). For now, just updates status

4. **Mark as paid**
   - "Mark Paid" button on sent/overdue invoices. Confirmation modal with invoice number
   - On confirm: status → paid, disable button during request. Flash confirmation. Button replaced with "Paid" badge

5. **Overdue detection**
   - Scheduled job (daily via cron/whenever gem): find invoices where status=sent AND due_date < Date.today, update to overdue
   - Dashboard summary cards: count per status, clicking a card filters the invoice list
   - Invoice list: filterable by status (tabs or dropdown), sorted by due_date ascending. Empty state per filter: "No overdue invoices — nice!"

### Phase 3: Polish
6. **PDF generation**
   - Generate PDF from invoice detail using Prawn. Layout: company header, client address block, line items table, total, notes, due date
   - "Download PDF" button on invoice detail page. Loading spinner while generating

7. **Dashboard refinements**
   - Total revenue (sum of paid invoices) and outstanding amount (sum of sent + overdue)
   - Responsive: cards stack vertically on mobile, table collapses to card view

## Assumptions
- Single-user app (no auth needed for v1, but queries scoped by user_id for future multi-user)
- No actual email delivery in v1 — "Send" updates status only (email is a Future Consideration)
- Currency: USD, formatted with commas and 2 decimal places
- Invoice numbers auto-increment (INV-0001, INV-0002, etc.)
- No tax calculation in v1
- No partial payments — invoice is either paid in full or not

## Out of Scope
- Multi-user / team features
- Recurring invoices
- Multiple currencies
- Payment gateway integration (Stripe, etc.)
- Client portal (clients viewing their own invoices)

## Future Considerations
- Email delivery: integrate SendGrid/Postmark to actually email invoices as PDF attachments
- Tax calculation: tax rate per line item or per invoice, with tax summary
- Recurring invoices: template + schedule for repeat clients
- Client portal: public link for clients to view and pay invoices
- Notification batching: scroll position restoration on list pages
- Browser tab title updates per page (e.g., "INV-0042 — Invoices")

## Self-Assessment
**Ratings** (1-5):
- Completeness: 4/5
- Specificity: 5/5
- Consistency: 5/5
- Proportionality: 5/5
- Translation Quality: 4/5
- Implementation Coverage: 5/5

**Issues caught and fixed:**
- Data model initially missing the notes field that the invoice form references — added it
- "Mark Paid" flow didn't specify what replaces the button after payment — added "Paid" badge
- Overdue detection needed a mechanism (background job) — specified cron schedule
- Line items form needed a minimum count enforced on submit — added to validation

**Remaining considerations:**
- Does the user want actual email sending in v1, or is status-only acceptable?
- Should overdue invoices trigger a notification/reminder, or just update silently?
```

Notice how every behavioral requirement (loading states, confirmation dialogs, error handling, empty states) appears as a sub-step within the implementation feature that needs it — not in a separate section. This is what actionable specs look like.

## The Refinement Process

Regardless of mode, follow this mental process:

### Step 1: Identify the Core Entities
What are the "nouns" in this application? Users, Products, Orders, Posts, Comments — whatever the fundamental data objects are. For each one, think about what attributes it has, how it relates to the other entities, and what lifecycle it follows (created → updated → archived? → deleted?).

### Step 2: Map the User Journeys
What does a user actually *do* in this application, from the moment they arrive? Trace each distinct flow: sign up, first-time setup, the main action they'll repeat, secondary actions, admin actions. Each journey becomes a sequence of screens/steps.

### Step 3: Fill the Gaps
Run through this checklist for every feature:
- **Authentication & authorization**: Who can do this? What role/permission is needed?
- **Validation**: What makes input valid or invalid? What are the boundaries?
- **Error handling**: What can go wrong? What does the user see when it does?
- **Empty states**: What does this screen look like with zero data?
- **Loading states**: What does the user see while waiting?
- **Edge cases**: What happens with very long text? Very large numbers? Special characters? Concurrent edits?
- **Mobile/responsive**: How does this adapt to different screen sizes?
- **Performance**: Will this need pagination? Caching? Lazy loading?
- **Accessibility**: Can this be used with keyboard only? Does it have proper labels, focus management, contrast ratios? Are interactive elements announced to screen readers? (Users almost never ask for this, but it's always needed.)
- **Security**: Is user input sanitized? Are there authorization checks? Rate limiting on forms?
- **Interaction feedback**: Does every form have a loading state, success message, and error display? Are destructive actions confirmed? Do buttons show their state (hover, active, disabled, loading)?
- **State preservation**: What happens on page refresh? Does the back button work? Can this page be bookmarked or shared via URL?

### Step 3.5: Compress to Essentials

After expanding, pull back. Not every expanded requirement belongs in the initial build. For each requirement, apply this test: **"Would the user notice if this was missing on day 1?"**

- **Keep** requirements that are structurally necessary (the app breaks without them), would cause data loss or user confusion if absent, or were explicitly requested.
- **Defer** to a "Future Considerations" section requirements that only matter at scale (notification batching, advanced caching), are optimization-level polish (scroll position restoration, browser tab title updates), or exist only because they appeared on a checklist.

**Spec length targets** — these are guidelines, not hard limits:
- Simple requests (todo list, guestbook): under 150 lines
- Medium complexity (invoice tracker, blog with auth): 150-300 lines
- Complex (marketplace, SaaS with billing): 300-500 lines

If a spec exceeds these ranges, compress before delivering. Move deferred items to Future Considerations rather than deleting them — the user can promote any back to scope.

### Step 4: Determine Implementation Order
Sequence the work so that foundational pieces come first and each step builds on the last. The AI assistant should be able to follow this order top to bottom without needing to jump around.

**The Actionability Rule:** Every requirement described anywhere in this spec — interaction feedback, edge cases, state preservation, UI behaviors — must appear as a sub-step within a numbered implementation step. If a behavior is described in a descriptive section but has no corresponding step that says *what to build* and *where to put it*, the builder will skip it. Descriptive sections (Interaction Feedback, Edge Cases, State Preservation) are analysis tools for the refiner. Before finalizing the spec, dissolve every requirement from those sections into the implementation steps. An orphaned requirement — described but never assigned to a step — is worse than an absent one, because it creates a false sense of completeness.

### Step 5: Rate and Refine (Self-Assessment)
After producing the spec, step back and critically evaluate your own work before presenting it to the user. This isn't optional — it's what separates a good spec from a great one.

**Rate the spec across these dimensions (1-5 scale):**

- **Completeness** — Does every feature have validation, error handling, empty states, and edge cases? Or did you gloss over some with vague language like "handle appropriately"?
- **Specificity** — Could an AI assistant build this without asking a single follow-up question? Or are there spots where it would need to guess?
- **Consistency** — Do the data model, user flows, and validation rules all agree with each other? If a field is required in the model, is there a validation rule for it? If a flow references an entity, does that entity exist in the data model?
- **Proportionality** — Does the spec's complexity match the request? A "simple photo upload" shouldn't produce a 500-line spec. A full e-commerce platform shouldn't be two paragraphs.
- **Translation Quality** — Did you actually expand the user's casual language into technical depth, or did you just reorganize what they already said? The value is in what you *added*, not what you *reformatted*.
- **Implementation Coverage** — Cross-reference every behavioral requirement described in descriptive sections (Interaction Feedback, Edge Cases, State Preservation, UI/UX Notes) against the numbered implementation steps. For each behavior, verify a matching sub-step exists that specifies: (a) what to build, (b) the interaction pattern to implement (e.g., "disable the submit button and swap its text to 'Saving...' while the request is in flight" — not just "show loading state"), and (c) how to verify it works. If any requirement exists only as a description without a corresponding implementation step, it is orphaned and will not be built.

**Detect areas of opportunity:**
After rating, identify the weakest areas. Common gaps include:
- Features mentioned in User Flows but missing from the Data Model
- Validation rules that don't cover all the fields in the forms
- Error handling that only covers the happy path
- Mobile/responsive behavior not addressed for complex layouts
- Missing UI patterns — did the user describe a behavior (like "hide and show the sidebar") that maps to a well-known pattern (collapsible sidebar with hamburger toggle) you should name and specify?
- Assumptions that were made silently instead of being documented
- Forms without a complete submission lifecycle (loading → success/error → next step)
- Buttons and actions without all their states defined (hover, disabled, loading)
- Destructive actions (delete, cancel) without a confirmation pattern
- Pages that would break on refresh or lose their state
- Orphaned requirements: behaviors described in Interaction Feedback, Edge Cases, or State Preservation that don't appear as sub-steps in the Implementation Order — these will be silently ignored by the builder

**Implement the findings:**
Don't just list what's wrong — fix it. Go back into the spec and fill the gaps, tighten the vague language, add the missing validation rules, and name the UI patterns. Then present the improved spec to the user. If the changes are significant, briefly note what you caught and fixed (e.g., "I noticed the data model was missing a status field for invoices that the user flow references, so I added it.").

The goal: the user should receive a spec that has already been through one round of quality review. They're the second pair of eyes, not the first.

## Output Format

The refined specification should use this structure. Not every section is needed for every project — use judgment about what's relevant, but err on the side of inclusion for non-trivial apps.

```
# [Project Name]

## Overview
[1-3 sentences describing what this application does and who it's for]

## Builder Notes
**Load-bearing requirements** (get these wrong and the app breaks):
- [3-5 requirements that are structurally critical to the core value proposition]

**Polish requirements** (important for UX but the app functions without them):
- [Requirements that can be simplified or deferred if time-constrained]

**Judgment calls** (scenarios this spec doesn't fully cover):
- [2-3 areas where the builder may encounter unspecified situations and should
 use good judgment, with guidance on what to optimize for]

## Tech Stack
[Explicit technology choices — framework, database, CSS approach, key libraries.
 If the user has preferences, honor them. If not, recommend and explain why.]

## Data Model

### [Entity Name]
- field_name: type (constraints) — purpose
- field_name: type (constraints) — purpose
- Relationships: belongs_to X, has_many Y

[Repeat for each entity]

## User Flows

### [Flow Name] (e.g., "Registration", "Create a Post")
1. User does X → they see Y
2. User inputs Z → system validates → on success: A / on failure: B
3. ...

[Repeat for each flow]

## Features (Implementation Order)

### Phase 1: Foundation
1. **Feature Name**
   - What it does
   - Acceptance criteria (specific, testable conditions)
   - Edge cases to handle
   - UI notes (layout, responsive behavior)

### Phase 2: Core Functionality
[...]

### Phase 3: Polish & Secondary Features
[...]

## Validation Rules (Reference Summary)
[Optional quick-reference table. Every rule here MUST also appear as a sub-step in the
 implementation feature where it applies. This section is a lookup aid, not the source of truth.]

## Error Handling (Reference Summary)
[Optional summary of error display patterns. Every error scenario MUST also be specified
 inline within the implementation step that can trigger it.]

## UI/UX Notes
[General layout guidance, responsive breakpoints, accessibility considerations]

## Assumptions
[Everything you assumed that the user didn't explicitly state — this is critical
 for transparency and allows the user to correct any wrong assumptions]

## Out of Scope
[What this spec explicitly does NOT cover, to prevent scope creep]

## Future Considerations
[Requirements identified during expansion but deferred because they are not essential
 for the initial build. Organized by priority so the user can promote any to current scope.]

## Self-Assessment
**Ratings** (1-5):
- Completeness: X/5
- Specificity: X/5
- Consistency: X/5
- Proportionality: X/5
- Translation Quality: X/5
- Implementation Coverage: X/5

**Issues caught and fixed:**
- [Brief description of what was detected and corrected during self-review]

**Remaining considerations:**
- [Anything that could still be improved but requires user input to resolve]
```

## Important Guidelines

**Don't over-engineer.** If someone asks for a simple to-do list, don't spec out a full project management suite. Match the complexity of the spec to the complexity of the request. A one-page app doesn't need a Phase 1/2/3 breakdown.

**Be specific, not prescriptive.** Say "paginated list showing 20 items per page with next/previous controls" rather than "implement an efficient data display pattern." The AI assistant executing this spec needs concrete details, not abstract principles.

**Surface assumptions visibly.** The Assumptions section is one of the most valuable parts of the output. Every time you make a decision the user didn't explicitly ask for, document it there. This turns invisible misunderstandings into visible, correctable choices.

**Respect the user's language.** If they said "recipe tracker," call it a recipe tracker in the spec, not a "culinary content management system." Technical precision in the implementation details, human language in the descriptions.

**Honor stated tech preferences.** If the user says they use Rails and Tailwind, the spec should be written with Rails conventions in mind (RESTful routes, ActiveRecord models, Stimulus/Turbo patterns, etc.). Don't suggest React if they didn't ask for it.

**Keep the spec self-contained.** An AI assistant should be able to read the refined spec top to bottom and build the application without needing to ask questions. That's the bar. If you find yourself writing "TBD" or "decide later," you haven't refined enough — either resolve it with a reasonable default (and add it to Assumptions) or flag it as a question for the user.

**Describe the pattern, not just the wish.** When specifying a behavior, describe the *interaction pattern* concretely — not just the desired effect. "Show a loading state on submit" is a wish that a builder can interpret in a dozen ways (or skip entirely). "Disable the submit button and swap its text to 'Saving...' while the request is in flight; re-enable on completion" is a pattern any builder can implement regardless of framework. You don't need to name the exact API or attribute (that's the builder's job for their tech stack), but you must specify the pattern concretely enough that the builder knows *what* to build without guessing the intent.

**Design for builder consumption.** The spec will be read and executed by an AI coding assistant. Structure it for how LLMs process instructions:
- **Colocate requirements with implementation steps.** Validation rules, error handling, and edge cases belong inline within the implementation step that builds the feature — not in separate sections the builder may lose track of. If you include standalone Validation Rules or Error Handling sections, treat them as reference summaries and ensure every rule ALSO appears as a sub-step in the implementation order.
- **Make phases independently buildable.** Each phase in "Features (Implementation Order)" should be completable without reading later phases. No forward references. If Phase 3 needs a field, introduce it there — or mark it clearly in the Data Model as "Added in Phase 3."
- **Respect spec length.** A 500-line spec that could be 200 lines wastes builder attention on padding. Simple apps: under 150 lines. Medium: 150-300. Complex: 300-500. If you're over these targets, compress (see Step 3.5).

## Mode-Specific Behavior

### One-Shot Mode
1. Read the user's description carefully
2. Produce the full refined spec. Colocate all behavioral requirements (validation, error handling, loading states, confirmations, edge cases) as sub-steps within the implementation features that need them — not in separate sections. Refer to the worked example.
3. **Run the self-assessment** (Step 5) — rate your spec, find the gaps, fix them in-place
4. Present the improved spec with a brief "Self-Assessment" summary showing your ratings and what you caught/fixed
5. At the end, include a "Questions for Consideration" section with 3-5 things the user might want to change
6. The user can then ask for revisions

### Interactive Mode
1. Acknowledge the request and summarize your understanding in 2-3 sentences
2. Ask 3-4 high-impact questions (the ones whose answers most change the architecture)
3. After answers, ask 2-3 follow-up questions about the next most impactful unknowns
4. Produce the full refined spec. Colocate all behavioral requirements as sub-steps within implementation features — not in separate sections. Refer to the worked example.
5. **Run the self-assessment** (Step 5) — rate, detect, and fix before presenting
6. Present the improved spec with the "Self-Assessment" summary
7. Ask if anything needs revision

### Hybrid Mode
1. Read the user's description
2. Produce a draft spec immediately (marking assumptions clearly)
3. After the draft, present 3-5 targeted questions about the biggest ambiguities
4. After answers, produce the **complete final spec** — not a patch on the draft, but the full spec rewritten with revisions incorporated. The final spec must follow the colocation principle: every validation rule, error handling pattern, loading state, confirmation dialog, and edge case must appear as a concrete sub-step within the implementation feature that needs it. Do NOT put these in separate Validation Rules or Error Handling sections — colocate them. Refer to the worked example for the correct structure.
5. **Run the self-assessment** (Step 5) — rate the final spec, detect gaps, implement fixes
6. Present the improved spec with the "Self-Assessment" summary showing what was caught and corrected

## Handling Revisions

After presenting the spec, the user may want changes. Common revision requests and how to handle them:

- **"Change the tech stack to X"** — Rewrite the Tech Stack section and update any framework-specific conventions throughout (e.g., switching from Rails to Next.js changes routing patterns, ORM syntax, etc.)
- **"Remove feature Y"** — Remove it from Features, User Flows, and any related validation rules. Check if any other features depended on it.
- **"Add feature Z"** — Follow the same expansion process (entities, flows, validation, edge cases) and integrate it into the existing spec at the right implementation phase.
- **"That assumption is wrong"** — Update the assumption and cascade the change through the spec. If the assumption was "single-user app" and the user says "actually, multiple users," that affects auth, authorization, data scoping, and UI — trace the full impact.
- **"This is too complex, simplify it"** — Reduce phases, cut secondary features to Out of Scope, simplify the data model. Re-run the self-assessment with Proportionality as the focus.

After any revision, re-run the self-assessment on the changed sections to make sure the edits didn't create inconsistencies.

## Output Delivery

For short specs (single feature, under ~100 lines), present the spec inline in the conversation.

For longer specs (full application, multiple features), offer to save it as a markdown file the user can download, share with other AI assistants, or hand to a developer. The spec should be fully self-contained in either format — no context from the conversation should be needed to understand it.
