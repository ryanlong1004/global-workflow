# Wrangler

## Logging

### Use the Correct Levels When Logging

It might be difficult to decide which level to assign each event. Fortunately, the Python logging module presents fewer levels than other logging libraries. This makes things easier by eliminating some potential ambiguity. When it comes to Python levels, here are the general guidelines:

- DEBUG: You should use this level for debugging purposes in development.
- INFO: You should use this level when something interesting—but expected—happens (e.g., a user starts a new project in a project management application).
- WARNING: You should use this level when something unexpected or unusual happens. It’s not an error, but you should pay attention to it.
- ERROR: This level is for things that go wrong but are usually recoverable (e.g., internal exceptions you can handle or APIs returning error results).
- CRITICAL: You should use this level in a doomsday scenario. The application is unusable. At this level, someone should be woken up at 2 a.m.

### Include a Timestamp for Each Log Entry

Knowing something happened without knowing when it happened is only marginally better than not knowing about the event at all. Make sure to add a timestamp to your log entries to make the lives of the people who use logs for troubleshooting easier. Doing so also allows developers to analyze the log entries to obtain insights/analytics about user behavior.

### Adopt the ISO-8601 Format for Timestamps

Timestamps are essential in log entries. Unfortunately, people can’t agree on the best way to express instants in time, so we came up with several conflicting formats.

Using the format widely used in your country might look like it’s the right choice, especially if you don’t plan to offer your application overseas.

But this couldn’t be further from the truth. By simply adopting a standard format for your timestamps, you can prevent problems, as third-party libraries and tools will expect the standard format in the first place.

This standard format exists, and it’s called ISO-8601. It’s an international standard for the exchange of date- and time-related data. Here’s an example of a timestamp expressed in ISO-8601 format:

`2020-03-14T15:00-03:00`

This is a basic example of how to configure the formatting to allow ISO-8601 timestamps:

```
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logging.info('Example of logging with ISO-8601 timestamp')
```

### Use the RotatingFileHandler Class

A general logging best practice—in any language—is to use log rotation. This is a mechanism designed to automatically archive, compress, or delete old log files to prevent full disks.

Fortunately, you don’t have to implement this by hand in Python. Instead, use the RotatingFileHandler class instead of the regular FileHandler one.

[Source](https://www.loggly.com/use-cases/6-python-logging-best-practices-you-should-be-aware-of/)
