#include <bits/stdc++.h>
#define pb push_back

using namespace std;

const int INF = 1e9+7;
const int MAX_N = 1000+1;

int time_matrix[MAX_N][MAX_N];
int N;

struct Node{
	Node(){};
	int ID, e, l, d, time_done = 0;
	Node(int ID, int e, int l, int d){
		this->ID = ID;
		this->e = e;
		this->l = l;
		this->d = d; 
	}
};

Node nodes[MAX_N+1];
vector<Node> route;

void import_data(){
	cin >> N;
	nodes[0] = Node(0, 0, INF, 0);
	for (int i = 1; i <= N; i++){
		int e, l,d;
		cin >> e >> l >> d;
		nodes[i] = Node(i, e, l, d);
	}

	for (int i = 0; i <= N; i++){
		for(int j = 0; j <= N; j++){
			cin >> time_matrix[i][j];
		}
	}
}

void calc_runtime(vector<Node> &route){
	int current_time = 0;
	for (int i = 0; i < route.size(); i++){
		if (i == 0){
			current_time += time_matrix[0][route[i].ID];
		}
		else{
			current_time += time_matrix[route[i-1].ID][route[i].ID];
		}

		if (current_time < route[i].e){
			current_time = route[i].e + route[i].d;
		}
		else if (route[i].e <= current_time && current_time <= route[i].l){
			current_time += route[i].d;
		}
		else{
			for (int j = 0; j < route.size(); j++){
				cout << route[j].ID << " " << route[j].time_done << endl;
			}
			cout << "???";
			exit(0);
		}
		route[i].time_done = current_time;
	}
}

void Insert(Node node){
	int best_time = INF;
	int best_pos = -1;

	for (int i = 0; i <= route.size(); i++){
		int current_time;
		if (i == 0){
			current_time = time_matrix[0][node.ID];
		}
		else{
			current_time = route[i-1].time_done + time_matrix[route[i-1].ID][node.ID];

		}
		if (current_time < node.e){
			current_time = node.e;
		}
		if (current_time > node.l){
			break;
		}

		current_time += node.d;

		bool check_constraint = true;
		int prev_id = node.ID;

		for(int j = i; j < route.size(); j++){
			current_time += time_matrix[prev_id][route[j].ID];
			if (current_time < route[j].e){
				current_time = route[j].e;
			}
			if (current_time > route[j].l){
				check_constraint = false;
				break;
			}
			current_time += route[j].d;
			prev_id = route[j].ID;
		}

		if (check_constraint){
			int run_time = current_time + time_matrix[prev_id][0];
			if (run_time < best_time){
				best_time = run_time;
				best_pos = i;
			}
		}

	}

	if (best_time != INF){
		route.insert(route.begin() + best_pos, node);
		calc_runtime(route);
	}

	else{
		cout << "WTF";
		exit(0);
	}
}

void solve(){
	for (int i = 1; i <= N; i++){
		Insert(nodes[i]);
	}
}

void print_sol(){
	cout << route.size() << endl;

	for(int i = 0; i < route.size(); i++){
		cout << route[i].ID << " ";
	}
}


int main(){
	import_data();
	solve();
	print_sol();
}
