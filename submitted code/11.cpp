#include<bits/stdc++.h>

#define pb push_back

using namespace std;

const int INF = 1e9+7;
const int MAX_N = 1000+1;
const int MAX_K = 100;

struct Truck{
	vector<int> route;
	int time = 0;
	Truck(){route.pb(0);};
};

int time_matrix[MAX_N][MAX_N];
int N, K;
bool visited[MAX_N];
Truck trucks[MAX_K];

void import_data(){
	cin >> N >> K;
	visited[0] = true;
	for (int i = 1; i <= N; i++){
		visited[i] = false;
	}
	for (int i = 0; i <= N; i++){
		for(int j = 0; j <= N; j++){
			cin >> time_matrix[i][j];
		}
	}

}



int calc_runtime(vector<int> route){
	int _time = 0;
	for (int i = 1; i< route.size();i++){
		_time += time_matrix[route[i-1]][route[i]];
	}
	return _time;
}

void solve(){
	
	for (int i = 1; i<= N; i++){
		int best_pos = -1;
		int best_time = INF;
		int best_node = -1;

		for (int node = 1; node <= N; node ++){
			if (visited[node]){
				continue;
			}

			for (int pos = 0; pos < K; pos++){
				
				int _time = trucks[pos].time + time_matrix[trucks[pos].route[trucks[pos].route.size()-1]][node];
				if (_time < best_time){
					best_pos = pos;
					best_time = _time;
					best_node = node;
				}

			}
			
		}
		trucks[best_pos].route.pb(best_node);
		trucks[best_pos].time = best_time;
		visited[best_node] = true;

	}
}


void print_sol(){
	cout << K << endl;
	for (int pos = 0; pos < K; pos++){
		cout << trucks[pos].route.size() << endl;
		for (int i = 0; i < trucks[pos].route.size();i++){
			cout << trucks[pos].route[i] << " ";
		}
		cout << endl;
	}
}

int main(){
	import_data();

	solve();

	print_sol();
}
