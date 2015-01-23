# Tail Calls

By starting with a platform that does not do TCO, we can look at ways to optionally do it and have the REPL warn us when a function in tail position is not tail callable. 

- Any of our own forms can (probably) be called in tail position

- But nothing that actually requires a CALL can be so (at least in python)

