from collections import defaultdict
from pathlib import Path

import numpy as np

from .common import (
    EvalAndHandProgress,
    GraphData,
    PlotData,
    get_eval_and_hand_progress,
    moving_average,
)


def calc_accuracy(
    pp_ehp: EvalAndHandProgress,
    pr_ehp: EvalAndHandProgress,
):
    pp_best_moves = set(pp_ehp.idx)
    pr_best_moves = set(pr_ehp.idx)
    
    # playerの最善手のうち、perfect playerの最善手と一致するものの数
    common_moves = pp_best_moves.intersection(pr_best_moves)
    
    # プレイヤーの最善手総数で割る
    return len(common_moves) / len(pr_ehp.idx)


def calc_accuracy_data(
    perfect_eval_files: list[Path],
    player_eval_files: list[Path],
) -> PlotData:
    """
    最善手率をプロットする。
    """
    result = PlotData(
        x_label="progress",
        y_label="accuracy",
        data={
            player_eval_file.parent.name: None for player_eval_file in player_eval_files
        },
    )
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
        result.data[player_eval_file.parent.name] = GraphData(
            x=moving_average(list(acc.keys()), 10).tolist(),
            y=moving_average(list(acc.values()), 10).tolist(),
        )
    return result


if __name__ == "__main__":
    calc_accuracy_data(
        perfect_eval_files=[
            Path("board_data/PP/eval-state-CNN_DEEP.txt"),
        ],
        player_eval_files=[
            Path("board_data/CNN_DEEP/eval.txt"),
        ],
    )
