#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexible_manipulation_flexbe_states.setup_proxy_moveit_client_state import SetupProxyMoveItClientState
from flexbe_states.log_key_state import LogKeyState
from flexible_manipulation_flexbe_states.user_data_to_move_action_state import UserDataToMoveActionState
from flexible_manipulation_flexbe_states.joint_values_to_move_action_state import JointValuesToMoveActionState
from flexible_manipulation_flexbe_states.get_joint_values_from_srdf_config_state import GetJointValuesFromSrdfConfigState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jan 29 2018
@author: David Conner
'''
class move_demoSM(Behavior):
    '''
    Simple demonstration of Flexible Manipulation
    '''


    def __init__(self):
        super(move_demoSM, self).__init__()
        self.name = 'move_demo'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1066 y:202, x:512 y:391
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.action_topic = "/move_group"
        _state_machine.userdata.move_group_arm = "arm"
        _state_machine.userdata.config_name = "Home"

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]


        with _state_machine:
            # x:41 y:57
            OperatableStateMachine.add('SetupMoveItProxy',
                                        SetupProxyMoveItClientState(robot_description="/robot_description", robot_description_semantic=None, move_group_capabilities="/move_group", action_type_and_topics=None, enter_wait_duration=0.5),
                                        transitions={'connected': 'GetHome', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'connected': Autonomy.Off, 'topics_unavailable': Autonomy.High, 'param_error': Autonomy.High},
                                        remapping={'robot_name': 'robot_name', 'move_groups': 'move_groups'})

            # x:469 y:185
            OperatableStateMachine.add('PrintConfig',
                                        LogKeyState(text=" Config {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'MoveHome'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_names'})

            # x:698 y:110
            OperatableStateMachine.add('MoveHome',
                                        UserDataToMoveActionState(joint_tolerance=0.05, constraint_weight=1.0, allowed_planning_time=2.0, wait_duration=2.0, timeout=30.0, action_topic=None),
                                        transitions={'reached': 'MoveVertical', 'param_error': 'failed', 'planning_failed': 'failed', 'control_failed': 'failed', 'failed': 'failed'},
                                        autonomy={'reached': Autonomy.Full, 'param_error': Autonomy.Full, 'planning_failed': Autonomy.Full, 'control_failed': Autonomy.Full, 'failed': Autonomy.Off},
                                        remapping={'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_names': 'joint_names', 'joint_values': 'joint_values', 'status_text': 'status_text'})

            # x:453 y:563
            OperatableStateMachine.add('MoveVertical',
                                        JointValuesToMoveActionState(joint_names=['m1n6s200_joint_1', 'm1n6s200_joint_2', 'm1n6s200_joint_3', 'm1n6s200_joint_4', 'm1n6s200_joint_5', 'm1n6s200_joint_6'], joint_values=[0.0,3.14,3.14,0.0,0.0,0.0], move_group="arm", action_topic="/move_group", joint_tolerance=0.05, constraint_weight=1.0, allowed_planning_time=2.0, wait_duration=2.0, timeout=10.0),
                                        transitions={'reached': 'GetHome', 'param_error': 'failed', 'planning_failed': 'failed', 'control_failed': 'failed', 'failed': 'failed'},
                                        autonomy={'reached': Autonomy.Low, 'param_error': Autonomy.High, 'planning_failed': Autonomy.High, 'control_failed': Autonomy.High, 'failed': Autonomy.High},
                                        remapping={'move_group': 'move_group', 'action_topic': 'action_topic', 'status_text': 'status_text', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:87 y:259
            OperatableStateMachine.add('GetHome',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'PrintConfig', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.High, 'param_error': Autonomy.High},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group_arm', 'config_name': 'config_name', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
