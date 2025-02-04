from collections import defaultdict
from pathlib import Path

import numpy as np

from .common import GraphData, PlotData, get_eval_and_hand_progress, moving_average


def plot_rel_error(
    perfect_eval_files: list[Path],
    player_eval_files: list[Path],
    output: Path,
    config: dict = {},
    is_show: bool = True,
) -> PlotData:
    """
    相対誤差をプロットする。
    """
    result = PlotData(
        x_label="progress",
        y_label="rel error",
        data={
            player_eval_file.parent.name: "" for player_eval_file in player_eval_files
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

        rel_err_dict = defaultdict(list)
        for pp_eval, pr_eval in zip(
            pp_eval_and_hand_progress, pr_eval_and_hand_progress
        ):
            bad_eval = min([ev for ev in pp_eval.evals if ev > -1e5])
            sub = pp_eval.evals[pr_eval.idx[0]] - pp_eval.evals[pp_eval.idx[0]]
            rel_err_dict[pp_eval.prg].append(
                sub / (pp_eval.evals[pp_eval.idx[0]] - bad_eval)
                if (pp_eval.evals[pp_eval.idx[0]] != bad_eval)
                else 0
            )

        # 平均を取る
        rel_err = {
            prg: np.mean(err_list)
            for prg, err_list in sorted(rel_err_dict.items(), key=lambda x: x[0])
        }
        result.data[player_eval_file.parent.name] = GraphData(
            x=moving_average(list(rel_err.keys()), 5).tolist(),
            y=moving_average(list(rel_err.values()), 5).tolist(),
        )
    return result
    #     plt.plot(
    #         moving_average(list(rel_err.keys()), 5).tolist(),
    #         moving_average(list(rel_err.values()), 5).tolist(),
    #         label=config.get("labels", {}).get(
    #             player_eval_file.parent.name, player_eval_file.parent.name
    #         ),
    #         color=config.get("colors", {}).get(
    #             player_eval_file.parent.name,
    #             None,
    #         ),
    #         linestyle=config.get("linestyles", {}).get(
    #             player_eval_file.parent.name, "solid"
    #         ),
    #     )
    # plt.xlabel("progress")
    # plt.ylabel("rel error")
    # plt.legend()
    # plt.savefig(output)
    # if is_show:
    #     plt.show()


if __name__ == "__main__":
    plot_rel_error(
        perfect_eval_files=[
            Path("board_data/PP/eval-state-CNN_DEEP.txt"),
        ],
        player_eval_files=[
            Path("board_data/CNN_DEEP/eval.txt"),
        ],
    )
