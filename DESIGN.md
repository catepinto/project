The bones of this project were my CS50 Finance problem set. I cleared out components I didn’t need, such as the login/logout and register aspects. I renamed all of the functions based on what I wanted them to do, and changed the heading, navigation bar, and other miscellaneous things so that the structure matched by project’s structure.

Part 1: The Aggregated List
This was the first feature I implemented, as it was the most straightforward. I modelled it after the “history” page of the CS50 Finance pset. In ‘application.py’, the code was fairly straightforward: querying the database for all fields and passing it into the ‘resources.html’ template.

In the html file, the first thing I did was modify the variable names. Using jinja, I also added two if/else statements within my jinja for loop (for the table rows) in order to account for some resources not having websites and/or emails (otherwise they would display an invalid hyperlink). I did not use an if/else statement for the phone numbers (even though some resources don’t have one) because resources without a phone number have a “NULL” entry in the database, which automatically prints as “None” in the table.

In the database, the phone numbers are entered as 10 digit strings, with no hyphens, commas, dots, parentheses, etc. I created a filter in ‘helpers.py’ called “phone,” which I applied to all instances of a phone number throughout my website. I modelled this filter after the usd filter in CS50 Finance, which uses a format string.

The last thing I did was style the table using CSS. The same table style, design, and structure that I created and used in resources.html is used to display the results from the search filter in ‘results.html’.

Part 2: The Search Filter
One of the biggest (and most time-consuming) challenges with this portion of the project was to figure out the optimal way to store my data in a SQL database. The problem was that each resource has different tags, and the number of tags each resource has is variable. Since the maximum number of tags a resource had was five, my initial thought was to store all of the information about the resources (including name, website, phone, email, and corresponding tags) in one table in my database. I was going to create five columns for potential tags, and for resources with less than five tags, I would make the entry NULL. This unfortunately did not work because the headings for each tag had to be different, which made it inefficient and of poor design to query the database in ‘application.py’.

After consulting with my TF, I landed on a new approach. Scrapping my previous table, I created two new tables. One table was called “resources” and the other was called “tags”. The resources table contained a unique identifier (primary key) called 'resource_id' for each resource, as well as the corresponding name, website, phone number, and email address. The second database, called “tags,” had two columns, one with the tag name and the other with the 'resource_id', a foreign key from the resources table. The tag names matched the values of each checkbox assigned in ‘search.html’.

I contemplated creating a third table for the tag ids, in which case I would have assigned each tag a primary key id number ('tag_id'), and then stored the id number instead of the tag name in the tags table. My tags table would then have two foreign keys, one of 'resource_id' and other of 'tag_id'. I weighed the pros and cons, and ultimately decided against this plan for two main reasons. One, I didn’t want to have a table with two foreign keys (and wasn’t even entirely sure this was possible), and two, I wanted the values in the table to match the values that the website would get from the form submission, which were the text names.

Once I had my SQL table set up, I could then move onto creating the actual algorithm that would query my database for the best possible resources. As described in more detail in README.md, a successful search returns ‘results.html’, which includes the percent match (how successful the search was) and a list of the matches. The following is the algorithm and the steps I took to make that happen:

1. Check to make sure the user checked at least one checkbox for a filter. If the user didn’t check anything, it returns the same page (‘search.html’), this time adding a banner prompting the user to check at least one box. I accomplished this banner through a jinja if statement in ‘search.html’. When the user doesn’t check a box, ‘search.html’ gets passed the variable 'error_msg', which is a string carrying the error message. The error message only displays on ‘search.html’ when the user submits an invalid search (and not every time the page is accessed) because it is only in this situation when the page gets passed the variable 'error_msg'.

2. Turn the variables from the form (which boxes the user checked off) into a dictionary called “submission”. I made it into a dictionary because I need to be able to access the individual components, namely, the tag values.

3. Create an empty list called “filters” to eventually store the text values of which filters the user checked (i.e. “advising” or “counseling”).

4. Get the number of tags the user selected by calculating the length of the dictionary submission.

5. Iterate over each element in the dictionary submission, appending the tag name to the list filters.

6. Query the database tags for all of the rows that match the tags in the list of filters

7. This is one of the most important steps: I created an empty list called 'resource_ids' in which to store all of the 'resource_id' values found in the previous query (step 6). This list will likely have duplicate values (and that’s a good thing). For example, if I checked the boxes “Students” and “Counseling”, I would want it to return the id of “CONTACT” twice, since the resource “CONTACT” has both of those tags. I accomplished this by iterating over the results of the query from step 6 and appending just the resource_id to the list resource_ids

8. Get the number of resources currently in the database. This gives me flexibility if I later add more resources to the database, and it avoids magic numbers.

9. This is the second crucial step in my search() function: calculating the match scores of each resource. First, I create an empty list called “scores”. Then I append a 0 for each resource currently in the database. I accomplish this via a for loop, using the number I got from step 8. Once my list of 0’s is set up, I now calculate the score of each resource. What I mean by this is “how many times was the resource returned based on the filters the users selected”. Resources that were returned more often are better matches because they matched more of the filters (had more of the characteristics) that the user wanted. Iterating over my list of resource_ids, I add one “point” to the appropriate list index that corresponds with the resource_id from the database. Note that the index and the resource_id are off by a factor of 1, due to the fact that the primary keys started at 1, but the list indices start at 0. By the end of this process, I have a list of scores for each resource in chronological order (as defined by the order the resources are listed in the table).

10. Find the best score in the list. This will not necessarily be the number of tags the user selected, though in an ideal situation (i.e. 100% match), it is.

11. Create a blank list called best_resources to append the id numbers of the best-matched resources.

12. Iterate over the scores list and append the index of that score to best_resources if and only if the score is equal to the best score (the one calculated in step 10).

13. Add 1 to all the values in the 'best_resources' list (this adjusts the index to match the actual resource_id value)

14. Calculate the percent match, which is the highest score (the number of matches each resource in the final list had) divided by the number of tags the user selected, times 100. I turned this number into an int because the decimals weren’t important for my purposes, and rounding was ok.

15. Finally, I query the database for the information about the resources (name, website, phone, email) based on the resource_id numbers saved in the list best_resources. Passing those queried results into the ‘results.html’ page along with the percent match variable gives the desired information on the ‘results.html’ page as described in README.md.

Part 3: The Search Bar
This was the last component I implemented. After I had finished the first two parts, I decided that I wanted to introduce one more feature that would make the website a little bit more dynamic and also allow me to utilize my knowledge of javascript.

To get started, I went into my CS50 Mashup problem set and looked the ‘scripts.js’ file. I copied the relevant portions into a file called ‘scripts.js’ in the ‘static’ folder of my project. This included the original Mashup search() function and the configure() function. Since I already had a function called search (used in part 2), I renamed this function “search_all”, and changed it in all of the appropriate places. When I copied over the ‘application.py’  def search(), I also edited the name to “search_all” to correspond with the javascript function. The ‘scripts.js’ function search_all() remained untouched, with the exception of the name change.

The configure() function, however, was a little bit more involved. First I removed all references to the google maps API, including the listeners and the refocusing. What remained was the “configure typehead” portion, which I left unchanged, and the display function, which I had to change. I made the limit for search results that displayed three, mainly for spatial reasons (I didn’t want the results extending too far down the page). Then for the handlebars suggestion, I concatenated it such that it would display the hyperlinked name of the resource, and clicking on it would take you directly to the resource’s website.

Next, I altered ‘application.py’ search_all so that it would query the resources table in the resources database for resources that matched the user’s input. I kept the ‘%’ wildcard, but I altered the SQL query so that it would only search the “names” column of the table in attempt to find matches with the query (as opposed to searching multiple columns such as in Mashup).

The last few things I did included adding ‘$(document).ready(configure)’ to the bottom of the javascript file, copying over the relevant src’s from layout.html so that my javascript functionality would work, and removing the autofocus on the homepage away from the search box.

After the functionality was complete, I played around with the CSS, added images to the home page, changed some font styles, added and changed the colors, and so on in order to make the website aesthetically pleasing and unique.