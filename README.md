# README



这是一个智能车的虚拟环境，方便大家进行雷达和ROS的练习



## 环境搭建



### 【1】仿真功能包创建，⾸先创建⼀个⼯作空间⽂件夹

```
sudo mkdir gazebo_test_ws
```

### 【2】将src文件放在 gazebo_test_ws 文件夹下

```
cd gazebo_test_ws
catkin_make
source devel/setup.bash
```



## 部分功能



### 【1】启动地图环境

```
roslaunch gazebo_pkg race.launch
```



### 【2】建图功能启动

```
roslaunch gazebo_pkg race.launch
roslaunch gazebo_map gmapping.launch
```



### 【3】导航功能测试

```
roslaunch gazebo_pkg race.launch
roslaunch gazebo_nav gazebo_nav.launch
```

