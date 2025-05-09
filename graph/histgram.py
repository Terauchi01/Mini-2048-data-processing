import re
from pathlib import Path

import matplotlib.pyplot as plt

BINS = 100


def plot_histgram(
    state_files: list[Path],
    output: Path,
    config: dict = {},
    is_show: bool = True,
):
    """
    得点分布をプロットする。
    """
    for state_file in state_files:
        text = state_file.read_text()
        score_txt = re.findall(r"score: (\d+)", text)
        scores = [int(score) for score in score_txt]

        plt.hist(scores, bins=BINS)
        plt.xlabel("score")
        plt.ylabel("frequency")
        plt.savefig(output.with_stem(f"{output.stem}-{state_file.parent.name}"))
        if is_show:
            plt.show()
        plt.close()
    return None


if __name__ == "__main__":
    plot_histgram(
        state_files=[
            Path("board_data/CNN_DEEP/state.txt"),
            Path("board_data/CNN_DEEP_restart/state.txt"),
            # Path("board_data/PP/state.txt"),
            # Path("NN-DEEP/state.txt"),
            # Path("NT4/state.txt"),
        ],
        output=Path("./output/histgram.pdf"),
    )
