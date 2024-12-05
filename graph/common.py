import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EvalAndHandProgress:
    evals: list[float]  # 長さ4のリスト
    prg: int  # progress

    @property
    def idx(self) -> list[int]:
        """
        evalsの最大値のindexのリストを返す。
        """
        max_eval = max(self.evals)
        return [i for i, eval in enumerate(self.evals) if eval == max_eval]


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
            evals=list(map(float, line.split()[:4])),
            prg=int(line.split()[4]),  # progress
        )
        for line in eval_lines
    ]
    return eval_and_hand_progress
