import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EvalAndHandProgress:
    eval: list[float]  # 長さ4のリスト
    idx: int  # 選んだ手のindex
    prg: int  # progress


def get_eval_and_hand_progress(eval_file: Path):
    """
    ファイルから
    評価値、選択した手、progressを取得する。
    """
    eval_txt = eval_file.read_text("utf-8")
    subed_eval_txt = re.sub(r"game.*\n", "", eval_txt)
    eval_lines = subed_eval_txt.splitlines()
    eval_and_hand_progress = [
        EvalAndHandProgress(
            eval=list(map(float, line.split()[:3])),
            idx=int(line[4]),
            prg=int(line[5]),
        )
        for line in eval_lines
    ]
    return eval_and_hand_progress
