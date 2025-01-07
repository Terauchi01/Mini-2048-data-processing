import os
import re
import sys


# 指定したディレクトリの平均スコアを計算
def calculate_average_score(directory):
    results = []
    # サブディレクトリを基点に走査
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            subdir = os.path.join(root, dir_name)
            file_path = os.path.join(subdir, "after-state.txt")

            if os.path.isfile(file_path):
                scores = []
                with open(file_path, "r") as file:
                    for line in file:
                        match = re.search(
                            r"gameover_turn: \d+; game: \d+; progress: \d+; score: (\d+)",
                            line,
                        )
                        if match:
                            scores.append(int(match.group(1)))

                if scores:
                    avg_score = sum(scores) / len(scores)
                    results.append((dir_name, avg_score))
                else:
                    results.append((dir_name, None))
    return results


# メイン処理
def main():
    default_base_directory = "../board_data"  # デフォルトの基点ディレクトリ

    if len(sys.argv) > 1:
        base_directory = os.path.join(
            default_base_directory, sys.argv[1]
        )  # board_dataの下を指定
    else:
        print("Error: Please specify a subdirectory under 'board_data'.")
        sys.exit(1)

    if not os.path.isdir(base_directory):
        print(f"Error: Directory '{base_directory}' does not exist.")
        sys.exit(1)

    results = calculate_average_score(base_directory)

    # スコアのある結果だけをフィルタリングしてソート
    valid_results = [(name, score) for name, score in results if score is not None]
    sorted_results = sorted(valid_results, key=lambda x: x[1], reverse=True)

    # 上位10件を表示
    print("\nTop 10 Directories by Average Score:")
    for name, score in sorted_results[:10]:
        print(f"{name}: {score:.2f}")

    # スコアがないディレクトリを表示
    no_score_results = [name for name, score in results if score is None]
    if no_score_results:
        print("\nDirectories with No Valid Scores:")
        for name in no_score_results:
            print(name)


if __name__ == "__main__":
    main()
