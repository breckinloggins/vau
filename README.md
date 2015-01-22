#vau: a lisp

This is vau. It is a lisp written in Python.

The name is due to John N. Shutt and his [Kernel](http://web.cs.wpi.edu/~jshutt/kernel.html) programming language. 

vau is an experiment (or rather, a collection of experiments).

### vau is multi-stage

The core of vau is designed to be easily easily lexed and analyzed. Thus vau **enforces** certain naming restrictions at the native interpreter level. Note that most user code will never see these symbols, because almost all vau code will live at higher syntax levels.

```%foo`` is a symbol named %foo that refers to "plain old data"

```$foo``` is an operative named $foo (argument evaluation controlled inside the operative)

```@foo``` is an applicative named @foo (argument evaluation controlled outside the operative)

```$foo!``` is an operative named $foo! that mutates the environment or causes other side effects

```@foo!``` is an applicative named @foo! that mutates the environment or causes other side effects

```#foo``` is a syntaxitive named #foo that changes the operation of the reader when foo is encountered

```#foo` ``` is a syntaxitive named #foo` that expects an expression afterward when foo is encountered

```.foo``` is a platform object named foo

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

Goals:
- Implementation based on abstractions, not data structures (a la Clojure)
- The core language should be as reflective as possible with respect to its host
- Core vau naming conventions (as above) are struct and will be enforced
- Built-in syntax abstractions (like Syntaxitives and full control over the reader and the expander)
- Macros and syntaxitives provide layers on top of vau
- Extremely rich integration with the reader and the repl
- Very little assumptions about the optimization semantics of the host (e.g. vau WILL have an explicit recur construct)

*"The Vau Programming Language" "vau-lang", and "vau-lang.org" are (c) Breckin Loggins 2015*
