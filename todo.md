# TODO
- split into stacklog object, module interface, and parallel packages
- maybe the module interface can be DRY by using some metaprogramming (decorator?) to automatically generate the module interface?
- python 2 and 3 support from the start?
- test python 2 and 3 with tox? (virtual environments?)
- is having an `src` file the right way to go?
- set an initialization option to use OrderedDicts or just regular dictionaries
- a separate module for pretty printing and matplotlib display
- where to put tests? do i include them in the installed package?

- do i really need a stack? or can I hold some of this information locally? (basically, use the implicit python stack)
- can i make a stacklog decorator that would properly decorate unittest functions? i suppose i would need to make sure that all the function metadata
is maintained (specifically the 'test' prefix in the name). this could be
great because then I'd know exactly how long each test took


- tox
- python 3 support?
- how to handle global state?
- use nose, pytest, or something else for testing?
