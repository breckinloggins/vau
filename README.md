#vau: a lisp

This is vau. It is a lisp written in Python.

The name is due to John N. Shutt and his [Kernel](http://web.cs.wpi.edu/~jshutt/kernel.html) programming language. 

vau is an experiment (or rather, a collection of experiments).

### vau is multi-stage

The core of vau is designed to be easily easily lexed and analyzed. Thus vau **enforces** certain naming restrictions at the native interpreter level. Note that most user code will never see these symbols, because almost all vau code will live at higher syntax levels.

```%foo``` is a symbol named %foo that refers to "plain old data"

```$foo``` is an operative named $foo (argument evaluation controlled inside the operative)

```@foo``` is an applicative named @foo (argument evaluation controlled outside the operative)

```$foo!``` is an operative named $foo! that mutates the environment or causes other side effects

```@foo!``` is an applicative named @foo! that mutates the environment or causes other side effects

```#foo``` is a syntaxitive named #foo that changes the operation of the reader when foo is encountered

```#foo` ``` is a syntaxitive named #foo` that expects an expression afterward when foo is encountered

```^foo``` is a symbol named ^foo that, when referred to as just "foo" by the reader, will be evaluated at read time

```.foo``` is a platform object named foo

```_``` is the name of a symbol that can never be bound (called `#ignore` in Kernel)

### vau has some nice syntactic sugar

(**coming soon**)
```foo/bar``` is short for ```(@evau bar foo)``` (thus treating environments as namespaces)

### vau has builtin operators for defining new syntax

Names that declare new syntax are called `Syntaxitives` and start with a `#`. A Syntaxitive is a combiner that is explicitly restricted to running at read-time in the current evaluation level. If a Syntaxitive symbol has one or more ``` ` ``` characters, each such character represents a "hole" where arguments will go when parsed by the reader. If no such holes are declared, the Syntaxitive is a regular syntax macro (as found in Common Lisp and Clojure).

Example syntaxitives (in prelude.vau):
```
#'` (x) -> ($quote x)             ;; 'foo -> ($quote foo)
#.` (x) -> ($platform-object x)   ;; .foo -> ($platform-object foo)
#my-quote (x) -> ($quote x)       ;; (my-quote foo) -> ($quote foo)
```



Note that overuse of syntaxitives may cause diarrhea of the semicolon.

### vau respects its platform

Platform integration (currently only python):

```
($def! %os (.__import__ 'os))
(((.getattr (.getattr %os 'path) 'join) 'foo 'bar) => foo/bar
```

### vau has bigger plans

- Implementation based on abstractions, not data structures (a la Clojure)
- The core language should be as reflective as possible with respect to its host
- Core vau naming conventions (as above) are strict and will be enforced
- Built-in syntax abstractions (like Syntaxitives and full control over the reader and the expander)
- Macros and syntaxitives provide layers on top of vau
- Extremely rich integration with the reader and the repl
- Very little assumptions about the optimization semantics of the host (e.g. vau WILL have an explicit recur construct)

*References*

- [Schrodinger's Equation of Software](http://gliese1337.blogspot.com/2012/04/schrodingers-equation-of-software.html)
- [The Kernel Underground](http://axisofeval.blogspot.com/2011/09/kernel-underground.html)

*"The Vau Programming Language" "vau-lang", and "vau-lang.org" are (c) Breckin Loggins 2015*
