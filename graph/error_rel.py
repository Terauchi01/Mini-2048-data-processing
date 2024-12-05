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
            bad_eval = min([ev for ev in pp_eval.eval if ev > -1e10])
            best_eval = max(pp_eval.eval)
            sub = pp_eval.eval[pr_eval.idx] - pr_eval.eval[pr_eval.idx]
            rel_err_dict[pp_eval.prg].append((best_eval - bad_eval) / sub if sub else 0)
        # 平均を取る
        rel_err = {prg: np.mean(err_list) for prg, err_list in rel_err_dict.items()}
        print(rel_err)


if __name__ == "__main__":
    plot_rel_error(
        perfect_eval_files=[
            Path("PP/PP_eval_NN-DEEP.txt"),
            Path("PP/PP_eval_NT6.txt"),
            Path("PP/PP_eval_NT4.txt"),
        ],
        player_eval_files=[
            Path("NT6/NT6_eval_PP.txt"),
            Path("NN-DEEP/NN-DEEP_eval_PP.txt"),
            Path("NT4/NT4_eval_PP.txt"),
        ],
    )
