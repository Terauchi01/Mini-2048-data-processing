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


def get_state_eval_files():
    pp_eval_files = (
        [
            d
            for d in board_dir.glob("PP/eval-state*.txt")
            if not re.search(exclude_match, str(d))
            and re.search(intersection_match, str(d))
        ]
        if args.perfect_data is None
        else [Path(d) for d in args.perfect_data]
    )
    pr_eval_files = (
        [
            d
            for d in board_dir.glob("**/eval.txt")
            if not re.search(exclude_match, str(d))
            and re.search(intersection_match, str(d))
        ]
        if args.player_data is None
        else [Path(d) for d in args.player_data]
    )
    assert len(pp_eval_files) == len(pr_eval_files), "ファイル数が一致しません。"
    return pp_eval_files, pr_eval_files


def get_eval_state_and_after_state_files():
    pp_eval_files = (
        [
            d
            for d in board_dir.glob("PP/eval-after-state*.txt")
            if not re.search(exclude_match, str(d))
            and re.search(intersection_match, str(d))
        ]
        if args.perfect_data is None
        else [Path(d) for d in args.perfect_data]
    )
    pr_eval_files = (
        [
            d
            for d in board_dir.glob("**/eval.txt")
            if not re.search(exclude_match, str(d))
            and re.search(intersection_match, str(d))
        ]
        if args.player_data is None
        else [Path(d) for d in args.player_data]
    )
    assert len(pp_eval_files) == len(pr_eval_files), "ファイル数が一致しません。"
    return pp_eval_files, pr_eval_files


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
    default=[],
    help="除外するディレクトリ名を指定する。",
)
file_group.add_argument(
    "--intersection",
    nargs="+",
    default=[],
    help="対象を指定したディレクトリのみに絞る。",
)
player_group = arg_parser.add_argument_group(
    "データ指定オプション", "コマンドラインから手動でデータを指定する。"
)
player_group.add_argument(
    "--perfect_data",
    nargs="+",
    help="パーフェクトプレイヤのデータを指定する。",
)
player_group.add_argument(
    "--player_data",
    nargs="+",
    help="プレイヤーのデータを指定する。",
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


if args.graph == "acc":
    output_name = args.output if args.output else "accuracy.pdf"

    pp_eval_files, pr_eval_files = get_state_eval_files()
    accuracy.plot_accuracy(
        perfect_eval_files=pp_eval_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
elif args.graph == "err-rel":
    output_name = args.output if args.output else "error_rel.pdf"
    pp_eval_files, pr_eval_files = get_state_eval_files()
    error_rel.plot_rel_error(
        perfect_eval_files=pp_eval_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
elif args.graph == "err-abs":
    output_name = args.output if args.output else "error_abs.pdf"
    pp_eval_files, pr_eval_files = get_state_eval_files()
    error_abs.plot_abs_error(
        perfect_eval_files=pp_eval_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
elif args.graph == "surv":
    output_name = args.output if args.output else "survival.pdf"
    state_files = (
        [
            d
            for d in board_dir.glob("**/eval.txt")
            if not re.search(exclude_match, str(d))
        ]
        if args.player_data is None
        else [Path(d) for d in args.player_data]
    )
    survival.plot_survival_rate(
        state_files=state_files,
        output=output_dir / output_name,
    )
elif args.graph == "scatter":
    output_name = args.output if args.output else "scatter.pdf"
    pp_eval_files, pr_eval_files = get_eval_state_and_after_state_files()
    scatter.plot_scatter(
        perfect_eval_files=pp_eval_files,
        player_eval_files=pr_eval_files,
        output=output_dir / output_name,
    )
