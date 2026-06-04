"""Simulate Codabench ingestion locally."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

INGESTION = ROOT / "codabench" / "ingestion_program"
PARTICIPANT = ROOT / "participant_starter"
DATA = ROOT / "competition_data"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        program = tmp / "program"
        ingested = tmp / "ingested_program"
        input_data = tmp / "input_data"
        output_dir = tmp / "output"

        shutil.copytree(INGESTION / "sbrp_env", program / "sbrp_env", dirs_exist_ok=True)
        for f in ["ingestion.py", "eval_runner.py"]:
            src = INGESTION / f if (INGESTION / f).exists() else ROOT / "sbrp_env" / f.replace("ingestion", "eval_runner")
        shutil.copy(INGESTION / "ingestion.py", program / "ingestion.py")
        shutil.copytree(ROOT / "sbrp_env", program / "sbrp_env", dirs_exist_ok=True)
        shutil.copy(PARTICIPANT / "agent.py", ingested / "agent.py")
        shutil.copytree(DATA / "graph_cache", input_data / "graph_cache")
        shutil.copy(DATA / "env_config.json", input_data / "env_config.json")
        shutil.copy(DATA / "seeds" / "dev_seeds.json", input_data / "eval_seeds.json")
        output_dir.mkdir()

        # Patch paths for local run
        code = (program / "ingestion.py").read_text(encoding="utf-8")
        code = code.replace('Path("/app/program")', f'Path(r"{program}")')
        code = code.replace('Path("/app/ingested_program")', f'Path(r"{ingested}")')
        code = code.replace('Path("/app/input_data")', f'Path(r"{input_data}")')
        code = code.replace('Path("/app/output")', f'Path(r"{output_dir}")')
        exec(compile(code, "ingestion.py", "exec"), {"__name__": "__main__"})

        with open(output_dir / "results.json", encoding="utf-8") as f:
            print(json.load(f))


if __name__ == "__main__":
    main()
