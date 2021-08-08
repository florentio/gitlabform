from gitlabform.gitlab import GitLab
from gitlabform.processors.defining_keys import And, Key
from gitlabform.processors.multiple_entities_processor import MultipleEntitiesProcessor


class DeployKeysProcessor(MultipleEntitiesProcessor):
    def __init__(self, gitlab: GitLab):
        super().__init__(
            "deploy_keys",
            gitlab,
            list_method_name="get_deploy_keys",
            add_method_name="post_deploy_key",
            delete_method_name="delete_deploy_key",
            defining=Key("title"),
            required_to_create_or_update=And(Key("title"), Key("key")),
            edit_method_name="put_deploy_key",
        )
