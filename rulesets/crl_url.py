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


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    InputHint,
    LevelDirection,
    migrate_to_float_simple_levels,
    SimpleLevels,
    String,
    TimeSpan,
    TimeMagnitude,
    validators,
)
from cmk.rulesets.v1.rule_specs import ActiveCheck, Topic


def _form_active_checks_crl_url() -> Dictionary:
    return Dictionary(
        help_text=Help('Check if a CRL given as URL is about to expire.'),
        elements={
            'name': DictElement(
                parameter_form=String(
                    title=Title('Name'),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            'url': DictElement(
                parameter_form=String(
                    title=Title('CRL Distribution Point Url'),
                    help_text = Help('The URL where the CRL should be checkd at.'),
                    custom_validate=(validators.Url(
                        protocols=[validators.UrlProtocol.HTTP, validators.UrlProtocol.HTTPS]
                    ),),
                ),
                required=True,
            ),
            'proxy': DictElement(
                parameter_form=String(
                    title=Title('Proxy'),
                    help_text = Help(
                        'Do not check this box if none is neded. If a proxy is needed for the query it can be specified here. '
                        'Will be uses as HTTP & HTTPS proxy.'
                    ),
                    custom_validate=(validators.Url(
                        protocols=[validators.UrlProtocol.HTTP, validators.UrlProtocol.HTTPS]
                    ),),
                ),
                required=False,
            ),
            'limit': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Remaining time till expiration.'),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE]
                    ),
                    migrate=migrate_to_float_simple_levels,
                    prefill_fixed_levels=InputHint(value=(86400 * 15, 86400 * 10)),
                ),
                required=True,
            ),
        },
    )


rule_spec_crl_url = ActiveCheck(
    title=Title('Check CRL Expiration'),
    topic=Topic.GENERAL,
    name="crl_url",
    parameter_form=_form_active_checks_crl_url,
)
