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
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Feb 06 2018
@author: David Conner
'''
class test_moveit_proxySM(Behavior):
	'''
	testing behavior
	'''


	def __init__(self):
		super(test_moveit_proxySM, self).__init__()
		self.name = 'test_moveit_proxy'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1453 y:629, x:807 y:466
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.action_topic = "/move_group"
		_state_machine.userdata.trajectory_action_topic = "/m1n6s200/effort_joint_trajectory_controller/follow_joint_trajectory"
		_state_machine.userdata.move_group_arm = "arm"
		_state_machine.userdata.config_vertical = "Vertical"
		_state_machine.userdata.config_home = "Home"
		_state_machine.userdata.config_retract = "Retract"

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

			# x:132 y:177
			OperatableStateMachine.add('Connected',
										LogState(text="Connected", severity=Logger.REPORT_HINT),
										transitions={'done': 'Vertical'},
										autonomy={'done': Autonomy.Off})

			# x:61 y:638
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
										TrajectoryToFollowJointTrajectoryActionState(goal_time_tolerance=3.0, max_delay=-1.0, wait_duration=2.0, timeout=1.0, action_topic=None),
										transitions={'reached': 'Decision', 'goal_failed': 'GoalFail', 'path_failed': 'PathFail', 'invalid_request': 'failed', 'param_error': 'failed', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Full, 'goal_failed': Autonomy.Low, 'path_failed': Autonomy.Low, 'invalid_request': Autonomy.Full, 'param_error': Autonomy.Full, 'failed': Autonomy.Full},
										remapping={'trajectory_action_topic': 'trajectory_action_topic', 'joint_trajectory': 'joint_trajectory', 'joint_goal_tolerances': 'joint_goal_tolerances', 'joint_path_tolerances': 'joint_path_tolerances', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})

			# x:342 y:441
			OperatableStateMachine.add('GoalTolerances',
										SetJointTrajectoryTolerancesState(position_constraints=[0.05], velocity_constraints=[0.0], acceleration_constraints=[0.0]),
										transitions={'configured': 'PathTolerances', 'param_error': 'failed'},
										autonomy={'configured': Autonomy.Off, 'param_error': Autonomy.Full},
										remapping={'joint_names': 'joint_names', 'joint_tolerances': 'joint_goal_tolerances'})

			# x:251 y:334
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
										OperatorDecisionState(outcomes=["home","vertical", "stop"], hint=None, suggestion=None),
										transitions={'home': 'Home', 'vertical': 'Vertical', 'stop': 'finished'},
										autonomy={'home': Autonomy.Off, 'vertical': Autonomy.Off, 'stop': Autonomy.Full})

			# x:1238 y:387
			OperatableStateMachine.add('PathFail',
										LogKeyState(text="Path failure {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Decision'},
										autonomy={'done': Autonomy.High},
										remapping={'data': 'status_text'})

			# x:1136 y:380
			OperatableStateMachine.add('GoalFail',
										LogKeyState(text="Goal failure {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Decision'},
										autonomy={'done': Autonomy.High},
										remapping={'data': 'status_text'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
