# Chapter 2: Core ROS 2 Primitives

This chapter dives into the fundamental building blocks of any ROS 2 application: Nodes, Topics, and Services. Understanding these primitives is crucial for designing and implementing robust robot behaviors.

## Nodes: The Workers

- **Definition**: A Node is an executable process that performs computations. It's the smallest unit of computation in ROS 2.
- **Purpose**: Each node should be responsible for a single, modular purpose (e.g., a node for reading sensor data, a node for controlling a motor).
- **Example**: `camera_publisher_node`, `motor_controller_node`, `navigation_node`.

## Topics: The Communication Buses

- **Definition**: Topics are named buses over which nodes exchange messages. It's a publish/subscribe communication model.
- **Purpose**: Used for streaming data that changes over time, like sensor readings, joint states, or camera images.
- **Mechanism**: A node *publishes* messages to a topic, and other nodes *subscribe* to that topic to receive the messages.
- **Example**: `/odom` (odometry data), `/camera/image` (camera images), `/cmd_vel` (velocity commands).

## Services: The Request-Response Calls

- **Definition**: Services are a request/reply communication model in ROS 2.
- **Purpose**: Used for request/response interactions, typically for actions that are not continuous or that require a specific outcome (e.g., triggering a robot to perform a task, querying a database).
- **Mechanism**: A node acts as a *service server* (providing a service), and another node acts as a *service client* (requesting the service).
- **Example**: `/move_robot_to_goal`, `/get_map_data`, `/set_gripper_state`.

## Summary and Interconnections

We will illustrate how Nodes, Topics, and Services work together to form complex robot systems, emphasizing the decentralized and modular nature of ROS 2.
