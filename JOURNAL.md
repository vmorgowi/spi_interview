Journal file per specifications in test instructions.


### 6:00pm - Initial Specifications Analysis
Overall project seems divided into two main parts: a UI front end for artists to display and update tasks, and a server back end to store data and be queried when the UI needs to update.

Building a server and especially a web app is fiddly. I'll focus on the front end, as that is where my expertise is. In theory, a front end mock up could also be displayed to artists for testing and feedback even if the server backing it is completely fake.

I'll be writing the app in Python, as speed of dev implementation is far more important than runtime efficiency of something like C++. Easier to get a Python environment set up on my personal laptop as well.

I am not familiar with free coding agents. My former company used Claude, so I will first investigate its free version. Ideally, I would like it to generate a basic template for a window that displays a list of rectangle widgets for tasks which I can then modify from there.

I will need to explain my code at a follow up interview, so using genAI for complex aspects of the project is a bad idea. I've also heard that free AI agents very quickly run out of tokens on complex coding tasks, so I may not be able to rely on it much at all.


### 6:40pm - Basic Environment Up

Got everything set up for a basic dev environment and made an account for free Claude. I'll try using the Sonnet 5 Medium setting.

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

### 8:30pm - Adventures in Editing

Having the combo box on the edit dialog reflect the same colors as on the rest of the UI is another unnecessary flourish, but it seems like a good thing to try to make sure I understand how these style sheets are working.

Whew, good thing I thought to test sorting after I integrated the edit dialog. Discovered a bug where "Review" and "Complete" were both set to the same order value! Fixed now.

I want to adjust the styling on the edit dialog since the OK/Cancel buttons are so hard to read. Which brings up another code cleanliness issue - ideally there should be one style sheet or at the very least a main palette the others could grab colors from to keep things consistent... yet another thing I would do if I had time.

### 9:00pm Colors and Comboboxes

Finally managed to change the individual colors in the drop down of the combo box. But the color of the non-drop down part doesn't update afterwards. Ah well. I feel like I learned something while doing this, at least.

And with that, ready for the second check in. What major pieces remain?
>Limiting the display to only show tasks belonging to a specific artist
>Adding the Project and Shot fields
>Adding a Notes field
>Adding a way for the artist to edit Notes

The Project and Shot fields will be straightforward to add. I'll do that manually myself. For limiting the display, let's see if Claude can successfully add a search/filter bar.

### 9:30pm - More AI integration

Realized that once I added the Project and Shot fields, I'd have to update all that sample data. Used a separate session of Claude to generate the new JSON instead. Following a predictable pattern is what LLMs are best at, after all.

I'll do a few fallback samples by hand just to have a clear example in the program itself.

Also had Claude add a notes field on the version it's working with. I want to test to see if it can sanitize the input. Theoretically, allowing an artist to stylize the notes might be interesting. But given that "error and failure handling" and "edge cases" are part of the judgement criteria, better to play it boring but safer.

### 10:00pm - Not Done Yet

The editable, sanitized Notes field is ready for check in, at least. Unfortunately, I haven't had time to thoroughly test its output. Claude wants me to add more bells and whistles like showing the full notes text on hover. Sounds lovely, but...

Given that I started at 6pm, this should be the cut off, but I haven't yet met the minimum requirements. 

The main piece remaining is being able to limit the display to just showing tasks for a specific artist. Once I have that, I feel it will be minimally functional. I'll see what I can do in the next hour, and probably call it after that.

### 11:00pm Almost There

Artist filter is now working, but I need better sample data to test it. Would also be nice to test more examples with missing notes.

I also noticed an unfortunate bug - the drop down for artists chokes and fails to display the name of an artist with a non-ASCII character in his name. That's important to fix - it would be very disrespectful to an artist if their name could not display correctly!