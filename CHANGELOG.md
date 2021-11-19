# Wagtailpurge Changelog

## 0.4.0 (TBC)

- Handle request processing in a separate thread using python's native `threading` module.

## 0.3.0 (2021-11-11)

- Add the `URLPurgeRequest` request type.
- Improve test coverage.

## 0.2.0 (2021-08-23)

- README improvements
- Hide 'Edit' functionality for purge requests
- Update `PurgeRequestSubmitView` to wrap the async process in `transaction.on_commit` to release any database locks on the object before it is processed.
- Test app / coverage improvements.

## 0.1.1 (2021-08-22)

- Fixed packaging issues (missing templates etc)

## 0.1.0 (2021-08-22)

- Initial release
