# Adapted from Rachel Tatman's example
# https://www.kaggle.com/code/rtatman/time-aligned-spectrograms-with-chat-files-in-r/notebook

# load in libraries we'll use
library(stringr) # string manipulation
library(tidyverse) # keepin' it tidy

# read in a CHAT transcript
transcript <- paste(readLines("326.cha"))

# \025 is the non-printing character surrounding the time stamps at the end of each line
# we can use regex & this character to get a list of time spans & their transcriptions
# That's decimal 21, octal 25 (NAK or ctl-U).

# create an empty tibble
timestamps <- tibble(talker = character(),
                     speech = character(), 
                     start = integer(), 
                     end = integer())

# if a line has two of the non-breaking characters in it, grab the text & time stamps 
# for the beginning & end of the text
for(i in 1:length(transcript)){
  if(grepl("\025.*\025", transcript[i])){
    extract <- str_match(transcript[i], "\\*(.*?):(.*?)\025(.*?)_(.*?)\025")
    timestamps <- add_row(timestamps, 
                          talker = extract[2],
                          speech = extract[3], 
                          start = as.numeric(extract[4]), 
                          end = as.numeric(extract[5]))
  }
}

# These next steps are optional but will make our final output a little
# bit easier to read. Skip them for close phoneitc analysis.

# remove rows with NA's
# timestamps <- timestamps[complete.cases(timestamps),]

# remove annotations
# timestamps$speech <- str_replace_all(timestamps$speech, "&=[a-z]+", "")

# get rid of punctuation (except for apostrophes)
# timestamps$speech <- str_replace_all(timestamps$speech, "[^[:alpha:]' ]", "")

# check out our file to make sure it looks ok
# head(timestamps)
