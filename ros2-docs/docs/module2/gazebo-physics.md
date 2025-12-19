---
sidebar_position: 1
---

# 1. Physics Simulation with Gazebo

This chapter focuses on setting up and performing physics simulations of humanoid robots using Gazebo. Gazebo is a powerful 3D robotics simulator that allows for accurate simulation of robots in complex indoor and outdoor environments. We will cover how to define robot models, simulate various physical phenomena, and interact with the simulation environment.

## 1.1 Defining Robot Models

Robot models in Gazebo are typically defined using URDF (Unified Robot Description Format) or SDFormat (Simulation Description Format). These formats allow you to specify the robot's links (rigid bodies), joints (connections between links), sensors, and visual and collision properties.

**Example: Simple Link in URDF**

```xml
<?xml version="1.0"?>
<robot name="simple_link">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="1 1 1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="1 1 1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>
</robot>
```

## 1.2 Simulating Gravity

Gazebo's physics engine automatically applies gravity to all simulated bodies. You can configure the gravity vector in your world file.

**Example: World File with Gravity**

```xml
<?xml version="1.0"?>
<sdf version="1.6">
  <world name="default">
    <gravity>0 0 -9.8</gravity>
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    <model name="my_robot">
      <pose>0 0 0.5 0 0 0</pose>
      <include>
        <uri>model://simple_link</uri> <!-- Replace with your humanoid robot model -->
      </include>
    </model>
  </world>
</sdf>
```

## 1.3 Collisions and Contact Physics

Gazebo accurately simulates collisions between robot parts and the environment. Collision properties such as friction and restitution (bounciness) can be defined for each link.

### Friction

Friction coefficients (mu1, mu2) determine how surfaces resist relative motion.

```xml
<collision>
  <surface>
    <friction>
      <ode>
        <mu>1.0</mu>
        <mu2>1.0</mu2>
      </ode>
    </friction>
  </surface>
  <geometry>
    <box size="0.1 0.1 0.1"/>
  </geometry>
</collision>
```

### Restitution

Restitution (e) dictates the "bounciness" of a collision, ranging from 0 (perfectly inelastic) to 1 (perfectly elastic).

```xml
<collision>
  <surface>
    <bounce>
      <restitution_coefficient>0.5</restitution_coefficient>
      <threshold>1e-5</threshold>
    </bounce>
  </surface>
  <geometry>
    <sphere radius="0.05"/>
  </geometry>
</collision>
```

## 1.4 Realistic Robot-Environment Interaction

To achieve realistic interaction, ensure your robot model has appropriate inertia values, joint limits, and controller configurations. ROS 2 provides robust tools for interfacing with Gazebo, allowing you to send commands to joints and receive sensor feedback.

This chapter provides the foundation for building physics-accurate digital twins of humanoid robots in Gazebo.
