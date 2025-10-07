# spotifyapp
spicetify APP


Introduction
This app is a copy of Spotify. In this app, songs are posted by singers, and normal users listen to those songs.


Authentication For This App.
  Registration:
               1 When the AHK is registered, it will provide data in which the app will have only two users.(Singer,Normal user).
               2 When the user registers, a welcome message will be sent to their email.
               3 In the app, the username and email are being used outside through AHK.If they are used twice, an error will appear saying:This email or username already exists in the database.
               4 If the user enters the same password in Password 1 and Password 2, it will be accepted.But if the user enters them incorrectly (they don’t match), this message will appear:"Passwords do not match."
  Login:
               1 When the user provides their email and password, their profile data will also be retrieved, along with a token.
               2 If the user enters the wrong email, the message will appear:"Invalid email".
               3 If the user enters the wrong password, the message will appear:"Invalid password"


  logout:
               1 In user authentication, the user will provide a token, and in the body, they will send their email and password.
               2 Will all access end when the token expires.

  Reset_password:
               1 When we do a password reset, we have to put the correct email in the body. The message will be: 'success': 'We have sent you a link to reset your password'
               2 If the user enters an incorrect email, this statement will appear: No user found with this email address. 

  Reset_confirm:
               1 When we change the password, an email is sent that contains a token. We copy that token and paste it into the body of the reset_confirm path. In the body, we include the email, token, and new password. Then the message will appear: Password has been reset successfully.
               2 If we paste a previous token, it will display: Invalid or expired token.

  Check Profile:
               1 A user can check their profile. When the user is logged in, they will pass the token in the authentication, and the profile data will be displayed.
               2 {"id", "email", "profile_image", "total_albums", "album_song", "without_album_song", "total_songs", "Follow_count", "Unfollow_count"}


  Created Album:
                1 Only the user who is a singer can create an album.
                2 If a singer has already created an album named 'ABC' and tries to create another one with the same name, the statement will appear: You already have an album with this name.
                3 If a normal user tries to create an album, the statement will appear: You do not have permission to perform this action.
                4 A singer can only access their own album, not another singer’s album.
                5 Only a normal user can like or unlike the album.
                6 If singers are not allowed to like or dislike albums, the English statement would be:Singers cannot like albums.
                7 Scenario:
                          A singer has created 5 albums (say Album 1 to Album 5).
                          A normal user tries to like Album 10, which does not exist.
                           Resulting message: "detail": "Album not found" 
Created song:
                1 Only a singer can post a song. They can choose to post it without an album, or, if they want, with an album.
                2 If a singer wants to post a song, they can post it in their album.
                3 A singer cannot post a song to another singer’s album.You cannot add a song to another singer's album.
                4 Only singers can post songs. You do not have permission to perform this action.You do not have permission to perform this action.
                5 Normal users have view-only access to all data.
                6 Users do not have permission to add or delete songs.
                7 Search functionality for songs, albums, and singer.

Created Playlist:
                1 Only a normal user can create a playlist.
                2 if singer crated to playlist (Only normal users can create playlists.)
                3 Songs can only be liked or unliked by normal users.
                4 if user put the wrong tha playlist output Playlist not found.
                5 if user put the wrong the song output Song not found.
                6 A normal user can add and remove albums.
                7 If a normal user provides the wrong album, it will show Album not found.
                8 If a normal user provides the wrong playlist, it will show "Playlist not found."




               
  