# Wunderlist2Joplin
 A python script to prepare the Wunderlist data for import into Joplin

The Wunderlist:registered: system gets shutdown and most of the people will migrate to Microsoft:registered:'s ToDo:tm:. That is O.K., but some of You might consider this as a point in time where You want to migrate the data to Your own cloud system. Since Joplin provides (at least for me) all the relevant features I came to the conclusion to go this way. The only problem was that I didn't want to loose all the data. Hence I investigated how to import the data and didn't find much. Hence I came up with the following (non-complete) solution:

* Get Yourself (unless You have it already) python3 and install it. Example:

  https://www.anaconda.com/distribution/
  
  I used Version 3.7.
* Download this repository and unzip it. Remember the folder. 
  Example: 'c:\Users\<Username>\Wunderlist2Joplin'
* Go to the wunderlist page to export all Your data (see how well organized Wunderlist is and I appreciate taht Microsoft as owner of Wunderlist provides this remarkable service):

  https://export.wunderlist.com

  By this You will get a zip-file for download which You can unzip to somewhere in Your system.
  In this folder You will find the file "Tasks.json". Enter the full path in the line 13 of the script c:\Users\<Username>\Wunderlist2Joplin\Wunderlist2Joplin.py.

* Create an empty folder somewhere on Your system. Enter the location in line 15 of the script c:\Users\<Username>\Wunderlist2Joplin\Wunderlist2Joplin.py.

* Execute the script by opening a command window and typing
  c: <Ret>
  cd  c:\Users\<Username>\Wunderlist2Joplin<Ret>
  python Wunderlist2Joplin<Ret>

* Open Joplin and choose File->Import->Raw Joplin Export Folder
  Wait for the import to finish.


**Remark:**
The import is incomplete and not all data of the Wunderlist can be imported by the script. Esp. attachments are not handled. Also not all useful fields of Joplin are filled since the data might not be available or I didn't take care.

Also there is no gurantee for useability or fittness or correcness of the result.

**Remark:**
The script should also work on Linux or MacOSX. It is not dependend on Windows in any way known to me. 

Enjoy.
