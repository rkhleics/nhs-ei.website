# Release process

## Staging

1. Open a pull request back into the `main` branch with your changes, including an entry into the `CHANGELOG` under the Unreleased heading
1. Get that pull request code reviewed and approved
1. Check that any prerequisite changes to things like environment variables or third-party service configuration is ready
1. Merge the pull request

The changes are deployed automatically to staging. On merge, a docker image is built with Github actions and pushed to 
the Azure container repository. The container is then deployed with Helm. See [deployment/README.md]()

Changes deployed to staging are still regarded as Unreleased in the changelog. Changes are not "released" until they are 
deployed to production
