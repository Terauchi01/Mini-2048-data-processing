from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .common import EvalAndHandProgress, get_eval_and_hand_progress, moving_average


def calc_accuracy(
    pp_ehp: EvalAndHandProgress,
    pr_ehp: EvalAndHandProgress,
):
    count = 0
    for pp_eval in pp_ehp.idx:
        for pr_eval in pr_ehp.idx:
            if pp_eval == pr_eval:
                count += 1
    return count / len(pr_ehp.idx)


def plot_accuracy(
    perfect_eval_files: list[Path],
    player_eval_files: list[Path],
    output: Path,
    config: dict = {},
    is_show: bool = True,
):
    """
    最善手率をプロットする。
    """
    for perfect_eval_file, player_eval_file in zip(
        sorted(perfect_eval_files), sorted(player_eval_files)
    ):
        pp_eval_and_hand_progress = get_eval_and_hand_progress(perfect_eval_file)
        pr_eval_and_hand_progress = get_eval_and_hand_progress(player_eval_file)

        assert len(pp_eval_and_hand_progress) == len(pr_eval_and_hand_progress), (
            f"データ数が異なります。{len(pp_eval_and_hand_progress)=}, {len(pr_eval_and_hand_progress)=}"
        )

        acc_dict = defaultdict(list)

        for pp_eval, pr_eval in zip(
            pp_eval_and_hand_progress, pr_eval_and_hand_progress
        ):
            acc_dict[pp_eval.prg].append(calc_accuracy(pp_eval, pr_eval))
        # 平均を取る
        acc = {
            prg: np.mean(err_list)
            for prg, err_list in sorted(acc_dict.items(), key=lambda x: x[0])
        }
        plt.plot(
            moving_average(list(acc.keys()), 10).tolist(),
            moving_average(list(acc.values()), 10).tolist(),
            label=config.get("labels", {}).get(
                player_eval_file.parent.name, player_eval_file.parent.name
            ),
            color=config.get("colors", {}).get(
                player_eval_file.parent.name,
                None,
            ),
        )
    plt.xlabel("progress")
    plt.ylabel("accuracy")
    plt.legend()
    plt.savefig(output)
    if is_show:
        plt.show()


if __name__ == "__main__":
    plot_accuracy(
        perfect_eval_files=[
            Path("board_data/PP/eval-state-CNN_DEEP.txt"),
        ],
        player_eval_files=[
            Path("board_data/CNN_DEEP/eval.txt"),
        ],
    )
