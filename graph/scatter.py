import random
import re
from pathlib import Path

import matplotlib.pyplot as plt

from .common import get_eval_and_hand_progress


def get_evals(eval_file: Path):
    eval_txt = eval_file.read_text("utf-8")
    subed_eval_txt = re.sub(r"game.*\n?", "", eval_txt)
    eval_lines = subed_eval_txt.splitlines()
    return [float(line) for line in eval_lines]


def plot_scatter(
    perfect_eval_files: list[Path],
    player_eval_files: list[Path],
    output: Path,
    is_show: bool = True,
    config: dict = {},
):
    """
    パーフェクトプレイヤとプレイヤーの評価値の散布図をプロットする。
    """
    for i, (perfect_eval_file, player_eval_file) in enumerate(
        zip(sorted(perfect_eval_files), sorted(player_eval_files))
    ):
        pp_evals = get_evals(perfect_eval_file)
        pr_eval_and_hand_progress = get_eval_and_hand_progress(player_eval_file)

        assert len(pp_evals) == len(pr_eval_and_hand_progress), (
            f"データ数が異なります。{len(pp_evals)=}, {len(pr_eval_and_hand_progress)=}"
        )

        scatter_data = [
            (ev, pr_eval.evals[pr_eval.idx[0]])
            for ev, pr_eval in zip(pp_evals, pr_eval_and_hand_progress)
        ]
        # 1000個のデータをランダムで取得
        scatter_data = random.sample(scatter_data, 1000)

        # 散布図のdotの大きさを指定
        plt.scatter(
            [d[0] for d in scatter_data],
            [d[1] for d in scatter_data],
            s=5,
        )
        # 直線を引く
        plt.plot(
            [0, 6000],
            [0, 6000],
            color="gray",
            linestyle="dashed",
        )
        plt.xlabel("perfect")
        plt.ylabel(
            config.get("labels", {}).get(
                player_eval_file.parent.name, player_eval_file.parent.name
            )
        )
        plt.savefig(output.with_stem(f"{output.stem}_{i}"))
        if is_show:
            plt.show()
        plt.close()
    return None


if __name__ == "__main__":
    plot_scatter(
        perfect_eval_file=Path("board_data/PP/eval-afterstate-CNN_DEEP.txt"),
        player_eval_file=Path("board_data/CNN_DEEP/eval.txt"),
    )
