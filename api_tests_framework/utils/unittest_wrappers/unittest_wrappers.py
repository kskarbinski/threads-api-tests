from unittest import TestCase
from pprint import pformat

from api_tests_framework.utils.types.model import ModelType
from api_tests_framework.utils.helpers import vars_recursive


class ModelValidationTestCase(TestCase):
    def assertModel(self, model, model_type):
        self.assertTrue(hasattr(model, "model_type"))
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "updated_at"))
        self.assertTrue(hasattr(model, "created_at"))

        self.assertEqual(model.model_type, model_type.value)
        self.assertTrue(model.id)
        self.assertTrue(model.updated_at)
        self.assertTrue(model.created_at)

    def assertUserModel(self, model):
        self.assertModel(model, model_type=ModelType.USER_MODEL)

        self.assertTrue(hasattr(model, "firstname"))
        self.assertTrue(hasattr(model, "lastname"))
        self.assertTrue(hasattr(model, "username"))

        self.assertTrue(model.firstname)
        self.assertTrue(model.lastname)
        self.assertTrue(model.username)

    def assertUsernameValidationModel(self, model):
        self.assertModel(model, model_type=ModelType.USERNAME_VALIDATION_MODEL)

        self.assertTrue(hasattr(model, "errors"))

    def assertThreadModel(self, model):
        self.assertModel(model, model_type=ModelType.THREAD_MODEL)

        self.assertTrue(hasattr(model, "name"))
        self.assertTrue(hasattr(model, "owner"))
        self.assertTrue(hasattr(model, "users"))
        self.assertTrue(hasattr(model, "private"))
        self.assertTrue(hasattr(model, "deleted"))

        self.assertTrue(model.name)
        self.assertTrue(model.owner)
        self.assertTrue(model.users)
        self.assertIsNotNone(model.private)
        self.assertIsNotNone(model.deleted)

    def assertThreadInvitationModel(self, model):
        self.assertModel(model, model_type=ModelType.THREAD_INVITATION_MODEL)

        self.assertTrue(hasattr(model, "user"))
        self.assertTrue(hasattr(model, "thread"))
        self.assertTrue(hasattr(model, "status"))
        self.assertTrue(hasattr(model, "invited_by"))
        self.assertTrue(hasattr(model, "users_in_thread"))
        self.assertTrue(hasattr(model, "deleted"))

        self.assertTrue(model.user)
        self.assertTrue(model.thread)
        self.assertIsNotNone(model.status)
        self.assertTrue(model.invited_by)
        self.assertIsNotNone(model.users_in_thread)
        self.assertIsNotNone(model.deleted)

    def assertThreadApplicationModel(self, model):
        self.assertModel(model, model_type=ModelType.THREAD_APPLICATION_MODEL)

        self.assertTrue(hasattr(model, "user"))
        self.assertTrue(hasattr(model, "thread"))
        self.assertTrue(hasattr(model, "status"))
        self.assertTrue(hasattr(model, "deleted"))

        self.assertTrue(model.user)
        self.assertTrue(model.thread)
        self.assertIsNotNone(model.status)
        self.assertIsNotNone(model.deleted)

    def assertThreadMessageModel(self, model):
        self.assertModel(model, model_type=ModelType.THREAD_MESSAGE_MODEL)

        self.assertTrue(hasattr(model, "user"))
        self.assertTrue(hasattr(model, "thread"))
        self.assertTrue(hasattr(model, "message"))
        self.assertTrue(hasattr(model, "deleted"))

        self.assertTrue(model.user)
        self.assertTrue(model.thread)
        self.assertTrue(model.message)
        self.assertIsNotNone(model.deleted)

    def assertModelInListOfModels(self, model, models, ignore_attributes=None):
        model = vars_recursive(model)
        models = [vars_recursive(obj=m, ignore_attributes=ignore_attributes) for m in models]

        self.assertIn(
            model,
            models,
            msg="\n{model}\n\nnot in\n\n{models}".format(model=pformat(model), models=pformat(models))
        )

    def assertModelsInListOfModels(self, container, models):
        for model in models:
            self.assertModelInListOfModels(model=model, models=container)

    def assertModelNotInListOfModels(self, model, models, ignore_attributes=None):
        model = vars_recursive(model)
        models = [vars_recursive(obj=m, ignore_attributes=ignore_attributes) for m in models]

        self.assertNotIn(
            model,
            models,
            msg="\n{model}\n\nunexpectedly in\n\n{models}".format(model=pformat(model), models=pformat(models))
        )

    def assertModelsNotInListOfModels(self, container, models):
        for model in models:
            self.assertModelNotInListOfModels(model=model, models=container)

    def assertModelsAreEqual(self, model1, model2, ignore_attributes=None):
        model1_vars = vars_recursive(model1, ignore_attributes=ignore_attributes)
        model2_vars = vars_recursive(model2, ignore_attributes=ignore_attributes)

        self.assertEqual(model1_vars, model2_vars)
