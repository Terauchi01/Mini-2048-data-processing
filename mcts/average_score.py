import os
import re
import sys
import statistics


# 指定したディレクトリの平均スコアと中央値を計算
def calculate_scores(directory):
    results = []
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
                    median_score = statistics.median(scores)
                    results.append((dir_name, avg_score, median_score))
                else:
                    results.append((dir_name, None, None))
    return results


# メイン処理
def main():
    default_base_directory = "../board_data/"  # デフォルトの基点ディレクトリ

    # 引数でサブディレクトリを指定
    if len(sys.argv) > 1:
        base_directory = os.path.join(default_base_directory, sys.argv[1])
    else:
        print("Error: Please specify a subdirectory under 'board_data'.")
        sys.exit(1)

    if not os.path.isdir(base_directory):
        print(f"Error: Directory '{base_directory}' does not exist.")
        sys.exit(1)

    # スコア計算
    results = calculate_scores(base_directory)

    # スコアのある結果だけをフィルタリングしてソート
    valid_results = [(name, avg, med) for name, avg, med in results if avg is not None]
    sorted_results = sorted(valid_results, key=lambda x: x[1], reverse=True)

    # 上位10件を表示
    print("\nTop 10 Directories by Average Score:")
    for name, avg, med in sorted_results[:10]:
        print(f"{name}: Average={avg:.2f}, Median={med:.2f}")

    # スコアがないディレクトリを表示
    no_score_results = [name for name, avg, med in results if avg is None]
    if no_score_results:
        print("\nDirectories with No Valid Scores:")
        for name in no_score_results:
            print(name)


if __name__ == "__main__":
    main()
