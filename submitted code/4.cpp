#include <bits/stdc++.h>
#define pb push_back

using namespace std;

const int MAX_N = 50 + 1;
const int MAX_M = 1000 + 1;
const int INF = 1e9 + 7;

int N, M;
int visited[MAX_N];
int Q[MAX_N][MAX_M];
int distance_matrix[MAX_M][MAX_M];
int q[MAX_N]; 
int current_load[MAX_N];

vector<int> route;

void import_data(){
	cin >> N >> M;

	for(int i = 1; i <= N; i++){
		for(int j = 1; j <= M; j++){
			cin >> Q[i][j];
		}
	}

	for(int i = 0;i <= M; i++){
		visited[i] = false;

		for(int j = 0; j <= M; j++){
			cin >> distance_matrix[i][j];
		}
	}
	for(int i = 1; i <= N; i++){
		cin >> q[i];
	}
}


void solve(){
	for(int i = 1; i <= N; i++){
		current_load[i] = 0;
	}

	int current_node = 0;

	while(true){
		int min_dist = INF; 
		int best_node = -1;

		for(int node = 1; node <= M; node ++){
			if (visited[node]){
				continue;
			}
			if(distance_matrix[current_node][node] < min_dist){
				min_dist = distance_matrix[current_node][node]; 
				best_node = node;
			}
		}

		for(int i = 1; i <= N; i++){
			current_load[i] += Q[i][best_node];
		}

		route.pb(best_node);

		current_node = best_node;
		visited[best_node] = true;

		bool check = true;
		for(int i = 1; i <= N; i++) {
			if(current_load[i] < q[i]){
				check = false; 
				break;
			}
		}

		if(check){
			break;
		}
	}

}

void print_sol(){
	cout << route.size() << endl;
	for(int i = 0; i < route.size(); i++){
		cout << route[i] << " ";
	}
}


int main(){
	import_data();

	solve();

	print_sol();
}
