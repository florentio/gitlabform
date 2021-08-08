from tests.acceptance import (
    run_gitlabform,
)


class TestDeployKeys:
    def test__deploy_key_to_all_projects(self, gitlab, group, project, other_project):
        # noinspection PyPep8
        deploy_key_to_all_projects = """
        projects_and_groups:
          "*":
            deploy_keys:
              foobar:
                key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC6OxCCViSjh8QUKNOoGqhUqs4LLDMyq/7DYuvMJu5lXwECWp0wFGoLXzYWCT6WOAP+vccncOrlVfsr9VJzXxR1QZq+p3joW25nWgjEw/HCPI6fnU1vROImzxnvwLS3EEJpy64Jq0FFwjt8vKSuQshPysEBSUTf5t3omb166MGlZ+Y6/tOf/8/3zqmvb8OqNmhUtfwxfE5oX8Z8bBaGrkxHlmYyJ9UBpfeEcFt1GqfiONPgchJJ4OqCJKqd7H4DZOosT64kTqPXhca44EOxiKQviCthv7bO+r7VSFo5TVo60ikq/sTR9ifXnd3B9x3LV1qzHHLlmnP//xkKHIZGxfyhgwtdGNWhEtKPiXUzZv4/48WUJMmtpjznhuEgjnpiJL3x0+vJCStA6WG0MiozBlS80Y4XHbt3X3bvlNSqSo/GpnxlPTUx+Lj/ASI75JDym14+C8RdSFN4iKl5Qjz5xFq4eXke00AahFvjAAV5BT8Qrlyg/cbt1pfWKND1T5Fqh6c=
                title: common_key
                can_push: false
        """
        run_gitlabform(deploy_key_to_all_projects, group)

        deploy_keys1 = gitlab.get_deploy_keys(f"{group}/{project}")
        assert len(deploy_keys1) == 1

        deploy_keys2 = gitlab.get_deploy_keys(f"{group}/{other_project}")
        assert len(deploy_keys2) == 1

    def test__deploy_key_delete(self, gitlab, group, project):
        group_and_project_name = f"{group}/{project}"

        # noinspection PyPep8
        config = f"""
        projects_and_groups:
          {group_and_project_name}:
            deploy_keys:
              foobar:
                key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDydRMMBVOXfD76kjfI9wjxcSkJqdqr9222naDd6EGLuoDPjwRdowGJXTPLO88iFux2hWpROfT3PaP8s/yi0LkKSi2Fwn4hEc9u8pVoXQVhEwu367cLmy0XCo5lOmkfXaBSvLqb+Z6v9CozdJzmsllcTCK1DoYcGD8NPnQMMEETqbHzropjUjLA/to/zfI/mYVP86X15w+pw0DsUtspj3MmQBxPks4v2EAF7tUGLgqMHMr/z5bsWkm6yR4fv7rfjLoh10tXUY8WrVvzAZzWCs7fnP1qf5CCU7MlzggSIhzbwLn2DcYMBnFKGgx3H/VwJIvtmoIq8duedlUQ8zxKaSK8ziF/WQ8EtMW19qCrI8W+6vOgJpooDpBkPnSE+gsS+ANyWoXOJhgGukjPtphYqGTvDQAAbAMIeXB7QqDwq62UkgRSr5TC4pTVQrzlRTLxrnWMpYhpYy/3fCvYWDvuRFV8+IH6mlXoCrcMfh78oShmwkv8+A9/j9pBBBiFBZ2x6sM=
                title: some_key
        """
        run_gitlabform(config, group_and_project_name)

        deploy_keys = gitlab.get_deploy_keys(group_and_project_name)
        assert any([key["title"] == "some_key" for key in deploy_keys])

        # noinspection PyPep8
        config = f"""
        projects_and_groups:
          {group_and_project_name}:
            deploy_keys:
              foobar:
                title: some_key
                delete: true
        """
        run_gitlabform(config, group_and_project_name)

        deploy_keys = gitlab.get_deploy_keys(group_and_project_name)
        assert not any([key["title"] == "some_key" for key in deploy_keys])

    def test__deploy_key_update(self, gitlab, group, project):
        group_and_project_name = f"{group}/{project}"

        # noinspection PyPep8
        key_before = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCz7QLHyLval1TS+MvLN9QwLi5It7f74BQWi7d5gxBKA7BaGxebOc3AmLF9B/XkBfSNLOEhKO6NZrq07U4C2c3j29IvHy1oAk/cg6YmDL6U7d9lxBxYHC/SsnN70LekGbjHhaMofNvfnDOpS7n5MvJjY42ovxag+SRAOhtp541no6R/Oj9OoW6Y3AtX59HIcP1JvGTx/Ohb8OUwOXbfIDxrqR4qt1kiSPLAAC8wLNNDTUYs89TVAqyvzuXXindmcXosVcEQ6EYzHPin66ge1rAYJfhBqei1tmS0OUrW4awzQxddBqrwVBq0occUrbkjJNRfEjHjYR2GDutk8bP/kZ7cJ3RMU7bCh6CNGvApN7BysSfFcS19/18BCVjWFWbZSHGoaB0DDjl9R5s7RzMuBvNULt4yTEQUOQKdmteJY6RxKApxiCglu8I+8fIzL75iDNejZ+UlXj1SnIfe2BrzR/EN2FAGubq2SLmKLGLSGk3lkwDBdPfNMjYJG9bdaeHt2mc="
        key_after = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICRgWbMGu+88gPVPEIAHQdG958oTzSFmuBnwmC0hunyp"

        config = f"""
        projects_and_groups:
          {group_and_project_name}:
            deploy_keys:
              foobar:
                key: {key_before}
                title: a_key
        """
        run_gitlabform(config, group_and_project_name)

        deploy_keys = gitlab.get_deploy_keys(group_and_project_name)
        assert any([key["key"] == key_before for key in deploy_keys])

        config = f"""
        projects_and_groups:
          {group_and_project_name}:
            deploy_keys:
              foobar:
                key: {key_after}
                title: a_key
        """
        run_gitlabform(config, group_and_project_name)

        deploy_keys = gitlab.get_deploy_keys(group_and_project_name)
        assert not any([key["key"] == key_before for key in deploy_keys])
        assert any([key["key"] == key_after for key in deploy_keys])
