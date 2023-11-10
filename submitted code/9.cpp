#include <bits/stdc++.h>
#define pb push_back

using namespace std;

const int INF = 1e9 + 7;
int N,K;

struct Data{
	int container_index, x, y, rotation;
	vector<pair<int, int>>::iterator pos;

	Data(int container_index, int x, int y, int rotation, vector<pair<int, int>>::iterator p){
		this->container_index = container_index;
		this->x = x; 
		this->y = y; 
		this->rotation = rotation; 
		this->pos = p;
	}

};

struct Container{
	Container(){};
	int ID;
	int W;
	int H;
	int cost;
	vector<int> boxes;
	bool used = false;
	vector<pair<int, int>> boxes_pos = {{0, 0}};
};

struct Box{
	Box(){};
	int ID;
	int w;
	int h;
	int truck;
	int x, y;
	bool rotation = false;
};


vector<Box> boxes;
vector<Container> containers;

void import_data(){

	cin >> N >> K;
	boxes.resize(N);
	containers.resize(K);

	for(int i = 0; i < N; i++){
		boxes[i].ID = i+1;
		cin >> boxes[i].w >> boxes[i].h;
	}
	for(int i = 0; i < K; i++){
		containers[i].ID = i+1;
		cin >> containers[i].W >> containers[i].H >> containers[i].cost;
	}
}

bool Box_check_intersect(Box box1, Box box2){
	int w1 = box1.w, h1 = box1.h;
	if(box1.rotation){
		swap(w1, h1);
	}

	int w2 = box2.w, h2 = box2.h;
	if(box2.rotation == 1){
		swap(w2, h2);
	}

	if (max(box1.x, box2.x) >= min(box1.x+w1, box2.x+w2) || max(box1.y, box2.y) >= min(box1.y+h1, box2.y+h2)){
		return false;
	}

	return true;

}


void Container_Insert_box(Box &box, Container &container, int x, int y, bool rotation){
	box.x = x; 
	box.y = y; 
	box.rotation = rotation;
	
	int w = box.w, h = box.h;
	if(box.rotation){
		swap(w, h);
	}

	container.boxes_pos.pb({x, y+h});
	container.boxes_pos.pb({x+w, y});
	container.boxes.pb(box.ID);

	box.truck = container.ID;
}

bool Container_check_box(Box &box, Container &container, int x, int y, bool rotation){

	int w = box.w, h = box.h;
	box.x = x;
	box.y = y;
	box.rotation = rotation;

	if(box.rotation){
		swap(w, h);
	}

	if (x + w > container.W || y + h > container.H){
		return false;
	}

	for(auto &box_ID: container.boxes){
		if(Box_check_intersect(box, boxes[box_ID-1])){
			return false;
		}
	}

	return true;
}



Data find_best_container(Box &box, bool used){
	vector<pair<int, int>>::iterator best_pos;
	int best_rotation = 0;
	int best_x = -1;
	int best_y = -1;
	int best_container_index = -1;
	int min_cost = INF;

	// don't know why x + y work here but who care :D, it's worked
	int sum_XY = -1;


	for (int i = 0; i < containers.size(); i++){
		if (containers[i].used == used){
			for(vector<pair<int, int>>::iterator pos = containers[i].boxes_pos.begin(); pos != containers[i].boxes_pos.end(); pos++){
				for(int rotation = 0; rotation <= 1; rotation++){
					if(Container_check_box(box, containers[i], pos->first, pos->second,rotation)){
						if(containers[i].cost < min_cost || containers[i].cost == min_cost && pos->first + pos->second < sum_XY){
							min_cost = containers[i].cost;
							best_container_index = i;
							best_rotation = rotation;
							best_pos = pos;
							best_x = pos->first;
							best_y = pos->second;
							sum_XY = best_x + best_y;
						}
					}
				}
			}

			if (containers[i].cost >= min_cost){
				break;
			}
		}
	}

	if (min_cost != INF){
		return Data(best_container_index, best_x, best_y, best_rotation, best_pos);
	}
	return find_best_container(box, false);

}


void solve(){
	sort(containers.begin(), containers.end(), [&](Container x, Container y){
		if (x.cost < y.cost){
			return true;
		}
		else if (x.cost == y.cost && x.ID < y.ID){
			return true;
		}
		return false;
	});



	// sort(boxes.begin(), boxes.end(), [&](Box x, Box y){
	// 	return x.x * x.y < y.x * y.y;
	// });


	for(auto &box: boxes){

		Data data = find_best_container(box, true);

		containers[data.container_index].boxes_pos.erase(data.pos);

		Container_Insert_box(box, containers[data.container_index], data.x, data.y, data.rotation);

		containers[data.container_index].used = true;

	}
}

void print_sol(){
	for(auto &box: boxes){
		cout << box.ID << " " << box.truck << " " << box.x << " " << box.y << " " << box.rotation << endl;
	}
}

int main(){
	import_data();
	solve();
	print_sol();
}
