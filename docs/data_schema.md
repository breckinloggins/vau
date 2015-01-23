# Data Schema
The motivating idea here is that you sometimes want to specify a "type" for data and then use that information for various purposes (type checking is just one of these purposes).

Instead of baking in the notion of a type or a class or any of those things, see if we can have a formal "schema" concept that maps to a tag. The primary immediate use case for such a thing is code completion and highlighting in the repl.

