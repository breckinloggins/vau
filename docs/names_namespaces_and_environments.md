# Names, Namespaces, and Environments

## Name prefixing

Kernel adds a "$" prefix to names that are operatives, as a hint that their evaluation strategy is special.  Currently, vau goes further and enforces "$" for operatives, "@" for applicatives, "^" for macros, and "%" for "plain old data".

Why are we doing this?

- It simplifies lexing the language
- It shows at a glance what symbols are for
- It allows us to know when a program has been fully expanded
- The underlying type restrictions actually allow us to prove what certain symbols are for

Downsides:
- It's ugly
- It removes some of the whole reason you want a lisp in the first place
- The discoverability problems could be solved by rich tooling instead
 
Some observations:
- I prefer the Clojure philosophy: a symbol - as such - is just a name. What it refers to is eval's business, not the symbol's business
- vau assumes rich tooling and the distinction between the vau language and the vau environment is really a non-distinction. I'm tired of being tied to a logical teletype
- The difference between an "operator" and an "applicative" seems too course. These could instead be both ends of a continuum of logical types. More on this later, but basically you should be able to specify PER ARGUMENT whether that argument will be pre-evaluated or not. This is strictly more powerful and is still analyzable

Observation number 1 is enough for me to say that enforced "prefix typing" of symbols is a non-starter and is now removed from the language.

Essentially this amounts to an act of faith that these issues can be solved another way.

I do like the idea that, in the repl, vau should be given a different color than all other operators. Operators that MUST be builtin should be a lighter shade of that color.

### Lexical prefixing and the use/mention distinction

I think I'll keep the # prefix for lexical reader macros and the ^ prefix for eval macros. My current rationale is that these symbols are "special" in several senses:

- They always refer to a special operation and never to something else

- In the case of reader macros, they have meanings encoded in their names (the position of the holes)

- They run at a different level in the interpreter tower

For these reasons the use/mention distinction is more important for these symbols. In the case of eval macros, it should be possible to mention them at eval time (by using their full names), while using their plain names uses them at read time. For reader macros, their mention/use forms are structurally distinct, so the only way to mention them without affecting the reader is to call them by name. Both of these cases have the property that the prefix "escapes" the use/mention distinction.

Since they are both "syntax" concepts, they are now unified under the defsyntax! form.


