# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# checkmk_crl_url - Checks the validity of a CRL.
#
# Copyright (C) 2021  Marius Rieder <marius.rieder@scs.ch>
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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    HTTPUrl,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)
try:
    from cmk.gui.plugins.wato.active_checks import RulespecGroupActiveChecks
except Exception:
    from cmk.gui.plugins.wato.active_checks.common import RulespecGroupActiveChecks

def _valuespec_active_checks_crl_url():
    return Dictionary(
        title = "Check CRL Expiration",
        help = "Check if a CRL given as URL is about to expire.",
        elements = [
            (
                'name',
                TextAscii(
                    title = _("Name"),
                    allow_empty = False
                ),
            ),
            (
                'url',
                HTTPUrl(
                    title = _("CRL Distribution Point Url"),
                    help = _("The URL where the CRL should be checkd at."),
                    allow_empty = False
                ),
            ),
            (
                'limit',
                Tuple(
                    title = _("Remaining time till expiration."),
                    elements = [
                        Age(title = _("Warnings if expired within"), default_value = 86400 * 15),
                        Age(title = _("Critical if expired within"), default_value = 86400 * 10),
                    ]
                ),
            ),
        ]
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupActiveChecks,
        match_type='all',
        name='active_checks:crl_url',
        valuespec=_valuespec_active_checks_crl_url,
    ))
