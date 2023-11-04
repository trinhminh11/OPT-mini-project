#include<bits/stdc++.h>
using namespace std;

const int MAX = 100;
const int INF = 1e9+7;

int N;
int K;
int distance_matrix[MAX][MAX];
bool visited[MAX];
int demands[MAX];
int hub = 0;
int ans[MAX];
int total_dist = INF;
int current_dist = 0;
int capacity = 0;
int _lower_bound = INF;

void import_data(){
	cin >> N;
	cin >> K;
	for(int i = 0; i <= 2*N; i++){
		for(int j = 0; j <= 2*N; j++){
			cin >> distance_matrix[i][j];

			if (distance_matrix[i][j] < _lower_bound && i!=j){
				_lower_bound = distance_matrix[i][j];
			}

		}
	}
	for(int i = 0; i <= 2*N; i++){
		visited[i] = false;
		if (i <= N){
			demands[i] = 1;
		}
		else{
			demands[i] = -1;
		}
	}
	demands[0] = 0;
}

void bt(int pos){
	if (pos == 2*N + 1){
		if (current_dist + distance_matrix[ans[2*N]][0] < total_dist){
			total_dist = current_dist + distance_matrix[ans[2*N]][0];
		}
		return ;
	}

	for(int i = 1; i <= 2*N;i++){
		if (i > N){
			if (!visited[i-N]){
				continue;
			}
		}
		if (visited[i] || capacity + demands[i] > K){
			continue;
		}

		ans[pos] = i;
		visited[i] = true;
		current_dist += distance_matrix[ans[pos-1]][ans[pos]];
		capacity += demands[i];
		
		if (current_dist + _lower_bound * (2*N+1-pos) < total_dist){
			bt(pos+1);
		}

		visited[i] = false;
		current_dist -= distance_matrix[ans[pos-1]][ans[pos]];
		capacity -= demands[i];
	}
}

void solve(){
	ans[0] = hub;
	visited[hub] = true;

	bt(1);
}
				
	
void print_sol(){
	cout << total_dist;
}

int main(){
	import_data();

	solve();

	print_sol();
}
