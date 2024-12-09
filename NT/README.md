## 注意出力ファイルは全てboard_dataディレクトリの下の各プレイヤーディレクトリの中に出力されます

## Nタプルプレイヤーのプレイした情報が欲しい,Nタプルプレイヤーを使ったグラフを書きたい場合
Play_NT_player.cppを動かします
- state.txt (プレイ中に出てきた全てのstate)
- after-state.txt (プレイ中に出てきた全てのaftar state)
- eval.txt (プレイ中に出てきたstateから選択できた全てのafterstateの評価値一覧)
この3種類のファイルが出てきます

# 動かしかた
"g++ Play_NT_player.cpp -std=c++20"
"./a.out seed ゲーム数 評価ファイル" 例"./a.out 0 100 4tuple_data_9.dat "
このように動かせば動きます。評価ファイルの先頭を参照してタプルを選んでいますので、評価ファイルの名前を変更する際は注意してください。

## 他のプレイヤーがプレイしたstateからNタプルプレイヤーが評価する場合
eval_state.cppを動かします。
- eval-state-PP.txt (stateから遷移可能なafterstateの評価値の一覧ファイル)
このファイルが出てきます。

# 動かしかた
"g++ eval_state.cpp -std=c++20"
"./a.out load-player-name EV-file" 例"./a.out PP 4tuple_data_9.dat"

## 他のプレイヤーがプレイしたafterstateをNタプルプレイヤーが評価する場合
eval_after_state.cppを動かします。
- eval-after-state-PP.txt (after stateの評価値の一覧ファイル,scatterを書くのに使う)

# 動かしかた
"g++ eval_after_state.cpp -std=c++20"
"./a.out load-player-name EV-file" 例"./a.out PP 4tuple_data_9.dat "
