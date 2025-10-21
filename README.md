# Producer-Consumer 💫✨

An implementation of the producer consumer problem in _Operating Systems_ using `semaphores`, **socket programming**, `XML` files, and `Object-Oriented Programming`.

## Producer

The producer produces data on _student information_ and stores the data on the ``ITstudent`` class. The class has these member variables.

- Student name
- Student ID (8 digits)
- Programme
- List of courses and related marks

**_Wrap the student information into an XML format_**. Place the file in the **_same directory it shares with the buffer_**. At the same time, **_insert an integer_**, on the buffer/queue, that corresponds to the file name. For example, if the file name is student1.xml, place 1 in the buffer.

## Consumer

The consumer reads the content of the XML file from the buffer; unwraps the XML file and gather the student information into the `ITstudent` class. At the same time, it should clear/delete the file and remove teh integer from the buffer.

- On `ITstudent`, the consumer should calculate the average mark based on teh allocated marks for all courses and then determine if the student passed or failed, given that the passing mark is 50%.
- Print on standard output
  - Student name
  - Student ID
  - Programme
  - Courses and associated marks
  - Average Mark
  - Pass or fail status

## Buffer

This is a `bounded buffer` problem given that it has a maximum size of 10 elements. That is, in the shared folder, we need to have 10 files and each file should have an associated number of the buffer.

The rules for accessing the buffer are:

1. The producer should not producer if the buffer if full
2. The consumer should not consume if hte buffer is empty
3. Buffer access should be mutually exclusive (one process at a time)

### Note

- Use `mutext/semaphores` to ensure buffer rules are enforced, especially the mutual exclusive one.
- Use `socket programming` to implement the producer and consumer problem.
