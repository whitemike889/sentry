from __future__ import absolute_import

from sentry.mediators.service_hooks import Creator
from sentry.models import ServiceHook
from sentry.testutils import TestCase


class TestCreator(TestCase):
    def setUp(self):
        self.user = self.create_user()
        self.org = self.create_organization(owner=self.user)
        self.project = self.create_project(name='foo', organization=self.org)
        self.sentry_app = self.create_sentry_app(owner=self.org)
        self.creator = Creator(application=self.sentry_app.application,
                               actor=self.sentry_app.proxy_user,
                               project=self.project,
                               events=('event.created',),
                               url=self.sentry_app.webhook_url)

    def test_creates_service_hook(self):
        self.creator.call()

        service_hook = ServiceHook.objects.get(
            application=self.sentry_app.application,
            actor_id=self.sentry_app.proxy_user.id,
            project_id=self.project.id,
            url=self.sentry_app.webhook_url,
        )

        assert service_hook
        assert service_hook.events == ['event.created']
