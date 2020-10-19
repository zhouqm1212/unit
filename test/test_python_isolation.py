import shutil

import pytest

from conftest import option
from conftest import unit_run
from conftest import unit_stop
from unit.applications.lang.python import TestApplicationPython
from unit.feature.isolation import TestFeatureIsolation


class TestPythonIsolation(TestApplicationPython):
    prerequisites = {'modules': {'python': 'any'}, 'features': ['isolation']}

    @classmethod
    def setup_class(cls, complete_check=True):
        check = super().setup_class(complete_check=False)

        unit = unit_run()
        option.temp_dir = unit['temp_dir']

        TestFeatureIsolation().check(option.available, unit['temp_dir'])

        assert unit_stop() is None
        shutil.rmtree(unit['temp_dir'])

        return check if not complete_check else check()

    def test_python_isolation_rootfs(self, is_su, temp_dir):
        isolation_features = option.available['features']['isolation'].keys()

        if 'mnt' not in isolation_features:
            pytest.skip('requires mnt ns')

        if not is_su:
            if 'user' not in isolation_features:
                pytest.skip('requires unprivileged userns or root')

            if not 'unprivileged_userns_clone' in isolation_features:
                pytest.skip('requires unprivileged userns or root')

        isolation = {
            'namespaces': {'credential': not is_su, 'mount': True},
            'rootfs': temp_dir,
        }

        self.load('empty', isolation=isolation)

        assert self.get()['status'] == 200, 'python rootfs'

        self.load('ns_inspect', isolation=isolation)

        assert (
            self.getjson(url='/?path=' + temp_dir)['body']['FileExists']
            == False
        ), 'temp_dir does not exists in rootfs'

        assert (
            self.getjson(url='/?path=/proc/self')['body']['FileExists']
            == False
        ), 'no /proc/self'

        assert (
            self.getjson(url='/?path=/dev/pts')['body']['FileExists'] == False
        ), 'no /dev/pts'

        assert (
            self.getjson(url='/?path=/sys/kernel')['body']['FileExists']
            == False
        ), 'no /sys/kernel'

        ret = self.getjson(url='/?path=/app/python/ns_inspect')

        assert (
            ret['body']['FileExists'] == True
        ), 'application exists in rootfs'

    def test_python_isolation_rootfs_no_language_deps(self, is_su, temp_dir):
        isolation_features = option.available['features']['isolation'].keys()

        if 'mnt' not in isolation_features:
            pytest.skip('requires mnt ns')

        if not is_su:
            if 'user' not in isolation_features:
                pytest.skip('requires unprivileged userns or root')

            if not 'unprivileged_userns_clone' in isolation_features:
                pytest.skip('requires unprivileged userns or root')

        isolation = {
            'namespaces': {'credential': not is_su, 'mount': True},
            'rootfs': temp_dir,
            'automount': {'language_deps': False}
        }

        self.load('empty', isolation=isolation)

        assert (self.get()['status'] != 200), 'disabled language_deps'

        isolation['automount']['language_deps'] = True

        self.load('empty', isolation=isolation)

        assert (self.get()['status'] == 200), 'enabled language_deps'
