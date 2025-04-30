#!/bin/bash

# コンパイル用ディレクトリを作成
mkdir -p bin

# play_greedy のコンパイル
for i in {1..9}; do
    g++ -DT${i} play/play_greedy.cpp -o bin/play_greedy_t${i} -std=c++20 -mcmodel=large -O2 -lz
done

# play_expectimax のコンパイル
for i in {1..9}; do
        g++ -DT$i play/play_expectimax.cpp -o bin/play_expectimax_t${i} -std=c++20 -mcmodel=large -O2 -lz
done

echo "Compilation completed."
