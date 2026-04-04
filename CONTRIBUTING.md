
 - Try to fit the existing structure and patterns of the codebase for a new evasion
 - Write tests for your evasion
 - Add your change to the CHANGELOG.md

## Release Process
#### For maintainers

 - run tests
 - run CI locally: `act`
 - tag version bump commit: git tag x.y.z
 - `poetry build`
 - `poetry publish`
