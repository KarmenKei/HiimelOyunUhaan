import random
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict


def most_common_kgram(seq: List[str], k: int) -> Tuple[Tuple[str, ...], int]:
    if k <= 0:
        raise ValueError("k 1-ээс их байх ёстой")
    if len(seq) < k:
        return tuple(), 0

    counts: Dict[Tuple[str, ...], int] = {}
    for i in range(len(seq) - k + 1):
        gram = tuple(seq[i:i + k])
        counts[gram] = counts.get(gram, 0) + 1

    best = max(counts.items(), key=lambda x: x[1])
    return best[0], best[1]


FEATURES = ("food", "bed", "toy")


@dataclass
class Room:
    features: List[str]

    @property
    def is_empty(self) -> bool:
        return len(self.features) == 0


def random_room(
    p_food: float = 0.35,
    p_bed: float = 0.25,
    p_toy: float = 0.30,
) -> Room:
    feats: List[str] = []
    if random.random() < p_food:
        feats.append("food")
    if random.random() < p_bed:
        feats.append("bed")
    if random.random() < p_toy:
        feats.append("toy")
    return Room(feats)


class Environment1D:
    def __init__(self, n_rooms: int, **room_probs):
        self.n = n_rooms
        self.room_probs = room_probs
        self.rooms: List[Room] = [random_room(**room_probs) for _ in range(n_rooms)]

    def reroll(self):
        self.rooms = [random_room(**self.room_probs) for _ in range(self.n)]


class Environment2D:
    def __init__(self, rows: int, cols: int, **room_probs):
        self.rows = rows
        self.cols = cols
        self.room_probs = room_probs
        self.grid: List[List[Room]] = [
            [random_room(**room_probs) for _ in range(cols)]
            for _ in range(rows)
        ]

    def reroll(self):
        self.grid = [
            [random_room(**self.room_probs) for _ in range(self.cols)]
            for _ in range(self.rows)
        ]


def serpentine_path(rows: int, cols: int) -> List[Tuple[int, int]]:
    path: List[Tuple[int, int]] = []
    for r in range(rows):
        if r % 2 == 0:
            for c in range(cols):
                path.append((r, c))
        else:
            for c in range(cols - 1, -1, -1):
                path.append((r, c))
    return path


class DogAgent:
    def __init__(self, lives: int, empty_streak_limit: int = 2):
        self.lives = lives
        self.empty_streak_limit = empty_streak_limit
        self.has_eaten = False
        self.empty_streak = 0
        self.life_losses = 0

    def lose_life(self, reason: str):
        self.lives -= 1
        self.life_losses += 1
        print(f"Амь хасагдлаа: {reason}. Үлдсэн амь = {self.lives}")
        self.has_eaten = False
        self.empty_streak = 0

    def choose_action(self, room: Room) -> str:
        if room.is_empty:
            return "empty"
        return random.choice(room.features)

    def step(self, room: Room) -> str:
        action = self.choose_action(room)

        print(f"Өрөөний онцлог: {room.features if room.features else ['empty']} | Сонгосон үйлдэл: {action}")

        if action == "food":
            self.has_eaten = True
            self.empty_streak = 0
            print("Нохой хоол идлээ")

        elif action == "bed":
            self.empty_streak = 0
            if self.has_eaten:
                self.lose_life("Хоол идсэний дараа унтсан")
            else:
                print("Нохой унтлаа")

        elif action == "toy":
            self.empty_streak = 0
            if not self.has_eaten:
                self.lose_life("Хоол идээгүй байхад тоглосон")
            else:
                print("Нохой тоглолоо")

        elif action == "empty":
            self.empty_streak += 1
            print(f"Хоосон өрөө. Дараалал = {self.empty_streak}")
            if self.empty_streak >= self.empty_streak_limit:
                self.lose_life("Хоосон өрөө дараалсан")

        else:
            raise ValueError("Тодорхойгүй үйлдэл")

        return action


def run_dog_game_2d(
    rows: int = 3,
    cols: int = 4,
    lives: int = 8,
    rounds: int = 30,
    empty_streak_limit: int = 2,
    room_probs: Optional[dict] = None,
):
    room_probs = room_probs or dict(p_food=0.38, p_bed=0.22, p_toy=0.30)
    env = Environment2D(rows, cols, **room_probs)
    dog = DogAgent(lives=lives, empty_streak_limit=empty_streak_limit)
    path = serpentine_path(rows, cols)

    for r in range(1, rounds + 1):
        if dog.lives <= 0:
            break

        print(f"\n{r}-р тойрог эхэллээ")
        visited_actions: List[str] = []

        for (rr, cc) in path:
            if dog.lives <= 0:
                break
            print(f"Өрөө ({rr},{cc})")
            visited_actions.append(dog.step(env.grid[rr][cc]))

        if len(visited_actions) >= 3:
            p1, c1 = most_common_kgram(visited_actions, 1)
            p2, c2 = most_common_kgram(visited_actions, 2)
            p3, c3 = most_common_kgram(visited_actions, 3)
            print("Энэ тойргийн давтамж")
            print(f"1 дараалал: {p1} -> {c1}")
            print(f"2 дараалал: {p2} -> {c2}")
            print(f"3 дараалал: {p3} -> {c3}")

        env.reroll()

    print("\nТоглоом дууслаа")
    print(f"Нийт амь хасалт: {dog.life_losses}")
    print(f"Үлдсэн амь: {dog.lives}")


if __name__ == "__main__":
    run_dog_game_2d()