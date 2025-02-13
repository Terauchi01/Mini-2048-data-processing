import os
import re
import sys
import statistics

# 指定したディレクトリの平均スコア、中央値、標準偏差を計算
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
                    std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
                    results.append((dir_name, avg_score, median_score, std_dev))
                else:
                    results.append((dir_name, None, None, None))
    return results

# メイン処理
def main():
    default_base_directory = "board_data/"  # デフォルトの基点ディレクトリ

    # 引数でサブディレクトリと表示件数を指定
    if len(sys.argv) > 1:
        base_directory = os.path.join(default_base_directory, sys.argv[1])
    else:
        print("Error: Please specify a subdirectory under 'board_data'.")
        sys.exit(1)

    if not os.path.isdir(base_directory):
        print(f"Error: Directory '{base_directory}' does not exist.")
        sys.exit(1)

    # 表示件数を指定 (デフォルトは10件)
    if len(sys.argv) > 2:
        try:
            display_count = int(sys.argv[2])
        except ValueError:
            print("Error: Display count must be an integer.")
            sys.exit(1)
    else:
        display_count = 10

    # スコア計算
    results = calculate_scores(base_directory)

    # スコアのある結果だけをフィルタリングしてソート
    valid_results = [(name, avg, med, std) for name, avg, med, std in results if avg is not None]
    sorted_results = sorted(valid_results, key=lambda x: x[1], reverse=True)

    # 表示件数を調整
    if display_count == -1:
        display_count = len(sorted_results)

    # 上位件数を表示
    print("\nTop Directories by Average Score:")
    for name, avg, med, std in sorted_results[:display_count]:
        print(f"{name}: Average={avg:.2f}, Median={med:.2f}, Std Dev={std:.2f}")

    # スコアがないディレクトリを表示
    no_score_results = [name for name, avg, med, std in results if avg is None]
    if no_score_results:
        print("\nDirectories with No Valid Scores:")
        for name in no_score_results:
            print(name)

if __name__ == "__main__":
    main()
