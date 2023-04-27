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
from flexbe_states.log_state import LogState
from flexbe_states.log_key_state import LogKeyState
from flexible_manipulation_flexbe_states.get_joint_names_from_move_group_state import GetJointNamesFromMoveGroupState
from flexbe_states.user_data_state import UserDataState
from flexible_manipulation_flexbe_states.get_current_joint_values_user_state import GetCurrentJointValuesUserState
from flexible_manipulation_flexbe_states.get_current_joint_values_list_state import GetCurrentJointValuesListState
from flexible_manipulation_flexbe_states.get_joint_values_from_srdf_config_state import GetJointValuesFromSrdfConfigState
from flexible_manipulation_flexbe_states.joint_values_to_trajectory_state import JointValuesToTrajectoryState
from flexible_manipulation_flexbe_states.trajectory_to_follow_joint_trajectory_action_state import TrajectoryToFollowJointTrajectoryActionState
from flexible_manipulation_flexbe_states.set_joint_trajectory_tolerances_state import SetJointTrajectoryTolerancesState
from flexible_manipulation_flexbe_states.joint_values_to_move_action_state import JointValuesToMoveActionState
from flexible_manipulation_flexbe_states.move_group_state import MoveGroupState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 2 2018
@author: David Conner
'''
class test_flexible_manipulation3SM(Behavior):
    '''
    testing behavior
    '''


    def __init__(self):
        super(test_flexible_manipulation3SM, self).__init__()
        self.name = 'test_flexible_manipulation3'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1490 y:191, x:764 y:433
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.action_topic = "/move_group"
        _state_machine.userdata.trajectory_action_topic = "/m1n6s200/effort_joint_trajectory_controller/follow_joint_trajectory"
        _state_machine.userdata.config_vertical = "Vertical"
        _state_machine.userdata.config_home = "Home"
        _state_machine.userdata.config_retract = "Retract"
        _state_machine.userdata.components = None

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]


        with _state_machine:
            # x:30 y:40
            OperatableStateMachine.add('MoveIt',
                                        SetupProxyMoveItClientState(robot_description="/robot_description", robot_description_semantic=None, move_group_capabilities=[["/move_group", ["arm", "gripper"]]], action_type_and_topics=None, enter_wait_duration=0.0),
                                        transitions={'connected': 'Connected', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'connected': Autonomy.High, 'topics_unavailable': Autonomy.Full, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'move_groups': 'move_groups'})

            # x:52 y:151
            OperatableStateMachine.add('Connected',
                                        LogState(text="Connected", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'SetMG'},
                                        autonomy={'done': Autonomy.Off})

            # x:690 y:610
            OperatableStateMachine.add('DumpJVUser',
                                        LogKeyState(text="Joint Values {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'GetJVList'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'user_joint_values'})

            # x:243 y:287
            OperatableStateMachine.add('GetNames',
                                        GetJointNamesFromMoveGroupState(),
                                        transitions={'retrieved': 'UserNames', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Off, 'param_error': Autonomy.Off},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'selected_move_group', 'move_group': 'move_group', 'joint_names': 'user_joint_names'})

            # x:51 y:257
            OperatableStateMachine.add('SetMG',
                                        UserDataState(data="arm"),
                                        transitions={'done': 'GetNames'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'selected_move_group'})

            # x:438 y:420
            OperatableStateMachine.add('GetJVUser',
                                        GetCurrentJointValuesUserState(timeout=5.0, joint_states_topic='/m1n6s200_driver/joint_states'),
                                        transitions={'retrieved': 'DumpJVUser', 'timeout': 'failed'},
                                        autonomy={'retrieved': Autonomy.Off, 'timeout': Autonomy.High},
                                        remapping={'joint_names': 'no_ee_names', 'joint_values': 'user_joint_values'})

            # x:853 y:612
            OperatableStateMachine.add('GetJVList',
                                        GetCurrentJointValuesListState(joint_names=['m1n6s200_joint_1', 'm1n6s200_joint_2', 'm1n6s200_joint_3', 'm1n6s200_joint_4'], timeout=None, joint_states_topic='/m1n6s200_driver/joint_states'),
                                        transitions={'retrieved': 'ListNames', 'timeout': 'failed'},
                                        autonomy={'retrieved': Autonomy.Off, 'timeout': Autonomy.High},
                                        remapping={'joint_names': 'list_joint_names', 'joint_values': 'list_joint_values'})

            # x:572 y:156
            OperatableStateMachine.add('ListNames',
                                        LogKeyState(text='List Names {}', severity=Logger.REPORT_HINT),
                                        transitions={'done': 'ListValues'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'list_joint_names'})

            # x:647 y:42
            OperatableStateMachine.add('ListValues',
                                        LogKeyState(text='List Values {}', severity=Logger.REPORT_HINT),
                                        transitions={'done': 'SetConfigName'},
                                        autonomy={'done': Autonomy.Full},
                                        remapping={'data': 'list_joint_values'})

            # x:188 y:388
            OperatableStateMachine.add('UserNames',
                                        LogKeyState(text='User names {}', severity=Logger.REPORT_HINT),
                                        transitions={'done': 'JustArmJoints'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'user_joint_names'})

            # x:222 y:484
            OperatableStateMachine.add('JustArmJoints',
                                        UserDataState(data=['m1n6s200_joint_1', 'm1n6s200_joint_2', 'm1n6s200_joint_3', 'm1n6s200_joint_4', 'm1n6s200_joint_5', 'm1n6s200_joint_6']),
                                        transitions={'done': 'GetJVUser'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'no_ee_names'})

            # x:1000 y:34
            OperatableStateMachine.add('GetRetract',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'JVTrajectory', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Off, 'param_error': Autonomy.Off},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group', 'config_name': 'config_name', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:802 y:44
            OperatableStateMachine.add('SetConfigName',
                                        UserDataState(data="Retract"),
                                        transitions={'done': 'GetRetract'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'config_name'})

            # x:1035 y:139
            OperatableStateMachine.add('JVTrajectory',
                                        JointValuesToTrajectoryState(duration=10.0),
                                        transitions={'done': 'SetGoal', 'param_error': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'joint_names': 'joint_names', 'joint_values': 'joint_values', 'joint_trajectory': 'joint_trajectory'})

            # x:1131 y:464
            OperatableStateMachine.add('FJTA',
                                        TrajectoryToFollowJointTrajectoryActionState(goal_time_tolerance=3.0, max_delay=-1.0, wait_duration=2.0, timeout=1.0, action_topic=None),
                                        transitions={'reached': 'JV2MoveAction', 'goal_failed': 'GoalTolFailure', 'path_failed': 'PathTolFailed', 'invalid_request': 'failed', 'param_error': 'failed', 'failed': 'failed'},
                                        autonomy={'reached': Autonomy.Full, 'goal_failed': Autonomy.Off, 'path_failed': Autonomy.Off, 'invalid_request': Autonomy.Full, 'param_error': Autonomy.Full, 'failed': Autonomy.Full},
                                        remapping={'trajectory_action_topic': 'trajectory_action_topic', 'joint_trajectory': 'joint_trajectory', 'joint_goal_tolerances': 'joint_goal_tolerances', 'joint_path_tolerances': 'joint_path_tolerances', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})

            # x:1051 y:230
            OperatableStateMachine.add('SetGoal',
                                        SetJointTrajectoryTolerancesState(position_constraints=[0.02], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
                                        transitions={'configured': 'SetPath', 'param_error': 'failed'},
                                        autonomy={'configured': Autonomy.Off, 'param_error': Autonomy.Off},
                                        remapping={'joint_names': 'joint_names', 'joint_tolerances': 'joint_goal_tolerances'})

            # x:1062 y:349
            OperatableStateMachine.add('SetPath',
                                        SetJointTrajectoryTolerancesState(position_constraints=[0.0], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
                                        transitions={'configured': 'FJTA', 'param_error': 'failed'},
                                        autonomy={'configured': Autonomy.Off, 'param_error': Autonomy.Off},
                                        remapping={'joint_names': 'joint_names', 'joint_tolerances': 'joint_path_tolerances'})

            # x:1386 y:539
            OperatableStateMachine.add('JV2MoveAction',
                                        JointValuesToMoveActionState(joint_names=['m1n6s200_joint_1', 'm1n6s200_joint_2'], joint_values=[0.0, 1.57], move_group='arm', action_topic='/move_group', joint_tolerance=0.02, constraint_weight=1.0, allowed_planning_time=4.0, wait_duration=0.2, timeout=30.0),
                                        transitions={'reached': 'SetConfigName_2', 'param_error': 'failed', 'planning_failed': 'failed', 'control_failed': 'CtrlFailed', 'failed': 'failed'},
                                        autonomy={'reached': Autonomy.Full, 'param_error': Autonomy.Full, 'planning_failed': Autonomy.Full, 'control_failed': Autonomy.Full, 'failed': Autonomy.Off},
                                        remapping={'move_group': 'move_group', 'action_topic': 'action_topic', 'status_text': 'status_text', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:1324 y:272
            OperatableStateMachine.add('CtrlFailed',
                                        LogState(text="Control failed", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Full})

            # x:1648 y:554
            OperatableStateMachine.add('GetHome',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'SayJointNames', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group', 'config_name': 'config_name', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:1489 y:749
            OperatableStateMachine.add('SetConfigName_2',
                                        UserDataState(data="Home"),
                                        transitions={'done': 'ConfigNamePrint'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'config_name'})

            # x:1644 y:267
            OperatableStateMachine.add('MoveGroup',
                                        MoveGroupState(timeout=30.0, wait_duration=0.02, move_group=None),
                                        transitions={'reached': 'finished', 'control_failed': 'CtrlFailed', 'planning_failed': 'failed', 'param_error': 'failed', 'failed': 'failed'},
                                        autonomy={'reached': Autonomy.Full, 'control_failed': Autonomy.Full, 'planning_failed': Autonomy.High, 'param_error': Autonomy.Full, 'failed': Autonomy.Full},
                                        remapping={'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values', 'status_text': 'status_text', 'planned_trajectory': 'planned_trajectory', 'executed_trajectory': 'executed_trajectory'})

            # x:1689 y:666
            OperatableStateMachine.add('ConfigNamePrint',
                                        LogKeyState(text="Config {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'GetHome'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'config_name'})

            # x:1701 y:450
            OperatableStateMachine.add('SayJointNames',
                                        LogKeyState(text="Joint names {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'SayJointValues'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_names'})

            # x:1550 y:367
            OperatableStateMachine.add('SayJointValues',
                                        LogKeyState(text="Values {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'MoveGroup'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_values'})

            # x:1113 y:682
            OperatableStateMachine.add('PathTolFailed',
                                        LogState(text="Path tolerance failure", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'JV2MoveAction'},
                                        autonomy={'done': Autonomy.High})

            # x:1240 y:661
            OperatableStateMachine.add('GoalTolFailure',
                                        LogState(text="Goal tolerance failure", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'JV2MoveAction'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
