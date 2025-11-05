#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import sys
import os
import time
import rospy
import random #随机
from gazebo_msgs.srv import SpawnModel, DeleteModel
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose, Point, Quaternion
 
def load_model(model_path):
    with open(model_path, 'r') as model_file:
        model_xml = model_file.read()
    return model_xml
 
def spawn_model(model_name, model_xml, pose, reference_frame="world"):
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        spawn_model_prox(model_name, model_xml, "", pose, reference_frame)
        rospy.loginfo("Model {} spawned successfully".format(model_name))
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: {}".format(e))
 
def delete_model(model_name):
    rospy.wait_for_service('/gazebo/delete_model')
    try:
        delete_model_prox = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        delete_model_prox(model_name)
        rospy.loginfo("Model {} deleted successfully".format(model_name))
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: {}".format(e))
 
if __name__ == "__main__":
    rospy.init_node('spawn_random_models_node')
    fruit_board_folders = ["fruit1_board", "fruit2_board", "fruit3_board"]
    vege_board_folders = ["vage1_board", "vage2_board", "vage3_board"]
    dessert_board_folders = ["dessert1_board", "dessert2_board", "dessert3_board"]
    # 模型名称和路径配置
    model_configs = [
        {"name_prefix": "fruit_board_", "path": f"/home/wy/.gazebo/models/{random.choice(fruit_board_folders)}/model.sdf"},
        {"name_prefix": "vage_board_", "path": f"/home/wy/.gazebo/models/{random.choice(vege_board_folders)}/model.sdf"},
        {"name_prefix": "dessert_board_", "path": f"/home/wy/.gazebo/models/{random.choice(dessert_board_folders)}/model.sdf"}
    ]

    # 加载所有模型
    models = [
        {"name_prefix": config["name_prefix"], "model_xml": load_model(config["path"])}
        for config in model_configs
    ]

    # 房间范围和生成规则配置
    rooms = [
        {"name": "A", "x_range": (0, 0.95), "y_range": (1.4, 3.4)},
        {"name": "B", "x_range": (1.5, 2.5), "y_range": (1.4, 3.4)},
        {"name": "C", "x_range": (3.5, 4.3), "y_range": (1.4, 3.4)},
    ]

    # 确保模型类型不会重复
    available_models = models.copy()

    for room in rooms:
        # 随机选择未使用的模型
        selected_model = random.choice(available_models)
        available_models.remove(selected_model)  # 移除已使用的模型

        # 随机生成模型位置
        pose = Pose()
        pose.position = Point(
            x=random.uniform(*room["x_range"]),
            y=random.uniform(*room["y_range"]),
            z=0
        )
        pose.orientation = Quaternion(x=0, y=0, z=0, w=1)

        # 生成模型
        model_name = f"{selected_model['name_prefix']}{room['name']}"
        spawn_model(model_name, selected_model["model_xml"], pose)
