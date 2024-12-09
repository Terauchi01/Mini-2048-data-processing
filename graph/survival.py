import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def plot_survival_rate(
    state_files: list[Path],
    output: Path,
    config: dict = {},
):
    """
    生存率をプロットする。
    """
    for state_file in state_files:
        text = state_file.read_text()
        progress_text = re.findall(r"progress: (\d+)", text)
        progresses = [int(progress) for progress in progress_text]

        droped_counter = Counter(progresses)
        max_value = len(progresses)
        survival_rate = []

        for i in range(max(progresses) + 10):
            max_value -= droped_counter[i]
            survival_rate.append(max_value / len(progresses))

        plt.plot(
            survival_rate,
            label=config.get("labels", {}).get(
                state_file.parent.name, state_file.parent.name
            ),
        )
    plt.xlabel("progress")
    plt.ylabel("survival rate")
    plt.legend()
    plt.savefig(output)
    plt.show()


if __name__ == "__main__":
    plot_survival_rate(
        state_files=[
            Path("board_data/CNN_DEEP/state.txt"),
            # Path("NN-DEEP/state.txt"),
            # Path("NT4/state.txt"),
        ],
    )
