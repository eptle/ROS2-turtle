# ROS2-turtle

## Запуск

1. Клонировать репозиторий в ```/home/{username}/ros2_ws/src```
2. Переименовать папку с репозиторием в ```my_turtle_pkg```
3. Собрать пакет:
```
cd ~/ros2_ws
colcon build --packages-select my_turtle_pkg
source install/setup.bash
```
4. Запустить:
```
# терминал 1
ros2 run turtlesim turtlesim_node

# терминал 2
ros2 run my_turtle_pkg turtle_controller
```