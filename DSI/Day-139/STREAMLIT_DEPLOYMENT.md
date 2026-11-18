# Deploying Data Science & ML Web Apps with Streamlit — A Comprehensive Note

## 1. What Streamlit Is and Why It Fits DS/ML

Streamlit is an open-source Python framework that turns data scripts into shareable web applications. You write plain Python — no HTML, CSS, or JavaScript — and get interactive widgets (`st.slider`, `st.selectbox`, `st.file_uploader`), charts, data editors, and layout components. This makes it exceptionally productive for data scientists and ML engineers who want to ship dashboards, model demos, and internal tools without becoming web developers.

Typical DS/ML use cases:

- **Model demos / inference front-ends** — upload data, adjust parameters, see predictions (e.g., the Snowflake "Tasty Bytes" price-optimization app, which trains an ML model and serves recommendations through a Streamlit UI).
- **Interactive dashboards** over warehouses or databases.
- **Internal data tools** — data entry, validation, approval workflows that write back to a database.
- **Prototypes and proofs of concept** that later evolve into production apps.

## 2. Deployment Options

### 2.1 Streamlit Community Cloud (free tier)

The fastest path: connect a GitHub repo, pick the main file, click Deploy, and your app is live at `your-app.streamlit.app`. Great for demos, coursework, and prototyping.

**Hard limits that matter commercially:**

| Constraint               | Detail                                                                                                                                                                                                                                             |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Terms of use**         | Community Cloud is licensed for **personal and non-commercial purposes** (evaluation, education, personal projects). Apps processing PII are restricted to non-commercial use only; processing financial, health, or biometric data is prohibited. |
| **Resources**            | ~2.7 GB RAM ceiling (with 2 CPU cores, 50 GB storage). Apps exceeding it crash and restart without warning.                                                                                                                                        |
| **Sleep**                | Apps sleep after ~12 hours without traffic; visitors hit a "wake up" page.                                                                                                                                                                         |
| **Privacy**              | Only **one private app** at a time; everything else must live in a public repo.                                                                                                                                                                    |
| **Branding**             | No custom domains — you're stuck on the `streamlit.app` subdomain.                                                                                                                                                                                 |
| **Fair-use enforcement** | Accounts can be blocked (403) by undocumented usage limits, sometimes triggered by rapid redeployments during debugging.                                                                                                                           |

**Verdict for commercial use: not suitable.** The terms explicitly exclude commercial use where personal information is processed, and the resource/privacy/branding limits make it inappropriate for anything customer-facing.

### 2.2 Streamlit in Snowflake (SiS) — the "official" commercial route

Snowflake acquired Streamlit in 2022, and SiS is Streamlit's sanctioned path to production. The app runs **inside your Snowflake account** as a native object: code lives in a Snowflake stage, data access uses an active session (no connection strings or credentials to manage), and access control inherits Snowflake RBAC.

- **Pricing:** billed in Snowflake credits based on the runtime (virtual warehouse or Snowpark Container Services compute pool) plus the query warehouse. Since March 2026, container runtimes are the default — long-running services without sleep timers, with broader PyPI package access via External Access Integrations.
- **Economics:** a container node costs ~0.11 credits/hour (≈$238/month at $3/credit if always-on) and hosts multiple apps; a real-world study found nightly suspension of idle pools cut a 25-dashboard deployment from ~$2,138 to ~$174/month.
- **Access control:** Snowflake roles govern who sees the app — strong for internal tools, but every viewer needs a Snowflake account or IdP-linked identity.

**Verdict:** excellent for internal/team-facing commercial tools when your data already lives in Snowflake; not ideal for high-traffic public-facing apps with strict latency needs.

### 2.3 Self-hosting (Docker on your own infrastructure)

This is the most common route for serious commercial deployments:

- **VPS (DigitalOcean, Hetzner, AWS EC2):** ~$5–15/month for small apps, full control, no platform limits. You run Streamlit in Docker behind **nginx with WebSocket support** (missing the `Upgrade` header causes the eternal "Connecting…" screen) plus Let's Encrypt SSL.
- **PaaS options** (Render ~$7–85/mo, Railway ~$10–25/mo, Fly.io from ~$2/mo, Heroku $5–50/mo): managed infrastructure with custom domains and secrets, but **no built-in viewer authentication** — you add it at the app layer (e.g., `st.login()` with OIDC, or a reverse proxy like OAuth2 Proxy / Cloudflare Access).
- **Kubernetes / cloud containers (ECS, Cloud Run, AKS):** the scaling path — multiple replicas behind a load balancer, health checks, rolling deploys. Higher complexity, but this is how you get true horizontal scale.

## 3. Can It Scale Commercially?

**Yes, with architecture.** Streamlit's execution model matters here:

1. **Script re-runs on every interaction.** Each widget change re-executes the whole script top-to-bottom. This is simple but means naive code re-trains models or re-queries databases on every click.
   - _Mitigation:_ `@st.cache_data` and `@st.cache_resource` for data/model loading, `@st.fragment` for partial re-runs, `st.session_state` for per-user state, and `st.spinner`/progress indicators for long operations.

2. **Each browser session holds a server-side session** over a persistent WebSocket. This makes Streamlit memory-hungry at scale — a few hundred concurrent users can exhaust a single instance, and sessions are not freely shareable across replicas without sticky sessions.

3. **No built-in horizontal scaling in Streamlit itself** — you scale with infrastructure: multiple replicas behind a load balancer with **session affinity (sticky sessions)**, or an external scaling layer. Third-party commercial offerings (e.g., Fastero) add built-in auth and managed scaling if you want Streamlit-specific hosting without building it yourself.

Realistic scaling tiers:

| Scale                 | Architecture                                                                                                                                                                            |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1–50 concurrent users | Single Docker container on a VPS or PaaS (2–4 GB RAM)                                                                                                                                   |
| 50–500 users          | 2–4 replicas behind nginx/ALB with sticky sessions; external DB; Redis for shared state                                                                                                 |
| 500+ users            | Kubernetes with HPA, stateless app design (push per-user state to Redis/DB), caching layer, CDN for static assets, model serving separated into a dedicated API (FastAPI + GPU workers) |

For genuinely high-volume or latency-sensitive ML products, a common production pattern is: **Streamlit as the UI layer calling a separate model-serving API** (FastAPI/TorchServe/SageMaker endpoints), rather than running inference inside Streamlit itself.

## 4. Key Considerations Checklist

**Licensing & commercial terms**

- Community Cloud is non-commercial only — plan on paid hosting from day one if revenue is involved.
- Streamlit itself is Apache-2.0 open source — no license fee for self-hosting, even commercially.

**Security**

- Authentication: `st.login()` (Streamlit ≥1.42, OIDC via Google, Entra, Auth0, Okta) or a reverse proxy; authorization logic must still be enforced server-side.
- Secrets via environment variables / platform secret managers — never in the repo.
- TLS everywhere; if self-hosting, WebSocket-enabled nginx config.
- Input validation; treat the app as you would any public web endpoint (injection, file upload limits, SSRF if fetching URLs).

**Performance & cost**

- Cache aggressively (`st.cache_resource` for model load — a loaded model per session × N sessions is your RAM killer).
- Watch memory per concurrent session; size instances accordingly.
- In SiS, suspend compute pools on a schedule — idle runtimes burn credits.
- Budget for cold starts (Snowflake container apps stop after 3 days without viewers; waking takes ~45s).

**Reliability & operations**

- CI/CD from Git (Streamlit Community Cloud deploys from GitHub; the same pattern works with Docker-based hosts).
- Health checks, logging, monitoring (Prometheus/Grafana or platform equivalents).
- Pin dependency versions; large ML dependencies (PyTorch, transformers) blow up container size and cold-start time — consider slim CPU-only builds.
- Sticky sessions or external state stores when running multiple replicas.

**Data & compliance**

- If the app touches PII, financial, or health data, Community Cloud is off-limits entirely; self-hosting or SiS (which inherits Snowflake's governance) is required.
- SiS keeps data inside your Snowflake perimeter — a genuine compliance advantage over shipping data to an external host.

**UX & product fit**

- Streamlit is code, not drag-and-drop — analysts who can't write Python can't maintain it.
- For pixel-perfect, consumer-grade front-ends, a custom React app may eventually replace Streamlit; treat it as the fastest path from prototype to internal/production data tool, not as a universal web framework.

## 5. Recommended Decision Path

1. **Prototype/demo** → Streamlit Community Cloud (free, non-commercial).
2. **Internal commercial tool, data in Snowflake** → Streamlit in Snowflake with container runtime + scheduled suspension.
3. **Customer-facing or custom-infra commercial app** → Dockerize, deploy on a PaaS or VPS behind nginx with auth (`st.login()` or proxy), add replicas with sticky sessions as traffic grows; move heavy inference to a dedicated API.
4. **High-traffic / strict latency / consumer product** → Streamlit for the internal-facing or MVP layer, or graduate to a custom front-end served by FastAPI.

The bottom line: Streamlit is genuinely production-viable for commercial data apps — the framework is free, and Snowflake's ownership provides an officially supported commercial hosting path — but the free Community Cloud is explicitly not licensed for business use, and scaling requires deliberate attention to caching, session memory, and replica architecture rather than being automatic.
