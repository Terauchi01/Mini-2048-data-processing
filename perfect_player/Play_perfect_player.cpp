#include <array>
#include <cfloat>
#include <climits>
#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <list>
#include <unordered_map>

namespace fs = std::filesystem;
using namespace std;

#include "Game2048_3_3.h"
#include "perfect_play.h"

class GameOver {
 public:
  int gameover_turn;
  int game;
  int progress;
  int score;
  GameOver(int gameover_turn_init, int game_init, int progress_init,
           int score_init)
      : gameover_turn(gameover_turn_init),
        game(game_init),
        progress(progress_init),
        score(score_init) {}
};
int progress_calculation(int board[9]) {
  int sum = 0;
  for (int i = 0; i < 9; i++) {
    sum += 1 << board[i];
  }
  return sum / 2;
}

int main(int argc, char** argv) {
  if (argc < 2 + 1) {
    fprintf(stderr, "Usage: playgreedy <seed> <game_counts>>\n");
    exit(1);
  }
  int seed = atoi(argv[1]);
  int game_count = atoi(argv[2]);
  fs::create_directory("../board_data");
  string dir = "../board_data/PP";
  fs::create_directory(dir);
  readDB2();
  srand(seed);
  list<array<int, 9>> state_list;
  list<array<int, 9>> after_state_list;
  list<array<double, 5>> eval_list;
  list<GameOver> GameOver_list;
  double score_sum = 0;
  for (int gid = 1; gid <= game_count; gid++) {
    state_t state = initGame();
    int turn = 0;
    while (true) {
      turn++;
      state_t copy;
      double max_evr = -DBL_MAX;
      int selected = -1;
      const int n = 5;
      double pp[n];
      for (int i = 0; i < n; i++) {
        pp[i] = -1.0e10;
      }
      for (int d = 0; d < 4; d++) {
        if (play(d, state, &copy)) {
          // int index = to_index(copy.board);
          pp[d] = eval_afterstate(copy.board);
          if (max_evr < pp[d]) {
            max_evr = pp[d];
            selected = d;
          }
        }
      }
      state_list.push_back(
          array<int, 9>{state.board[0], state.board[1], state.board[2],
                        state.board[3], state.board[4], state.board[5],
                        state.board[6], state.board[7], state.board[8]});
      play(selected, state, &state);
      after_state_list.push_back(
          array<int, 9>{state.board[0], state.board[1], state.board[2],
                        state.board[3], state.board[4], state.board[5],
                        state.board[6], state.board[7], state.board[8]});
      state_list.push_back(array<int, 9>{0, 1, 2, 3, 4, 5, 6, 7, 8});
      eval_list.push_back(array<double, 5>{pp[0], pp[1], pp[2], pp[3], pp[4]});
      putNewTile(&state);

      if (gameOver(state)) {
        GameOver_list.push_back(GameOver(
            turn, gid, progress_calculation(state.board), state.score));
        // score_sum += state.score;
        // printf("score = %d\n", state.score);
        break;
      }
    }
  }
  printf("average = %f\n", score_sum / game_count);
  string file = "state.txt";
  string fullPath = dir + file;
  const char* filename = fullPath.c_str();
  // 書き込みモードでファイルを開く
  FILE* fp = fopen(filename, "w+");
  int i = 0;
  auto trun_itr = GameOver_list.begin();
  for (auto itr = state_list.begin(); itr != state_list.end(); itr++) {
    i++;
    if ((trun_itr)->gameover_turn == i) {
      i = 0;
      printf("gameover_turn: %d; game: %d; progress: %d; score: %d\n",
             (trun_itr)->gameover_turn, (trun_itr)->game, (trun_itr)->progress,
             (trun_itr)->score);
    } else {
      for (int j = 0; j < 9; j++) {
        printf("%d ", (*itr)[j]);
      }
      printf("\n");
    }
  }
  fclose();
  string file = "after-state.txt";
  string fullPath = dir + file;
  const char* filename = fullPath.c_str();
  // 書き込みモードでファイルを開く
  FILE* fp = fopen(filename, "w+");
  int i = 0;
  auto trun_itr = GameOver_list.begin();
  for (auto itr = state_list.begin(); itr != state_list.end(); itr++) {
    i++;
    if ((trun_itr)->gameover_turn == i) {
      i = 0;
      printf("gameover_turn: %d; game: %d; progress: %d; score: %d\n",
             (trun_itr)->gameover_turn, (trun_itr)->game, (trun_itr)->progress,
             (trun_itr)->score);
    } else {
      for (int j = 0; j < 9; j++) {
        printf("%d ", (*itr)[j]);
      }
      printf("\n");
    }
  }
}