# Graph
このプロジェクトは、2048のプレイヤデータを可視化するためのツールです。

## ドキュメント

### PlayerDataクラス

#### フィールド

| フィールド名 | 説明 |
|------------|------|
| `name` | プレイヤの名前 |
| `target_dir` | プレイヤのデータが格納されているディレクトリ |
| `pp_dir` | プレイヤのPPデータが格納されているディレクトリ |

#### プロパティ

| プロパティ名 | 説明 |
|------------|------|
| `state_file` | プレイヤのstateファイルのパス |
| `eval_file` | プレイヤの評価値ファイルのパス |
| `pp_eval_state` | プレイヤのプレイで現れたstateをPPに評価させた評価値ファイルのパス |
| `pp_eval_after_state` | プレイヤのプレイで現れたafter_stateをPPに評価させた評価値ファイルのパス |

### common.py

#### データクラス

##### EvalAndHandProgress

評価値とゲーム進行度を格納するデータクラスです。

| フィールド | 型 | 説明 |
|-----------|-----|-----|
| `evals` | `list[float]` | 長さ4のリスト。4方向（上右下左）への評価値 |
| `prg` | `int` | ゲームの進行度（progress） |

###### プロパティ

| プロパティ名 | 戻り値 | 説明 |
|------------|-------|------|
| `idx` | `list[int]` | `evals`の中で最大値を持つインデックスのリスト |

##### PlotData

プロット用のデータを格納するデータクラスです。

| フィールド | 型 | 説明 |
|-----------|-----|-----|
| `x_label` | `str` | X軸のラベル |
| `y_label` | `str` | Y軸のラベル |
| `data` | `dict[str, GraphData]` | プレイヤー名をキーとするGraphDataの辞書 |

##### GraphData

グラフデータを格納するデータクラスです。

| フィールド | 型 | 説明 |
|-----------|-----|-----|
| `x` | `list[float]` | X軸の値のリスト |
| `y` | `list[float]` | Y軸の値のリスト |

#### 関数

##### get_eval_and_hand_progress

```python
def get_eval_and_hand_progress(eval_file: Path) -> list[EvalAndHandProgress]
```

評価値ファイルから評価値、選択した手、進行度を取得します。

| 引数 | 型 | 説明 |
|-----|-----|-----|
| `eval_file` | `Path` | 評価値ファイルのパス |

**戻り値**: `EvalAndHandProgress`のリスト

##### moving_average

```python
def moving_average(data, window_size)
```

移動平均を計算します。

| 引数 | 型 | 説明 |
|-----|-----|-----|
| `data` | `list[float]` or `numpy.ndarray` | 移動平均を計算するデータ |
| `window_size` | `int` | 移動平均の窓サイズ |

**戻り値**: 移動平均が計算された`numpy.ndarray`

## 導入

1. [uv](https://docs.astral.sh/uv/getting-started/installation/)をインストール。
2. `uv sync`を実行。ライブラリがインストールされる。

## 実行

`uv run -m graph [graph_type]`を実行。指定したグラフがプロットされる。

## グラフの種類

| グラフタイプ | 説明 |
|------------|------|
| `surv` | 生存率 |
| `surv-diff` | 生存率(パーフェクトプレイヤとの差) |
| `scatter` | パーフェクトプレイヤとの散布図 |
| `err-abs` | 絶対誤差 |
| `err-rel` | 相対誤差 |
| `acc` | 正確性 |
| `histgram` | 得点分布 |
| `evals` | 評価値のProgressごとの散布図 |

## 引数の説明

### graph_type (必須)

グラフの種類を指定する。上記のグラフの種類から選択。

### --exclude

プロットを行う際に除外するプレイヤを指定する。複数指定可能。

**例**: NT4プレイヤを除外する場合
```
--exclude NT4
```

### --intersection

プロットを行う際に含めるプレイヤを指定する。複数指定可能。
指定しない場合は全てのプレイヤをプロットする。

**例**: NT4プレイヤとNT6プレイヤのみをプロットする場合
```
--intersection NT4 NT6
```

### --help, -h

コマンドのヘルプを表示する。

### --is-show

完成したグラフを表示する。

## 今後の予定

上から順に優先度が高い。

- [ ] サブディレクトリ内のデータを参照できるようにする。(確認必要)
- [ ] surv diff を出せるようにする。
- [ ] グラフ設定を行えるようにする。
- [ ] ファイル指定を tkinter でグラフィカルに行えるようにする。