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

from cmk.graphing.v1 import graphs, metrics, perfometers, Title

metric_ttl = metrics.Metric(
    name='ttl',
    title=Title('CRL Lifetime'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.LIGHT_BLUE,
)

perfometer_ttl = perfometers.Perfometer(
    name='ttl',
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(10)),
    segments=['ttl'],
)

graph_ttl = graphs.Graph(
    name='crl_url',
    title=Title('CRL Lifetime'),
    compound_lines=['ttl'],
    simple_lines=[
        metrics.WarningOf('ttl'),
        metrics.CriticalOf('ttl'),
    ],
)
