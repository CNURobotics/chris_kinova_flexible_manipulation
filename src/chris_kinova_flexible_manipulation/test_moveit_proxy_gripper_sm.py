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
from flexible_manipulation_flexbe_states.get_joint_values_from_srdf_config_state import GetJointValuesFromSrdfConfigState
from flexible_manipulation_flexbe_states.joint_values_to_moveit_plan_state import JointValuesToMoveItPlanState
from flexible_manipulation_flexbe_states.trajectory_to_follow_joint_trajectory_action_state import TrajectoryToFollowJointTrajectoryActionState
from flexible_manipulation_flexbe_states.set_joint_trajectory_tolerances_state import SetJointTrajectoryTolerancesState
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.operator_decision_state import OperatorDecisionState
from flexbe_states.decision_state import DecisionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Feb 06 2018
@author: David Conner
'''
class test_moveit_proxy_gripperSM(Behavior):
    '''
    testing behavior that uses different move groups for controling the arm and gripper
    '''


    def __init__(self):
        super(test_moveit_proxy_gripperSM, self).__init__()
        self.name = 'test_moveit_proxy_gripper'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:273 y:335, x:947 y:170
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.action_topic = "/move_group"
        _state_machine.userdata.trajectory_action_topic = "/m1n6s200/effort_joint_trajectory_controller/follow_joint_trajectory"
        _state_machine.userdata.gripper_action_topic = "/m1n6s200/effort_finger_trajectory_controller/follow_joint_trajectory"
        _state_machine.userdata.move_group_arm = "arm"
        _state_machine.userdata.move_group_gripper = "gripper"
        _state_machine.userdata.config_name_vertical = "Vertical"
        _state_machine.userdata.config_name_home = "Home"
        _state_machine.userdata.config_name_retract = "Retract"
        _state_machine.userdata.config_name_open = "Open"
        _state_machine.userdata.config_name_close = "Close"

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]


        with _state_machine:
            # x:30 y:40
            OperatableStateMachine.add('MoveIt',
                                        SetupProxyMoveItClientState(robot_description="/robot_description", robot_description_semantic=None, move_group_capabilities="/move_group", action_type_and_topics=[["MoveGroupAction",["/move_group"]]], enter_wait_duration=2.0),
                                        transitions={'connected': 'Connected', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'connected': Autonomy.High, 'topics_unavailable': Autonomy.Full, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'move_groups': 'move_groups'})

            # x:132 y:177
            OperatableStateMachine.add('Connected',
                                        LogState(text="Connected", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Decision'},
                                        autonomy={'done': Autonomy.Off})

            # x:303 y:531
            OperatableStateMachine.add('Vertical',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'GoalTolerances', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Low, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group_arm', 'config_name': 'config_name_vertical', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:823 y:29
            OperatableStateMachine.add('Plan',
                                        JointValuesToMoveItPlanState(timeout=5.0, enter_wait_duration=0.5, action_topic=None),
                                        transitions={'planned': 'SwitchController', 'failed': 'failed', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'planned': Autonomy.Low, 'failed': Autonomy.Full, 'topics_unavailable': Autonomy.Full, 'param_error': Autonomy.Full},
                                        remapping={'action_topic': 'action_topic', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values', 'joint_trajectory': 'joint_trajectory'})

            # x:1611 y:323
            OperatableStateMachine.add('Execute',
                                        TrajectoryToFollowJointTrajectoryActionState(goal_time_tolerance=3.0, max_delay=-1.0, wait_duration=2.0, timeout=1.0, action_topic=None),
                                        transitions={'reached': 'Decision', 'goal_failed': 'LogFail', 'path_failed': 'LogFail', 'invalid_request': 'InvalidRequestError', 'param_error': 'failed', 'failed': 'LogFail'},
                                        autonomy={'reached': Autonomy.Full, 'goal_failed': Autonomy.Off, 'path_failed': Autonomy.Off, 'invalid_request': Autonomy.Off, 'param_error': Autonomy.Full, 'failed': Autonomy.Off},
                                        remapping={'trajectory_action_topic': 'trajectory_action_topic', 'joint_trajectory': 'joint_trajectory', 'joint_goal_tolerances': 'joint_goal_tolerances', 'joint_path_tolerances': 'joint_path_tolerances', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})

            # x:469 y:348
            OperatableStateMachine.add('GoalTolerances',
                                        SetJointTrajectoryTolerancesState(position_constraints=[0.05], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
                                        transitions={'configured': 'PathTolerances', 'param_error': 'failed'},
                                        autonomy={'configured': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'joint_names': 'joint_names', 'joint_tolerances': 'joint_goal_tolerances'})

            # x:372 y:200
            OperatableStateMachine.add('PathTolerances',
                                        SetJointTrajectoryTolerancesState(position_constraints=[0.08], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
                                        transitions={'configured': 'DumpGoalTolerance', 'param_error': 'failed'},
                                        autonomy={'configured': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'joint_names': 'joint_names', 'joint_tolerances': 'joint_path_tolerances'})

            # x:348 y:16
            OperatableStateMachine.add('DumpGoalTolerance',
                                        LogKeyState(text="Goal tolerance {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'DumpPathTolerance'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_goal_tolerances'})

            # x:530 y:21
            OperatableStateMachine.add('DumpPathTolerance',
                                        LogKeyState(text="Path tolerance {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'LogActiveMoveGroup'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_path_tolerances'})

            # x:912 y:495
            OperatableStateMachine.add('Home',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'GoalTolerances', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Low, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group_arm', 'config_name': 'config_name_home', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:187 y:726
            OperatableStateMachine.add('Decision',
                                        OperatorDecisionState(outcomes=["home","vertical", "stop","close","open"], hint=None, suggestion=None),
                                        transitions={'home': 'Home', 'vertical': 'Vertical', 'stop': 'finished', 'close': 'Close', 'open': 'Open'},
                                        autonomy={'home': Autonomy.Low, 'vertical': Autonomy.Low, 'stop': Autonomy.Full, 'close': Autonomy.Low, 'open': Autonomy.Low})

            # x:748 y:676
            OperatableStateMachine.add('Close',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'GoalTolerances', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Low, 'param_error': Autonomy.High},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group_gripper', 'config_name': 'config_name_close', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:1083 y:49
            OperatableStateMachine.add('SwitchController',
                                        DecisionState(outcomes=["arm","gripper"], conditions=lambda mg : "gripper" if mg == "gripper" else "arm"),
                                        transitions={'arm': 'Execute', 'gripper': 'Gripper'},
                                        autonomy={'arm': Autonomy.Low, 'gripper': Autonomy.Low},
                                        remapping={'input_value': 'move_group'})

            # x:1244 y:428
            OperatableStateMachine.add('Gripper',
                                        TrajectoryToFollowJointTrajectoryActionState(goal_time_tolerance=3.0, max_delay=-1.0, wait_duration=2.0, timeout=1.0, action_topic=None),
                                        transitions={'reached': 'Decision', 'goal_failed': 'LogFail', 'path_failed': 'LogFail', 'invalid_request': 'InvalidRequestError', 'param_error': 'failed', 'failed': 'LogFail'},
                                        autonomy={'reached': Autonomy.Off, 'goal_failed': Autonomy.Off, 'path_failed': Autonomy.Off, 'invalid_request': Autonomy.Off, 'param_error': Autonomy.High, 'failed': Autonomy.Off},
                                        remapping={'trajectory_action_topic': 'gripper_action_topic', 'joint_trajectory': 'joint_trajectory', 'joint_goal_tolerances': 'joint_goal_tolerances', 'joint_path_tolerances': 'joint_path_tolerances', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})

            # x:612 y:757
            OperatableStateMachine.add('Open',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'GoalTolerances', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Low, 'param_error': Autonomy.High},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group_gripper', 'config_name': 'config_name_open', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:745 y:1002
            OperatableStateMachine.add('InvalidRequestError',
                                        LogState(text="Invalid request", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Decision'},
                                        autonomy={'done': Autonomy.Off})

            # x:1315 y:971
            OperatableStateMachine.add('LogFail',
                                        LogKeyState(text="Failed {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Decision'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'status_text'})

            # x:716 y:88
            OperatableStateMachine.add('LogActiveMoveGroup',
                                        LogKeyState(text="Active Move Group is {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Plan'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'move_group'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
