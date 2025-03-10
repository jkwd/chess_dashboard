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

{% docs game_uuid %}
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

{% docs time_control_base %}
In chess time control there is a base time and an increment time. For example, 15|10 indicates a base of 15 mins and increment of 10 seconds per move. This column captures the base time in seconds.
{% enddocs %}


{% docs time_control_add_seconds %}
In chess time control there is a base time and an increment time. For example, 15|10 indicates a base of 15 mins and increment of 10 seconds per move. This column captures the incremental time in seconds.
{% enddocs %}

{% docs pgn_moves %}
The string of the move sequence in the entire PGN. This contains the move and the system clock timing of the move
{% enddocs %}

{% docs pgn_move_extract %}
The list of moves extracted from pgn_moves
{% enddocs %}

{% docs pgn_clock_extract %}
The list of timings of each move from pgn_moves
{% enddocs %}

{% docs pgn_move_extract_string %}
The sequence of pgn move extract in string format
{% enddocs %}

{% docs game_analysis_url %}
The link to an open source (Lichess) analysis of the game
{% enddocs %}

{% docs eco %}
Encyclopaedia of Chess Openings
{% enddocs %}

{% docs eco_url %}
Chess.com link to the given Encyclopaedia of Chess Openings
{% enddocs %}

{% docs eco_name %}
Name of the Chess Openings played in the game
{% enddocs %}

{% docs player_color %}
Color of the player of interest in the game
{% enddocs %}

{% docs player_rating %}
Rating of the player of interest in the game upon completion
{% enddocs %}

{% docs player_result %}
Result of the player of interest in the game
{% enddocs %}

{% docs opponent_rating %}
Rating of the opponent of interest in the game upon completion
{% enddocs %}

{% docs opponent_result %}
Result of the opponent of interest in the game
{% enddocs %}

{% docs is_stronger_opponent %}
Flag to indicate if the opponent is stronger
{% enddocs %}

{% docs player_wdl %}
Indicate if the player win/lost/draw the game
{% enddocs %}

{% docs player_wdl_reason %}
Explains the reason of the player's result
{% enddocs %}

{% docs game_start_date %}
Date in which the game started
{% enddocs %}

{% docs game_start_time %}
Time in which the game started
{% enddocs %}

{% docs game_start_timestamp %}
Timestamp in which the game started
{% enddocs %}

{% docs game_end_timestamp %}
Timestamp in which the game ended
{% enddocs %}

{% docs time_played_interval %}
Duration of the game played
{% enddocs %}

{% docs time_played_seconds %}
Duration of the game played in seconds
{% enddocs %}