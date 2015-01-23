#vau: a lisp

This is vau. It is a lisp written in Python.

The name is due to John N. Shutt and his [Kernel](http://web.cs.wpi.edu/~jshutt/kernel.html) programming language. 

vau is an experiment (or rather, a collection of experiments).

### vau is multi-stage

```#foo` ``` is a syntaxitive named ``` #foo` ``` that expects an expression afterward when foo is encountered

```^foo``` is a syntaxitive named `^foo` that, when mentioned as just `foo`, will be evaluated at read/expand time

### vau has some nice syntactic sugar

```.foo``` is a platform object named foo

```_``` is the name of a symbol that can never be bound (called `#ignore` in Kernel)

(**coming soon**)
```foo/bar``` is short for ```(evau bar foo)``` (thus treating environments as namespaces)

```::``` takes the place of `define`. It is read "as" (as in the analogy symbol) or "is now". So `(:: foo 3)` is read "foo as 3" or "foo is now 3". This syntax is composible, and in general if you see `foo::` it means that `foo` is also defined.

Examples:
```
(:: foo 3) (foo)        ;; => 3     (read as "foo is now 3")
(let foo 4) (foo)       ;; => 3     (read as "a binding from foo to 4")
(let:: foo 4) (foo)     ;; => 4     (read as "foo is now a binding to 4")
(syntax:: #s ...)       ;;          (read as "#s is now the syntax for ...")
(fn (x) ...)            ;;          (read as "a function from x to ...")
(fn:: foo (x) ...)      ;;          (read as "foo is now a function from x to ...")

```

### vau has builtin operators for defining new syntax

Names that declare new syntax are called `Syntaxitives` and start with a `#` or a `^`. A Syntaxitive is a combiner that is explicitly restricted to running at read-time in the current evaluation level. If a Syntaxitive symbol has one or more ``` ` ``` characters, each such character represents a "hole" where arguments will go when parsed by the reader. If no such holes are declared, the Syntaxitive is a regular syntax macro (as found in Common Lisp and Clojure).

Example syntaxitives (in prelude.vau):
```
#'` (x) -> (quote x)             ;; 'foo -> (quote foo)
#.` (x) -> (python-object x)     ;; .foo -> (python-object foo)
^my-quote (x) -> (quote x)       ;; (my-quote foo) -> (quote foo)
```

Note that overuse of syntaxitives may cause diarrhea of the semicolon.

### vau respects its platform

Platform integration (currently only python):

```
(:: os (.__import__ 'os))
(((.getattr (.getattr os 'path) 'join) 'foo 'bar) => foo/bar
```

### vau has bigger plans

- Implementation based on abstractions, not data structures (a la Clojure)
- The core language should be as reflective as possible with respect to its host
- Core vau naming conventions (as above) are strict and will be enforced
- Built-in syntax abstractions (like Syntaxitives and full control over the reader and the expander)
- Macros and syntaxitives provide layers on top of vau
- Extremely rich integration with the reader and the repl
- Very little assumptions about the optimization semantics of the host (though this is farther in the future)

*References*

- [Schrodinger's Equation of Software](http://gliese1337.blogspot.com/2012/04/schrodingers-equation-of-software.html)
- [The Kernel Underground](http://axisofeval.blogspot.com/2011/09/kernel-underground.html)

*"The Vau Programming Language" "vau-lang", and "vau-lang.org" are (c) Breckin Loggins 2015*
