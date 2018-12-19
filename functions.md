<h1>How to Write a Function in Python3</h1>
<h4>Best practices for writing your own functions</h4>

![PythonLogo](https://www.python.org/static/opengraph-icon-200x200.png)

<h5>What is a function?</h5>
In Python, a function is a block of code that runs only when it's called.  This is referred to as a "function call."  Functions can be simple or complex, but regardless, you'll want to use functions as extensively as possible.  There's an unwritten rule among programmers that a function should be used anytime you'll type that same piece of code more than two times.  Write as many functions as possible, regardless of how trivial they may seem.

<h5>Components of a function</h5>
Best practices for writing functions should at the minimum include the steps below.  One of the most frustrating parts of programming is working with poorly commented code to include incomplete function design.  If you follow these steps you'll write solid functions that are clear and useful to others.  Here are the six steps I use(modified from multiple sources referenced below):

***

1.  Give examples of what your function should do.
    - Think about what your function should do.  (i.e. - Convert pounds to kilograms.)
    - Come up with a name for your function - usually a verb or action phrase. (i.e. `lbs_to_kg`)
    - Type a couple of examples which will be stored as future reference in the built-in `help()` function.  These are recreations of what will happen at the Python prompt when you run your function.
        - \>>> lbs_to_kg(2.2)<br>
        1<br>
        \>>> lbs_to_kg(100)<br>
        45.36
2.  Create the type contract.
    - What are the parameter types used in your function (i.e. number, int, float, str, etc.)
    - Make sure to include the value returned.  Here is our type contract: (number) -> number
    - This is what our function looks like so far (''' indicates block comment in Python also called a docstring):
        - ''' (number) -> (number)<br><br>
        \>>> lbs_to_kg(2.2)<br>
        1<br>
        \>>> lbs_to_kg(100)<br>
        45.36
        '''
3.  Define the Function Header.
    - The function header format is a keyword, name of the function, and function parameters in parantheses followed by a colon.
        - Function Header Format - def function_name(parameters):
    - Choose your input parameter names and try to make them self explanatory.
        - def lbs_to_kg(lbs)
    - Our function code so far:
        - def lbs_to_kg(lbs)<br>
        ''' (number) -> (number)<br><br>
        \>>> lbs_to_kg(2.2)<br>
        1<br>
        \>>> lbs_to_kg(100)<br>
        45.36
        '''
4.  Write a concise description of your function.
    - Include between the type contract and examples.
    - This will be a key part of this function's comments in `help()`
    - Description: Return the number of kilograms equivalent to the input parameter pounds (lbs).
    - Updated function code:
        - def lbs_to_kg(lbs)<br>
        ''' (number) -> (number)<br><br>
        Return the number of kilograms equivalent to the input parameter pounds (lbs).<br><br>
        \>>> lbs_to_kg(2.2)<br>
        1<br>
        \>>> lbs_to_kg(100)<br>
        45.36
        '''
5.  Body of the Function
    - Includes the `return` and/or `print` statement followed by the function formula.
    - `return` will send the value of parameter `(lbs)` to the caller or memory address even if it's None.  To display the value from a `return` statement store the value in a variable and call the variable with a `print()` statement.
    - `return` will also exit the current function. If `return` is skipped an implicit `return None` is included at the end of the function.
    - `print` will display to standard output the value of a parameter, in this case `(lbs)`.  `print` does not affect the control flow of execution in any way or exit the function.
    - This function's body: return lbs / 2.205
6.  Test
    - Save your function to a .py file (i.e. lbs_to_kg.py)
    - Load the file and restart your kernel to ensure the new function is loaded to Python.
        - You can check this by typing help(lbs_to_kg) to make sure everything is working.
    - Recreate the examples in the function help file `help(lbs_to_kg)` to ensure everything is working correctly.
    
<h5>Here's what our completed function looks like:</h5><br>

Filename: lbs_to_kg.py
***
def lbs_to_kg(lbs)<br>
        ''' (number) -> (number)<br><br>
        Return the number of kilograms equivalent to the input parameter pounds (lbs).<br><br>
        \>>> lbs_to_kg(2.2)<br>
        1<br>
        \>>> lbs_to_kg(100)<br>
        45.36<br>
        '''<br><br>
        return lbs / 2.205
***
*References

Coursera Function Design Recipe - [Link](https://d18ky98rnyall9.cloudfront.net/_96168b6c868aaef1d7f57b6f4a7b0b03_designrecipe.html?Expires=1545264000&Signature=Ezo-CSNHqxbb8ZTV7ayNqkZzwBzqQHmGTLPhPi5eylik8mReyYhlk0MvNnSoF8kF5EOgTm8itHqZ~o9JNzczcHTqCi~45Dam8w5tYfvdPvnUUSETfCFoR~kt8HVWURqnnMWJnHDz9KIJovlQTbOI64oKG4s8Kfylsh-~WnlRIPo_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A)<br>
University of Toronto Function Design - [Link](http://www.cs.toronto.edu/~ahchinaei/teaching/20165/csc148/function_design_recipe.pdf)<br>
How to Think Like a Computer Scientist: Learning with Python - [Link](http://openbookproject.net/thinkcs/python/english2e/ch03.html)<br>
