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
from flexible_manipulation_flexbe_states.clear_octomap_state import ClearOctomapState
from flexible_manipulation_flexbe_states.query_planners_state import QueryPlannersState
from flexible_manipulation_flexbe_states.get_planning_scene_state import GetPlanningSceneState
from flexible_manipulation_flexbe_states.apply_planning_scene_state import ApplyPlanningSceneState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 2 2018
@author: David Conner
'''
class test_flexible_manipulationSM(Behavior):
    '''
    testing behavior
    '''


    def __init__(self):
        super(test_flexible_manipulationSM, self).__init__()
        self.name = 'test_flexible_manipulation'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # ! 1394 491 
        # Applying planning scene breaks planning due to invalid state



    def create(self):
        # x:1500 y:655, x:784 y:398
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.action_topic = "/move_group"
        _state_machine.userdata.trajectory_action_topic = "/m1n6s200/effort_joint_trajectory_controller/follow_joint_trajectory"
        _state_machine.userdata.move_group_arm = "arm"
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
                                        SetupProxyMoveItClientState(robot_description="/robot_description", robot_description_semantic=None, move_group_capabilities="/move_group", action_type_and_topics=None, enter_wait_duration=0.0),
                                        transitions={'connected': 'Connected', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'connected': Autonomy.High, 'topics_unavailable': Autonomy.Full, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'move_groups': 'move_groups'})

            # x:146 y:145
            OperatableStateMachine.add('Connected',
                                        LogState(text="Connected", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'RobotName'},
                                        autonomy={'done': Autonomy.Off})

            # x:645 y:678
            OperatableStateMachine.add('Vertical',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'GoalTolerances', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Low, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group_arm', 'config_name': 'config_vertical', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:823 y:29
            OperatableStateMachine.add('Plan',
                                        JointValuesToMoveItPlanState(timeout=5.0, enter_wait_duration=0.5, action_topic=None),
                                        transitions={'planned': 'Execute', 'failed': 'failed', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'planned': Autonomy.High, 'failed': Autonomy.Full, 'topics_unavailable': Autonomy.Full, 'param_error': Autonomy.Full},
                                        remapping={'action_topic': 'action_topic', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values', 'joint_trajectory': 'joint_trajectory'})

            # x:1215 y:121
            OperatableStateMachine.add('Execute',
                                        TrajectoryToFollowJointTrajectoryActionState(goal_time_tolerance=3.0, max_delay=-1.0, wait_duration=2.0, timeout=5.0, action_topic=None),
                                        transitions={'reached': 'Decision', 'goal_failed': 'GoalFailedLog', 'path_failed': 'PathTolLog', 'invalid_request': 'failed', 'param_error': 'failed', 'failed': 'failed'},
                                        autonomy={'reached': Autonomy.Full, 'goal_failed': Autonomy.Off, 'path_failed': Autonomy.Off, 'invalid_request': Autonomy.Full, 'param_error': Autonomy.Full, 'failed': Autonomy.Full},
                                        remapping={'trajectory_action_topic': 'trajectory_action_topic', 'joint_trajectory': 'joint_trajectory', 'joint_goal_tolerances': 'joint_goal_tolerances', 'joint_path_tolerances': 'joint_path_tolerances', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})

            # x:616 y:559
            OperatableStateMachine.add('GoalTolerances',
                                        SetJointTrajectoryTolerancesState(position_constraints=[0.05], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
                                        transitions={'configured': 'LogValues', 'param_error': 'failed'},
                                        autonomy={'configured': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'joint_names': 'joint_names', 'joint_tolerances': 'joint_goal_tolerances'})

            # x:544 y:189
            OperatableStateMachine.add('PathTolerances',
                                        SetJointTrajectoryTolerancesState(position_constraints=[0.08], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
                                        transitions={'configured': 'DumpGoalTolerance', 'param_error': 'failed'},
                                        autonomy={'configured': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'joint_names': 'joint_names', 'joint_tolerances': 'joint_path_tolerances'})

            # x:389 y:34
            OperatableStateMachine.add('DumpGoalTolerance',
                                        LogKeyState(text="Goal tolerance {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'DumpPathTolerance'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_goal_tolerances'})

            # x:560 y:50
            OperatableStateMachine.add('DumpPathTolerance',
                                        LogKeyState(text="Path tolerance {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Plan'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_path_tolerances'})

            # x:889 y:579
            OperatableStateMachine.add('Home',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'Plan', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group_arm', 'config_name': 'config_home', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:1265 y:670
            OperatableStateMachine.add('Decision',
                                        OperatorDecisionState(outcomes=["home","vertical", "PS","stop"], hint=None, suggestion=None),
                                        transitions={'home': 'Home', 'vertical': 'Vertical', 'PS': 'ApplyPS', 'stop': 'finished'},
                                        autonomy={'home': Autonomy.Off, 'vertical': Autonomy.Off, 'PS': Autonomy.Low, 'stop': Autonomy.Full})

            # x:48 y:261
            OperatableStateMachine.add('ClearOM',
                                        ClearOctomapState(timeout=5.0, wait_duration=5, action_topic="/clear_octomap"),
                                        transitions={'done': 'QueryPlanners', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Low, 'failed': Autonomy.High},
                                        remapping={'action_topic': 'action_topic'})

            # x:47 y:402
            OperatableStateMachine.add('QueryPlanners',
                                        QueryPlannersState(timeout=5.0, wait_duration=0.001, action_topic="/query_planner_interface"),
                                        transitions={'done': 'LogPlanners', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'action_topic': 'action_topic', 'planner_interfaces': 'planner_interfaces'})

            # x:108 y:527
            OperatableStateMachine.add('LogPlanners',
                                        LogKeyState(text="Available Planners {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'GetPlanningScene'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'planner_interfaces'})

            # x:87 y:641
            OperatableStateMachine.add('GetPlanningScene',
                                        GetPlanningSceneState(components=1023, timeout=5.0, wait_duration=5, action_topic="/get_planning_scene"),
                                        transitions={'done': 'LogPS', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Low, 'failed': Autonomy.Low},
                                        remapping={'action_topic': 'action_topic', 'scene': 'scene'})

            # x:1411 y:534
            OperatableStateMachine.add('ApplyPS',
                                        ApplyPlanningSceneState(timeout=5.0, wait_duration=5, action_topic="/apply_planning_scene"),
                                        transitions={'done': 'Decision', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Low, 'failed': Autonomy.Low},
                                        remapping={'action_topic': 'action_topic'})

            # x:363 y:684
            OperatableStateMachine.add('LogPS',
                                        LogKeyState(text="Planning Scence {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Vertical'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'scene'})

            # x:1157 y:336
            OperatableStateMachine.add('PathTolLog',
                                        LogState(text="Path tolerance failure", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Decision'},
                                        autonomy={'done': Autonomy.High})

            # x:1254 y:288
            OperatableStateMachine.add('GoalFailedLog',
                                        LogState(text="Failed to reach goal tolerance", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Decision'},
                                        autonomy={'done': Autonomy.High})

            # x:279 y:190
            OperatableStateMachine.add('RobotName',
                                        LogKeyState(text="Robot Name ({})", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'ClearOM'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'robot_name'})

            # x:632 y:279
            OperatableStateMachine.add('LogValues',
                                        LogKeyState(text="Joint Values {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'PathTolerances'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_values'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
