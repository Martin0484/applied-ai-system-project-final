My original project was applied-ai-music-application
It's original goal was to recommend multiple songs based on attributes like genre. It could provide a number
between 0 and 1 for each song that represents how good of a match that song is.

My project adds a reliability check to the original project, which helps increase the accuracy of output.

Input goes into the CSV file or User Prefs. Afterwards, the values are utilized in the load_songs() and
score_song() methods. The numbers returned by the score_song method are utilized in the recommend_songs()
method to create an array of songs with the number. Each song is associated with a number
between 1 and 0, and reasons for the score. An array of songs with their number and reasons are returned
by the recommend_songs() method and printed to the screen. The output is checked by a human to see if
it makes sense.

Instruction to run the code:
1. From the project root, run "python3 -m src.main" in the terminal
2. Type the song genre you are looking for
3. Type the song mood you are looking for

Sample Output 1:

All reliability tests passed.

Available genres: ambient, folk, indie pop, jazz, lofi, pop, rock, synthwave
Enter a genre: folk
Available moods: chill, focused, happy, intense, moody, relaxed
Enter a mood: chill

Top recommendations:

Midnight Coding - Score: 0.77
Because: mood match (+0.25), energy similarity (+0.28), tempo_bpm similarity (+0.07), valence similarity (+0.09), danceability similarity (+0.04), acousticness similarity (+0.04)

Moonlit Pages - Score: 0.75
Because: mood match (+0.25), energy similarity (+0.26), tempo_bpm similarity (+0.08), valence similarity (+0.08), danceability similarity (+0.05), acousticness similarity (+0.03)

Library Rain - Score: 0.74
Because: mood match (+0.25), energy similarity (+0.26), tempo_bpm similarity (+0.07), valence similarity (+0.09), danceability similarity (+0.05), acousticness similarity (+0.03)

Cloud Atlas Drift - Score: 0.70
Because: mood match (+0.25), energy similarity (+0.23), tempo_bpm similarity (+0.06), valence similarity (+0.09), danceability similarity (+0.05), acousticness similarity (+0.03)

Spacewalk Thoughts - Score: 0.70
Because: mood match (+0.25), energy similarity (+0.23), tempo_bpm similarity (+0.06), valence similarity (+0.09), danceability similarity (+0.05), acousticness similarity (+0.03)

Sample Output 2:

All reliability tests passed.

Available genres: ambient, folk, indie pop, jazz, lofi, pop, rock, synthwave
Enter a genre: ambient
Available moods: chill, focused, happy, intense, moody, relaxed
Enter a mood: happy

Top recommendations:

Golden Hour Ride - Score: 0.72
Because: mood match (+0.25), energy similarity (+0.23), tempo_bpm similarity (+0.10), valence similarity (+0.07), danceability similarity (+0.03), acousticness similarity (+0.04)

Rooftop Lights - Score: 0.71
Because: mood match (+0.25), energy similarity (+0.22), tempo_bpm similarity (+0.10), valence similarity (+0.07), danceability similarity (+0.03), acousticness similarity (+0.04)

Sunrise City - Score: 0.69
Because: mood match (+0.25), energy similarity (+0.20), tempo_bpm similarity (+0.10), valence similarity (+0.07), danceability similarity (+0.04), acousticness similarity (+0.03)

Cloud Atlas Drift - Score: 0.60
Because: genre match (+0.15), energy similarity (+0.23), tempo_bpm similarity (+0.06), valence similarity (+0.09), danceability similarity (+0.05), acousticness similarity (+0.03)

Spacewalk Thoughts - Score: 0.60
Because: genre match (+0.15), energy similarity (+0.23), tempo_bpm similarity (+0.06), valence similarity (+0.09), danceability similarity (+0.05), acousticness similarity (+0.03)

I built it this way to give the user freedom to control the input. One trade-off is that I had to increase
the runtime of the program by adding more methods to main.py in order to allow the user to control input.

What worked is that I managed to provide a well-calculated score for each song. What didn't work was the
program not working when the user provided an invalid genre or mood, which had to be fixed. That made
me learn the importance of input validation.

This project taught me that AI is flawed but can be improved with human observation

I tested the AI's reliability by reviewing it's output. By looking at the numbers associated with each song
attribute, I could tell whether the song was being matched too closely or not closely enough. 

One limitation of my system is that it does not let the user search songs of a genre that is not recognized
by the code. The size of the database can also be quite limited.

While testing my AI's reliability, I was surprised that it provided reliable answers for various inputs.

AI gave me a helpful suggestion by telling me to incorporate a reliability check in the main.py file.
However, it also gave me a flawed suggestion by telling me to structure the code in a way that makes it
difficult to read.

This project shows that I have gained alot of experience with AI and have found very useful ways of
utilizing it. It also shows that I am now capable of applying my experience to create a useful
program that can make someone's life by filtering though countless songs and only displaying the
ones that would be most relevant to the user. And it gives me greater insight into the inner-workings
of AI to know how it functions at a low level.

https://www.loom.com/share/bcf82027b5334317a54a27f08d35c9f0
