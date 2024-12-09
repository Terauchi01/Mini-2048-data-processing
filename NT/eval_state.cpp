#include <array>
#include <cfloat>
#include <filesystem>
#include <iostream>

#include "4tuples_sym.h"
#include "6tuples_sym.h"
#include "Game2048_3_3.h"
#include "fread.h"
#include "play_table.h"
namespace fs = std::filesystem;
using namespace std;
int progress_calculation(int board[9]) {
  int sum = 0;
  for (int i = 0; i < 9; i++) {
    if (board[i] != 0) {
      sum += 1 << board[i];
    }
  }
  return sum / 2;
}
int main(int argc, char** argv) {
  if (argc < 2 + 1) {
    fprintf(stderr, "Usage: playgreedy <load-player-name> <EV-file>\n");
    exit(1);
  }
  string dname = argv[1];
  char* evfile = argv[2];
  string number(1, evfile[0]);
  double average = 0;
  FILE* fp = fopen(evfile, "rb");
  if (fp == NULL) {
    fprintf(stderr, "cannot open file: %s\n", evfile);
    exit(1);
  }
  if (number == "4") {
    NT4::readEvs(fp);
  } else {
    NT6::readEvs(fp);
  }
  fclose(fp);
  string s = "../board_data/" + dname + "/state.txt";
  fs::create_directory("../board_data");
  string dir = "../board_data/NT" + number + "/";
  fs::create_directory(dir);

  read_state_one_game(s);
  string file = "eval-state-" + dname + ".txt";
  string fullPath = dir + file;
  const char* filename = fullPath.c_str();
  fp = fopen(filename, "w+");
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
          double eval;
          if (number == "4") {
            eval = NT4::calcEv(tmp.board);
          } else {
            eval = NT6::calcEv(tmp.board);
          }
          fprintf(fp, "%f ", eval);
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