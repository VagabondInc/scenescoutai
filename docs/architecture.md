# Architecture

The research toolkit is organized around a simple data flow.

```text
Script
  -> Parser
  -> Visual Beat Planner
  -> Archive Metadata Matcher
  -> Prompt Candidate Generator
  -> Package Plan JSON
```

## Components

### Script Parser

Breaks a news script into structured sections such as anchor intro, reporter tracks, sound bites, and anchor tags.

### Visual Beat Planner

Creates a visual intent for each script section.

### Archive Metadata Matcher

Compares script context against metadata extracted from a video archive.

### Prompt Candidate Generator

Creates fal-compatible prompt candidates only when archive footage is missing or insufficient.

### Package Plan

Outputs a structured JSON file for editorial review.
