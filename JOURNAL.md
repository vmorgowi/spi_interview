Journal file per specifications in test instructions.


### 6:00pm - Initial Specifications Analysis
Overall project seems divided into two main parts: a UI front end for artists to display and update tasks, and a server back end to store data and be queried when the UI needs to update.

Building a server and especially a web app is fiddly. I'll focus on the front end, as that is where my expertise is. In theory, a front end mock up could also be displayed to artists for testing and feedback even if the server backing it is completely fake.

I'll be writing the app in Python, as speed of dev implementation is far more important than runtime efficiency of something like C++. Easier to get a Python environment set up on my personal laptop as well.

I am not familiar with free coding agents. My former company used Claude, so I will first investigate its free version. Ideally, I would like it to generate a basic template for a window that displays a list of rectangle widgets for tasks which I can then modify from there.

I will need to explain my code at a follow up interview, so using genAI for complex aspects of the project is a bad idea. I've also heard that free AI agents very quickly run out of tokens on complex coding tasks, so I may not be able to rely on it much at all.


### 6:40pm - Basic Environment Up

Got everything set up for a basic dev environment and made an account for free Claude.

As expected, Claude added a lot of unasked for details. It generated sample data and quite a lot of styling for the QWidgets for the tasks. But this may be a good starting point; while the further suggestions of Click-to-edit and the ability sort ascending/descending are useful, I want to be sure I fully understand the code it gave me before I ask for bells and whistles.

Running the raw generated app also revealed some expected problems. The window is too small for the size of the cards and the fonts it chose.

I'll commit what it gave me as a first pass. Second pass will be fixing the sizing, manually modifying the style, and adjusting the Status values to better match the specification as a way to see if I am understanding it all correctly.


### 7:00pm Tweaking Generated Code

Decided to add in the Priority field as another test. The question is: should it be integers, or a defined set of strings/enums? Integers that the artists can modify themselves could allow them to create their own custom sortings, which might be handy. On the other hand, the production systems I've worked with used set definitions.

I'll go with set definitions for simplicity, but this might be interesting to return to if I had more time and the ability to ask artists for what they prefer.

### 7:30pm - A few problems
Ah, already discovered another issue. Claude organized the labels in a grid. I probably would have used something more flexible.

Adding in the priority label is proving difficult due to the inflexible formatting. I'd like it to look nicer, but I need to move on to more important things (like getting minimum functionality like adding notes) now. If I have time, I'll come back to it.

Would have been fun to color code the styling on it too...


### 8:00pm - How to re-integrate genAI...

Asked Claude to add persistent data storage via loading/saving a JSON file, plus click-to-edit on the status field. Of course, since I wasn't able to have it run on my modified version, I'll need to hand integrate its changes.

That will take a while... but it will mean I understand those changes once I'm done.

Raw generated code again had styling issues on the new edit dialog, so I'll need to fix those too.

I wonder if I should change the way the Statuses are kept track of. Claude loves its arrays of strings. In theory, they should actually be an enum. Or possibly a struct that keeps track of the associated color too. But, is it worth the time taken to neaten up the code to do that? Probably not, as much as it pains me to look at it...