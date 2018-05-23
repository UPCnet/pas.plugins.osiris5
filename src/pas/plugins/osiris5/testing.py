# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pas.plugins.osiris5


class PasPluginsOsiris5Layer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=pas.plugins.osiris5)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'pas.plugins.osiris5:default')


PAS_PLUGINS_OSIRIS5_FIXTURE = PasPluginsOsiris5Layer()


PAS_PLUGINS_OSIRIS5_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PAS_PLUGINS_OSIRIS5_FIXTURE,),
    name='PasPluginsOsiris5Layer:IntegrationTesting',
)


PAS_PLUGINS_OSIRIS5_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PAS_PLUGINS_OSIRIS5_FIXTURE,),
    name='PasPluginsOsiris5Layer:FunctionalTesting',
)


PAS_PLUGINS_OSIRIS5_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PAS_PLUGINS_OSIRIS5_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PasPluginsOsiris5Layer:AcceptanceTesting',
)
