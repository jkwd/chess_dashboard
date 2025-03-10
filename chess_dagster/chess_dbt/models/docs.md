{% docs url %}
The url of the game in chess.com
{% enddocs %}

{% docs pgn %}
PGN (short for Portable Game Notation) is the standard format for recording a game in a text file that is processible by computers. The PGN also stores other information like the names of the players, the place where the game was played, the time control, the players' ratings, the game's result, and so on. Therefore, you can think of it as a chess score sheet that computers can read.
{% enddocs %}

{% docs time_control %}
The game time in seconds
{% enddocs %}

{% docs end_time %}
The timestamp in which the game ended
{% enddocs %}

{% docs rated %}
Flag to indicate if the game is rated which impacts the elo rating
{% enddocs %}

{% docs accuracies__white %}
The overall game accuracy for white calculated by chess.com
{% enddocs %}

{% docs accuracies__black %}
The overall game accuracy for black calculated by chess.com
{% enddocs %}

{% docs uuid %}
The chess game unique id
{% enddocs %}

{% docs initial_setup %}
The initial chess board pieces setup
{% enddocs %}

{% docs fen %}
The pieces final position when the game ended
{% enddocs %}

{% docs time_class %}
Ratings-group speed of the game. Possible values are: "daily", "rapid", "blitz", "bullet".
{% enddocs %}

{% docs rules %}
To indicate chess-variant play. Possible values are: "chess", "chess960", "bughouse", "kingofthehill", "threecheck", "crazyhouse"
{% enddocs %}

{% docs white__rating %}
The player white's rating after the game finished
{% enddocs %}

{% docs white__result %}
The result of player white. E.g. win/checkmated/etc.
{% enddocs %}

{% docs white__aid %}
API url to player white.
{% enddocs %}

{% docs white__username %}
Username of player white.
{% enddocs %}

{% docs white__uuid %}
Unique identifier of player white
{% enddocs %}

{% docs black__rating %}
The player black's rating after the game finished
{% enddocs %}

{% docs black__result %}
The result of player black. E.g. win/checkmated/etc.
{% enddocs %}

{% docs black__aid %}
API url to player black.
{% enddocs %}

{% docs black__username %}
Username of player black.
{% enddocs %}

{% docs black__uuid %}
Unique identifier of player black
{% enddocs %}