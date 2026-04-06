# Mindspeller Chatbot: Challenge Report

## Problem Statement

The original requirement was to build a chatbot inside the Mindspeller project while respecting a strict compatibility constraint: the backend had to work on an older Python runtime, specifically Python 3.8 or earlier-compatible syntax and dependencies. The key challenge was that many modern AI client libraries now target newer Python versions, which makes direct SDK-based integration risky when older runtime support is mandatory.

In other words, the task was not just to build a chatbot. The task was to build a chatbot that could be implemented, tested, and deployed without depending on a modern Python-only stack.

## What Made This Challenging

1. Many official AI SDKs require Python 3.10+ or newer.
2. Older Python environments often break when libraries introduce newer syntax or dependency requirements.
3. A chatbot still needs reliable model access, request handling, CORS, and deployment support.
4. The solution had to remain simple enough to run locally, test in CI, and deploy on a platform where runtime version can be pinned.

## Research-Based Approach

Instead of depending on a provider-specific Python SDK, the backend uses direct HTTP requests to Groq's OpenAI-compatible endpoint. That decision was intentional.

The reasoning was:

- HTTP and JSON are stable across Python versions.
- `requests` is a widely used library that remains compatible with older Python releases.
- Avoiding the official SDK reduces version lock-in.
- The same API behavior can be achieved without sacrificing functionality.

This is the core compatibility strategy used in the implementation.

## Requirements Interpreted as Engineering Constraints

The project was implemented with the following constraints in mind:

- Backend must be Flask-based.
- Backend must use `requests`, not the `groq` package.
- API key must come from `.env` through `python-dotenv`.
- Python syntax must stay compatible with 3.7/3.8.
- Frontend must be Next.js with TypeScript.
- Frontend must use Tailwind CSS.
- Chat history must be maintained in React state.
- Deployment must work with separate backend and frontend services.
- Production setup should preserve Python 3.8 on the backend.

## Implementation Summary

### Backend

The backend was implemented in Flask with one main chat endpoint:

- `POST /api/chat`

It accepts:

```json
{
  "message": "user message",
  "history": []
}
```

The backend then:

1. loads `GROQ_API_KEY` from `.env`,
2. builds a message history array,
3. calls Groq's API using `requests.post`,
4. extracts the assistant reply,
5. returns updated history back to the client.

This approach keeps the backend lightweight and compatible with older Python.

### Frontend

The frontend was implemented as a Next.js TypeScript chat interface with:

- message bubbles,
- input box,
- send button,
- loading indicator,
- error display,
- chat history stored in React state.

The frontend was also changed to read the backend URL from `NEXT_PUBLIC_BACKEND_URL`, which allows local development and production deployment to use the same codebase without hardcoding localhost.

### Deployment Support

To ensure Python 3.8 remains the runtime in production, the backend includes a Dockerfile based on `python:3.8-slim`. That is the practical deployment pin.

In parallel, a GitHub Actions workflow was added to verify compatibility on Python 3.8 and Python 3.11. This gives a cloud-based proof that the codebase still works with the older runtime even if the local machine only has a newer Python version installed.

## How the Challenge Was Solved

The solution was built around compatibility-first architecture.

Instead of asking whether the latest SDK could be forced onto Python 3.8, the implementation asked a better question: what is the smallest stable interface needed to talk to the model provider?

The answer was:

- HTTP request to the chat completions endpoint,
- stable Python libraries,
- environment-based configuration,
- pinned runtime in Docker,
- CI verification across Python versions.

That combination solved the original challenge without compromising on functionality.

## Final Outcome

The result is a chatbot application that:

- runs locally,
- supports older Python compatibility,
- avoids the official Groq SDK,
- is deployable on standard hosting platforms,
- has a clear verification path through CI,
- and can be explained as a deliberate engineering choice rather than a workaround.

## Short Summary

This project demonstrates how to build a modern chatbot while respecting an older Python runtime requirement. The main idea was to bypass SDK dependency risk and implement the LLM connection at the HTTP layer. That made the solution more durable, more compatible, and easier to defend in a technical review.
