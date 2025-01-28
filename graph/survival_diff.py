import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def plot_survival_diff_rate(
    state_files: list[Path],
    output: Path,
    config: dict = {},
    is_show: bool = True,
):
    """
    パーフェクトプレイヤとの生存率の差をプロットする。
    """

    pp_state_file = Path("board_data/PP/state.txt")
    text = pp_state_file.read_text()
    progress_text = re.findall(r"progress: (\d+)", text)
    progresses = [int(progress) for progress in progress_text]

    droped_counter = Counter(progresses)
    max_value = len(progresses)
    pp_survival_rate = []

    for i in range(max(progresses) + 10):
        max_value -= droped_counter[i]
        pp_survival_rate.append(max_value / len(progresses))
    # 上でパーフェクトプレイヤの生存率を計算したので、差を計算する

    for state_file in state_files:
        if state_file == pp_state_file:
            continue
        text = state_file.read_text()
        progress_text = re.findall(r"progress: (\d+)", text)
        progresses = [int(progress) for progress in progress_text]

        droped_counter = Counter(progresses)
        max_value = len(progresses)
        diff_survival_rate = []

        for i in range(max(progresses) + 10):
            max_value -= droped_counter[i]
            diff_survival_rate.append(
                abs(max_value / len(progresses) - pp_survival_rate[i])
            )

        plt.plot(
            diff_survival_rate,
            label=config.get("labels", {}).get(
                state_file.parent.name, state_file.parent.name
            ),
            color=config.get("colors", {}).get(
                state_file.parent.name,
                None,
            ),
            linestyle=config.get("linestyles", {}).get(state_file.parent.name, "solid"),
        )
    plt.xlabel("progress")
    plt.ylabel("difference in survival rate for PP")
    plt.legend()
    plt.savefig(output)
    if is_show:
        plt.show()


if __name__ == "__main__":
    plot_survival_diff_rate(
        state_files=[
            Path("board_data/CNN_DEEP/state.txt"),
            Path("board_data/CNN_DEEP_restart/state.txt"),
            # Path("NT4/state.txt"),
        ],
        output=Path("./output/survival_diff.pdf"),
    )
