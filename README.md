# .gitinclude
During the process of development, I have found that directories are often litered with extraneous files from the build system or IDE,
to the point that it is easier to specify which files and directories should be included in a
git respository rather than specifying those which should be ignored. Unfortunately, git does not examine folders and files which it has been told to ignore.
As a result, gitignore rules which ignore everything in a directory and then attempt to include files in subdirectories fail to behave as one might expect.
To achieve the desired behaviour, I find myself ignoring everything in the root directory, then include a directory, then ignore everything in that
directory, etc. Using an ordered dictionary, this command line application automates this pattern, generating .gitignore files from a list of
directories and a collection of regex which to include.

## Structure of .gitignore
.gitinclude files are structured similarly to .gitignore files. A line in a .gitinclude file specifies the directory and file types to include.
```
# Sample .gitinclude entry ignoring all files and directories
# except those necessary to include files matching *.py, *.cpp
# or sample in /sample/path/to/directory/

/sample/path/to/directory/ [*.py, *.cpp, sample]
```
All file paths are taken relative to repository root, so if the above .gitinclude file is in a git repository at
/this/is/git/root/, then files will be included in /this/is/git/root/sample/path/to/directory/.
