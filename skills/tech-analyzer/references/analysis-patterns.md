# Technical Analysis Patterns

This document provides detailed patterns and guidelines for performing deep technical analysis of open-source projects.

## Analysis Framework

### 1. Project Discovery

**What to look for:**
- Top-level project directories
- Project indicators: README.md, package.json, requirements.txt, etc.
- Documentation directories (docs/, documentation/)
- Configuration files that reveal project type

**Key files to examine:**
- `README.md` - Project overview and purpose
- `package.json` / `requirements.txt` / `Cargo.toml` - Dependencies and tech stack
- `CHANGELOG.md` - Evolution and recent changes
- `AGENTS.md` / `CONTRIBUTING.md` - Design guidelines and patterns
- `docs/` directory - Architecture documentation

### 2. Core Principles Extraction

**Questions to answer:**
1. What fundamental problem does this project solve?
2. What are the core design decisions?
3. What trade-offs were made and why?
4. What are the key abstractions?

**Analysis approach:**
- Read README for high-level purpose
- Review architecture documentation
- Examine source code structure (src/, lib/, etc.)
- Look for design patterns in code organization
- Identify extension/plugin mechanisms

### 3. Architecture Analysis

**Components to identify:**
- Main entry points
- Core modules/components
- Extension/plugin system
- Communication mechanisms
- Data flow patterns

**Documentation structure:**
- System overview diagram (text-based)
- Component descriptions
- Interaction patterns
- Extension points

### 4. Implementation Deep Dive

**Areas to cover:**
- Technology stack (languages, frameworks, libraries)
- Build and deployment processes
- Configuration mechanisms
- Testing approaches
- Development workflow

**Code analysis:**
- Review key source files
- Understand module organization
- Identify design patterns used
- Review extension/plugin implementation

### 5. Latest Updates Analysis

**Sources:**
- CHANGELOG.md
- Recent commits (if accessible)
- Release notes
- Documentation updates

**What to extract:**
- Recent architectural changes
- New features and their implementation
- Breaking changes
- Performance improvements
- Security updates

## Analysis Patterns by Project Type

### Node.js/TypeScript Projects

**Key files:**
- `package.json` - Dependencies, scripts, project metadata
- `tsconfig.json` - TypeScript configuration
- `src/` or `lib/` - Source code
- `extensions/` - Plugin system (if present)

**Analysis focus:**
- Module system (ESM vs CommonJS)
- Build process
- Extension/plugin architecture
- Type system usage

### Python Projects

**Key files:**
- `requirements.txt` or `pyproject.toml` - Dependencies
- `setup.py` or `setup.cfg` - Package configuration
- `src/` or package directory - Source code

**Analysis focus:**
- Package structure
- Dependency management
- Virtual environment setup
- Testing framework

### Multi-language Projects

**Analysis approach:**
- Identify language boundaries
- Understand inter-language communication
- Document platform-specific components
- Explain integration patterns

## Documentation Generation Guidelines

### Structure

Each analysis should produce three documents:

1. **Core Principles** (`<project>-core-principles.md`)
   - Fundamental design decisions
   - Key abstractions
   - Architectural patterns
   - Latest technical updates

2. **Architecture** (`<project>-architecture.md`)
   - System overview
   - Component descriptions
   - Data flow
   - Extension points
   - Communication patterns

3. **Implementation** (`<project>-implementation.md`)
   - Technology stack
   - Dependencies
   - Implementation patterns
   - Build and deployment
   - Configuration

### Writing Style

- **Be concise but comprehensive** - Focus on essence, not details
- **Use examples** - Code snippets when they illustrate principles
- **Reference specific files** - Point to actual source files/components
- **Use structured text** - Clear sections, bullet points, code blocks
- **Highlight innovations** - What makes this project unique?

### Quality Checklist

- [ ] Core principles clearly identified
- [ ] Architecture explained with component relationships
- [ ] Technology stack documented
- [ ] Extension mechanisms described
- [ ] Latest updates included
- [ ] Code examples provided where relevant
- [ ] References to source files included
- [ ] Clear, concise writing

## Example Analysis Workflow

1. **Initial Discovery**
   ```bash
   python scripts/analyze_project.py --project-dir project/ --output-dir sumup/
   ```

2. **Deep Dive Analysis**
   - Read README.md for overview
   - Review docs/ directory
   - Examine source code structure
   - Analyze key components
   - Review CHANGELOG.md for recent changes

3. **Documentation Generation**
   - Fill in core principles document
   - Complete architecture overview
   - Document implementation details
   - Add code examples
   - Include latest updates

4. **Review and Refine**
   - Ensure completeness
   - Verify accuracy
   - Check for clarity
   - Add missing details
