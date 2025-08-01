#ifndef __6TUPLES_SYM_H__
#define __6TUPLES_SYM_H__
#include <float.h>

#include <algorithm>
#include <climits>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

/**
 *  6タプルの定義．複数 cpp ファイルから #include は不可 (コード簡単化のため)
 */
namespace NT6 {
#define TUPLE_SIZE 6
#define NUM_STAGES 2
constexpr long long VARIATION_TILE = 11;
constexpr long long ARRAY_LENGTH =
    (VARIATION_TILE * VARIATION_TILE * VARIATION_TILE * VARIATION_TILE *
     VARIATION_TILE * VARIATION_TILE);

// #ifdef NT6
#define NUM_TUPLES 16
const int poss[NUM_TUPLES][TUPLE_SIZE] = {
    {0, 1, 2, 3, 4, 5}, {0, 1, 2, 3, 4, 6}, {0, 1, 2, 3, 5, 6},
    {0, 1, 2, 3, 4, 8}, {0, 1, 2, 3, 4, 7}, {0, 1, 2, 4, 6, 7},
    {0, 1, 3, 4, 5, 8}, {0, 1, 2, 3, 5, 7}, {0, 1, 3, 4, 5, 7},
    {0, 1, 4, 5, 6, 7}, {0, 1, 2, 3, 7, 8}, {0, 1, 3, 5, 7, 8},
    {0, 1, 4, 5, 6, 8}, {0, 1, 2, 3, 6, 8}, {0, 1, 2, 4, 6, 8},
    {0, 1, 2, 6, 7, 8},
};

int num_tuple = 2;
int num_stages = 2;  // NUM_STAGESを変数化
int** pos = nullptr;

// 動的メモリ管理用ポインタ
double*** evs = nullptr;
double*** errs = nullptr;
double*** aerrs = nullptr;
int*** updatecounts = nullptr;

const int sympos[8][9] = {
    {0, 1, 2, 3, 4, 5, 6, 7, 8}, {0, 3, 6, 1, 4, 7, 2, 5, 8},
    {2, 1, 0, 5, 4, 3, 8, 7, 6}, {2, 5, 8, 1, 4, 7, 0, 3, 6},
    {6, 7, 8, 3, 4, 5, 0, 1, 2}, {6, 3, 0, 7, 4, 1, 8, 5, 2},
    {8, 7, 6, 5, 4, 3, 2, 1, 0}, {8, 5, 2, 7, 4, 1, 6, 3, 0},
};

void possetting(int a, vector<vector<int>>& combinations) {
  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < TUPLE_SIZE; j++) {
      pos[i][j] = poss[combinations[a][i]][j];
    }
  }
}

inline void init(int a, int stages) {
  num_stages = stages;  // 引数で受け取る
  vector<vector<int>> combinations;
  int total_combinations = pow(2, NUM_TUPLES);

  for (int mask = 1; mask < total_combinations; ++mask) {
    vector<int> current_combination;
    for (int i = 0; i < NUM_TUPLES; ++i) {
      if (mask & (1 << i)) {
        current_combination.push_back(i);
      }
    }
    combinations.push_back(current_combination);
  }
  auto customSort = [](const vector<int>& a, const vector<int>& b) {
    if (a.size() != b.size()) {
      return a.size() < b.size();
    }
    return a < b;
  };
  sort(combinations.begin(), combinations.end(), customSort);
  num_tuple = combinations[a].size();
  evs = new double**[num_stages];
  errs = new double**[num_stages];
  aerrs = new double**[num_stages];
  updatecounts = new int**[num_stages];
  pos = new int*[num_tuple];
  for (int i = 0; i < num_tuple; i++) {
    pos[i] = new int[TUPLE_SIZE];
  }

  for (int s = 0; s < num_stages; ++s) {
    evs[s] = new double*[num_tuple];
    errs[s] = new double*[num_tuple];
    aerrs[s] = new double*[num_tuple];
    updatecounts[s] = new int*[num_tuple];

    for (int t = 0; t < num_tuple; ++t) {
      evs[s][t] = new double[ARRAY_LENGTH]();
      errs[s][t] = new double[ARRAY_LENGTH]();
      aerrs[s][t] = new double[ARRAY_LENGTH]();
      updatecounts[s][t] = new int[ARRAY_LENGTH]();
      for (int u = 0; u < ARRAY_LENGTH; u++) {
        evs[s][t][u] = 0;
        errs[s][t][u] = 0;
        aerrs[s][t][u] = 0;
        updatecounts[s][t][u] = 0;
      }
    }
  }
  possetting(a, combinations);
}

// 解放関数
inline void cleanup() {
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      delete[] evs[s][t];
      delete[] errs[s][t];
      delete[] aerrs[s][t];
      delete[] updatecounts[s][t];
    }
    delete[] evs[s];
    delete[] errs[s];
    delete[] aerrs[s];
    delete[] updatecounts[s];
  }
  delete[] evs;
  delete[] errs;
  delete[] aerrs;
  delete[] updatecounts;
  for (int i = 0; i < num_tuple; i++) {
    delete[] pos[i];
  }
  delete[] pos;
}

inline void initEvs(double initEv) {
  double iev = initEv / num_tuple / 8;
  for (int s = 0; s < num_stages; s++) {
    for (int i = 0; i < num_tuple; i++) {
      for (long long j = 0; j < ARRAY_LENGTH; j++) {
        // printf("%d %d %d\n",s,i,j);
        evs[s][i][j] = iev;
      }
    }
  }
}

inline void print_info() {
  int k = 0;
  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < 9; j++) {
      if (pos[i][k] == j) {
        printf("1 ");
        k++;
      } else {
        printf("0 ");
      }
      if (j % 3 == 2) printf("\n");
    }
    printf("\n");
    k = 0;
  }
}

inline void writeEvs(FILE* fp) {
  size_t count;

  // evsを書き込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fwrite(evs[s][t], sizeof(double), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(stderr,
            "in writeEvs(): evs written %ld elements (should be %lld)\n", count,
            static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }

  // errsを書き込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fwrite(errs[s][t], sizeof(double), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(
        stderr, "in writeEvs(): errs written %ld elements (should be %lld)\n",
        count, static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }

  // aerrsを書き込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fwrite(aerrs[s][t], sizeof(double), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(
        stderr, "in writeEvs(): aerrs written %ld elements (should be %lld)\n",
        count, static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }

  // updatecountsを書き込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fwrite(updatecounts[s][t], sizeof(int), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(
        stderr,
        "in writeEvs(): updatecounts written %ld elements (should be %lld)\n",
        count, static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }
}

inline void readEvs(FILE* fp) {
  size_t count;

  // evs を読み込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fread(evs[s][t], sizeof(double), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(stderr, "in readEvs(): evs read %ld elements (should be %lld)\n",
            count,
            static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }

  // errs を読み込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fread(errs[s][t], sizeof(double), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(stderr, "in readEvs(): errs read %ld elements (should be %lld)\n",
            count,
            static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }

  // aerrs を読み込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fread(aerrs[s][t], sizeof(double), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(stderr, "in readEvs(): aerrs read %ld elements (should be %lld)\n",
            count,
            static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }

  // updatecounts を読み込む
  count = 0;
  for (int s = 0; s < num_stages; ++s) {
    for (int t = 0; t < num_tuple; ++t) {
      count += fread(updatecounts[s][t], sizeof(int), ARRAY_LENGTH, fp);
    }
  }
  if (count != num_stages * num_tuple * ARRAY_LENGTH) {
    fprintf(stderr,
            "in readEvs(): updatecounts read %ld elements (should be %lld)\n",
            count,
            static_cast<long long>(num_stages * num_tuple * ARRAY_LENGTH));
  }
}

inline int get_stage(const int* board) {
  int s = 0;
  if (num_stages == 2) {
    for (int i = 0; i < 9; i++) {
      if (board[i] >= 9) s = 1;
    }
  }
  return s;
}

inline void get_filterd_board_upper(const int* board, int* filterd_board) {
  int s = get_stage(board);
  for (int i = 0; i < 9; i++) {
    if(board[i] > 6){
        filterd_board[i] = 7;
    }
    else{
      filterd_board[i] = board[i];
    }
  }
}

inline void get_filterd_board_under(const int* board, int* filterd_board) {
  int s = get_stage(board);
  for (int i = 0; i < 9; i++) {
    if(board[i] < 6 && board[i] != 0){
        filterd_board[i] = 1;
    }
    else{
      filterd_board[i] = board[i];
    }
  }
}

inline double calcEv(const int* board) {
//   int s = get_stage(board);
    int filtered_board_upper[9];
    int filtered_board_under[9];
    get_filterd_board_upper(board, filtered_board_upper);
    get_filterd_board_under(board, filtered_board_under);

  double ev = 0;
  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < 8; j++) {
    //   int index = 0;
    int index_upper = 0,index_under = 0;
      for (int k = 0; k < TUPLE_SIZE; k++) {
        index_upper = index_upper * VARIATION_TILE + filtered_board_upper[sympos[j][pos[i][k]]];
        index_under = index_under * VARIATION_TILE + filtered_board_under[sympos[j][pos[i][k]]];
      }
      ev += evs[0][i][index_upper];
      ev += evs[1][i][index_under];
      // printf(" %f", evs[s][i][index]);
    }
  }
  // printf("\n");
  return ev;
}

inline double calcErr(const int* board) {
  int s = get_stage(board);

  double err = 0;
  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < 8; j++) {
      int index = 0;
      for (int k = 0; k < TUPLE_SIZE; k++) {
        index = index * VARIATION_TILE + board[sympos[j][pos[i][k]]];
      }
      err += errs[s][i][index];
    }
  }
  return err;
}

inline double calcAErr(const int* board) {
  // int s = get_stage(board);
  // int index_upper = 0, index_under = 0;
  int filtered_board_upper[9];
  int filtered_board_under[9];
  get_filterd_board_upper(board, filtered_board_upper);
  get_filterd_board_under(board, filtered_board_under);

  double aerr = 0;
  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < 8; j++) {
      int index_upper = 0,index_under = 0;
      for (int k = 0; k < TUPLE_SIZE; k++) {
        index_upper = index_upper * VARIATION_TILE + filtered_board_upper[sympos[j][pos[i][k]]];
        index_under = index_under * VARIATION_TILE + filtered_board_under[sympos[j][pos[i][k]]];
      }
      aerr += aerrs[0][i][index_upper];
      aerr += aerrs[1][i][index_under];
    }
  }
  return aerr;
}

inline double calcMinAErr(const int* board) {
  // int s = get_stage(board);
  // int index_upper = 0, index_under = 0;
  int filtered_board_upper[9];
  int filtered_board_under[9];
  get_filterd_board_upper(board, filtered_board_upper);
  get_filterd_board_under(board, filtered_board_under);

  double minAerr = DBL_MAX;
  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < 8; j++) {
      int index_upper = 0,index_under = 0;
      for (int k = 0; k < TUPLE_SIZE; k++) {
        index_upper = index_upper * VARIATION_TILE + filtered_board_upper[sympos[j][pos[i][k]]];
        index_under = index_under * VARIATION_TILE + filtered_board_under[sympos[j][pos[i][k]]];
      }
      if (minAerr > aerrs[0][i][index_upper]) {
        minAerr = aerrs[0][i][index_upper];
      }
      if (minAerr > aerrs[1][i][index_under]) {
        minAerr = aerrs[1][i][index_under];
      }
    }
  }
  return minAerr;
}

inline int calcMinCount(const int* board) {
  // int s = get_stage(board);
  int filtered_board_upper[9];
  int filtered_board_under[9];
  get_filterd_board_upper(board, filtered_board_upper);
  get_filterd_board_under(board, filtered_board_under);

  int minCount = INT_MAX;
  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < 8; j++) {
      int index_upper = 0, index_under = 0;
      for (int k = 0; k < TUPLE_SIZE; k++) {
        index_upper = index_upper * VARIATION_TILE + filtered_board_upper[sympos[j][pos[i][k]]];
        index_under = index_under * VARIATION_TILE + filtered_board_under[sympos[j][pos[i][k]]];
      }
      if (minCount > updatecounts[0][i][index_upper]) {
        minCount = updatecounts[0][i][index_upper];
      }
      if (minCount > updatecounts[1][i][index_under]) {
        minCount = updatecounts[1][i][index_under];
      }
    }
  }
  return minCount;
}

inline void update(const int* board, double diff) {
  // diff = diff / (num_tuple * 8 * 2);
  diff = diff / (num_tuple * 8);
//   int s = get_stage(board);

  for (int i = 0; i < num_tuple; i++) {
    for (int j = 0; j < 8; j++) {
      int index_upper = 0, index_under = 0;
      int filtered_board_upper[9];
      int filtered_board_under[9];
      get_filterd_board_upper(board, filtered_board_upper);
      get_filterd_board_under(board, filtered_board_under);
      for (int k = 0; k < TUPLE_SIZE; k++) {
          index_upper = index_upper * VARIATION_TILE + filtered_board_upper[sympos[j][pos[i][k]]];
          index_under = index_under * VARIATION_TILE + filtered_board_under[sympos[j][pos[i][k]]];
      }
      aerrs[0][i][index_upper] += fabs(diff);
      errs[0][i][index_upper] += diff;
      aerrs[1][i][index_under] += fabs(diff);
      errs[1][i][index_under] += diff;
      if (aerrs[0][i][index_upper] == 0) {
          evs[0][i][index_upper] += diff;
      } else {
          evs[0][i][index_upper] +=
              diff * (fabs(errs[0][i][index_upper]) / aerrs[0][i][index_upper]);
      }
      if (aerrs[1][i][index_under] == 0) {
          evs[1][i][index_under] += diff;
      } else {
          evs[1][i][index_under] +=
              diff * (fabs(errs[1][i][index_under]) / aerrs[1][i][index_under]);
      }
      updatecounts[0][i][index_upper]++;
      updatecounts[1][i][index_under]++;
    }
  }
}
}  // namespace NT6
#endif  // __TUPLES6_SYM_H__
