# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# checkmk_crl_url - Checks the validity of a CRL.
#
# Copyright (C) 2021-2024  Marius Rieder <marius.rieder@durchmesser.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pytest
from cmk_addons.plugins.crl_url.server_side_calls import crl_url
from cmk.server_side_calls.v1 import HostConfig, ActiveCheckCommand


@pytest.mark.parametrize('input', [
    {'name': 'foo', 'url': 'foo', 'limit': ('fixed', (2, 3))},
    {'name': 'foo', 'url': 'https://$HOSTNAME$/foo', 'limit': ('no_levels', None)},
])
def test_model_validate(input):
    assert crl_url.Params.model_validate(input)


@pytest.mark.parametrize('input,commands', [
    [
        {'name': 'foo', 'url': 'foo', 'limit': ('fixed', (2, 3))},
        [ActiveCheckCommand(service_description='CRL foo', command_arguments=['--url', 'foo', '--warning', '2', '--critical', '3'])]
    ],
    [
        {'name': 'foo', 'url': 'https://$HOSTNAME$/foo', 'limit': ('no_levels', None)},
        [ActiveCheckCommand(service_description='CRL foo', command_arguments=['--url', 'https://pytest/foo'])]
    ],
    [
        {'name': 'OnlyFoo', 'url': 'https://$HOSTNAME$/foo', 'limit': ('no_levels', None), 'prefix': 'none'},
        [ActiveCheckCommand(service_description='OnlyFoo', command_arguments=['--url', 'https://pytest/foo'])]
    ],
])
def test_commands_function(input, commands):
    host_config = HostConfig(name='pytest', macros={'$HOSTNAME$': 'pytest'})
    params = crl_url.Params.model_validate(input)
    assert list(crl_url.commands_function(params, host_config)) == commands
