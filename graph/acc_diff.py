import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
    count = 0
    for pp_eval in pp_ehp.idx:
        for pr_eval in pr_ehp.idx:
            if pp_eval == pr_eval:
                count += 1
    return count / len(pr_ehp.idx)


def acc_diff_plot(
    perfect_eval_files: list[Path],
    player_eval_files: list[Path],
    config: dict = {},
) -> PlotData:
    """
    最善手率の差分を計算し、プロットする。
    """
    result = PlotData(
        x_label="progress",
        y_label="accuracy",
        data={},
    )

    for perfect_eval_file, player_eval_file in zip(
        sorted(perfect_eval_files), sorted(player_eval_files)
    ):
        pp_eval_and_hand_progress = get_eval_and_hand_progress(perfect_eval_file)
        pr_eval_and_hand_progress = get_eval_and_hand_progress(player_eval_file)

        assert len(pp_eval_and_hand_progress) == len(
            pr_eval_and_hand_progress
        ), f"データ数が異なります。{len(pp_eval_and_hand_progress)=}, {len(pr_eval_and_hand_progress)=}"

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
            x=moving_average(list(acc.keys()), 10).tolist(),  # スムージング
            y=moving_average(list(acc.values()), 10).tolist(),
        )

    # 差分を計算
    sorted_files = sorted(player_eval_files)

    if len(sorted_files) < 2:
        raise ValueError("少なくとも2つの player_eval_files が必要です。")

    first_key = sorted_files[0].parent.name
    second_key = sorted_files[1].parent.name

    result2 = PlotData(
        x_label="progress",
        y_label="accuracy difference",
        data={first_key + "-" + second_key: GraphData(x=[], y=[])},
    )

    x_values_first = result.data[first_key].x
    x_values_second = result.data[second_key].x
    y_values_first = result.data[first_key].y
    y_values_second = result.data[second_key].y

    diff_x = []
    diff_y = []

    # x 値を統一しながら処理
    for x1, y1 in zip(x_values_first, y_values_first):
        if x1 in x_values_second:
            index2 = x_values_second.index(x1)
            y2 = y_values_second[index2]
        else:
            y2 = 0  # 存在しない場合は0

        diff_x.append(x1)
        diff_y.append(y1 - y2)

    for x2, y2 in zip(x_values_second, y_values_second):
        if x2 not in x_values_first:
            y1 = 0  # 存在しない場合は0
            diff_x.append(x2)
            diff_y.append(y1 - y2)

    # 結果を保存
    result2.data[first_key + "-" + second_key] = GraphData(
        x=diff_x,
        y=diff_y,
    )

    # y=0 を基準に色分け
    colors = ["blue" if y > 0 else "red" for y in diff_y]

    # プロットを作成
    plt.figure()
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1.0)  # y=0 の基準線
    plt.scatter(
        diff_x,
        diff_y,
        c=colors,
        s=10,
        label=f"{config.get(first_key).get('label')} - {config.get(second_key).get('label')}",
    )
    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="blue",
            markersize=8,
            label=f"{config.get(first_key).get('label')} > {config.get(second_key).get('label')}",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="red",
            markersize=8,
            label=f"{config.get(second_key).get('label')} > {config.get(first_key).get('label')}",
        ),
    ]
    plt.legend(handles=legend_elements)
    plt.plot(diff_x, diff_y, linestyle="-", alpha=0.5)

    plt.xlabel("Progress")
    plt.ylabel("Accuracy Difference")
    plt.title("Accuracy Difference Plot (Colored by Sign)")
    # plt.legend()
    plt.grid()
    plt.savefig("output/acc_diff_plot.pdf")
    # plt.show()

    # 出力を確認
    # print(f"result2.x: {result2.data[first_key + '-' + second_key].x}")
    # print(f"result2.y: {result2.data[first_key + '-' + second_key].y}")

    return None


if __name__ == "__main__":
    acc_diff_plot(
        perfect_eval_files=[
            Path("board_data/PP/eval-state-CNN_DEEP.txt"),
        ],
        player_eval_files=[
            Path("board_data/CNN_DEEP/eval.txt"),
            Path("board_data/OTHER_MODEL/eval.txt"),  # 2つ以上のデータを渡す
        ],
    )
