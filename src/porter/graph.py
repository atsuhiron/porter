from dataclasses import dataclass

from porter.vo import PostId


@dataclass(frozen=True)
class PostPath:
    path: tuple[PostId, ...]
    total_time: float


@dataclass(frozen=True)
class PostGraph:
    posts: dict[PostId, dict[PostId, float]]  # post_id -> (post_id -> time)

    def get_times_from(self, post_id: PostId) -> dict[PostId, float]:
        return self.posts[post_id]


    def find_shortest_path(self, from_id: PostId, to_id: PostId) -> PostPath:
        visited = set()
        path = []
        current_id = from_id
        total_time = 0

        while current_id != to_id:
            visited.add(current_id)
            path.append(current_id)

            next_id = None
            min_time = float("inf")
            for neighbor_id, time in self.get_times_from(current_id).items():
                if neighbor_id in visited:
                    continue
                if time < min_time:
                    min_time = time
                    next_id = neighbor_id

            if next_id is None:
                raise ValueError(f"No path from {from_id} to {to_id}")

            total_time += min_time
            current_id = next_id

        path.append(to_id)
        return PostPath(tuple(path), total_time)


if __name__ == "__main__":
    graph = PostGraph(
        posts={
            PostId("A"): {PostId("B"): 1, PostId("C"): 4},
            PostId("B"): {PostId("A"): 1, PostId("C"): 2, PostId("D"): 5},
            PostId("C"): {PostId("A"): 4, PostId("B"): 2, PostId("D"): 1},
            PostId("D"): {PostId("B"): 5, PostId("C"): 1},
        }
    )
    path = graph.find_shortest_path(PostId("A"), PostId("D"))
    print(path)  # noqa: T201
