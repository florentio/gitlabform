from gitlabform.gitlab.projects import GitLabProjects


class GitLabProjectDeployKeys(GitLabProjects):
    def post_deploy_key(self, project_and_group_name, deploy_key):
        # deploy_key has to be like this:
        # {
        #     'title': title,
        #     'key': key,
        #     'can_push': can_push,
        # }
        # ..as documented at: https://docs.gitlab.com/ce/api/deploy_keys.html#add-deploy-key
        self._make_requests_to_api(
            "projects/%s/deploy_keys",
            project_and_group_name,
            "POST",
            deploy_key,
            expected_codes=201,
        )

    def get_deploy_keys(self, project_and_group_name):
        return self._make_requests_to_api(
            "projects/%s/deploy_keys", project_and_group_name
        )

    def put_deploy_key(self, project_and_group_name, deploy_key):
        return self._make_requests_to_api(
            "projects/%s/deploy_keys",
            project_and_group_name,
            "PUT",
            deploy_key,
        )

    def delete_deploy_key(self, project_and_group_name, id):
        return self._make_requests_to_api(
            "projects/%s/deploy_keys/%s",
            (project_and_group_name, id),
            method="DELETE",
            expected_codes=[204, 404],
        )

    def get_deploy_key(self, project_and_group_name, id):
        return self._make_requests_to_api(
            "projects/%s/deploy_keys/%s", (project_and_group_name, id), "GET"
        )
