## 注意 
- スタック領域を大量に消費するのでメモリ16G以上のLinux環境で動かしてください
- 出力ファイルは全てboard_dataディレクトリの下の各プレイヤーディレクトリの中に出力されます

## Nタプルプレイヤーのプレイした情報が欲しい,Nタプルプレイヤーを使ったグラフを書きたい場合
Play_PP_player.cppを動かします
- state.txt (プレイ中に出てきた全てのstate)
- after-state.txt (プレイ中に出てきた全てのaftar state)
- eval.txt (プレイ中に出てきたstateから選択できた全てのafterstateの評価値一覧)
この3種類のファイルが出てきます

# 動かしかた
"g++ Play_perfect_player.cpp -std=c++20 -mcmodel=large"
"./a.out seed ゲーム数" 例"./a.out 0 100"

## 他のプレイヤーがプレイしたstateからNタプルプレイヤーが評価する場合
eval_state.cppを動かします。
- eval-state-NT4.txt (stateから遷移可能なafterstateの評価値の一覧ファイル)
このファイルが出てきます。

# 動かしかた
"g++ eval_state.cpp -std=c++20 -mcmodel=large"
"./a.out load-player-name" 例"./a.out NT4"

## 他のプレイヤーがプレイしたafterstateをNタプルプレイヤーが評価する場合
eval_after_state.cppを動かします。
- eval-after-state-NT4.txt (after stateの評価値の一覧ファイル,scatterを書くのに使う)

# 動かしかた
"g++ eval_after_state.cpp -std=c++20 -mcmodel=large"
"./a.out load-player-name" 例"./a.out NT4"
