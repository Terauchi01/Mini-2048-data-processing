#include <cfloat>
#include <climits>
#include <filesystem>
#include <iostream>

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
  string s = "../board_data/" + dname + "/after-state.txt";
  fs::create_directory("../board_data");
  string dir = "../board_data/" + eval_player + "/";
  fs::create_directory(dir);

  read_state_one_game(s);
  string file = "eval-after-state-" + dname + ".txt";
  string fullPath = dir + file;
  const char* filename = fullPath.c_str();
  FILE* fp = fopen(filename, "w+");
  int i = 0;
  for (array<int, 9>& arr : boards) {
    if (arr[0] == -1) {
      fprintf(fp, "%s\n", gameovers[i].c_str());
      i++;
    } else {
      int board[9];
      for (int j = 0; j < 9; j++) {
        board[j] = arr[j];
      }
      double eval = eval_afterstate(board);
      fprintf(fp, "%f\n", eval);
    }
  }
  fclose(fp);

  return 0;
}