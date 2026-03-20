# Turtlesim Waypoint Navigator

A ROS2 Python node that autonomously navigates a turtle in Turtlesim through a series of user-defined waypoints using proportional control.

---

## Demo

The turtle automatically steers through each waypoint in sequence and stops when all waypoints are reached. The default configuration draws a **5-pointed star** pattern.

```
Waypoints visited:
  (5.5, 9.0) → (2.3, 3.5) → (8.7, 7.2) → (2.3, 7.2) → (8.7, 3.5) → (5.5, 9.0)
```

## Demo

![Waypoint Navigator Demo](media/waypoint_navigator_1.gif)

---

## How It Works

The node subscribes to `/turtle1/pose` to get the turtle's live position and heading. On every pose update it:

1. Computes the straight-line distance to the current target waypoint
2. Computes the heading error (angle difference between where the turtle faces and where the waypoint is)
3. Publishes a `Twist` command on `/turtle1/cmd_vel` with speed proportional to distance and turn rate proportional to heading error
4. Advances to the next waypoint once the turtle is within `goal_tolerance` of the target

This is a classic **proportional controller** — no PID, no path planning library, just clean geometry and ROS2 pub/sub.

---

## Requirements

- ROS2 Jazzy (or compatible distro)
- Python 3.10+
- `turtlesim` package

Install turtlesim if you don't have it:

```bash
sudo apt install ros-jazzy-turtlesim
```

---

## Installation

```bash
# 1. Navigate to your ROS2 workspace src folder
cd ~/ros2_ws/src

# 2. Clone the repository
git clone https://github.com/YOUR_USERNAME/turtlesim-waypoint-navigator.git

# 3. Go back to workspace root and build
cd ~/ros2_ws
colcon build --packages-select turtlesim_waypoint_navigator

# 4. Source the workspace
source install/setup.bash
```

---

## Running the Node

You need two terminals.

**Terminal 1 — start turtlesim:**

```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — run the waypoint navigator:**

```bash
ros2 run turtlesim_waypoint_navigator waypoint_navigator
```

You should see log messages like:

```
[INFO] Waypoint Navigator Node has been started.
[INFO] Reached waypoint 0: (5.5, 9.0)
[INFO] Reached waypoint 1: (2.3, 3.5)
...
[INFO] All waypoints reached!
```

---

## Customising Waypoints

Open `turtlesim_waypoint_navigator/waypoint_navigator.py` and edit the `self.waypoints` list in `__init__`:

```python
self.waypoints = [
    (5.5, 9.0),   # top point
    (2.3, 3.5),   # bottom-left point
    (8.7, 7.2),   # middle-right point
    (2.3, 7.2),   # middle-left point
    (8.7, 3.5),   # bottom-right point
    (5.5, 9.0),   # close the star
]
```

Turtlesim's coordinate space runs from `0.0` to `11.0` on both axes, with `(5.5, 5.5)` as the centre. Keep all waypoints within this range.

You can also tune the controller behaviour:

| Parameter | Default | Effect |
|---|---|---|
| `goal_tolerance` | `0.15` | How close (metres) to count a waypoint as reached |
| `linear_gain` | `1.5` | How fast the turtle drives (higher = faster) |
| `angular_gain` | `6.0` | How sharply the turtle turns (higher = snappier) |

---

## Project Structure

```
turtlesim_waypoint_navigator/
├── turtlesim_waypoint_navigator/
│   ├── __init__.py
│   └── waypoint_navigator.py   # main node
├── resource/
│   └── turtlesim_waypoint_navigator
├── package.xml
├── setup.py
├── setup.cfg
└── README.md
```

---

## Key Concepts

**Proportional control** — the speed and turn rate are both proportional to the error (distance and heading error respectively). This means the turtle naturally slows down as it approaches a waypoint and straightens out as it lines up with the target.

**Heading error normalisation** — raw angle subtraction can give values outside `[-π, π]`, causing the turtle to spin the long way around. The node normalises using `math.atan2(sin(e), cos(e))` to always take the shortest arc.

**Pose callback loop** — `pose_callback` is called ~62 times per second by ROS2. Each call is one iteration of the control loop: read position → compute error → publish correction.

---

## License

MIT License. Feel free to use, modify, and share.