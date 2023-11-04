#include<bits/stdc++.h>
#define pb push_back

using namespace std;

const int MAX_N = 1000;
const int MAX_M = 20;
const int INF = 1e9+7;

struct Room{
	Room(){};
	int ID;
	int capacity;
};

struct Slot{
	Slot(){};
	int ID = ID;
	set<int> used;
	Slot(int ID){
		this->ID = ID;
	}
};

struct Class{
	Class(){};
	int ID;
	int num_student;
	set<int> share_course;
	set<int> rooms;
	int exam;
	int slot;
};

int N, M, K;

Class classes[MAX_N+1];
int class_indexes[MAX_N+1];
Room rooms[MAX_M+1];
vector<Slot> slots;


void import_data(){
	cin >> N >> M;
	for (int i = 1; i<=N;i++){
		class_indexes[i] = i;
		classes[i].ID = i;
		cin >> classes[i].num_student;
	}

	for (int i = 1; i<=M; i++){
		rooms[i].ID = i;
		cin >> rooms[i].capacity;
	}

	cin >> K;
	for (int _ = 0; _ < K; _++){
		int u, v;
		cin >> u >> v;
		classes[u].share_course.insert(v);
		classes[v].share_course.insert(u);
	}


    // for(auto &c: classes[2].share_course){	
    //     cout << c << " ";
    // }

	// exit(0);

}


void find_possible_rooms(){
	for (int i = 1; i <= N; i++){
		for(int j = 1; j <= M; j++){
			if (rooms[j].capacity >= classes[i].num_student){
				classes[i].rooms.insert(j);
			}
		}
	}
}

void solve(){
	find_possible_rooms();

	sort(class_indexes+1, class_indexes+1 + N, [&](int x, int y){
		return classes[x].rooms.size() < classes[y].rooms.size();
	});


	for (int i = 1; i <= N; i++){
		int c = class_indexes[i];
		int slot = 1;
		while (true){
			if (slot > slots.size()){
				slots.pb(Slot(slot));
			}
			bool _check = true;
			for (auto &c2: classes[c].share_course){
				if (slot == classes[c2].slot){
					_check = false;
					break;
				}
			}
			if (_check){
				bool check = false;
				for(auto &room: classes[c].rooms){
					auto pos = slots[slot-1].used.find(room);
					if (pos == slots[slot-1].used.end()){
						classes[c].exam = rooms[room].ID;
						classes[c].slot = slot;
						slots[slot-1].used.insert(room);
						check = true;
						// if (classes[c].ID == 2 || classes[c].ID == 31){
							// cout << classes[c].ID << " " << classes[c].slot << endl;
						// }
						break;
					}
				}
				if(check){
					break;
				}
			}
			slot ++;
		}
	}
	sort(classes, classes + N, [&](Class x, Class y){
		return x.ID < y.ID;
	});
}

void print_sol(){
	for(int c = 1; c <= N; c++){
		cout << classes[c].ID << " " << classes[c].slot << " " << classes[c].exam << endl;
	}
}


int main(){
	import_data();
	
	solve();

	print_sol();
}
