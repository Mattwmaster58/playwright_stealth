I don't have a formal guide for contributing yet - this file primarily serves as a reminder to myself to do releases.

## Release Process

#

 - run tests
 - run CI locally: `act`
 - tag version bump commit: git tag x.y.z
 - `poetry build`
 - `poetry publish`
