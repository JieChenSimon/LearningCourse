we are looking at the fuzzing techniques that use information from the program in order to guide the input generation process towards specific features. one of these features that we are looking into today that help fuzzers be guides towards specific programming features is **code coverage**.  **coverage means that we are tracking which parts of a program are actually executed during a test run**.

so if we have a small program for instance and we know some specific parts  have not been executed yet then we typically want to test them because if a line of code is not executed at all during testing, then this means that any bug that may still be in there.

and we want of course our tests to execute every single line of code because if they do not execute this code then there is no chance for the test generator for the fuzzer to find any bugs in there either. 

So achieving a high amount of coverage covering as many features of the program as possible is important and these features typically are lines in the program, but can also be more advanced features, such as branches in the program or pairs of function functions calling each other there's a great.