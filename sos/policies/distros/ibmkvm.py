# Copyright (C) IBM Corporation, 2015
#
# Authors: Kamalesh Babulal <kamalesh@linux.vnet.ibm.com>
#
# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import PowerKVMPlugin, ZKVMPlugin
from sos.policies.distros.redhat import RedHatPolicy

import os


class PowerKVMPolicy(RedHatPolicy):
    distro = "PowerKVM"
    vendor = "IBM"
    vendor_urls = [
        ('Commercial Support',
         'http://www-03.ibm.com/systems/power/software/linux/powerkvm')
    ]

    def __init__(self, sysroot=None, init=None, probe_runtime=True,
                 remote_exec=None):
        super(PowerKVMPolicy, self).__init__(sysroot=sysroot, init=init,
                                             probe_runtime=probe_runtime,
                                             remote_exec=remote_exec)
        self.valid_subclasses += [PowerKVMPlugin]

    @classmethod
    def check(cls, remote=''):
        """This method checks to see if we are running on PowerKVM.
           It returns True or False."""

        if remote:
            return cls.distro in remote

        return os.path.isfile('/etc/ibm_powerkvm-release')

    def dist_version(self):
        try:
            with open('/etc/ibm_powerkvm-release', 'r') as fp:
                version_string = fp.read()
                return version_string[2][0]
        except IOError:
            return False


class ZKVMPolicy(RedHatPolicy):
    distro = "IBM Hypervisor"
    vendor = "IBM Hypervisor"
    vendor_urls = [
        ('Commercial Support',
         'http://www.ibm.com/systems/z/linux/IBMHypervisor/support/')
    ]

    def __init__(self, sysroot=None):
        super(ZKVMPolicy, self).__init__(sysroot=sysroot)
        self.valid_subclasses += [ZKVMPlugin]

    @classmethod
    def check(cls, remote=''):
        """This method checks to see if we are running on IBM Z KVM. It
        returns True or False."""

        if remote:
            return cls.distro in remote

        return os.path.isfile('/etc/base-release')

    def dist_version(self):
        try:
            with open('/etc/base-release', 'r') as fp:
                version_string = fp.read()
                return version_string.split(' ', 4)[3][0]
        except IOError:
            return False


# vim: set ts=4 sw=4