import re
from collections import Counter
from pathlib import Path

from .common import GraphData, PlotData


def plot_survival_rate(
    state_files: list[Path],
    output: Path,
    config: dict = {},
    is_show: bool = True,
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
    #     plt.plot(
    #         survival_rate,
    #         label=config.get("labels", {}).get(
    #             state_file.parent.name, state_file.parent.name
    #         ),
    #         color=config.get("colors", {}).get(
    #             state_file.parent.name,
    #             None,
    #         ),
    #         linestyle=config.get("linestyles", {}).get(state_file.parent.name, "solid"),
    #     )
    # plt.xlabel("progress")
    # plt.ylabel("survival rate")
    # plt.legend()
    # plt.savefig(output)
    # if is_show:
    #     plt.show()


if __name__ == "__main__":
    plot_survival_rate(
        state_files=[
            Path("board_data/PP/state.txt"),
            Path("board_data/CNN_DEEP/state.txt"),
            Path("board_data/CNN_DEEP_restart/state.txt"),
            # Path("NT4/state.txt"),
        ],
        output=Path("./output/survival.pdf"),
    )
