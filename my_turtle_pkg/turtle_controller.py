import os
from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        pkg_dir = get_package_share_directory('my_turtle_pkg')
        traj_path = os.path.join(pkg_dir, 'trajectory.txt')
        self.commands = self.load_trajectory(traj_path)

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.send_next_command)
        self.command_index = 0

    def load_trajectory(self, file_path):
        commands = []
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue
                cmd, value = parts[0].upper(), float(parts[1])
                commands.append((cmd, value))
        return commands

    def send_next_command(self):
        if self.command_index >= len(self.commands):
            self.get_logger().info('Траектория завершена')
            self.timer.cancel()
            return

        cmd, value = self.commands[self.command_index]
        twist = Twist()

        if cmd == 'FORW':
            twist.linear.x = value
        elif cmd == 'BACK':
            twist.linear.x = -value
        elif cmd == 'ROT':
            twist.angular.z = -value
        else:
            self.get_logger().warn(f'Неизвестная команда: {cmd}')

        self.publisher_.publish(twist)
        self.get_logger().info(f'Выполняется команда: {cmd} {value}')
        self.command_index += 1

def main():
    rclpy.init()
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
