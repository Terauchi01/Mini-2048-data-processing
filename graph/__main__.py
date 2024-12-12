import argparse
import json
import re
from pathlib import Path

from . import accuracy, error_abs, error_rel, scatter, survival

BASE_DIR = Path(__file__).resolve().parent
board_dir = BASE_DIR.parent / "board_data"
board_data_dirs = [d for d in board_dir.iterdir() if d.is_dir()]
__version__ = "1.0.0"


def read_config(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


def write_config(path: Path, config: dict) -> None:
    path.write_text(json.dumps(config, indent=4, ensure_ascii=False), "utf-8")


class PlayerData:
    def __init__(self, target_dir: Path):
        self.name = target_dir.name
        self.target_dir = target_dir
        self.pp_dir = self.target_dir.parent / "PP"

    @property
    def state_file(self):
        state_file = self.target_dir / "state.txt"
        if not state_file.exists():
            raise FileNotFoundError(f"{state_file}が存在しません。")
        return state_file

    @property
    def eval_file(self):
        eval_file = self.target_dir / "eval.txt"
        if not eval_file.exists():
            raise FileNotFoundError(f"{eval_file}が存在しません。")
        return eval_file

    @property
    def pp_eval_state(self):
        pp: Path = self.pp_dir / f"eval-state-{self.name}.txt"
        if not pp.exists():
            raise FileNotFoundError(f"{pp}が存在しません。")
        return pp

    @property
    def pp_eval_after_state(self):
        pp: Path = self.pp_dir / f"eval-after-state-{self.name}.txt"
        if not pp.exists():
            raise FileNotFoundError(f"{pp}が存在しません。")
        return pp


def get_config():
    if config_path.exists():
        config = read_config(config_path)
        # config["labels"]に存在しないディレクトリがあれば追加
        for d in board_data_dirs:
            if d.name not in config["labels"]:
                config["labels"][d.name] = d.name
    else:
        config = {"labels": {d.name: d.name for d in board_data_dirs}}
    write_config(config_path, config)
    return config


def get_files():
    data = [
        PlayerData(d)
        for d in board_data_dirs
        if re.search(intersection_match, str(d))
        and not re.search(exclude_match, str(d))
    ]
    pp_eval_files = [d.pp_eval_state for d in data]
    pp_eval_after_files = [d.pp_eval_after_state for d in data]
    pr_eval_files = [d.eval_file for d in data]
    state_files = [d.state_file for d in data]
    return pp_eval_files, pp_eval_after_files, pr_eval_files, state_files


arg_parser = argparse.ArgumentParser(
    prog="graph",
    usage="uv run python -m %(prog)s [options]",
    description="指定したオプションに応じてグラフを描画するプログラム。詳細はREADME.mdを参照。",
)
arg_parser.add_argument(
    "graph",
    choices=["acc", "err-rel", "err-abs", "surv", "scatter"],
    help="実行するグラフを指定する。",
)
arg_parser.add_argument(
    "--output",
    "-o",
    type=str,
    help="出力するファイルを指定する。",
)
file_group = arg_parser.add_mutually_exclusive_group()
file_group.add_argument(
    "--exclude",
    nargs="+",
    default=["PP"],
    help="除外するディレクトリ名を指定する。",
)
file_group.add_argument(
    "--intersection",
    nargs="+",
    default=[],
    help="対象を指定したディレクトリのみに絞る。",
)
arg_parser.add_argument(
    "--config",
    type=str,
    help="設定ファイルのパスを指定する。現在は未使用。",
)
arg_parser.add_argument(
    "--version",
    "-v",
    action="version",
    version=f"""
    %(prog)s version {__version__}
""",
)

args = arg_parser.parse_args()
exclude_match = re.compile("|".join(args.exclude + ["sample"]))
intersection_match = re.compile("|".join(args.intersection))
dirs = [d for d in board_data_dirs if not re.search(exclude_match, str(d))]
output_dir = BASE_DIR.parent / "output"
output_dir.mkdir(exist_ok=True)

config_path = BASE_DIR / "config.json"
pp_eval_files, pp_eval_after_files, pr_eval_files, state_files = get_files()

if args.graph == "acc":
    output_name = args.output if args.output else "accuracy.pdf"

    accuracy.plot_accuracy(
        perfect_eval_files=pp_eval_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
elif args.graph == "err-rel":
    output_name = args.output if args.output else "error_rel.pdf"

    error_rel.plot_rel_error(
        perfect_eval_files=pp_eval_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
elif args.graph == "err-abs":
    output_name = args.output if args.output else "error_abs.pdf"

    error_abs.plot_abs_error(
        perfect_eval_files=pp_eval_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
elif args.graph == "surv":
    output_name = args.output if args.output else "survival.pdf"

    survival.plot_survival_rate(
        state_files=state_files,
        output=output_dir / output_name,
    )
elif args.graph == "scatter":
    output_name = args.output if args.output else "scatter.pdf"

    scatter.plot_scatter(
        perfect_eval_files=pp_eval_after_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
