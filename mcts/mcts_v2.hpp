#pragma once
#include <unordered_map>
using namespace std;

#include "Game2048_3_3.h"
// #define DEBUGOUT(x) {x}
#define DEBUGOUT(x) \
  {}

/**
 * 盤面のハッシュ関数を定義
 */
static size_t hashBoard(const int board[9]) {
  size_t hashValue = 100;
  const int base = 12;
  for (int i = 0; i < 9; i++) {
    hashValue = hashValue * base + board[i];
  }
  return hashValue;
}

class node_t;

class edge_t {
 public:
  int tag;
  int r;
  node_t *cnode;
  int count;
  edge_t(int tag, int r, node_t *cnode)
      : tag(tag), r(r), cnode(cnode), count(0) {}

  string toString() const {
    char buf[1024];
    sprintf(buf, "(%d, %d, %p)", tag, r, cnode);
    return string(buf);
  }
};

class node_t {
 public:
  state_t state;
  int visit_count;
  double Q_value;
  bool expand_flg;
  vector<edge_t *> children;
  double ev;
  node_t(const state_t &state, double ev)
      : state(state),
        visit_count(0),
        Q_value(0),
        expand_flg(false),
        children(),
        ev(ev) {}

  double getQValue() const { return Q_value; }

  string toString() const {
    char buf[1024];
    sprintf(buf, "node p=%p vc=%d Qv=%.3f ef=%d cs=%ld ev=%.3f", this,
            visit_count, Q_value, expand_flg, children.size(), ev);
    string retval(buf);
    for (edge_t *e : children) retval += e->toString();
    return retval;
  }
};

class mcts_searcher_t {
  // search parameters
  int simulations;
  int randomTurn;
  int expand_count;
  double c;
  bool Boltzmann;
  bool expectimax;
  bool debug;

  // state-hashmap
  unordered_map<size_t, node_t *> stateNodeMap;
  unordered_map<size_t, node_t *> afterstateNodeMap;

  // counter
  int number_ev_calc;

  node_t *find_or_create_node_state(const state_t &state,
                                    unordered_map<size_t, node_t *> &nodemap) {
    size_t hvalue = hashBoard(state.board);
    if (nodemap.find(hvalue) == nodemap.end()) {
      node_t *node = new node_t(state, 0);
      nodemap[hvalue] = node;
    }
    return nodemap[hvalue];
  }

  node_t *find_or_create_node_afterstate(
      const state_t &afterstate, unordered_map<size_t, node_t *> &nodemap) {
    size_t hvalue = hashBoard(afterstate.board);
    if (nodemap.find(hvalue) == nodemap.end()) {
      double ev = calcEv(afterstate.board);
      number_ev_calc++;
      node_t *node = new node_t(afterstate, ev);
      nodemap[hvalue] = node;
    }
    return nodemap[hvalue];
  }

  void expand_state(node_t *node) {
    if (node->expand_flg) return;
    node->expand_flg = true;

    for (int d = 0; d < 4; d++) {
      state_t as;
      if (play(d, node->state, &as)) {
        node_t *cnode = find_or_create_node_afterstate(as, afterstateNodeMap);
        node->children.push_back(
            new edge_t(d, as.score - node->state.score, cnode));
      }
    }
    DEBUGOUT(printf("state expanded %s\n", node->toString().c_str()););
  }

  void expand_afterstate(node_t *node) {
    if (node->expand_flg) return;
    node->expand_flg = true;

    state_t state = node->state;
    for (int i = 0; i < 9; i++) {
      if (state.board[i] != 0) continue;

      {
        state.board[i] = 1;
        node_t *cnode = find_or_create_node_state(state, stateNodeMap);
        node->children.push_back(new edge_t(i, 0, cnode));
      }
      {
        state.board[i] = 2;
        node_t *cnode = find_or_create_node_state(state, stateNodeMap);
        node->children.push_back(new edge_t(i + 10, 0, cnode));
      }
      state.board[i] = 0;
    }
    DEBUGOUT(printf("afterstate expanded %s\n", node->toString().c_str()););
  }

  edge_t *do_state_select(node_t *node) {
    edge_t *retval = NULL;
    double max_value = -DBL_MAX;
    for (edge_t *e : node->children) {
      if (e->count == 0) {
        double v = 100000.0 + e->cnode->ev;
        if (max_value < v) {
          max_value = v;
          retval = e;
        }
      }
    }
    if (retval) {
      DEBUGOUT(printf("do_state_select: select unvisited edge %s\n",
                      retval->toString().c_str()););
      return retval;  // 未訪問のノードがあったら優先して辿る
    }

    if (Boltzmann) {
      double t = 100;  // FIXME
      vector<double> vals;
      for (edge_t *e : node->children)
        vals.push_back(exp(e->cnode->getQValue() / t));
      DEBUGOUT(printf("do_state_select: Boltzmann vals = ");
               for (double d
                    : vals) { printf("%.3f ", d); } printf("\n"););
      double sum_vals = reduce(vals.begin(), vals.end());

      double r = (double)rand() / RAND_MAX;
      DEBUGOUT(printf("do_state_select: Boltzmann r = %f\n", r););
      for (int i = 0; i < node->children.size(); i++) {
        if (r < vals[i] / sum_vals) {
          retval = node->children[i];
          break;
        }
        r -= vals[i] / sum_vals;
      }
      assert(retval);
      DEBUGOUT(printf("do_state_select: Boltzmann select edge %s\n",
                      retval->toString().c_str()););
      return retval;
    } else {
      // UCB に基づいて子を選ぶ
      int total_visit_count = 0;
      for (edge_t *e : node->children) total_visit_count += e->count;
      double lc = c;
      if (lc == -1) {
        lc = -DBL_MAX;
        for (edge_t *e : node->children) lc = max(lc, e->cnode->getQValue());
      }
      lc = max(lc, 1.0);
      double maxUCB = -DBL_MAX;
      DEBUGOUT(printf("do_state_select: UCB ucb = "););
      for (edge_t *e : node->children) {
        double ucb = e->cnode->getQValue() +
                     lc * sqrt(2.0 * log(total_visit_count) / e->count);
        DEBUGOUT(printf("%.3f ", ucb););
        if (maxUCB < ucb) {
          maxUCB = ucb;
          retval = e;
        }
      }
      DEBUGOUT(printf("\n"); printf("do_state_select: UCB select edge %s\n",
                                    retval->toString().c_str()););
      return retval;
    }

#ifdef STATE_SELECT_RANDOM  // ランダムに子を選ぶ
    return node->children[rand() % node->children.size()];
#endif
  }
  edge_t *do_afterstate_select(node_t *node) {
    // 重みつきランダムに子を選ぶ
    int pos = rand() % (node->children.size() / 2);
    int num = (rand() % 10 < 9) ? 0 : 1;
    DEBUGOUT(printf("do_afterstate_select: pos = %d num=%d select edge %s\n",
                    pos, num,
                    node->children[pos * 2 + num]->toString().c_str()););
    return node->children[pos * 2 + num];

#ifdef AFTERSTATE_SELECT_UNIFORM_RANDOM  // 単純ランダムで子を選択する場合はこちら
    return node->children[rand() % node->children.size()];
#endif
  }
  double do_playout(node_t *node) {
    double retval;
    if (randomTurn == 0) {
      retval = node->ev;

    } else {
      state_t state = node->state;
      bool reach_gameOver = false;
      for (int rt = 0; rt < randomTurn; rt++) {
        putNewTile(&state);
        if (gameOver(state)) {
          retval = state.score - node->state.score;
          reach_gameOver = true;
          break;
        }
        while (true) {
          int d = rand() % 4;
          if (play(d, state, &state)) break;
        }
      }
      if (!reach_gameOver) {
        retval = calcEv(state.board);
        number_ev_calc++;
      }
    }

    DEBUGOUT(printf("do_playout: retval = %.3f\n", retval););
    DEBUGOUT(
        printf("do_playout: node->Q_value updated %.3f -> ", node->Q_value););
    node->Q_value =
        (node->Q_value * (node->visit_count - 1) + retval) / node->visit_count;
    DEBUGOUT(printf(" %.3f\n", node->Q_value););
    assert(!isnan(node->Q_value));
    return retval;
  }

  void do_state_update(node_t *node, double ev) {
    DEBUGOUT(printf("do_state_update: node %s\n", node->toString().c_str()););
    DEBUGOUT(printf("do_state_update: node->Q_value updated %.3f -> ",
                    node->Q_value););
    if (expectimax) {
      // 子ノードの値の最大 (ただし，count > 0 のedgeのみ)
      node->Q_value = -DBL_MAX;
      for (edge_t *e : node->children) {
        if (e->count == 0) continue;
        double v = e->cnode->getQValue() + e->r;
        node->Q_value = max(node->Q_value, v);
      }
      assert(!isnan(node->Q_value));
    } else {
      // 出現したevの単純平均
      node->Q_value =
          (node->Q_value * (node->visit_count - 1) + ev) / node->visit_count;
    }
    DEBUGOUT(printf(" %.3f\n", node->Q_value););
  }

  void do_afterstate_update(node_t *node, double ev) {
    DEBUGOUT(
        printf("do_afterstate_update: node %s\n", node->toString().c_str()););
    DEBUGOUT(printf("do_afterstate_update: node->Q_value updated %.3f -> ",
                    node->Q_value););
    if (expectimax) {
      // 子ノードの値の重み付き平均 (ただし，count > 0 のedgeのみ)
      double sum = 0;
      int count = 0;
      for (int i = 0; i < node->children.size(); i++) {
        if (node->children[i]->count == 0) continue;
        sum += node->children[i]->cnode->getQValue() * ((i % 2 == 0) ? 9 : 1);
        count += ((i % 2 == 0) ? 9 : 1);
      }
      node->Q_value = sum / count;
      assert(!isnan(node->Q_value));
    } else {
      // 出現したevの単純平均
      node->Q_value =
          (node->Q_value * (node->visit_count - 1) + ev) / node->visit_count;
    }
    DEBUGOUT(printf(" %.3f\n", node->Q_value););
  }

  double simulation_afterstate_rec(node_t *node) {
    DEBUGOUT(printf("in simulation_afterstate_rec: %s\n",
                    node->toString().c_str()););
    node->visit_count++;
    if (node->visit_count > expand_count) expand_afterstate(node);

    if (node->expand_flg) {
      // 再帰的に木を下る
      edge_t *e = do_afterstate_select(node);
      double ev = simulation_state_rec(e->cnode) + e->r;
      e->count++;
      do_afterstate_update(node, ev);
      return ev;
    } else {
      double ev = do_playout(node);
      return ev;
    }
  }

  double simulation_state_rec(node_t *node) {
    DEBUGOUT(
        printf("in simulation_state_rec: %s\n", node->toString().c_str()););
    node->visit_count++;
    // state では評価値を計算できないので，必ず展開する
    expand_state(node);
    if (node->children.size() == 0) {
      DEBUGOUT(printf("exiting: game over with value 0\n"););
      return 0;  // ゲームオーバー時には子がない
    }

    // 再帰的に木を下る
    edge_t *e = do_state_select(node);
    double ev = simulation_afterstate_rec(e->cnode) + e->r;
    e->count++;
    do_state_update(node, ev);
    return ev;
  }

  void print_tree(node_t *node, int depth) {
    if (node->visit_count == 0) return;
    for (int i = 0; i < depth; i++) printf("  ");
    printf("%s\n", node->toString().c_str());
    for (edge_t *e : node->children) {
      print_tree(e->cnode, depth + 1);
    }
  }

  void do_simulation(node_t *root) { simulation_state_rec(root); }

 public:
  mcts_searcher_t(int simulations, int randomTurn, int expand_count, double c,
                  bool Boltzmann, bool expectimax, bool debug)
      : simulations(simulations),
        randomTurn(randomTurn),
        expand_count(expand_count),
        c(c),
        Boltzmann(Boltzmann),
        expectimax(expectimax),
        debug(debug),
        number_ev_calc(0) {}

  void clearCache() {
    for (auto kv : stateNodeMap) {
      for (auto e : kv.second->children) delete e;
      delete kv.second;
    }
    stateNodeMap.clear();
    for (auto kv : afterstateNodeMap) {
      for (auto e : kv.second->children) delete e;
      delete kv.second;
    }
    afterstateNodeMap.clear();
  }

  int search(const state_t &state, array<double, 5> &evals) {
    number_ev_calc = 0;
    node_t *root = find_or_create_node_state(state, stateNodeMap);
    expand_state(root);

    DEBUGOUT(printf("starting search for \n"););
    DEBUGOUT(state.print(););
    for (int nsim = 0; number_ev_calc < simulations and nsim < simulations;
         nsim++) {
      DEBUGOUT(
          printf("simulation %d number_ev_calc %d\n", nsim, number_ev_calc););
      DEBUGOUT(print_tree(root, 0););
      DEBUGOUT(printf("starting simulation\n"););
      do_simulation(root);
    }

    double maxv = -DBL_MAX;
    int move = -1;

    // 各子ノードの評価値を取得し、evals に格納
    for (edge_t *e : root->children) {
      double v = e->cnode->getQValue() + e->r;
      // if (e->tag >= 0 && e->tag < 4) {
      evals[e->tag] = v;  // 子ノードの評価値を evals に格納
      // }
      if (maxv < v) {
        maxv = v;
        move = e->tag;  // 最大評価値の手を更新
      }
    }

    evals[4] = maxv;  // 最後の要素に最大評価値を格納（オプション）
    return move;  // 最適な手を返す
  }
};
