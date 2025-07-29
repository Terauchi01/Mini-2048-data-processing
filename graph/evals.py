from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
import random
from .common import get_eval_and_hand_progress


def calc_eval_data(
    player_eval_files: list[Path],
    output: Path,
    is_show: bool = True,
    config: dict = {},
):
    # 各プレイヤータイプに対して一度だけラベルを使用するために追跡する辞書
    used_labels = {}
    
    for i, player_eval_file in enumerate(sorted(player_eval_files)):
        pr_eval_and_hand_progress = get_eval_and_hand_progress(player_eval_file)
        abs_err_dict = defaultdict(list)

        pr_eval_and_hand_progress = random.sample(pr_eval_and_hand_progress, 1000)
        for pr_eval in pr_eval_and_hand_progress:
            abs_err_dict[pr_eval.prg].append(
                pr_eval.evals[pr_eval.idx[0]] 
            )
        player_name = player_eval_file.parent.name
        player_config = config.get(player_name, {})
        for key, value in abs_err_dict.items():
            # 散布図の設定を作成
            scatter_params = player_config.copy()
            scatter_params["color"] = scatter_params["color"] if scatter_params["color"] else f"C{i % 10}"
            # 初めて出現したプレイヤータイプでない場合はラベルを非表示に
            if player_name in used_labels:
                scatter_params['label'] = '_nolegend_'  # これで凡例に表示されなくなる
            else:
                used_labels[player_name] = True
                
            plt.scatter(
                [key] * len(value),
                value,
                s=5,
                alpha=0.5,
                **scatter_params
            )
    # グリッドを追加
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("progress")
    plt.ylabel("player")
    plt.legend()
    plt.tight_layout()  # 追加：はみ出しを防ぐ
    
    plt.savefig(output.with_stem(f"{output.stem}"))
    print(output.with_stem(f"saved as {output.stem}"))
    if is_show:
        plt.show()
    plt.close()
    return None


if __name__ == "__main__":
    calc_eval_data(
        perfect_eval_files=[
            Path("board_data/PP/eval-state-CNN_DEEP.txt"),
        ],
        player_eval_files=[
            Path("board_data/CNN_DEEP/eval.txt"),
        ],
    )
