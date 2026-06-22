## What are AI Agents?

### Parts of an AI Agent

`LLM` - powers the reasoning behind the AI agents.

Reasoning means being able to identify the task requested by users, create a plan to perform that task and complete the action of that plan (This should go into a loop with some some conditionals if-else statements).

`Memory` - plays a critical role in AI agents by helping them remember user preferences and context during interactions. This enables agents to improve their responses over time.

Memory can be `short-term`, i.e. the context of the conversation between the user and the agent, or `long-term`, which is a collection of data that allows the agent to improve over time in completing the task.

`Tools` - This can be different services accessed by APIs that perform an action, data to help determine what action to take or different functions that we will run to send information to the AI agent.

And combining of all these things, an agent uses the LLM to recognise the task of the user would want to complete, identify the available tools needed to complete that task, and memory to gather the information and data that's needed to complete that task.

**AI agents** are autonomous systems that perceive their environment, reason about it, and take actions to achieve a goal — often in a loop, without human intervention at each step.

Unlike a simple LLM call (prompt → response), an agent can:

- **Plan** multi-step strategies to reach a goal
- **Use tools** (web search, code execution, APIs, databases)
- **Maintain memory** across steps (short-term and long-term)
- **Self-correct** by observing outcomes and retrying

The core loop is: **Perceive → Think → Act → Observe → Repeat**

---

## Best Use Cases

| Category                | Examples                                                    |
| ----------------------- | ----------------------------------------------------------- |
| **Automation**          | Email triage, report generation, data pipelines             |
| **Research**            | Web research, literature review, competitive analysis       |
| **Coding**              | Code generation, debugging, PR review (like GitHub Copilot) |
| **Customer Support**    | Multi-turn Q&A with CRM/DB tool access                      |
| **Data Analysis**       | Query DBs, run SQL/Python, summarize results                |
| **Operations**          | Infrastructure monitoring, alerting, remediation            |
| **Personal Assistants** | Scheduling, task management, multi-app workflows            |

---

## How to Start

### 1. Understand the building blocks

- **LLM** — the reasoning core (GPT-4o, Claude, Gemini, etc.)
- **Tools/Functions** — things the agent can call (APIs, code runners, search)
- **Memory** — context window (short-term) + vector store / DB (long-term)
- **Orchestrator** — the loop that connects planning, tool calls, and observation

### 2. Pick a framework

| Framework                 | Best for                                       |
| ------------------------- | ---------------------------------------------- |
| **LangChain / LangGraph** | General-purpose, Python-first, large ecosystem |
| **AutoGen (Microsoft)**   | Multi-agent conversations                      |
| **CrewAI**                | Role-based agent teams                         |
| **Semantic Kernel**       | .NET/Python, enterprise/Azure integration      |
| **OpenAI Assistants API** | Quickest start with built-in tools             |
| **Microsoft Foundry**     | End-to-end Azure-native agents                 |

### 3. Build a minimal agent (Python + OpenAI)

```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the web for current information",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the latest in AI agents?"}],
    tools=tools
)
```

### 4. Key concepts to learn next

- **ReAct** pattern (Reasoning + Acting)
- **RAG** (Retrieval-Augmented Generation) for long-term memory
- **Multi-agent systems** — agents delegating to sub-agents
- **Evals** — how to measure and improve agent reliability

---

The fastest way to experiment is the **OpenAI Assistants API** or **LangGraph** with a few tools wired up. Start simple: one agent, one tool, one task.

Think of it like a person doing a job:

---

### Short-term memory (Context Window)

> Like your **working memory** right now — what you're holding in your head during a single conversation.

When you chat with an AI agent, everything in the current conversation (your messages, the agent's replies, tool results) sits in the **context window**. It's fast and instantly available, but:

- It has a **size limit** (e.g. 128k tokens for GPT-4o)
- It **disappears** when the conversation ends — next session, it's gone

---

### Long-term memory (Vector Store / DB)

> Like a **notebook or filing cabinet** the agent can search through later.

When you need the agent to remember things _across sessions_ or search through _large amounts of data_ (docs, past conversations, a knowledge base), you store that information externally. A **vector store** is a special database that lets the agent search by _meaning_ (not just exact keywords).

Example: You tell an agent your coding preferences on day 1. On day 5, it searches its vector store and retrieves those preferences — even though the original conversation is long gone.

---

### Simple analogy side-by-side

|                         | Short-term            | Long-term                               |
| ----------------------- | --------------------- | --------------------------------------- |
| Like...                 | RAM in a computer     | Hard drive                              |
| Capacity                | Limited               | Large                                   |
| Speed                   | Instant               | Requires a search                       |
| Survives after session? | No                    | Yes                                     |
| Example                 | Current chat messages | User profile, past docs, knowledge base |

---

**In practice:** most beginner agents only use short-term memory. Long-term memory (RAG + vector stores) is the next step once you need the agent to "remember" things or work with large document sets.

---

### Agentic Framework

> What are Agentic frameworks?
> Why use them?
> Which one to use?

## Agentic Frameworks

**What they are**

Agentic frameworks are libraries/platforms that let you build AI systems where LLMs don't just respond once — they **plan, take actions, use tools, and iterate** until a goal is achieved. The LLM acts as a "reasoning engine" that decides _what_ to do next.

Core components they provide:

- **Agent loop** — perceive → think → act → observe → repeat
- **Tool/function calling** — agents invoke code, APIs, search, etc.
- **Memory** — short-term (context) and long-term (vector stores, DBs)
- **Orchestration** — coordinating multiple agents or steps
- **State management** — tracking what's been done across turns

---

**Why use them**

| Without a framework         | With a framework                   |
| --------------------------- | ---------------------------------- |
| Manual prompt chaining      | Automatic loop + retry logic       |
| Hand-wired tool calls       | Declarative tool registration      |
| No shared state             | Built-in memory/context management |
| Single-agent only           | Multi-agent coordination           |
| Roll your own observability | Tracing/logging built in           |

They handle the boilerplate so you focus on _what_ your agent does, not _how_ the loop works.

---

**Which one to use**

| Framework               | Best for                                                           |
| ----------------------- | ------------------------------------------------------------------ |
| **LangGraph**           | Complex, stateful, multi-agent workflows with fine-grained control |
| **LangChain**           | Rapid prototyping, large ecosystem, many integrations              |
| **AutoGen** (Microsoft) | Conversational multi-agent systems, code execution agents          |
| **CrewAI**              | Role-based multi-agent teams, simpler API                          |
| **Semantic Kernel**     | .NET/Python, enterprise Microsoft stack (Azure OpenAI)             |
| **OpenAI Agents SDK**   | Lightweight, native OpenAI tool-calling, low overhead              |
| **Haystack**            | RAG-heavy pipelines, document processing                           |

**Rule of thumb:**

- Starting out / simple tasks → **OpenAI Agents SDK** or **CrewAI**
- Complex state machines / production → **LangGraph**
- Microsoft/Azure ecosystem → **Semantic Kernel** or **AutoGen**
- Heavy RAG / search → **Haystack**

## Single-Agent vs Multi-Agent (Beginner Explanation)

### Single Agent — "One person doing everything"

Imagine you ask **one employee** to plan your entire vacation:

- They search for flights
- They book a hotel
- They find restaurants
- They create the itinerary

One AI agent, one loop, handles everything start to finish.

```
You → [Agent] → thinks → uses tools → thinks → responds → You
```

**Good for:** Simple, focused tasks. Easy to build and debug.  
**Bad for:** Complex tasks — it can lose track, hit context limits, or get overwhelmed.

---

### Multi-Agent — "A team of specialists"

Now imagine a **travel agency with a team**:

- A **Flight Specialist** only books flights
- A **Hotel Specialist** only finds accommodation
- A **Manager** coordinates them and gives you the final plan

Each agent is an expert at one thing. A **coordinator/orchestrator** agent delegates tasks to the right specialist.

```
You → [Orchestrator Agent]
           ├── [Research Agent]  → searches the web
           ├── [Coder Agent]     → writes/runs code
           └── [Writer Agent]    → drafts the final report
                        ↓
                    You get result
```

**Good for:** Complex, long tasks that can be split up. Faster (agents work in parallel). Each agent stays focused.  
**Bad for:** Overkill for simple tasks. Harder to build and debug.

---

### Quick Comparison

|                | Single Agent                          | Multi-Agent                                             |
| -------------- | ------------------------------------- | ------------------------------------------------------- |
| **Structure**  | One agent, all tasks                  | Many agents, each specialized                           |
| **Complexity** | Simple                                | Complex                                                 |
| **Speed**      | Sequential                            | Can run in parallel                                     |
| **Use case**   | Q&A, summarization, simple automation | Research pipelines, software dev, complex workflows     |
| **Example**    | ChatGPT answering a question          | AutoGen writing _and_ testing code with separate agents |

---

**The analogy that sticks:**

> Single agent = a Swiss Army knife. Multi-agent = a surgical team. Both cut — but one is better for open-heart surgery.
