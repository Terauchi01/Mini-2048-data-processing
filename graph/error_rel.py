from collections import defaultdict
from pathlib import Path

import numpy as np
from common import get_eval_and_hand_progress


def plot_rel_error(
    perfect_eval_files: list[Path],
    player_eval_files: list[Path],
):
    """
    相対誤差をプロットする。
    """
    for perfect_eval_file, player_eval_file in zip(
        sorted(perfect_eval_files), sorted(player_eval_files)
    ):
        pp_eval_and_hand_progress = get_eval_and_hand_progress(perfect_eval_file)
        pr_eval_and_hand_progress = get_eval_and_hand_progress(player_eval_file)
        rel_err_dict = defaultdict(list)

        for pp_eval, pr_eval in zip(
            pp_eval_and_hand_progress, pr_eval_and_hand_progress
        ):
            bad_eval = min([ev for ev in pp_eval.evals if ev > -1e10])
            best_eval = max(pp_eval.evals)
            sub = pp_eval.evals[pr_eval.idx[0]] - pr_eval.evals[pr_eval.idx[0]]
            rel_err_dict[pp_eval.prg].append((best_eval - bad_eval) / sub if sub else 0)
        # 平均を取る
        rel_err = {prg: np.mean(err_list) for prg, err_list in rel_err_dict.items()}
        print(rel_err)


if __name__ == "__main__":
    plot_rel_error(
        perfect_eval_files=[
            Path("board_data/test2/eval.txt"),
        ],
        player_eval_files=[
            Path("board_data/test2/eval.txt"),
        ],
    )
