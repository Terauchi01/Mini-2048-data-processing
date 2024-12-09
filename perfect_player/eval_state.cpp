#include <cfloat>
#include <filesystem>
#include <iostream>
#include <climits>

#include "Game2048_3_3.h"
#include "fread.h"
#include "perfect_play.h"
#include "play_table.h"
namespace fs = std::filesystem;
using namespace std;
int main(int argc, char** argv) {
  if (argc < 1 + 1) {
    fprintf(stderr, "Usage: playgreedy <load-player-name>\n");
    exit(1);
  }
  string dname = argv[1];
  string eval_player = "PP";
  double average = 0;
  readDB2();
  string s = "../board_data/" + dname + "/state.txt";
  fs::create_directory("../board_data");
  string dir = "../board_data/" + eval_player + "/";
  fs::create_directory(dir);

  read_state_one_game(s);
  string file = "eval-state-" + dname + ".txt";
  string fullPath = dir + file;
  const char* filename = fullPath.c_str();
  FILE* fp = fopen(filename, "w+");
  int i = 0;
  vector<vector<double>> eval_list;
  for (array<int, 9>& arr : boards) {
    vector<double> evals(4, -10000);
    if (arr[0] == -1) {
      fprintf(fp, "%s\n", gameovers[i].c_str());
      i++;
    } else {
      state_t state, tmp;
      for (int j = 0; j < 9; j++) {
        state.board[j] = arr[j];
      }
      for (int d = 0; d < 4; d++) {
        if (play(d, state, &tmp)) {
          fprintf(fp, "%f ", eval_afterstate(tmp.board));
        } else {
          fprintf(fp, "-10000000000.000000 ");
        }
        if (d == 3) {
          fprintf(fp, "%d\n", progress_calculation(state.board));
        }
      }
    }
  }
  fclose(fp);

  return 0;
}