"""
Run on a batch of SWE-bench as jsonl format.

[cyan][bold]=== BASIC OPTIONS ===[/bold][/cyan]

  -h --help           Show help text and exit
  --help_option      Print specific help text and exit

[cyan][bold]=== EXAMPLES ===[/bold][/cyan]

Basic usage: Run over a [bold][cyan]SWE-bench lite[/bold][/cyan][green]:

sweagent run-json problem_path \\
    --config config/default.yaml \\
    --agent.model.name gpt-4o \\ # configure model
    --num_worker 1
[/green]
"""

import sys
from pathlib import Path
import json
from tqdm import tqdm

from sweagent.run.common import BasicCLI, ConfigHelper
from sweagent.run.run_batch import run_from_config, RunBatchConfig
from sweagent.utils.files import load_file


def run_from_cli(args: list[str] | None = None):
    if args is None:
        jsonl_path = sys.argv[2]
        args = [sys.argv[1]] + sys.argv[3:]
    else:
        jsonl_path = args[0]
        args = args[1:]

    assert __doc__ is not None

    help_text = (  # type: ignore
        __doc__ + "\n[cyan][bold]=== ALL THE OPTIONS ===[/bold][/cyan]\n\n" + ConfigHelper().get_help(RunBatchConfig)
    )

    config = BasicCLI(RunBatchConfig, help_text=help_text).get_config(args)
    jsonl_to_prob(jsonl_path, config.instances.path)
    run_from_config(config)  # type: ignore


def jsonl_to_prob(jsonl_path: str|Path, save_path:str|Path):
    rows = load_file(jsonl_path)

    problems = []
    for row in tqdm(rows, total=len(rows), desc="parsing problems"):
        problem = {"env":
                    {"deployment":{
                        "type": "docker",
                        "image" : row["docker_image"],
                        "python_standalone_dir":"/root",
                        "docker_args": ["-e", "JAVA_HOME=/opt/java/openjdk","-e", "PATH=/opt/java/openjdk/bin:/root/python3.11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"]
                    }, 
                    "repo":{
                        "type":"github",
                        "github_url": "https://github.com/" + row["repo"],
                        "base_commit": row["base_commit"]
                    }},
                    "problem_statement":{
                        "type":"text",
                        "text":row["PR_Title"],
                        "id": row["instance_id"]
                    }
                    }
        problems.append(problem)

    save_path.write_text(json.dumps(problems, indent=2))

if __name__ == "__main__":
    run_from_cli()
