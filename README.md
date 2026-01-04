# AI-First Digital Marketing Automation Prototype

This repository contains a local prototype that demonstrates an AI-first, agent-based approach to automating a common digital marketing workflow.

The system accepts a product image and basic product information, generates marketing copy using an LLM, applies approved text onto images, and produces platform-specific creatives suitable for social media platforms.

This is a prototype built to showcase system design, agent orchestration, and practical AI usage under time constraints. It is not a production-ready system.

---

## Problem Overview

Digital marketing workflows often involve repetitive manual steps such as:
- Writing multiple headline options
- Adapting captions per platform
- Ensuring text fits correctly across different image formats

This prototype explores how these steps can be automated using AI while retaining a human-in-the-loop approval process.

---

## End-to-End Workflow

1. User uploads a product image
2. User provides:
   - Product name
   - Key features
   - Brand tone
3. AI generates:
   - A structured campaign brief
   - Three headline options
   - Two captions per platform (LinkedIn, Instagram, Facebook)
4. User reviews and approves:
   - One headline
   - One caption per platform
5. AI decides visual layout rules for the approved headline
6. System generates resized creatives with text overlays
7. Final assets are exported locally

Publishing to external platforms is intentionally disabled for this prototype to keep the demo deterministic and reliable.

---

## Architecture

The system is built using a small set of single-responsibility agents. Each agent produces structured outputs that are consumed by downstream agents.
            User Input
                |
                v
            Copy Agent
                |
                v
            Layout Agent
                |
                V
            Resize Agent
                |
                v
            publisher Agent


Each agent operates independently and communicates via structured data (JSON-like dictionaries).

---

## Agent Responsibilities

### CopyAgent
- Accepts raw product inputs (name, features, tone)
- Generates:
  - A campaign brief (internal)
  - Three headline options
  - Two captions per platform (LinkedIn, Instagram, Facebook)
- Uses a single LLM call to reduce cost and latency

### LayoutAgent
- Acts as a creative decision-maker
- Decides:
  - Text position
  - Font weight
  - Background style
  - Text color
  - Safe margins
- Returns strict JSON to ensure predictable rendering

### ResizeAgent
- Performs deterministic image processing
- Resizes images to platform-specific dimensions
- Applies text overlays using layout rules
- Ensures text is not clipped across aspect ratios

### PublisherAgent
- Represents the publishing boundary
- For this prototype:
  - Writes a publish manifest
  - Does not call external APIs
- Designed so real publishing can be enabled with minimal changes

---

## Human-in-the-Loop Design

The system intentionally includes a review step:
- User selects one headline
- User selects one caption per platform

This mirrors real-world marketing workflows and avoids fully autonomous publishing.

---

## Logging and Traceability

Each agent logs:
- Inputs received
- Decisions made
- Outputs produced

Raw prompts and LLM chain-of-thought are not logged.  
Logs are intended to show agent intent and reasoning at a high level.

---

## Technology Stack

- Python 3.11
- Streamlit (UI)
- Google Gemini API (LLM)
- Pillow (image processing)
- Custom lightweight logger

No database is used. All state is held in memory for simplicity.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd AgentProject
