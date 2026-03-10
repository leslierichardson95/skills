# Evaluation Guide

Create evaluations that measure how effectively LLMs use your MCP server tools.

## Evaluation Criteria

Every evaluation question should be:

| Criterion | Meaning |
|-----------|---------|
| **Independent** | Not dependent on other questions or prior state |
| **Read-only** | Uses only non-destructive operations |
| **Complex** | Requires multiple tool calls and reasoning |
| **Realistic** | Based on real use cases for the server |
| **Verifiable** | Has a single, clear, deterministic answer |
| **Stable** | Answer won't change over time |

## XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<evaluation>
  <metadata>
    <server_name>MyMcpServer</server_name>
    <version>1.0.0</version>
    <created_date>2026-03-01</created_date>
  </metadata>

  <qa_pair>
    <question>
      Using the user search tool, find all users in the "engineering" team
      who joined after 2024. What is the email domain most commonly used
      by these users?
    </question>
    <answer>company.com</answer>
    <difficulty>medium</difficulty>
    <required_tools>search_users, list_teams</required_tools>
  </qa_pair>

  <qa_pair>
    <question>
      Find the project with the most active contributors in the last month.
      What is the project's internal ID?
    </question>
    <answer>proj-42</answer>
    <difficulty>hard</difficulty>
    <required_tools>list_projects, get_project_stats</required_tools>
  </qa_pair>

  <!-- Aim for 10 questions -->
</evaluation>
```

## Creating Good Questions

### Good question patterns

- **Multi-step retrieval**: "Find X, then use that to look up Y" — requires chaining tool calls
- **Aggregation**: "Which category has the most items matching criteria Z?" — requires gathering and comparing
- **Cross-referencing**: "Find the overlap between set A and set B" — uses multiple tools

### Examples

**Good:**
- "Find the user who created the most issues in 'backend' this year. What is their username?"
- "Which team has the highest average code review turnaround time? Return the team name."
- "How many open issues are labeled 'critical' and assigned to users in the 'security' team?"

**Bad:**
- "What is 2 + 2?" — doesn't use tools
- "List all users" — too simple, single tool call, no reasoning
- "Create a new issue…" — not read-only, mutates state
- "What's the current weather?" — answer changes over time
- "Tell me about the system" — no verifiable answer

## Evaluation Process

1. **Explore available data** — use read-only tools to understand what data exists
2. **Draft questions** that require reasoning across multiple tool calls
3. **Solve each question manually** to confirm the answer is correct and deterministic
4. **Verify stability** — run the evaluation twice to ensure answers are consistent
5. **Aim for 10 questions** with a mix of medium and hard difficulty

## Difficulty Guidelines

| Difficulty | Tool Calls | Description |
|------------|-----------|-------------|
| Easy | 1 | Single tool, direct answer |
| Medium | 2-3 | Chain tools, simple reasoning |
| Hard | 4+ | Multiple tools, aggregation, cross-referencing |
