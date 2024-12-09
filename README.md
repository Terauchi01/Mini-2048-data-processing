# Mini-2048-data-processing

## python 注意点

uv を用いてpythonのライブラリの管理を行っています。
詳しい内容は[このREADME](./graph/README.md)を確認してください。

## perfect_player 注意点

perfect_player はメモリ不足が懸念されるので、サーバで動かしてください。
それ以外の環境の場合動作の保証はしません。
詳しい内容は[このREADME](./perfect_player/README.md)を確認してください。

## NT注意点

4tuple_data_9.datのような各タプルの学習済みファイルが必要です。
詳しい内容は[このREADME](./perfect_player/README.md)を確認してください。

## TODO

- [ ] グラフプロット用コードを記述する。
  - [x] accuracy
  - [x] error-relative
  - [x] error-absolute
  - [x] survival-rate
  - [ ] scatter

- [ ] グラフプロット用コードをマージする。
  - [ ] `__main__.py`を完成させる。
  - [ ] 各コードでプロットできるようにする。

- [ ] 他のplayerのstateをPerfect Playerに食わせて、evalを出力するコードを記述する。(PP/eval_state_[player].txt)
- [ ] 他のplayerのafterstateをPerfect Playerに食わせて、evalを出力するコードを記述する。 (PP/eval_saftertate_[player].txt)
