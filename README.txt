Charles Hodgens
10/17/2013

This set of scripts takes annotated data regarding images and makes mosaic images. Each of the scripts relies on implicit delimiters in the metadata. Prepare your metadata file in excel, then export to a tab-separated text file.

Make sure that there is a line break between every set of images you want graphed sequentially horizontally. For example, to get all images of one colony's time course, make sure those images and only those images are grouped together with a line break above and below the group. Make sure the Top->Bottom order matches the desired Left->Right order.

Then, run colony_poster_implicit.py on the individual images.

Repeat the grouping and sorting on the files you get out, grouping them into things you want organized vertically. Run vert_tile.py.

See the individual python script files for more detailed expectations regarding formatting and expected input.


Usage Workflow

Go to the folder with your images
get a text file with the contents of your folder
[dir > dir.txt]
do a search and replace and some manual cutting to get just your imagenames
a search for [^.*DSC] with a replacement for [DSC] cuts out all the nonsense before the actual imagename
copy the filenames into a template excel document and curate the data
split up the files with a linebreak between sets you want graphed together.
run colony_poster_implicit

do the above steps again, only instead of copying into a template file, copy into two columns
split the second column by the delimiter [;]
sort to your desired groupings

run vert_tile