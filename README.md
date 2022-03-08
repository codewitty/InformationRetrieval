ABOUT
-------------------------
This is the base implementation of a full search engine.


USAGE
-------------------------

**ARGS**

*directory*:

The input folder containing all the sub-folders with the json files.

*output_directory*:

This is the directory that contains the partial indexes before the merging

*query_directory*:

This is the directory that contains the final split index that is used for searches.

Users can then interact with the UI to run their queries.


EXECUTION
-------------------------

To execute the search engine execute the script indexer.py from the command line as follows:
```python3 indexer.py directory output_directory query_directory```

The function builds the inverted_index and displays the count of documents as a visual feedback for the user. Once the index is built, the program asks the user to input their search term and delivers the results to the user.
