from collections import defaultdict
from pathlib import Path

import numpy as np
from common import get_eval_and_hand_progress


def plot_accuracy(
    perfect_eval_files: list[Path],
    player_eval_files: list[Path],
):
    """
    最善手率をプロットする。
    """
    for perfect_eval_file, player_eval_file in zip(
        sorted(perfect_eval_files), sorted(player_eval_files)
    ):
        pp_eval_and_hand_progress = get_eval_and_hand_progress(perfect_eval_file)
        pr_eval_and_hand_progress = get_eval_and_hand_progress(player_eval_file)
        acc_dict = defaultdict(list)

        for pp_eval, pr_eval in zip(
            pp_eval_and_hand_progress, pr_eval_and_hand_progress
        ):
            acc_dict[pp_eval.prg].append(
                1 if pp_eval.eval[pr_eval.idx] == pr_eval.eval[pr_eval.idx] else 0
            )
        # 平均を取る
        acc = {prg: np.mean(err_list) for prg, err_list in acc_dict.items()}
        print(acc)


if __name__ == "__main__":
    plot_accuracy(
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
