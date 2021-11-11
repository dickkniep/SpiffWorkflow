# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
import unittest
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.task import Task
from tests.SpiffWorkflow.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

__author__ = 'essweine'


class NavIndexOOBTest(BpmnWorkflowTestCase):
    """
    """

    def setUp(self):
        self.spec = self.load_workflow1_spec()

    def load_workflow1_spec(self):
        return self.load_workflow_spec('ind_update*.bpmn','Process_04jm0bm')

    def testRunThroughHappy(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.workflow.do_engine_steps()

        ready_tasks = self.workflow.get_tasks(Task.READY)
        nav_list = self.workflow.get_deep_nav_list()
        self.assertEqual(ready_tasks[0].task_spec.name, 'Activity_ConfirmStatus')
        ready_tasks[0].update_data({
            'isStudyExempt': False,
            'IND1_HolderType': 'UVaPI',
            'isIND1_HolderNameInPB': True,
            'IND2_HolderType': 'UVaPI',
            'isIND2_HolderNameInPB': False,
        })
        self.workflow.complete_task_from_id(ready_tasks[0].id)

        self.workflow.do_engine_steps()
        ready_tasks = self.workflow.get_tasks(Task.READY)
        nav_list = self.workflow.get_deep_nav_list()
        self.assertEqual(ready_tasks[0].task_spec.name, 'UserTask_SelectEntityFromPB')
        ready_tasks[0].update_data({ 'isEntity_InSponsors': True})
        self.workflow.complete_task_from_id(ready_tasks[0].id)

        self.workflow.do_engine_steps()
        ready_tasks = self.workflow.get_tasks(Task.READY)
        nav_list = self.workflow.get_deep_nav_list()
        self.assertEqual(ready_tasks[0].task_spec.name, 'UserTask_SelectEntityFromLDAP')
        ready_tasks[0].update_data({ 'isEntity_InLDAP': False })
        self.workflow.complete_task_from_id(ready_tasks[0].id)

        self.workflow.do_engine_steps()
        ready_tasks = self.workflow.get_tasks(Task.READY)
        nav_list = self.workflow.get_deep_nav_list()
        self.assertEqual(self.workflow.is_completed(), True)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(NavIndexOOBTest)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
