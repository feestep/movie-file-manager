
import os, re, shutil

# Define regular expressions to find file type, movie year, and movie quality
typeRegex = re.compile(r'(\.\w{3})$')
yearRegex = re.compile(r'[\(\[]?(19|20)\d\d[\)\]]?')
qualityRegex = re.compile(r'[\(\[]?\d{3,4}p[\)\]]?')

# Define a string of the characters we want to remove from the title
wordBreakCharacters = '._-:()[]'

movieFolderAddress = r'F:\Media\Movies'
#movieFolderAddress = r'E:\Test' # Temporary for testing

# Loop through all movie files/folders in the directory
for movie in os.listdir(movieFolderAddress):
    # Check if the movie is a folder or a file
    fileType = typeRegex.search(movie)
    if fileType: # Evaluates to true if file extension found - i.e. not a folder
        spacedMovie = re.split(typeRegex, movie)[0] # Remove the file extension
    else:
        spacedMovie = movie
        
    # Replace word break characters with spaces
    for character in wordBreakCharacters:
        spacedMovie = spacedMovie.replace(character, ' ')
    
    # Empty string to start building the new folder name on
    newFolderName = ''

    # -----Get info for renaming the folder-----
    year = yearRegex.search(spacedMovie)
    if year: # Evaluates to true only if a year was found
        splitYear = re.split(yearRegex, spacedMovie)
        title = splitYear[0].strip()
        quality = qualityRegex.search(splitYear[2])
    else:# If no year was found
        quality = qualityRegex.search(spacedMovie)
        if quality:
            title = re.split(qualityRegex, spacedMovie)[0].strip()
        else:
            title = spacedMovie

    # Form the new folder name
    newFolderName += title # They all have a title
    if year: # But not all have a year
        newFolderName += f' ({year[0]})'
    if quality: # And not all have a quality
        newFolderName += f' [{quality[0]}]'
    
    # If no change to the name, skip to the next folder
    if newFolderName == movie.replace('-', ' '):
        continue
    
    # Otherwise, print the old and new folder names
    print(f'Old Name: {movie}\nNew Name: {newFolderName}\n')

    # Then ask the user to accept the new name or enter their own
    response = input('''To rename/create folder using the new name provided, press enter.
To keep the current folder name, enter 'y'.
Otherwise, manually enter desired folder name:\n''')
    
    # Get path for old folder/file
    oldPath = os.path.join(movieFolderAddress, movie)
    
    if response == 'y': # If the user enters 'y', continue to the next file/folder
        continue
    elif response: # If the user gave a different folder name, use it to rename the folder
        newPath = os.path.join(movieFolderAddress, response)
    else: # Otherwise, use the generated name
        newPath = os.path.join(movieFolderAddress, newFolderName)
    
    if fileType: # If the movie is a file, create the folder we want and move it to it
        os.mkdir(newPath)
        shutil.move(oldPath, newPath)
    else: # If it is a folder, we can just go ahead and move (rename) it to the new path
        shutil.move(oldPath, newPath)
