# Design choices

## What is an MVC architecture and why follow it?
MVC stands for Model-View-Controller. It basically separates the internal or business logic,
the display of messages/graphical components destined to the user, and the handling of user requests.

In this case the model is inside the `model` package, and contains classes representing mods, games, dependencies,
installations and such. All they do is provide metadata.
Then there is the `view` package which contains classes and functions used to print messages or format outputs in the
terminal for the user to see.
The `controller` package contains the handlers for each command, it requests data from the model, operates on it, then
display information to the user using the `view`.

I chosed to rewrite this application and follow an MVC architecture because it reminded me of a web application.
Commands can be seen as routes, and therefore each command has its corresponding controller. This also allows to export
the model in the future for another rewrite or the making of a similar application in another language, using other
frameworks etc.

## Why make the session an attribute of the application?
From the [official SQLAlchemy documentation](https://docs.sqlalchemy.org/en/14/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it):
> For a command-line script, the application would create a single,
> global `Session` that is established when the program begins to do its work,
> and commits it right as the program is completing its task.

If the application ever got adapted into a GUI application, this would follow another pattern.
