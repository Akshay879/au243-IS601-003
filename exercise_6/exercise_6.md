# Exercise 6

Since we have been discussing debugging, today we're going to analyze some code and see if we can figure out what's going wrong.

Here's our case study:

Alice is designing a prefix notation adding machine.

This machine uses parentheses and the plus sign to designate two arguments to add together.

Arguments must either be integers or another addition operation.

For example:

```lisp
(+ 1 1)          ; (1)
(+ 1 2)          ; (2)
(+ 2 (+ 3 3))    ; (3)
```

1. `<1>` this would yield `2`
2. `<2>` this would yield `3`
3. `<3>` this would yield `8`

You can find Alice's code in the class git repo `exercise_6` directory.

You'll also find it here for reference:

[parser.py](https://raw.githubusercontent.com/MattToegel/IS601/refs/heads/main/exercise_6/parser.py)

Run Alice's program and answer the following questions:

1. **In what function are you getting an error?**

   The error occurs in the get_argument() function. Specifically, this happens when the parser tries to convert a non-integer value to an integer using int(), as it encounters the character F in the input string "(+ (+ 1 2) (+ (+ 3 F) 5))".

2. **What function called the function that's giving you an error?**

   The function perform_operation() calls get_argument() to retrieve the arguments for the addition operation. get_argument() is invoked twice: once for the first argument (arg1) and once for the second argument (arg2).

3. **How many function calls in total were there before the error occurred?**

    find_open_parenthesis() — extracts the string inside the parentheses.
    perform_operation() — called by find_open_parenthesis().
    get_argument() — called by perform_operation() to retrieve the first argument of the addition.
    perform_operation() (nested call) — called recursively within get_argument() for the nested expression.
    get_argument() — called again by the recursive perform_operation() to retrieve the first argument (3).
    get_argument() (failing call) — called again to retrieve the second argument, but it fails when it encounters F.
    There were 6 function calls in total before the error.

4. **What is the type of error you're getting?**

   The type of error is a ValueError. Specifically, it occurs when int() tries to convert the non-integer character F into an integer, which is not possible.

5. **Is the error a problem with the parser or its input?**

   The error is an input problem. The input string "(+ (+ 1 2) (+ (+ 3 F) 5))" contains an invalid character F where an integer is expected. Alice's machine expects valid integers or addition expressions, but F is neither.

6. **If it's an input problem, how would you fix the input?**

   To fix the input, we should replace F with a valid integer. For example: text = "(+ (+ 1 2) (+ (+ 3 4) 5))"

7. **If it's a parser problem, how would you fix the parser?**

   If the parser needs to handle this, it should validate the input arguments and raise a specific error when invalid arguments are encountered. For example, before trying to convert to an integer, it could check if the argument is a valid integer.

8. **How could you make the parser raise a `ParserError` if this happens again in the future?**

   We can modify get_argument() to raise a ParserException when it encounters invalid arguments. The parser raises a ParserException when it encounters an invalid argument like F. We can further enhance this by adding similar error-checking mechanisms in other parts of the parser, such as checking for unknown operations (currently only + is valid).

9. **How many arguments does the addition operation in Alice's machine take?**

   Alice's machine uses two arguments for each addition operation. Every addition operation (+ a b) adds two numbers or nested operations.