from odoo import Command

from odoo.tests.common import TransactionCase, tagged

@tagged("-at_install", "post_install")
class TestStudioApprovals(TransactionCase):
    def test_approval_method_two_models(self):
        IrModel = self.env["ir.model"]
        other_user = self.env["res.users"].create({
            "name": "test",
            "login": "test",
            "email": "test@test.test",
            "groups_id": [Command.link(self.env.ref("base.group_user").id)]
        })

        self.env["studio.approval.rule"].create([
            {
                "model_id": IrModel._get("test.studio.model_action").id,
                "method": "action_confirm",
                "responsible_id": 2,
                "users_to_notify": [Command.link(2)],
                "exclusive_user": True,
            },
            {
                "model_id": IrModel._get("test.studio.model_action").id,
                "method": "action_confirm",
                "responsible_id": 2,
                "users_to_notify": [Command.link(2)],
                "exclusive_user": True,
            },
            {
                "model_id": IrModel._get("test.studio.model_action").id,
                "method": "action_confirm",
                "notification_order": "2",
                "responsible_id": 2,
                "users_to_notify": [Command.link(other_user.id)],
                "exclusive_user": True,
            },
            {
                "model_id": IrModel._get("test.studio.model_action2").id,
                "method": "action_confirm",
                "responsible_id": 2,
                "users_to_notify": [Command.link(2)],
                "exclusive_user": True,
            }
        ])

        model_action = self.env["test.studio.model_action"].create({
            "name": "test"
        })

        with self.with_user("demo"):
            self.env["test.studio.model_action"].browse(model_action.id).action_confirm()

        self.assertFalse(model_action.confirmed)
        self.assertEqual(model_action.message_ids[0].preview, "@Mitchell Admin An approval for 'False' has been requested on test")
        self.assertEqual(len(model_action.activity_ids), 1)

        with self.with_user("admin"):
            self.env["test.studio.model_action"].browse(model_action.id).action_confirm()

        self.assertFalse(model_action.confirmed)
        self.assertEqual(model_action.message_ids[0].preview, "@test An approval for 'False' has been requested on test")
        self.assertEqual(len(model_action.activity_ids), 1)

        with self.with_user("test"):
            self.env["test.studio.model_action"].browse(model_action.id).action_confirm()

        self.assertTrue(model_action.confirmed)
        self.assertEqual(model_action.message_ids[0].preview, "Approved as User types / Internal User")
        self.assertEqual(len(model_action.activity_ids), 0)

    def test_notify_higher_notification_order(self):
        IrModel = self.env["ir.model"]
        other_user = self.env["res.users"].create({
            "name": "test",
            "login": "test",
            "email": "test@test.test",
            "groups_id": [Command.link(self.env.ref("base.group_user").id)]
        })

        self.env["studio.approval.rule"].create([
            {
                "model_id": IrModel._get("test.studio.model_action").id,
                "method": "action_step",
                "domain": "[('step', '<', 1)]",
                "responsible_id": 2,
                "users_to_notify": [Command.link(2)],
            },
            {
                "model_id": IrModel._get("test.studio.model_action").id,
                "method": "action_step",
                "domain": "[('step', '>=', 1)]",
                "notification_order": "2",
                "responsible_id": 2,
                "users_to_notify": [Command.link(other_user.id)],
            },
            {
                "model_id": IrModel._get("test.studio.model_action2").id,
                "method": "action_step",
                "notification_order": "1",
                "responsible_id": 2,
                "users_to_notify": [Command.link(2)],
            },
        ])

        model_action = self.env["test.studio.model_action"].create({
            "name": "test"
        })
        with self.with_user("demo"):
            self.env["test.studio.model_action"].browse(model_action.id).action_step()

        self.assertEqual(model_action.step, 1)
        self.assertEqual(model_action.message_ids[0].preview, "@test An approval for 'False' has been requested on test")
        self.assertEqual(len(model_action.activity_ids), 1)
