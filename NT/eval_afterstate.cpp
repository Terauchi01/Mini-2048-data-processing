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
int main(int argc, char** argv) {
  if (argc < 1 + 1) {
    fprintf(stderr, "Usage: playgreedy <load-player-name> <EV-file>\n");
    exit(1);
  }
  string dname = argv[1];
  char* evfile = argv[2];
  double average = 0;
  FILE* fp = fopen(evfile, "rb");
  if (fp == NULL) {
    fprintf(stderr, "cannot open file: %s\n", evfile);
    exit(1);
  }
  string number(1, evfile[0]);
  if (number == "4") {
    NT4::readEvs(fp);
  } else {
    NT6::readEvs(fp);
  }
  fclose(fp);
  string s = "../board_data/" + dname + "/after-state.txt";
  fs::create_directory("../board_data");
  string dir = "../board_data/NT" + number + "/";
  fs::create_directory(dir);

  read_state_one_game(s);
  string file = "eval-afterstate-" + dname + ".txt";
  string fullPath = dir + file;
  const char* filename = fullPath.c_str();
  fp = fopen(filename, "w+");
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
      double eval;
      if (number == "4") {
        eval = NT4::calcEv(board);
      } else {
        eval = NT6::calcEv(board);
      }
      fprintf(fp, "%f\n", eval);
    }
  }
  fclose(fp);

  return 0;
}