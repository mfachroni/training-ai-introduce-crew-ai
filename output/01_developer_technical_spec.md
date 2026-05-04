# Technical Specification Document: ComplainHub

**Project:** ComplainHub (Complaint Management System)  
**Role:** Senior System Architect  
**Status:** Final Technical Design

---

## 1. System Architecture Overview

ComplainHub is designed as a **modular monolithic architecture** (transitionable to microservices) deploying a **Stateless Backend** and a **Decoupled Frontend**. This approach ensures high availability, scalability for high ticket volumes, and ease of maintenance.

### 1.1 High-Level Architecture Diagram (Textual Representation)
```text
[User Interface Layer]
       ^
       | (HTTPS / JSON / REST)
       v
[API Gateway / Load Balancer]
       |
       +-----> [Authentication Service] <---> [Identity Provider / JWT]
       |
       +-----> [Core Ticket Engine] <---------- [Routing Engine (Rules Logic)]
       |               |
       |               +---> [SLA Manager (Background Worker/Cron)]
       |               |
       |               +---> [Notification Service] ---> [Email/SMTP, In-App]
       |
       +-----> [Analytics Engine] <--- [Read-Optimized Database View]
       |
       +-----> [Knowledge Base Service] <--- [ElasticSearch/Full-Text Search]
       |
[Data Persistence Layer]
       |
       +-----> [Primary DB: PostgreSQL] (Relational Data, Tickets, Users)
       |
       +-----> [Cache: Redis] (Session Management, SLA Timers, Rate Limiting)
       |
       +-----> [Blob Storage: AWS S3/Azure Blob] (Attachments, Evidence)
```

### 1.2 Technology Stack
*   **Frontend:** React.js with Tailwind CSS (Responsive design for CX and AX modes).
*   **Backend:** Node.js (NestJS) or Python (FastAPI) for high-concurrency asynchronous I/O.
*   **Database:** PostgreSQL (Primary) for ACID compliance on ticket states.
*   **Caching/Queue:** Redis (for session caching and RabbitMQ/BullMQ for background SLA tasks).
*   **Search:** Elasticsearch (for Knowledge Base and Ticket history search).
*   **Infrastructure:** Dockerized containers orchestrated via Kubernetes (K8s).

---

## 2. Data Models (Schema Design)

### 2.1 Core Entities (ERD Definition)

#### `User`
| Field | Type | Description |
| :--- | :--- | :--- |
| `user_id` | UUID (PK) | Unique identifier |
| `email` | String (Unique) | User login and notification address |
| `password_hash` | String | Bcrypt hashed password |
| `role` | Enum | `CUSTOMER`, `AGENT`, `DEPT_HEAD`, `ADMIN` |
| `dept_id` | UUID (FK) | Link to Department (Null for customers) |
| `created_at` | Timestamp | Account creation date |

#### `Department`
| Field | Type | Description |
| :--- | :--- | :--- |
| `dept_id` | UUID (PK) | Unique identifier |
| `name` | String | e.g., "Billing", "Technical Support" |
| `sla_target_hours`| Integer | Default resolution target for this dept |
| `manager_id` | UUID (FK) | Link to `User` (Dept Head) |

#### `Ticket`
| Field | Type | Description |
| :--- | :--- | :--- |
| `ticket_id` | UUID (PK) | Unique identifier |
| `ticket_number` | String (Unique) | Human-readable ID (e.g., CH-1001) |
| `customer_id` | UUID (FK) | Link to `User` (Customer) |
| `assigned_agent_id`| UUID (FK) | Link to `User` (Agent) |
| `dept_id` | UUID (FK) | Linked department |
| `status` | Enum | `OPEN`, `IN_PROGRESS`, `PENDING`, `RESOLVED`, `CLOSED` |
| `priority` | Enum | `LOW`, `MEDIUM`, `HIGH`, `URGENT` |
| `category` | String | Categorization for routing rules |
| `subject` | String | Short summary of the complaint |
| `description` | Text | Detailed complaint |
| `sla_deadline` | Timestamp | Calculated deadline based on priority/dept |
| `created_at` | Timestamp | Ticket creation time |
| `updated_at` | Timestamp | Last activity timestamp |

#### `Interaction` (Conversation Thread)
| Field | Type | Description |
| :--- | :--- | :--- |
| `interaction_id` | UUID (PK) | Unique identifier |
| `ticket_id` | UUID (FK) | Link to `Ticket` |
| `user_id` | UUID (FK) | Who wrote the message |
| `type` | Enum | `PUBLIC_REPLY` (Customer sees), `INTERNAL_NOTE` (Agent only) |
| `content` | Text | Message body |
| `created_at` | Timestamp | Time of message |

#### `RoutingRule`
| Field | Type | Description |
| :--- | :--- | :--- |
| `rule_id` | UUID (PK) | Unique identifier |
| `keyword` | String | Keyword to trigger the rule |
| `target_dept_id` | UUID (FK) | Department to assign to |
| `priority_level` | Integer | Order of execution (higher = processed first) |
| `is_active` | Boolean | Toggle for the rule |

---

## 3. API Design (RESTful)

### 3.1 Customer API (`/api/v1/customer`)
| Endpoint | Method | Description | Auth |
| :--- | :--- | :--- | :--- |
| `/tickets` | POST | Submit a new complaint (starts intake) | Public/User |
| `/tickets` | GET | List all tickets for the authenticated customer | JWT |
| `/tickets/{id}` | GET | Get specific ticket details & timeline | JWT |
| `/tickets/{id}/reply` | POST | Add a public reply/attachment to a ticket | JWT |
| `/survey/{id}` | POST | Submit CSAT survey results | Token-based |

### 3.2 Agent API (`/api/v1/agent`)
| Endpoint | Method | Description | Auth |
| :--- | :--- | :--- | :--- |
| `/inbox` | GET | Fetch tickets based on filters (SLA breach, Priority) | JWT (Agent+) |
| `/tickets/{id}/assign` | PATCH | Assign ticket to self or another agent | JWT (Agent+) |
| `/tickets/{id}/status` | PATCH | Update status (e.g., Open $\rightarrow$ Resolved) | JWT (Agent+) |
| `/tickets/{id}/notes` | POST | Add an internal private note | JWT (Agent+) |
| `/kb/suggest` | GET | Get suggested KB articles based on ticket text | JWT (Agent+) |

### 3.3 Admin & Management API (`/api/v1/admin`)
| Endpoint | Method | Description | Auth |
| :--- | :--- | :--- | :--- |
| `/routing/rules` | POST/PUT/DELETE| Manage keyword-based routing rules | JWT (Admin) |
| `/analytics/kpis` | GET | Get ART, FRT, and Volume metrics | JWT (DeptHead+) |
| `/analytics/heatmap` | GET | Get ticket volume data by hour/day | JWT (DeptHead+) |
| `/users/roles` | PATCH | Update user permissions and department assignments | JWT (Admin) |

---

## 4. Third-Party Integrations

1.  **Email Gateway (SendGrid / AWS SES):** 
    *   *Inbound:* Listen to emails $\rightarrow$ Parse body $\rightarrow$ Create Ticket.
    *   *Outbound:* Trigger notifications for status changes and SLA alerts.
2.  **Cloud Storage (AWS S3):** Securely host evidence (images, PDFs) uploaded by customers.
3.  **Auth0 / Okta (Optional):** For Enterprise SSO integration for employees (Dept Heads/Agents).
4.  **Elasticsearch:** To power the "Knowledge Base" keyword search and high-speed historical ticket lookup.

---

## 5. Critical Logic Implementations

### 5.1 Automated Routing Logic (The "Engine")
Upon ticket creation, the system iterates through `RoutingRule` table:
1.  Fetch all `is_active = true` rules sorted by `priority_level`.
2.  Scan `subject` and `description` for `keyword` matches.
3.  If match found $\rightarrow$ Set `dept_id` and assign via **Round-Robin** (fetch agent in dept with the lowest current ticket count).
4.  If no match $\rightarrow$ Assign to `General Queue` (Default Dept).

### 5.2 SLA Tracking Engine (Background Worker)
A cron-job/worker runs every 15 minutes:
1.  **Calculation:** `SLA_Deadline = Created_At + (Dept_SLA_Target * Priority_Multiplier)`.
2.  **State Check:** Identify tickets where `current_time` is approaching `SLA_Deadline` and status $\neq$ `RESOLVED`.
3.  **Escalation:** If `current_time > SLA_Deadline`, update `ticket.priority` to `URGENT` and trigger a notification to the `manager_id` of the assigned department.