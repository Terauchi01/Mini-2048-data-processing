from pathlib import Path

import matplotlib.pyplot as plt
from common import get_eval_and_hand_progress


def plot_scatter(
    perfect_eval_file: Path,
    player_eval_file: Path,
):
    """
    パーフェクトプレイヤとプレイヤーの評価値の散布図をプロットする。
    """
    pp_eval_and_hand_progress = get_eval_and_hand_progress(perfect_eval_file)
    pr_eval_and_hand_progress = get_eval_and_hand_progress(player_eval_file)

    scatter_data = {
        "x": [
            pp_eval.evals[pr_eval.idx[0]]
            for pp_eval, pr_eval in zip(
                pp_eval_and_hand_progress, pr_eval_and_hand_progress
            )
        ],
        "y": [pr_eval.evals[pr_eval.idx[0]] for pr_eval in pr_eval_and_hand_progress],
    }
    # 散布図のdotの大きさを指定
    plt.scatter(scatter_data["x"], scatter_data["y"], s=5)
    # 直線を引く
    plt.plot(
        [0, 6000],
        [0, 6000],
        color="gray",
        linestyle="dashed",
    )
    plt.xlabel("perfect")
    plt.ylabel("player")
    plt.show()


if __name__ == "__main__":
    plot_scatter(
        perfect_eval_file=Path("board_data/test/eval.txt"),
        player_eval_file=Path("board_data/test/eval.txt"),
    )
