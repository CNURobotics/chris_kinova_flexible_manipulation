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
from flexible_manipulation_flexbe_states.set_joint_trajectory_tolerances_state import SetJointTrajectoryTolerancesState
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.operator_decision_state import OperatorDecisionState
from flexible_manipulation_flexbe_states.execute_known_trajectory_state import ExecuteKnownTrajectoryState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 2 2018
@author: David Conner
'''
class test_flexible_manipulation2SM(Behavior):
    '''
    testing behavior
    '''


    def __init__(self):
        super(test_flexible_manipulation2SM, self).__init__()
        self.name = 'test_flexible_manipulation2'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1423 y:790, x:784 y:398
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.action_topic = "/move_group"
        _state_machine.userdata.trajectory_action_topic = "/m1n6s200/effort_joint_trajectory_controller/follow_joint_trajectory"
        _state_machine.userdata.move_group = "arm"
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
                                        SetupProxyMoveItClientState(robot_description="/robot_description", robot_description_semantic=None, move_group_capabilities="/move_group", action_type_and_topics=[ [ "MoveGroupAction", ["/move_group"] ] ], enter_wait_duration=0.0),
                                        transitions={'connected': 'Connected', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'connected': Autonomy.High, 'topics_unavailable': Autonomy.Full, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'move_groups': 'move_groups'})

            # x:146 y:145
            OperatableStateMachine.add('Connected',
                                        LogState(text="Connected", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Vertical'},
                                        autonomy={'done': Autonomy.Off})

            # x:481 y:644
            OperatableStateMachine.add('Vertical',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'GoalTolerances', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Low, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group', 'config_name': 'config_vertical', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:909 y:136
            OperatableStateMachine.add('Plan',
                                        JointValuesToMoveItPlanState(timeout=5.0, enter_wait_duration=0.5, action_topic=None),
                                        transitions={'planned': 'ExecTraj', 'failed': 'failed', 'topics_unavailable': 'failed', 'param_error': 'failed'},
                                        autonomy={'planned': Autonomy.High, 'failed': Autonomy.Full, 'topics_unavailable': Autonomy.Full, 'param_error': Autonomy.Full},
                                        remapping={'action_topic': 'action_topic', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values', 'joint_trajectory': 'joint_trajectory'})

            # x:461 y:479
            OperatableStateMachine.add('GoalTolerances',
                                        SetJointTrajectoryTolerancesState(position_constraints=[0.05], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
                                        transitions={'configured': 'PathTolerances', 'param_error': 'failed'},
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

            # x:653 y:50
            OperatableStateMachine.add('DumpPathTolerance',
                                        LogKeyState(text="Path tolerance {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Plan'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'joint_path_tolerances'})

            # x:760 y:584
            OperatableStateMachine.add('Home',
                                        GetJointValuesFromSrdfConfigState(),
                                        transitions={'retrieved': 'Plan', 'param_error': 'failed'},
                                        autonomy={'retrieved': Autonomy.Off, 'param_error': Autonomy.Full},
                                        remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group', 'config_name': 'config_home', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

            # x:551 y:799
            OperatableStateMachine.add('Decision',
                                        OperatorDecisionState(outcomes=["home","vertical","stop"], hint=None, suggestion=None),
                                        transitions={'home': 'Home', 'vertical': 'Vertical', 'stop': 'finished'},
                                        autonomy={'home': Autonomy.Off, 'vertical': Autonomy.Off, 'stop': Autonomy.Full})

            # x:1085 y:601
            OperatableStateMachine.add('ExecTraj',
                                        ExecuteKnownTrajectoryState(timeout=3.0, max_delay=5.0, wait_duration=0.25, action_topic="/execute_trajectory"),
                                        transitions={'done': 'Decision', 'failed': 'failed', 'param_error': 'ErrLog'},
                                        autonomy={'done': Autonomy.High, 'failed': Autonomy.High, 'param_error': Autonomy.Off},
                                        remapping={'action_topic': 'action_topic', 'trajectory': 'joint_trajectory', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})

            # x:999 y:715
            OperatableStateMachine.add('ErrLog',
                                        LogState(text="Param error on exec traj", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'StatusLog'},
                                        autonomy={'done': Autonomy.Off})

            # x:897 y:761
            OperatableStateMachine.add('StatusLog',
                                        LogKeyState(text=" Status {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Decision'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'status_text'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
