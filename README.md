# michi

Michi was designed to be an optimal path solver for racing lines. The intuition was to find the shortest path through a circuit, where the "road" was defined by two lines on a graph.

This was solved using a modified version of Dijkstra's algorithm, but I realized that this approach is actually flawed. The optimal line around a circuit is usually the line that sets the vehicle up for the best exit around a turn, both in racing line positioning and speed.
