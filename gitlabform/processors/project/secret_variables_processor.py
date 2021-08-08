import copy
import textwrap

import cli_ui
import yaml

from gitlabform.processors.util.difference_logger import hide

# TODO: support this
# if (
#         self.gitlab.get_project_settings(project_and_group)["builds_access_level"]
#         == "disabled"
# ):
#     cli_ui.warning(
#         "Builds disabled in this project so I can't set secret variables here."
#     )
#     return

from gitlabform.gitlab import GitLab
from gitlabform.processors.defining_keys import Key, And
from gitlabform.processors.multiple_entities_processor import MultipleEntitiesProcessor


class SecretVariablesProcessor(MultipleEntitiesProcessor):
    def __init__(self, gitlab: GitLab):
        super().__init__(
            "secret_variables",
            gitlab,
            list_method_name="get_secret_variables",
            add_method_name="post_secret_variable",
            delete_method_name="delete_secret_variable",
            defining=Key("key"),
            required_to_create_or_update=And(Key("key"), Key("value")),
            edit_method_name="put_secret_variable",
        )

    def _print_diff(self, project_and_group: str, configuration):

        try:
            current_secret_variables = self.gitlab.get_secret_variables(
                project_and_group
            )

            for secret_variable in current_secret_variables:
                secret_variable["value"] = hide(secret_variable["value"])

            cli_ui.debug(f"Secret variables for {project_and_group} in GitLab:")

            cli_ui.debug(
                textwrap.indent(
                    yaml.dump(current_secret_variables, default_flow_style=False),
                    "  ",
                )
            )
        except:
            cli_ui.debug(
                f"Secret variables for {project_and_group} in GitLab cannot be checked."
            )

        cli_ui.debug(f"Secret variables in {project_and_group} in configuration:")

        configured_secret_variables = copy.deepcopy(configuration)
        for key in configured_secret_variables.keys():
            configured_secret_variables[key]["value"] = hide(
                configured_secret_variables[key]["value"]
            )

        cli_ui.debug(
            textwrap.indent(
                yaml.dump(configured_secret_variables, default_flow_style=False),
                "  ",
            )
        )
