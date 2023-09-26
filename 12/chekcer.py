from CONSTANT import Node, import_data


def Checker(Nodes: list[Node], Time_matrix: list[list], nodesIDs):
	current_time = 0
	check_ID = [0]
	print("current node: 0, time = 0")
	for i in range(1, len(nodesIDs)):


		if nodesIDs[i] in check_ID:
			print(f'Node {nodesIDs[i]} is already served')
			exit()

		print(f'current node: {nodesIDs[i]}')

		check_ID.append(nodesIDs[i])
		prev_node = Nodes[nodesIDs[i-1]]
		current_node = Nodes[nodesIDs[i]]


		current_time += Time_matrix[prev_node.ID][current_node.ID]

		print(f'time to go from node {nodesIDs[i-1]} to node {nodesIDs[i]} is: {Time_matrix[prev_node.ID][current_node.ID]}')


		if current_time < current_node.e:
			print(f'time window = [{current_node.e}, {current_node.l}]')
			print(f'arrived early, time = {current_time}')

			current_time = current_node.e

			print(f'after waiting, time = {current_time}')

		elif current_node.e <= current_time <= current_node.l:
			print(f'time window = [{current_node.e}, {current_node.l}]')
			print(f'time = {current_time}')
		else:
			print(f'current time: {current_time} is greater than time window of Node {current_node.ID} ({current_node.e} - {current_node.l})')
			exit()		

		current_time += current_node.d

		print(f'load: {current_node.d}')

		print(f'time after load: {current_time}')

	
	print("True")


def import_output(file):
	with open(file, 'r') as f:
		f.readline()
		nodeIDs = list(map(int, f.readline().split()))
	
	nodeIDs = [0] + nodeIDs
	return nodeIDs

def main():
	N, Nodes, Time_matrix = import_data('test.txt')
	nodeIDs = import_output('output.txt')

	Checker(Nodes, Time_matrix, nodeIDs)


if __name__ == "__main__":
	main()