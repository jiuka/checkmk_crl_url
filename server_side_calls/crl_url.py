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

from collections.abc import Iterator

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    replace_macros,
)


class Params(BaseModel, frozen=True):
    name: str
    url: str
    proxy: str | None = None
    limit: tuple[str, tuple[float, float] | None]


def commands_function(
    params: Params,
    host_config: object,
) -> Iterator[ActiveCheckCommand]:
    command_arguments = ['--url', replace_macros(params.url, host_config.macros)]
    if params.proxy:
        command_arguments += ['--proxy', params.proxy]
    if params.limit[0] == 'fixed':
        command_arguments += ['--warning', str(int(params.limit[1][0])), "--critical", str(int(params.limit[1][1]))]

    yield ActiveCheckCommand(
        service_description=f"CRL {params.name}",
        command_arguments=command_arguments,
    )


active_check_crl_url = ActiveCheckConfig(
    name='crl_url',
    parameter_parser=Params.model_validate,
    commands_function=commands_function,
)
