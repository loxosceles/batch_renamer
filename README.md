# Batch Renamer

## Update file names recursively based on keywords

### Description
Batch Renamer will descend from the given path into the file hirarchy and find every
ocurrence for the search pattern. It will only look for full strings, not substrings.
#### Example
    Search pattern: Niño
    Will find:      Niño, Niño3, 3Niño, 3Niño3, -Niño-, !Niño?, etc
    Will not find:  aNiño, Niños, niño, etc 

### Command Line Usage
#### Example
    batch_renamer SEARCH_PATTERN REPLACE_PATTERN PATH

### Interactive Usage
In interactive mode the program will ask for *keyword* (seach pattern), *keyword replace* and
*path*.


