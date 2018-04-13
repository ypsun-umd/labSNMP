#!/usr/bin/env python
#
# Last Change: Fri Apr 13, 2018 at 12:08 PM -0400

from os import environ
from os.path import dirname, abspath, join
from pysnmp.hlapi import *
from pysnmp.smi import builder

py_mib_path = join(dirname(dirname(abspath(__file__))), 'compiled')


class BiDict(dict):
    # NOTE: Here we implicitly assumed that the forward mapping is injective.
    def __init__(self, *args, **kwargs):
        super(BiDict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.iteritems():
            self.inverse[value] = key


class BasePowerSupplyControl(object):
    community = 'public'
    total_chs = 0
    power_status_code = BiDict({
        'on':    0,
        'off':   1,
        'cycle': 2
    })

    def __init__(self, ip):
        # FIXME: Use environmental variable to enable PySNMP to load compiled
        # MIBs.
        environ['PYSNMP_MIB_PKGS'] = py_mib_path

        self.ip = ip
        self.mibBuilder = builder.MibBuilder()

    def DoCmd(self, cmd, oidtype):
        queryCmd = cmd(
            SnmpEngine(),
            CommunityData(self.community),
            UdpTransportTarget((self.ip, 161)),
            ContextData(),
            oidtype
        )

        try:
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in queryCmd:

                if errorIndication:
                    return errorIndication

                elif errorStatus:
                    return errorStatus

                else:
                    status = [0, ]
                    for varBind in varBinds:
                        for x in varBind:
                            status.append(x.prettyPrint())
                    return status

        except Exception as err:
            return err

    def PowerOffCh(self, ch_num):
        pass

    def PowerOnCh(self, ch_num):
        pass

    def PowerCycleCh(self, ch_num):
        pass

    def PowerOffAll(self):
        pass

    def PowerOnAll(self):
        pass

    def PowerCycleAll(self):
        pass

    def ChStatus(self, ch_num):
        pass

    def ChsAllStatus(self):
        pass