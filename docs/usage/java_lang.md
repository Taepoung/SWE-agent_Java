
# Mandatory Configuration for Java Problems

When using **JSON Mode with Java repositories**, the following configuration **must be provided** to ensure correct execution.



### 1. `python_standalone_dir`

```json
"python_standalone_dir": "/root"
````

* Enables the **standalone Python runtime** required by `swerex-remote`.
* Necessary because most Java Docker images do not include Python by default.

---

### 2. `docker_args` (PATH Injection)

```json
"docker_args": [
  "-e",
  "PATH=/root/python3.11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
]
```

* Ensures that the standalone Python binaries are **discoverable via `PATH`**.
* Required to correctly resolve executables that rely on:

```bash
#!/usr/bin/env python3
```

---

### 3. `post_startup_commands` (Install System Python)

```json
"post_startup_commands": [
  "apt-get update",
  "apt-get install -y python3"
]
```

* Installs a **system-level `python3`** inside the container.
* Guarantees compatibility with tools that depend on `env python3`.

---

## 3. Complete Example (Java / SpotBugs)

```json
{
  "env": {
    "deployment": {
      "type": "docker",
      "image": "<docker image>",
      "python_standalone_dir": "/root",
      "docker_args": [
        "-e",
        "PATH=/root/python3.11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
      ]
    },
    "repo": {
      "type": "github",
      "github_url": "github_url",
      "base_commit": "base_commit"
    }
  },
  "post_startup_commands": [
    "apt-get update",
    "apt-get install -y python3"
  ],
  "problem_statement": {
    "type": "text",
    "id": "problem id",
    "text": "problem statement"
  }
}
```