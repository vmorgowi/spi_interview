# spi_interview
Coding Test for Sony Pictures Imageworks interview

## Running the application

Application depends on on PyQt5.

To Run:
```
    pip install PyQt5
    python production_tracker.py
```

## My Approach

### Architecture and Technologies

This application is a PyQt front end to display data loaded from a JSON file, built with assistance from the free version of Claude. Ultimately, my decision to use Python, PyQt, JSON, and Claude was primarily due to the importance of speed of implementation and my familiarity with these specific technologies. For more detail, see [Initial Specifications Analysis](./JOURNAL.md#6:00pm_-_Initial_Specifications_Analysis) in the Journal.

All code is contained in `production_tracker.py`. The main application is `MainWindow` (a QMainWindow), which contains a list of `TaskItemWidgets` (QFrames). There is also a small QDialog (`EditTaskDialog`) used to modify the underlying `TaskItem` data class.

### Artist Experience

The tool allows the artist to select their name to view a list of tasks assigned to them. The tasks can be ordered by Due Date, Status, and Priority. The artist can then click on a task item in order to update its Status or add Notes.

### Assumptions
* A valid JSON file with Task data exists; the application includes fallback data in case the JSON file is malformed, but fallback data would be of little practical use to an artist.
* The user is an artist whose name is included in at least one entry in the JSON file.
* The user prefers to have Due Date, Status, and Priority sorted in ascending order.
* The default size values for the UI both fit the data and will not need to be adjusted by the user.

### Tradeoffs
* Simplicity over extraneous functionality: The UI is extremely bare bones, as the more vibe-coded additions get made, the more difficult it would be to debug and modify the code.
* Function over form: The UI layout is not especially nice to look at; achieving minimal functionality of viewing/changing the underlying data was more important.
* Function over efficiency: Python is not the most fast or performant language, and I did not have a chance to add optimizations to improve how the data is handled. Again, achieving minimal functionality was more important.

### Limitations
* The underlying data file for this application is completely local and static. A real production database would likely need a central server for which this tool would be a client.
* The UI relies on many hardcoded values; real users would likely want to be able to resize it and sort, filter, and view the data in more flexible ways.
* The code is not optimized to handle data especially efficiently, and may not scale well for realistic numbers of users or tasks.
* No tests were written for the application or data. 
* The code has not been user-tested and therefore it is unknown if it would truly meet artists' needs.

### With More Time
In order of priority:
1. Ability to switch between ascending/descending sort orders
2. Task filtering in addition to task sorting (e.g. filter by Project, Shot, Status, Priority)
3. Better handling and display for long Notes
4. Resize UI components to fit the data and the window (rather than being hardcoded estimates)
5. Improve input of artist name to be more scalable to large numbers of artists
6. Create a mock server and turn this into a client front end (if I had a LOT more time)
7. Polish the UI and consolidate style sheets

### Time Taken
* 1 hour for environment setup
* 5 hours for coding
* 2 hours to write README & AI_Account
* 30 minutes to set up and record demo video


