---
name: tech-analyzer
description: Analyze open-source technologies in the project directory to extract core technical principles and architecture. Generate comprehensive technical documentation summarizing the latest technologies, their core principles, implementation details, and architectural patterns. Use when the user wants to understand the technical essence of projects in the project/ directory, extract core principles, or generate technical summaries in the sumup/ directory.
---

# Tech Analyzer

## Overview

This skill analyzes open-source technologies in the `project/` directory, extracts their core technical principles, architecture patterns, and implementation details, then generates comprehensive technical documentation in the `sumup/` directory.

## Workflow

### 1. Discover Projects

Scan the `project/` directory to identify technology projects:
- Look for top-level directories (e.g., `project/clawdbot/`)
- Identify project type by examining key files (README.md, package.json, etc.)
- List all discovered projects

### 2. Analyze Each Project

For each discovered project, perform deep analysis:

**Project Identification:**
- Read README.md to understand project purpose
- Check package.json/requirements.txt for dependencies and tech stack
- Review project structure to understand organization

**Core Principles Extraction:**
- Identify architectural patterns (e.g., gateway pattern, plugin system, multi-channel architecture)
- Extract core design decisions and trade-offs
- Understand data flow and component interactions
- Identify key abstractions and interfaces

**Technical Deep Dive:**
- Analyze source code structure (src/, extensions/, etc.)
- Understand extension/plugin mechanisms
- Review configuration and deployment patterns
- Identify communication protocols and APIs

**Documentation Review:**
- Read docs/ for architecture explanations
- Review AGENTS.md or similar for design guidelines
- Check CHANGELOG.md for evolution and recent changes

### 3. Generate Technical Documentation

Create structured markdown documents in `sumup/` directory:

**Document Structure:**
```
sumup/
├── <project-name>-core-principles.md    # Core technical principles
├── <project-name>-architecture.md      # Architecture overview
└── <project-name>-implementation.md    # Implementation details
```

**Content Requirements:**
- **Core Principles**: Fundamental design decisions, architectural patterns, key abstractions
- **Architecture**: System components, data flow, interaction patterns
- **Implementation**: Key technologies, frameworks, patterns used
- **Latest Updates**: Recent changes from CHANGELOG or recent commits

### 4. Analysis Script Usage

Use `scripts/analyze_project.py` to automate project discovery and initial analysis:

```bash
python scripts/analyze_project.py --project-dir project/ --output-dir sumup/
```

The script will:
- Discover all projects in the directory
- Extract basic metadata (name, description, tech stack)
- Generate initial analysis structure
- Create markdown files ready for detailed content

## Analysis Guidelines

### Focus Areas

1. **Core Principles**: What are the fundamental design decisions? What problems does this solve?
2. **Architecture**: How is the system structured? What are the main components?
3. **Extension Mechanism**: How does the system allow extensions/plugins?
4. **Communication Patterns**: How do components communicate?
5. **Technology Stack**: What technologies, frameworks, and patterns are used?
6. **Latest Innovations**: What are the most recent technical updates?

### Documentation Quality

- Be concise but comprehensive
- Focus on technical essence, not surface details
- Include code examples when they illustrate core principles
- Reference specific files/components when relevant
- Use diagrams or structured text to explain architecture
- Highlight unique or innovative approaches

## Example Analysis: Clawdbot

For a project like Clawdbot, the analysis should cover:

**Core Principles:**
- Gateway-based control plane architecture
- Multi-channel messaging abstraction
- Skill-based extensibility
- Local-first design

**Architecture:**
- Gateway WebSocket control plane
- Channel extensions (WhatsApp, Telegram, Slack, etc.)
- Agent runtime with tool streaming
- Session management and routing

**Implementation:**
- TypeScript/Node.js core
- Extension system with workspace packages
- Browser automation via CDP
- Voice and Canvas capabilities

## Output Format

Generate documents in Markdown with clear sections:

```markdown
# <Project Name> - Core Technical Principles

## Overview
Brief description of the project and its purpose.

## Core Design Principles
1. Principle 1: Explanation
2. Principle 2: Explanation
...

## Architecture Overview
[Architecture description]

## Key Technologies
- Technology 1: Purpose
- Technology 2: Purpose
...

## Latest Updates
[Recent technical changes]
```

## Resources

### scripts/analyze_project.py
Automated project discovery and initial analysis script. See script documentation for usage.

### references/analysis-patterns.md
Detailed patterns and guidelines for technical analysis.
