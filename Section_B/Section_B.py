import sys
import io

INPUT = """\
4
2 2
1 2
5 3
1 2
1 3
1 4
1 5
6 3
1 2
1 3
2 4
2 5
3 6
10 5
3 8
6 10
7 8
8 1
1 4
4 5
9 2
2 5
5 10
"""

def tree():
 
    input_data = INPUT.split()
    iterator = iter(input_data)
    
    try:
        t = int(next(iterator))
    except StopIteration:
        return

    out = []
    for _ in range(t):
        n = int(next(iterator))
        k = int(next(iterator))
        
        # Build the adjacency list for the tree
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u = int(next(iterator))
            v = int(next(iterator))
            adj[u].append(v)
            adj[v].append(u)
            
        # Initialize subtree sizes and parent array
        sz = [1] * (n + 1)
        parent = [0] * (n + 1)
        
        # Iterative BFS to establish a top-down order (avoids recursion limits)
        order = [1]
        visited = [False] * (n + 1)
        visited[1] = True
        
        head = 0
        while head < len(order):
            u = order[head]
            head += 1
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    order.append(v)
                    
        # Traverse bottom-up (reverse of BFS order) to compute subtree sizes
        for i in range(n - 1, -1, -1):
            u = order[i]
            p = parent[u]
            if p != 0:
                sz[p] += sz[u]
                
        # Calculate Kawaiiness
        # Every node is a valid LCA when it is chosen as the root (since n >= k)
        ans = n 
        
        # Every node (except root 1) represents an edge to its parent
        for u in range(2, n + 1):
            s1 = sz[u]         # Size of the component containing 'u'
            s2 = n - s1        # Size of the component containing the 'parent'
            
            # If rooted in parent's side, u's subtree size is s1
            if s1 >= k:
                ans += s2
            
            # If rooted in u's side, parent's branch size is s2
            if s2 >= k:
                ans += s1
                
        out.append(str(ans))
        
    # Output all results at once
    print('\n'.join(out))

if __name__ == '__main__':
    tree()