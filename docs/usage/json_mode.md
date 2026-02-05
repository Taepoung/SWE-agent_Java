# JSON Mode Usage Guide

## 1. Overview

JSON Mode is an execution mode **built on top of Batch Mode**.  
It is designed for cases where the problem set is provided in a **structured format** such as JSON, JSONL, or YAML.

In JSON Mode, the given problem set is **automatically converted into an `expert_instance`-based batch input** and then executed.  
This allows users to directly run structured datasets without manually converting them into batch specifications.

---

## 2. Data Format and Prerequisites

JSON Mode is **designed specifically for SWE-bench–style datasets**.  
Therefore, the input problem set must conform to the SWE-bench data schema and assumptions.

---

## 3. Required Fields (SWE-bench Format)

Each problem entry **must include the following required keys**.  
If any of these fields are missing, the problem **cannot be executed** in JSON Mode.

### 3.1 Mandatory Keys

- `repo`  
  The target repository identifier (e.g., `owner/repository`).

- `instance_id`  
  A unique identifier for the problem instance.

- `base_commit`  
  The base commit hash representing the initial state of the repository.

- `PR_Title`  
  A short title or description of the problem, typically derived from the pull request or issue title.

- `docker_image`  
  The Docker image used to execute and evaluate the problem.

> All five fields are **strictly required** for every problem entry.  
> If the key names differ, they must be **revised either by modifying the code or by updating the documentation accordingly**.


---

## 4. Docker Image Requirement

Each problem **must explicitly specify a Docker image** via the `docker_image` field.

- JSON Mode executes each problem inside an isolated Docker container
- The specified image must be:
  - Pre-built and locally available, or
  - Pullable from a Docker registry at runtime

Problems without a valid `docker_image` entry **will fail at execution time**.

---

## 5. Key Features of JSON Mode

- Extension of Batch Mode
- Supports structured input formats:
  - `json`
  - `jsonl`
  - `yaml`
- Automatically converts SWE-bench–formatted problems into `expert_instance` batches
- Executes each problem in an isolated Docker environment

---

## 6. Usage

### 6.0.0 Install

```bash
git clone https://github.com/SWE-agent/SWE-agent.git
pip install -e .
```
### 6.0.1 Environment Variable
```bash
# Remove the comment '#' in front of the line for all keys that you have set
OPENAI_API_BASE="https://your-custom-api.com/v1"
GITHUB_TOKEN='GitHub Token for access to private repos'
OPENAI_API_KEY='OpenAI API Key Here if using OpenAI Model'
ANTHROPIC_API_KEY='Anthropic API Key Here if using Anthropic Model'
TOGETHER_API_KEY='Together API Key Here if using Together Model'
```
### 6.0.1 Supported Model
Model should be supported by litellm.
[supported list](https://docs.litellm.ai/docs/providers)

### 6.1 Basic Command

```bash
sweagent run-json <problem_file_path> \
    --agent.model.name gpt-4o-mini \
    --config <expert_config_file> \
```

All command-line arguments other than the problem file path and JSON-specific options are identical to those used in Batch Mode.
