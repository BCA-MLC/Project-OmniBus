"""
Package the Codabench competition bundle and participant starter zip.

Run from repo root:
  python scripts/build_codabench_bundle.py
"""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
CB = ROOT / "codabench"
DATA = ROOT / "competition_data"
STARTER = ROOT / "participant_starter"


def zip_dir(source_dir: Path, zip_path: Path, arc_prefix=""):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in source_dir.rglob("*"):
            if file.is_file():
                arc = Path(arc_prefix) / file.relative_to(source_dir)
                zf.write(file, arc.as_posix())


def zip_files(files: list[tuple[Path, str]], zip_path: Path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, arc in files:
            zf.write(src, arc)


def prepare_ingestion_program(staging: Path):
    dest = staging / "ingestion_program"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(CB / "ingestion_program", dest)
    shutil.copytree(ROOT / "sbrp_env", dest / "sbrp_env")


def prepare_input_data(seeds_name: str, staging: Path):
    dest = staging / "input_data"
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DATA / "graph_cache", dest / "graph_cache")
    shutil.copy(DATA / "env_config.json", dest / "env_config.json")
    shutil.copy(DATA / "seeds" / seeds_name, dest / "eval_seeds.json")


def main():
    if not (DATA / "graph_cache" / "time_matrix.npy").exists():
        raise SystemExit("Run: python scripts/precompute_competition_data.py")

    OUT.mkdir(exist_ok=True)
    staging = OUT / "_staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()

    # Ingestion + scoring zips
    prepare_ingestion_program(staging)
    zip_dir(staging / "ingestion_program", OUT / "ingestion_program.zip")

    zip_dir(CB / "scoring_program", OUT / "scoring_program.zip")

    # Input data per phase
    for phase, seeds in [("dev", "dev_seeds.json"), ("final", "final_seeds.json")]:
        phase_dir = staging / f"input_{phase}"
        if phase_dir.exists():
            shutil.rmtree(phase_dir)
        prepare_input_data(seeds, phase_dir)
        zip_dir(phase_dir / "input_data", OUT / f"input_data_{phase}.zip")

    # Reference data (config only — for organizer visibility)
    ref_dir = staging / "reference"
    ref_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(DATA / "env_config.json", ref_dir / "env_config.json")
    zip_dir(ref_dir, OUT / "reference_data.zip")

    # Example solution = participant agent only
    zip_files([(STARTER / "agent.py", "agent.py")], OUT / "example_solution.zip")

    # Participant starter kit (for download — not part of competition bundle)
    starter_files = [
        (STARTER / "agent.py", "agent.py"),
        (STARTER / "HOW_TO_SUBMIT.md", "HOW_TO_SUBMIT.md"),
        (STARTER / "run_submission.py", "run_submission.py"),
    ]
    zip_files(starter_files, OUT / "participant_starter_kit.zip")

    # Full competition bundle
    bundle = staging / "bundle"
    bundle.mkdir()
    for name in [
        "competition.yaml",
        "overview.md",
        "evaluation.md",
        "terms_and_conditions.md",
        "data.md",
    ]:
        shutil.copy(CB / name, bundle / name)

    shutil.copy(OUT / "ingestion_program.zip", bundle / "ingestion_program.zip")
    shutil.copy(OUT / "scoring_program.zip", bundle / "scoring_program.zip")
    shutil.copy(OUT / "reference_data.zip", bundle / "reference_data.zip")
    shutil.copy(OUT / "example_solution.zip", bundle / "example_solution.zip")

    phases = bundle / "phases"
    (phases / "dev").mkdir(parents=True)
    (phases / "final").mkdir(parents=True)
    shutil.copy(OUT / "input_data_dev.zip", phases / "dev" / "input_data.zip")
    shutil.copy(OUT / "input_data_final.zip", phases / "final" / "input_data.zip")

    # Minimal logo placeholder (1x1 PNG)
    logo = bundle / "logo.png"
    if not (CB / "logo.png").exists():
        logo.write_bytes(
            bytes.fromhex(
                "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
                "0000000a49444154789c6300010000050001b80cc6d20000000049454e44ae426082"
            )
        )
    else:
        shutil.copy(CB / "logo.png", logo)

    zip_dir(bundle, OUT / "hackensack_sbrp_competition.zip")
    shutil.rmtree(staging)

    print(f"Built: {OUT / 'hackensack_sbrp_competition.zip'}")
    print(f"Built: {OUT / 'participant_starter_kit.zip'}")
    print("Upload hackensack_sbrp_competition.zip to Codabench > Benchmark > Management > Upload")


if __name__ == "__main__":
    main()
