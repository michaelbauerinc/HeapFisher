# HeapFisher


## Game Controls/Rules

- Move your ship left and right with the arrow keys

- Press spacebar to drop your hook

- Your goal is to hook as much valuable treasure from the chests as possible before the time is up.

- After hooking a chest, the value will be added to a queue of numbers.

- After this queue reaches 4, the next hooked treasure will add the sum to your score.

- If your hook collides with a piranha, it will automatically retract up.

- You may not hook a chest in the top row more than twice in a row.


## Installation

### Dependencies

- Python3
- Pygame

### Without virtual environment

1. 
```
pip3 install pygame
```

2. 
```
python3 GameRun.py
```

### With virtual environment

1. 
```
python3 -m venv venv
```

2. 
```
source venv/bin/activate
```

3. 
```
pip3 install pygame
```

4. 
```
python3 GameRun.py
```
