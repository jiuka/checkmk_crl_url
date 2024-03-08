# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# checkmk_crl_url - Checks the validity of a CRL.
#
# Copyright (C) 2021-2024  Marius Rieder <marius.rieder@scs.ch>
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


from cmk.rulesets.v1 import form_specs, Help, rule_specs, Title


def _migrate(params: dict) -> dict:
    if 'limit' not in params:
        params['limit'] = ('no_levels', None)
    return params


def _form_active_checks_crl_url() -> form_specs.Dictionary:
    return form_specs.Dictionary(
        help_text=Help(
            "Check if a CRL given as URL is about to expire."
        ),
        elements=dict(
            name=form_specs.DictElement[str](
                parameter_form=form_specs.String(
                    title=Title("Name"),
                    custom_validate=form_specs.validators.DisallowEmpty(),
                ),
                required=True,
            ),
            url=form_specs.DictElement[str](
                parameter_form=form_specs.String(
                    title=Title("CRL Distribution Point Url"),
                    help_text = Help("The URL where the CRL should be checkd at."),
                    custom_validate=form_specs.validators.Url(
                        protocols=[form_specs.validators.UrlProtocol.HTTP, form_specs.validators.UrlProtocol.HTTPS]
                    ),
                ),
                required=True,
            ),
            proxy=form_specs.DictElement[str](
                parameter_form=form_specs.String(
                    title=Title("Proxy"),
                    help_text = Help(
                        "Do not check this box if none is neded. If a proxy is needed for the query it can be specified here. "
                        "Will be uses as HTTP & HTTPS proxy."
                    ),
                    custom_validate=form_specs.validators.Url(
                        protocols=[form_specs.validators.UrlProtocol.HTTP, form_specs.validators.UrlProtocol.HTTPS]
                    ),
                ),
                required=False,
            ),
            limit=form_specs.DictElement[form_specs.SimpleLevels[float]](
                parameter_form=form_specs.SimpleLevels[float](
                    title=Title("Remaining time till expiration."),
                    level_direction=form_specs.LevelDirection.LOWER,
                    form_spec_template=form_specs.TimeSpan(
                        displayed_magnitudes=[form_specs.TimeMagnitude.DAY, form_specs.TimeMagnitude.HOUR, form_specs.TimeMagnitude.MINUTE]
                    ),
                    migrate=form_specs.migrate_to_float_simple_levels,
                    prefill_fixed_levels=form_specs.InputHint(value=(86400 * 15, 86400 * 10)),
                ),
                required=True,
            ),
        ),
        migrate=_migrate,
    )


rule_spec_crl_url = rule_specs.ActiveCheck(
    title=Title("Check CRL Expiration"),
    topic=rule_specs.Topic.GENERAL,
    name="crl_url",
    parameter_form=_form_active_checks_crl_url,
)
