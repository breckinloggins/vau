**vau: a lisp**

This is vau. It is a lisp written in Python.

The name is due to John N. Shutt and his [Kernel](http://web.cs.wpi.edu/~jshutt/kernel.html) programming language. 

vau is an experiment (or rather, a collection of experiments).

Naming conventions:

```
$foo    - an operative named $foo (argument evaluation controlled inside the operative)
foo     - an applicative named foo (argument evaluation controlled outside the operative)
$foo!   - an operative named $foo! that mutates the environment or causes other side effects
foo!    - an applicative named foo! that mutates the environment or causes other side effects
foo`    - a syntaxitive named foo` that changes the operation of the reader when foo is encountered
.foo    - a platform object named foo
```

Note that overuse of syntaxitives may cause diarrhea of the semicolon.

Current syntaxitives in prelude:
```
'` (x) -> ($quote x)
.` (x) -> ($platform-object x)
```

Platform integration (currently only python):

```
($def! os (.__import__ 'os))
(((.getattr (.getattr os 'path) 'join) 'foo 'bar) => foo/bar
```
