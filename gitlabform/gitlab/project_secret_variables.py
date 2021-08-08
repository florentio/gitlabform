from gitlabform.gitlab.projects import GitLabProjects


class GitLabProjectSecretVariables(GitLabProjects):
    def delete_secret_variable(self, project_and_group_name, secret_variable_key):
        self._make_requests_to_api(
            "projects/%s/variables/%s",
            (project_and_group_name, secret_variable_key),
            method="DELETE",
            expected_codes=[204, 404],
        )

    def post_secret_variable(self, project_and_group_name, secret_variable):
        # secret_variable has to be like documented at:
        # https://docs.gitlab.com/ee/api/project_level_variables.html#create-variable
        self._make_requests_to_api(
            "projects/%s/variables",
            project_and_group_name,
            "POST",
            secret_variable,
            expected_codes=201,
        )

    def put_secret_variable(self, project_and_group_name, secret_variable):
        # secret_variable has to be like documented at:
        # https://docs.gitlab.com/ce/api/build_variables.html#update-variable
        self._make_requests_to_api(
            "projects/%s/variables/%s",
            (project_and_group_name, secret_variable["key"]),
            "PUT",
            secret_variable,
        )

    def get_secret_variable(self, project_and_group_name, secret_variable_key):
        return self._make_requests_to_api(
            "projects/%s/variables/%s", (project_and_group_name, secret_variable_key)
        )["value"]

    def get_secret_variables(self, project_and_group_name):
        return self._make_requests_to_api(
            "projects/%s/variables", project_and_group_name
        )
