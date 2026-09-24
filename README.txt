"""
Rocket League Tracker V1

Requirement to use the tracker :
  Python : 3.11 or more
  PyQt6 : 6.6.1 or more
  websockets : 16.0 or more
  curl_cffi : 0.15.0 or more

To install a module : pip install 'module name'

When you've download module and script, you need to change the file named : "DefaultStatsAPI.txt" in your game files.
Change the PacketSendRate to 30. 
After that, save the modification.
You can make a shortcut of the .bash on your desktop to lunch the tracker easily.
When the you lunch the .bash write your in-game pseudo.

Now you can start the game and enjoy the tracker.

Often issues :
-  If the tracker doesn't find the rank, it's because of the Tracker Network API.
-  Sometime, players aren't in the database of Tracker Network
-  If the tracker doesn't work, look at the WebPort number in the "DefaultStatsAPI.txt" and replace in the api.py the URI : "ws://127.0.0.1:{WebPortnumber}"

"""
