---
sidebar_position: 3
---

# 3. Sensor Simulation for Humanoid Robots

Accurate sensor simulation is vital for developing and testing perception pipelines for humanoid robots in a digital twin environment. This chapter covers the simulation of common robotic sensors: LiDAR, depth cameras, and Inertial Measurement Units (IMUs).

## 3.1 Simulating LiDAR

LiDAR (Light Detection and Ranging) sensors measure distances by emitting laser pulses and calculating the time it takes for them to return. Simulating LiDAR involves generating point clouds that accurately represent the virtual environment's geometry.

### Gazebo LiDAR Simulation

Gazebo includes a ray sensor plugin that can be configured to simulate LiDAR.

**Example: LiDAR Plugin in URDF/XACRO**

```xml
<gazebo reference="hokuyo_link">
  <sensor type="ray" name="head_hokuyo_sensor">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>40</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-1.570796</min_angle>
          <max_angle>1.570796</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.10</min>
        <max>10.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="gazebo_ros_head_hokuyo_controller" filename="libgazebo_ros_laser.so">
      <topicName>/scan</topicName>
      <frameName>hokuyo_link</frameName>
    </plugin>
  </sensor>
</gazebo>
```

This configuration generates a `/scan` ROS topic, which can be consumed by perception nodes.

## 3.2 Simulating Depth Cameras

Depth cameras provide both color (RGB) and depth information, crucial for 3D reconstruction and object detection.

### Gazebo Depth Camera Simulation

Gazebo's camera sensor can be configured to output depth images.

**Example: Depth Camera Plugin in URDF/XACRO**

```xml
<gazebo reference="camera_link">
  <sensor type="depth" name="camera">
    <alwaysOn>true</alwaysOn>
    <update_rate>30.0</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.05</near>
        <far>3.0</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_depth_camera.so">
      <alwaysOn>true</alwaysOn>
      <updateRate>30.0</updateRate>
      <cameraName>camera</cameraName>
      <imageTopicName>image_raw</imageTopicName>
      <cameraInfoTopicName>camera_info</cameraInfoTopicName>
      <depthImageTopicName>depth/image_raw</depthImageTopicName>
      <depthImageInfoTopicName>depth/camera_info</depthImageInfoTopicName>
      <pointCloudTopicName>depth/points</pointCloudTopicName>
      <frameName>camera_link</frameName>
      <hackBaseline>0.07</hackBaseline>
      <distortionK1>0.0</distortionK1>
      <distortionK2>0.0</distortionK2>
      <distortionK3>0.0</distortionK3>
      <distortionT1>0.0</distortionT1>
      <distortionT2>0.0</distortionT2>
    </plugin>
  </sensor>
</gazebo>
```

This plugin will publish images and depth data on specified ROS topics.

## 3.3 Simulating IMUs

An IMU (Inertial Measurement Unit) measures angular velocity, linear acceleration, and orientation.

### Gazebo IMU Simulation

Gazebo provides an IMU sensor plugin to simulate these measurements.

**Example: IMU Plugin in URDF/XACRO**

```xml
<gazebo reference="imu_link">
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <visualize>true</visualize>
    <plugin filename="libgazebo_ros_imu_sensor.so" name="imu_plugin">
      <topicName>/imu</topicName>
      <bodyName>imu_link</bodyName>
      <updateRate>100</updateRate>
      <gaussianNoise>0.005</gaussianNoise>
      <xyzOffset>0 0 0</xyzOffset>
      <rpyOffset>0 0 0</rpyOffset>
      <frameName>imu_link</frameName>
    </plugin>
  </sensor>
</gazebo>
```

This IMU will publish data to the `/imu` ROS topic.

By simulating these sensors, you can develop and test complex perception algorithms in a controlled virtual environment before deploying them on a real humanoid robot.
