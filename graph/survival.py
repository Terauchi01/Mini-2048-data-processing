import re
from collections import Counter
from pathlib import Path

from .common import GraphData, PlotData


def calc_survival_rate_data(
    state_files: list[Path],
) -> PlotData:
    """
    生存率をプロットする。
    """
    result = PlotData(
        x_label="progress",
        y_label="survival rate",
        data={state_file.parent.name: None for state_file in state_files},
    )
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

        result.data[state_file.parent.name] = GraphData(
            x=list(range(len(survival_rate))),
            y=survival_rate,
        )
    return result


if __name__ == "__main__":
    calc_survival_rate_data(
        state_files=[
            Path("board_data/PP/state.txt"),
            Path("board_data/CNN_DEEP/state.txt"),
            Path("board_data/CNN_DEEP_restart/state.txt"),
            # Path("NT4/state.txt"),
        ],
        output=Path("./output/survival.pdf"),
    )
