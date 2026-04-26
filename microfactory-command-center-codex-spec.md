# MicroFactory Command Center: Codex Build Specification

## 0. Purpose

Build a polished, demo ready full stack application for the Palantir Year at Palantir Forward Deployed Software Engineer, Warp Speed application screen.

The application should be a Palantir inspired operational command center for small hardware and manufacturing teams. It should not claim to use Palantir AIP, Foundry, or Warp Speed directly. It should demonstrate the same engineering patterns: operational object modeling, fragmented data integration, downstream impact analysis, human approved workflows, auditability, and AI grounded in real operational data.

## 1. Product Summary

**Product name:** MicroFactory Command Center

**One sentence pitch:**

MicroFactory Command Center turns fragmented manufacturing data into an operational command layer that detects supply chain blockers, traces downstream impact, recommends recovery plans, and lets humans approve auditable actions.

**Core demo scenario:**

A supplier delay causes part `DRV-042` to become unavailable. The system detects that this shortage blocks 7 work orders, affects 3 final builds, puts a Friday shipment at risk, recommends substitute part `DRV-042B`, proposes a machine reschedule, requires engineering approval, and logs every action in an audit trail.

## 2. What This Project Must Demonstrate

The app must prove that the builder can:

1. Model a messy operational domain using connected objects.
2. Ingest fragmented data sources.
3. Calculate downstream operational impact.
4. Use an LLM only after deterministic business logic has grounded the context.
5. Keep a human in the loop for critical decisions.
6. Log every recommendation and action.
7. Present the system in a visually credible, non generic, enterprise command center UI.

## 3. Non Goals

Do not build these unless everything else is complete:

1. Full production authentication.
2. Multi tenant organizations.
3. Payments.
4. Complex onboarding.
5. Real supplier API integrations.
6. Real manufacturing execution system integrations.
7. A generic chatbot interface.
8. A marketing landing page.

This is a demo of operational software, not a SaaS homepage.

## 4. Tech Stack

### 4.1 Frontend

Use:

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui, customized heavily
- React Flow for operational object graph
- Recharts for charts and operational metrics
- TanStack Table for dense work order tables
- TanStack Query for API state
- Zustand for local UI state
- GSAP for controlled operational animations
- Lucide React for icons
- React Hook Form for forms
- Zod for client side validation
- Sonner for toast notifications

Frontend package manager:

- pnpm

### 4.2 Backend

Use:

- FastAPI
- Python 3.12
- Uvicorn
- Pydantic v2
- SQLAlchemy 2.0
- Alembic
- Pandas for CSV ingestion
- PyPDF or pypdf for optional PDF parsing
- HTTPX for calling Ollama local API
- Pytest for backend tests
- Ruff for linting and formatting

### 4.3 Database

Use:

- PostgreSQL
- Dockerized Postgres for local development
- Neon Postgres or Supabase Postgres for hosted deployment
- pgvector optional only if RAG is added later

For this demo, use relational tables to model the operational ontology. Do not use Neo4j unless explicitly requested later.

### 4.4 Local Open Source LLM

Use:

- Ollama as the local LLM runtime
- Qwen 2.5 7B Instruct as the default model
- Qwen 2.5 14B Instruct as optional stronger model
- Llama 3.1 8B Instruct as backup

Default local setup:

```bash
ollama pull qwen2.5:7b-instruct
```

Backend should call Ollama locally through:

```txt
http://localhost:11434/api/chat
```

The LLM must return structured JSON. Validate the result with Pydantic before sending it to the frontend.

### 4.5 Deployment

Recommended:

- Frontend: Vercel
- Backend: Render, Railway, or Fly.io
- Database: Neon Postgres

For the application demo, local running is acceptable as long as it is stable and screen recordable.

## 5. Monorepo Structure

Create this structure:

```txt
microfactory-command-center/
  README.md
  docker-compose.yml
  .env.example
  .gitignore

  frontend/
    package.json
    pnpm-lock.yaml
    next.config.ts
    tsconfig.json
    tailwind.config.ts
    postcss.config.mjs
    app/
      layout.tsx
      page.tsx
      globals.css
    components/
      dashboard/
        CommandCenter.tsx
        MetricsStrip.tsx
        DisruptionBanner.tsx
        OntologyGraph.tsx
        RecoveryPanel.tsx
        WorkOrderTable.tsx
        AuditTimeline.tsx
        SupplierPanel.tsx
        MachineSchedule.tsx
        ApprovalDrawer.tsx
      ui/
        shadcn components here
    lib/
      api.ts
      types.ts
      utils.ts
      mock-fallback.ts
    stores/
      command-center-store.ts

  backend/
    pyproject.toml
    alembic.ini
    app/
      main.py
      core/
        config.py
        database.py
        logging.py
      models/
        __init__.py
        base.py
        part.py
        supplier.py
        work_order.py
        machine.py
        build.py
        quality_check.py
        issue.py
        audit_event.py
        action.py
      schemas/
        __init__.py
        part.py
        supplier.py
        work_order.py
        machine.py
        build.py
        quality_check.py
        issue.py
        audit_event.py
        action.py
        recovery_plan.py
        graph.py
      api/
        __init__.py
        routes/
          health.py
          dashboard.py
          ontology.py
          work_orders.py
          disruptions.py
          recovery.py
          actions.py
          audit.py
          seed.py
      services/
        impact_engine.py
        recommendation_engine.py
        ontology_service.py
        agent_service.py
        workflow_service.py
        audit_service.py
        seed_service.py
      data/
        seed_parts.csv
        seed_suppliers.csv
        seed_work_orders.csv
        seed_machines.csv
        seed_builds.csv
        seed_quality_checks.csv
      tests/
        test_impact_engine.py
        test_workflow_service.py
        test_recovery_plan_schema.py
```

## 6. Domain Model

### 6.1 Core Objects

The app should model these objects:

1. Part
2. Supplier
3. WorkOrder
4. Machine
5. Build
6. QualityCheck
7. Issue
8. Action
9. AuditEvent

### 6.2 Part

Fields:

- id
- part_code, example: `DRV-042`
- name
- category
- quantity_on_hand
- quantity_required
- reorder_threshold
- lead_time_days
- supplier_id
- substitute_part_code, nullable
- compatibility_score, nullable
- status: `available`, `low_stock`, `shortage`, `substitute_available`
- created_at
- updated_at

### 6.3 Supplier

Fields:

- id
- name
- reliability_score, 0 to 100
- average_delay_days
- current_delay_days
- contact_email
- status: `normal`, `delayed`, `critical`
- created_at
- updated_at

### 6.4 WorkOrder

Fields:

- id
- work_order_code, example: `WO-018`
- build_id
- required_part_code
- machine_id
- owner_name
- status: `ready`, `blocked`, `at_risk`, `in_progress`, `completed`
- blocker_reason, nullable
- due_at
- estimated_hours
- priority: `low`, `medium`, `high`, `critical`
- created_at
- updated_at

### 6.5 Machine

Fields:

- id
- machine_code, example: `CNC-2`
- name
- capability
- status: `available`, `busy`, `maintenance`, `offline`
- available_window
- current_work_order_id, nullable
- created_at
- updated_at

### 6.6 Build

Fields:

- id
- build_code, example: `BUILD-A`
- name
- customer
- shipment_due_at
- status: `on_track`, `at_risk`, `blocked`, `shipped`
- priority
- created_at
- updated_at

### 6.7 QualityCheck

Fields:

- id
- check_code, example: `QC-104`
- work_order_id
- part_code
- status: `pending`, `passed`, `failed`, `requires_review`
- defect_reason, nullable
- qa_owner
- created_at
- updated_at

### 6.8 Issue

Fields:

- id
- issue_code, example: `ISS-009`
- type: `supplier_delay`, `part_shortage`, `machine_conflict`, `qa_failure`
- severity: `low`, `medium`, `high`, `critical`
- title
- description
- affected_part_code, nullable
- affected_supplier_id, nullable
- status: `open`, `investigating`, `resolved`, `dismissed`
- created_at
- updated_at

### 6.9 Action

Fields:

- id
- action_code, example: `ACT-022`
- issue_id
- type: `approve_substitute`, `reschedule_machine`, `request_qa`, `notify_supplier`, `manual_override`
- label
- description
- status: `recommended`, `pending_approval`, `approved`, `rejected`, `completed`
- requires_approval
- approver_role
- created_by
- approved_by, nullable
- created_at
- updated_at

### 6.10 AuditEvent

Fields:

- id
- event_type
- entity_type
- entity_id
- actor
- role
- message
- before_state JSONB, nullable
- after_state JSONB, nullable
- created_at

Audit events are append only. Never update or delete audit events through normal app flows.

## 7. Seed Data

Create realistic seed data.

### 7.1 Suppliers

Use at least 5 suppliers:

1. Northline Components
2. Apex Motion Supply
3. Vertex Electronics
4. BlueForge Metals
5. Orion Industrial Systems

### 7.2 Parts

Use at least 12 parts:

1. `DRV-042` Motor Driver Board
2. `DRV-042B` Motor Driver Board Substitute
3. `SNS-118` Optical Sensor
4. `BRK-201` Aluminum Bracket
5. `PWR-090` Power Regulator
6. `CBL-014` Shielded Cable
7. `MNT-300` Mounting Plate
8. `FAN-022` Cooling Fan
9. `PCB-700` Control PCB
10. `ENC-044` Enclosure
11. `BOLT-006` M6 Bolt Kit
12. `QA-JIG-03` Test Jig

### 7.3 Builds

Use at least 3 builds:

1. `BUILD-A` Autonomous Drone Assembly
2. `BUILD-B` Sensor Rig Prototype
3. `BUILD-C` Inspection Robot Batch

### 7.4 Work Orders

Use at least 15 work orders. At least 7 should depend on `DRV-042` so the demo disruption has meaningful impact.

Example affected work orders:

- `WO-018`
- `WO-021`
- `WO-024`
- `WO-026`
- `WO-031`
- `WO-033`
- `WO-037`

### 7.5 Machines

Use at least 5 machines:

1. `CNC-1`
2. `CNC-2`
3. `ASM-1`
4. `QA-BENCH-2`
5. `PRINT-3D-4`

## 8. Backend API Requirements

Base API path:

```txt
/api
```

### 8.1 Health

`GET /api/health`

Returns:

```json
{
  "status": "ok",
  "service": "microfactory-command-center-backend"
}
```

### 8.2 Dashboard Summary

`GET /api/dashboard/summary`

Returns:

```json
{
  "activeIssues": 1,
  "blockedWorkOrders": 7,
  "atRiskBuilds": 3,
  "estimatedDelayDays": 4,
  "manualAnalysisMinutesSaved": 30,
  "lastUpdated": "2026-04-26T21:30:00Z"
}
```

### 8.3 Ontology Graph

`GET /api/ontology/graph`

Returns nodes and edges for React Flow:

```json
{
  "nodes": [
    {
      "id": "supplier-northline",
      "type": "supplier",
      "label": "Northline Components",
      "status": "delayed",
      "metadata": {}
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "supplier-northline",
      "target": "part-drv-042",
      "label": "supplies"
    }
  ]
}
```

### 8.4 Work Orders

`GET /api/work-orders`

Supports optional query params:

- status
- build_code
- part_code
- priority

`GET /api/work-orders/{work_order_code}`

### 8.5 Trigger Demo Disruption

`POST /api/disruptions/supplier-delay`

Request:

```json
{
  "supplierName": "Northline Components",
  "partCode": "DRV-042",
  "delayDays": 4
}
```

Behavior:

1. Mark supplier as delayed.
2. Mark part `DRV-042` as shortage.
3. Mark dependent work orders as blocked or at risk.
4. Mark dependent builds as at risk.
5. Create an open issue.
6. Create audit events.
7. Return impact analysis.

Response:

```json
{
  "issueCode": "ISS-009",
  "affectedPart": "DRV-042",
  "blockedWorkOrders": ["WO-018", "WO-021", "WO-024", "WO-026", "WO-031", "WO-033", "WO-037"],
  "affectedBuilds": ["BUILD-A", "BUILD-B", "BUILD-C"],
  "estimatedDelayDays": 4,
  "substitutePart": "DRV-042B",
  "approvalRequired": true
}
```

### 8.6 Generate Recovery Plan

`POST /api/recovery/generate`

Request:

```json
{
  "issueCode": "ISS-009"
}
```

Behavior:

1. Load issue.
2. Load impacted parts, suppliers, work orders, machines, builds, quality checks.
3. Run deterministic impact engine first.
4. Send grounded context to Ollama.
5. Ask for structured JSON only.
6. Validate with Pydantic.
7. Store recommended actions.
8. Create audit event showing that an AI recovery plan was generated.

Response:

```json
{
  "summary": "DRV-042 delay blocks 7 work orders and puts BUILD-A, BUILD-B, and BUILD-C at risk.",
  "riskLevel": "medium",
  "confidence": 82,
  "reasoningBullets": [
    "DRV-042 is required by 7 active work orders.",
    "DRV-042B has a 91% compatibility score but requires QA validation.",
    "CNC-2 has an available slot tonight from 8 PM to 11 PM."
  ],
  "recommendedActions": [
    {
      "type": "approve_substitute",
      "label": "Approve DRV-042B as substitute after QA validation",
      "requiresApproval": true,
      "approverRole": "Manufacturing Engineer"
    },
    {
      "type": "reschedule_machine",
      "label": "Move WO-018 to CNC-2 tonight",
      "requiresApproval": true,
      "approverRole": "Operations Manager"
    },
    {
      "type": "request_qa",
      "label": "Create QA validation check for DRV-042B",
      "requiresApproval": false,
      "approverRole": null
    }
  ]
}
```

### 8.7 Approve Action

`POST /api/actions/{action_code}/approve`

Request:

```json
{
  "actor": "Maya R.",
  "role": "Manufacturing Engineer"
}
```

Behavior for `approve_substitute`:

1. Mark action as approved.
2. Update affected work orders from blocked to ready or at risk depending on QA status.
3. Create or update quality check for substitute validation.
4. Add audit event.
5. Return updated issue, work orders, and audit event.

### 8.8 Reject Action

`POST /api/actions/{action_code}/reject`

Request:

```json
{
  "actor": "Maya R.",
  "role": "Manufacturing Engineer",
  "reason": "Substitute part has not passed QA validation."
}
```

### 8.9 Audit Events

`GET /api/audit`

Supports optional query params:

- entity_type
- entity_id
- issue_code
- limit

### 8.10 Seed Reset

`POST /api/seed/reset`

For demo stability, this should reset the database to the initial clean scenario.

## 9. Impact Engine Requirements

Implement `impact_engine.py` as deterministic logic.

### 9.1 Main Function

```python
def analyze_supplier_delay(part_code: str, delay_days: int) -> ImpactAnalysis:
    pass
```

### 9.2 ImpactAnalysis Schema

Fields:

- affected_part_code
- supplier_name
- delay_days
- blocked_work_orders
- at_risk_work_orders
- affected_builds
- available_substitutes
- machines_with_available_capacity
- estimated_delay_days
- severity
- approval_required

### 9.3 Severity Rules

Use deterministic rules:

```txt
critical: more than 10 work orders blocked or shipment due within 24 hours
high: 6 to 10 work orders blocked or shipment due within 48 hours
medium: 2 to 5 work orders blocked or shipment due within 5 days
low: 1 work order blocked and no near term shipment at risk
```

For the main demo, 7 blocked work orders should return `high` or `medium-high`. The UI may display it as `High operational risk`.

## 10. Recommendation Engine Requirements

Implement `recommendation_engine.py` as deterministic recommendation logic before the LLM.

It should recommend:

1. Substitute part if compatibility score is greater than or equal to 0.85.
2. QA validation if substitute part is used.
3. Machine reschedule if an available machine exists.
4. Supplier notification if delay is greater than 2 days.
5. Manager escalation if 3 or more builds are at risk.

The LLM should improve the explanation, not invent the business logic.

## 11. Agent Service Requirements

Implement `agent_service.py`.

### 11.1 Responsibilities

1. Format grounded operational context.
2. Call Ollama local API.
3. Request structured JSON.
4. Validate response using Pydantic.
5. Fall back to deterministic recovery plan if Ollama is unavailable.

### 11.2 Ollama System Prompt

Use this system prompt:

```txt
You are an operations recovery planner for a small manufacturing team. You must only use the operational context provided. Do not invent suppliers, parts, machines, work orders, or approvals. Return only valid JSON matching the provided schema. Critical actions require human approval. You are allowed to summarize risk and recommend next actions, but you are not allowed to directly approve or execute actions.
```

### 11.3 Fallback Behavior

If Ollama is not installed, not running, or returns invalid JSON:

1. Do not crash.
2. Return a deterministic recovery plan generated by `recommendation_engine.py`.
3. Add a response field:

```json
{
  "aiStatus": "fallback_used"
}
```

This keeps the demo stable.

## 12. Frontend UI Requirements

The frontend should look like a serious operational command center, not an AI generated SaaS landing page.

### 12.1 Visual Style

Use:

- Dark industrial interface
- Dense but readable cards
- Thin borders
- Realistic status chips
- No generic gradient blobs
- No huge empty landing page sections
- No excessive animation

### 12.2 Color Palette

Use these tokens:

```txt
Background: #0B0F14
Panel: #111827
Elevated card: #162033
Border: #263244
Primary blue: #3B82F6
Warning amber: #F59E0B
Critical red: #EF4444
Success green: #22C55E
Text primary: #E5E7EB
Text muted: #94A3B8
```

### 12.3 Typography

Use:

- IBM Plex Sans or Geist Sans
- Small labels in uppercase with letter spacing
- Dense tables with clean spacing
- Avoid marketing style headings

### 12.4 Main Dashboard Layout

Single page app layout:

```txt
┌──────────────────────────────────────────────────────────────┐
│ Top bar: MicroFactory Command Center | Role Switcher | Reset │
├───────────────┬──────────────────────────────┬───────────────┤
│ Left rail     │ Main operational graph        │ Recovery panel│
│               │                              │               │
│ Builds        │ Supplier → Part → WorkOrder   │ AI/Recovery   │
│ Work Orders   │ → Machine → Build             │ Plan          │
│ Suppliers     │                              │ Actions       │
│ Machines      │                              │ Approval      │
├───────────────┴──────────────────────────────┴───────────────┤
│ Bottom: Work order table + audit timeline                     │
└──────────────────────────────────────────────────────────────┘
```

### 12.5 Components

#### CommandCenter.tsx

Top level component that fetches dashboard summary, graph data, work orders, and audit logs.

#### MetricsStrip.tsx

Cards:

1. Active issues
2. Blocked work orders
3. At risk builds
4. Estimated delay
5. Manual analysis saved

#### DisruptionBanner.tsx

Shows the active supplier delay:

```txt
Supplier delay detected: Northline Components delayed DRV-042 by 4 days.
7 work orders blocked. 3 builds at risk.
```

Buttons:

- Trigger Demo Disruption
- Generate Recovery Plan
- Reset Demo

#### OntologyGraph.tsx

Use React Flow.

Must show nodes for:

- Supplier
- Part
- Substitute Part
- Work Orders
- Machines
- Builds
- Quality Check

When disruption is triggered:

- Supplier node turns red or amber
- `DRV-042` node turns critical red
- Affected work orders turn red
- Affected builds turn amber
- Substitute part node is highlighted blue

#### RecoveryPanel.tsx

Shows:

- Recovery summary
- Risk level
- Confidence score
- Reasoning bullets
- Recommended actions
- Approval buttons

#### WorkOrderTable.tsx

Use TanStack Table.

Columns:

- Work order
- Build
- Required part
- Machine
- Owner
- Status
- Due time
- Priority
- Blocker

#### AuditTimeline.tsx

Shows append only event list.

Each event should include:

- Time
- Actor
- Role
- Entity
- Message

Example:

```txt
21:42:13 · System · Supplier delay detected for DRV-042
21:42:14 · Impact Engine · 7 blocked work orders identified
21:42:20 · Local LLM · Recovery plan generated
21:43:02 · Maya R. · Approved DRV-042B substitute validation
```

#### Role Switcher

Use a fake role switcher for demo:

- Operator
- Manufacturing Engineer
- Operations Manager

Only Manufacturing Engineer can approve substitute part.
Only Operations Manager can approve machine reschedule.

If the wrong role clicks approve, show a toast:

```txt
Approval blocked: this action requires Manufacturing Engineer permissions.
```

## 13. GSAP Animation Requirements

Use GSAP only for meaningful operational moments.

### 13.1 Disruption Propagation Animation

When the supplier delay is triggered:

1. Supplier node pulses red.
2. Edge from supplier to part highlights.
3. Part node turns critical.
4. Affected work orders light up sequentially.
5. Affected builds turn amber.
6. Recovery panel slides in.

### 13.2 Approval Animation

When substitute is approved:

1. Action card changes from pending to approved.
2. Work orders change from blocked to ready or at risk.
3. Audit log receives new entry with a subtle highlight.
4. Substitute part node glows briefly.

Do not add random animations.

## 14. Demo Flow Requirements

The app must support this exact 3 minute video flow.

### 14.1 Start State

Show dashboard with mostly normal operations:

- 0 active critical issues
- Work orders mostly ready or in progress
- Builds on track
- Supplier nodes normal

### 14.2 Trigger Disruption

Click `Trigger Demo Disruption`.

Expected result:

- Banner appears
- Graph highlights impact
- Metrics update
- Work order table shows 7 blocked rows
- Audit timeline logs system events

### 14.3 Generate Recovery Plan

Click `Generate Recovery Plan`.

Expected result:

- Backend sends grounded context to local Ollama
- Recovery panel displays structured plan
- Recommended actions appear
- Audit log adds AI plan generated event

### 14.4 Approve Substitute

Switch role to Manufacturing Engineer.

Click `Approve DRV-042B Substitute`.

Expected result:

- Action status becomes approved
- QA validation appears or updates
- Work orders improve from blocked to ready or at risk
- Audit log records approval

### 14.5 Close With Impact

Dashboard should show:

- Blocked work orders reduced
- Issue status improved
- Human approval recorded
- Recovery path visible

## 15. README Requirements

Create a README with:

1. Project description
2. Why this exists
3. Tech stack
4. Local setup instructions
5. Ollama setup instructions
6. Environment variables
7. How to run frontend
8. How to run backend
9. How to seed/reset database
10. Demo script
11. Architecture diagram in Mermaid

## 16. Environment Variables

Root `.env.example`:

```env
# Backend
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/microfactory
BACKEND_CORS_ORIGINS=http://localhost:3000
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct

# Frontend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## 17. Docker Compose

Create `docker-compose.yml` for Postgres:

```yaml
services:
  postgres:
    image: postgres:16
    container_name: microfactory-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: microfactory
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 18. Backend Implementation Order

Build in this order:

1. FastAPI app setup
2. Database connection
3. SQLAlchemy models
4. Alembic migrations
5. Seed service
6. Health route
7. Dashboard summary route
8. Work order route
9. Ontology graph route
10. Impact engine
11. Supplier delay route
12. Recommendation engine
13. Ollama agent service
14. Recovery plan route
15. Action approval routes
16. Audit routes
17. Tests

## 19. Frontend Implementation Order

Build in this order:

1. Next.js app setup
2. Tailwind theme tokens
3. Dashboard layout shell
4. Metrics strip
5. Work order table with mock data
6. Audit timeline with mock data
7. API client
8. Real backend data integration
9. React Flow ontology graph
10. Disruption button flow
11. Recovery panel
12. Approval workflow
13. GSAP animation polish
14. Loading, error, and fallback states
15. Final visual polish

## 20. Testing Requirements

Backend tests:

1. `test_impact_engine.py`
   - Supplier delay for `DRV-042` returns 7 blocked work orders.
   - Affected builds include `BUILD-A`, `BUILD-B`, and `BUILD-C`.
   - Substitute `DRV-042B` is recommended.

2. `test_workflow_service.py`
   - Approving substitute creates audit event.
   - Wrong role cannot approve restricted action.
   - Work order statuses update correctly.

3. `test_recovery_plan_schema.py`
   - Valid recovery plan passes Pydantic validation.
   - Invalid LLM response triggers fallback.

Frontend tests are optional for the demo but include at least basic type safety and linting.

## 21. Design Quality Rules

The UI must avoid these AI generated patterns:

1. No generic gradient hero section.
2. No excessive glowing cards.
3. No vague copy like “unlock insights.”
4. No empty dashboard with three oversized cards.
5. No fake charts with meaningless data.
6. No chatbot as the central interface.

Use realistic operational language:

- BOM
- lead time
- supplier delay
- substitute part
- compatibility score
- QA validation
- work order
- machine slot
- blocked build
- audit event
- manual override
- approval required

## 22. Copywriting Requirements

Use concrete operational copy.

Bad:

```txt
AI transforms your operations with powerful insights.
```

Good:

```txt
DRV-042 shortage blocks 7 work orders and puts BUILD-A at risk for Friday shipment.
```

Bad:

```txt
Click here to optimize workflow.
```

Good:

```txt
Approve DRV-042B substitute after QA validation.
```

## 23. Demo Script

Include this in README.

```txt
0:00 to 0:20
Small hardware teams do not fail because they cannot design. They fail because execution data is fragmented across inventory sheets, supplier updates, work orders, machine schedules, and quality notes. I built MicroFactory Command Center to turn that fragmented data into an operational command layer.

0:20 to 0:50
The system models the factory as connected objects: suppliers, parts, substitute parts, work orders, machines, builds, and quality checks. This lets the software reason across relationships instead of treating every spreadsheet as isolated.

0:50 to 1:25
Here I trigger a supplier delay. Northline Components is delayed four days on DRV-042. The system immediately traces downstream impact: 7 work orders are blocked, 3 builds are at risk, and the Friday shipment is threatened.

1:25 to 2:00
Now I generate a recovery plan using a local open source model through Ollama. The model does not invent actions. It receives grounded context from the impact engine and returns a structured recovery plan: approve DRV-042B as a substitute, run QA validation, and reschedule WO-018 to CNC-2 tonight.

2:00 to 2:35
Critical changes require human approval. I switch into the Manufacturing Engineer role and approve the substitute action. The system updates the work orders, creates a QA follow up, and records the approval in an append only audit trail.

2:35 to 3:00
This prototype reduces manual impact analysis from around 30 minutes to under 10 seconds. More importantly, it shows how operational software should work: grounded in real objects, close to the user, human approved, and auditable.
```

## 24. Acceptance Criteria

The project is complete when:

1. `pnpm dev` runs the frontend.
2. `uvicorn app.main:app --reload` runs the backend.
3. Docker Compose starts Postgres.
4. Seed reset creates all demo data.
5. Dashboard loads real backend data.
6. Trigger disruption updates graph, table, metrics, and audit log.
7. Generate recovery plan uses Ollama when available.
8. Recovery plan falls back gracefully when Ollama is unavailable.
9. Approve action updates operational state and audit log.
10. The app can be demoed cleanly in under 3 minutes.

## 25. Build Priorities

If time is limited, prioritize in this order:

1. Polished dashboard UI
2. Realistic seed data
3. Deterministic impact engine
4. React Flow operational graph
5. Audit trail
6. Approval workflow
7. Ollama recovery plan
8. GSAP animations
9. File ingestion
10. Auth

The LLM is not the product. The operational workflow is the product.
