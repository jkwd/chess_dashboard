select
    'b5d3f880-3fe6-11df-8000-000000010001' as game_uuid
    , 'rapid' as time_class
    , 1500 as time_control_base
    , 25 as time_control_add_seconds
    , cast(
        '[Event "Live Chess"]
        [Site "Chess.com"]
        [Date "2014.12.14"]
        [Round "-"]
        [White "MagnusCarlsen"]
        [Black "RainnWilson"]
        [Result "1-0"]
        [CurrentPosition "8/pp5p/1k1pN1pB/1Q1P4/3q2n1/2N5/PPP2PPP/6K1 b - -"]
        [Timezone "UTC"]
        [ECO "B06"]
        [ECOUrl "https://www.chess.com/openings/Modern-Defense-Bishop-Attack-3...d6-4.Nf3"]
        [UTCDate "2014.12.14"]
        [UTCTime "18:11:36"]
        [WhiteElo "2862"]
        [BlackElo "1200"]
        [TimeControl "1500+25"]
        [Termination "MagnusCarlsen won by checkmate"]
        [StartTime "18:11:36"]
        [EndDate "2014.12.14"]
        [EndTime "18:37:13"]
        [Link "https://www.chess.com/game/live/998800720"]

        1. e4 {[%clk 0:24:55.5]} 1... g6 {[%clk 0:24:03.5]} 2. Nf3 {[%clk 0:25:13.7]} 2... d6 {[%clk 0:23:55.1]} 3. d4 {[%clk 0:24:57.4]} 3... Bg7 {[%clk 0:24:13.6]} 4. Bc4 {[%clk 0:25:02]} 4... Bg4 {[%clk 0:24:22.4]} 5. Bxf7+ {[%clk 0:25:12.6]} 5... Kxf7 {[%clk 0:24:40.3]} 6. Ng5+ {[%clk 0:25:07.5]} 6... Ke8 {[%clk 0:24:53.8]} 7. Qxg4 {[%clk 0:24:49.9]} 7... Nh6 {[%clk 0:24:53.9]} 8. Qh3 {[%clk 0:25:05.4]} 8... Nd7 {[%clk 0:24:57.3]} 9. Ne6 {[%clk 0:25:17]} 9... Qc8 {[%clk 0:24:21.8]} 10. Nxg7+ {[%clk 0:25:35.8]} 10... Kd8 {[%clk 0:24:34.8]} 11. Ne6+ {[%clk 0:25:29.2]} 11... Ke8 {[%clk 0:24:51.9]} 12. Bxh6 {[%clk 0:25:01.9]} 12... Nf6 {[%clk 0:25:06.9]} 13. Nc3 {[%clk 0:25:11.6]} 13... Kf7 {[%clk 0:23:58]} 14. d5 {[%clk 0:25:33.1]} 14... c6 {[%clk 0:23:30.4]} 15. O-O {[%clk 0:25:50.5]} 15... cxd5 {[%clk 0:23:46.8]} 16. exd5 {[%clk 0:26:06.7]} 16... Qc4 {[%clk 0:22:18.8]} 17. Ng5+ {[%clk 0:25:59.8]} 17... Ke8 {[%clk 0:22:33.3]} 18. Qe6 {[%clk 0:26:20.3]} 18... Qg4 {[%clk 0:21:43.4]} 19. Qf7+ {[%clk 0:26:03.6]} 19... Kd7 {[%clk 0:21:58]} 20. Rae1 {[%clk 0:25:44.4]} 20... Rae8 {[%clk 0:21:51.8]} 21. Re6 {[%clk 0:25:49.2]} 21... Qd4 {[%clk 0:20:58.7]} 22. Rfe1 {[%clk 0:26:06.1]} 22... Ng4 {[%clk 0:20:26.8]} 23. Rxe7+ {[%clk 0:26:24.7]} 23... Rxe7 {[%clk 0:20:43.4]} 24. Rxe7+ {[%clk 0:26:28.9]} 24... Kc8 {[%clk 0:20:50]} 25. Re8+ {[%clk 0:26:35.4]} 25... Rxe8 {[%clk 0:21:03.5]} 26. Qxe8+ {[%clk 0:26:16]} 26... Kc7 {[%clk 0:21:21.3]} 27. Ne6+ {[%clk 0:26:03.6]} 27... Kb6 {[%clk 0:21:30]} 28. Qb5# {[%clk 0:26:01.9]} 1-0'
        as varchar
    ) as pgn
    , cast('[Event "Live Chess"]
        [Site "Chess.com"]
        [Date "2014.12.14"]
        [Round "-"]
        [White "MagnusCarlsen"]
        [Black "RainnWilson"]
        [Result "1-0"]
        [CurrentPosition "8/pp5p/1k1pN1pB/1Q1P4/3q2n1/2N5/PPP2PPP/6K1 b - -"]
        [Timezone "UTC"]
        [ECO "B06"]
        [ECOUrl "https://www.chess.com/openings/Modern-Defense-Bishop-Attack-3...d6-4.Nf3"]
        [UTCDate "2014.12.14"]
        [UTCTime "18:11:36"]
        [WhiteElo "2862"]
        [BlackElo "1200"]
        [TimeControl "1500+25"]
        [Termination "MagnusCarlsen won by checkmate"]
        [StartTime "18:11:36"]
        [EndDate "2014.12.14"]
        [EndTime "18:37:13"]
        [Link "https://www.chess.com/game/live/998800720"]' as varchar) as pgn_header
    , cast(
        '[1. e4,1... g6,
        2. Nf3,2... d6,
        3. d4,3... Bg7,
        4. Bc4,4... Bg4,
        5. Bxf7+,5... Kxf7,
        6. Ng5+,6... Ke8,
        7. Qxg4,7... Nh6,
        8. Qh3,8... Nd7,
        9. Ne6,9... Qc8,
        10. Nxg7+,10... Kd8,
        11. Ne6+,11... Ke8,
        12. Bxh6,12... Nf6,
        13. Nc3,13... Kf7,
        14. d5,14... c6,
        15. O-O,15... cxd5,
        16. exd5,16... Qc4,
        17. Ng5+,17... Ke8,
        18. Qe6,18... Qg4,
        19. Qf7+,19... Kd7,
        20. Rae1,20... Rae8,
        21. Re6,21... Qd4,
        22. Rfe1,22... Ng4,
        23. Rxe7+,23... Rxe7,
        24. Rxe7+,24... Kc8,
        25. Re8+,25... Rxe8,
        26. Qxe8+,26... Kc7,
        27. Ne6+,27... Kb6,
        28. Qb5#]' as varchar []
    ) as pgn_move_extract
    , cast(
        '[{[%clk 0:24:55.5]},{[%clk 0:24:03.5]},
        {[%clk 0:25:13.7]},{[%clk 0:23:55.1]},
        {[%clk 0:24:57.4]},{[%clk 0:24:13.6]},
        {[%clk 0:25:02]},{[%clk 0:24:22.4]},
        {[%clk 0:25:12.6]},{[%clk 0:24:40.3]},
        {[%clk 0:25:07.5]},{[%clk 0:24:53.8]},
        {[%clk 0:24:49.9]},{[%clk 0:24:53.9]},
        {[%clk 0:25:05.4]},{[%clk 0:24:57.3]},
        {[%clk 0:25:17]},{[%clk 0:24:21.8]},
        {[%clk 0:25:35.8]},{[%clk 0:24:34.8]},
        {[%clk 0:25:29.2]},{[%clk 0:24:51.9]},
        {[%clk 0:25:01.9]},{[%clk 0:25:06.9]},
        {[%clk 0:25:11.6]},{[%clk 0:23:58]},
        {[%clk 0:25:33.1]},{[%clk 0:23:30.4]},
        {[%clk 0:25:50.5]},{[%clk 0:23:46.8]},
        {[%clk 0:26:06.7]},{[%clk 0:22:18.8]},
        {[%clk 0:25:59.8]},{[%clk 0:22:33.3]},
        {[%clk 0:26:20.3]},{[%clk 0:21:43.4]},
        {[%clk 0:26:03.6]},{[%clk 0:21:58]},
        {[%clk 0:25:44.4]},{[%clk 0:21:51.8]},
        {[%clk 0:25:49.2]},{[%clk 0:20:58.7]},
        {[%clk 0:26:06.1]},{[%clk 0:20:26.8]},
        {[%clk 0:26:24.7]},{[%clk 0:20:43.4]},
        {[%clk 0:26:28.9]},{[%clk 0:20:50]},
        {[%clk 0:26:35.4]},{[%clk 0:21:03.5]},
        {[%clk 0:26:16]},{[%clk 0:21:21.3]},
        {[%clk 0:26:03.6]},{[%clk 0:21:30]},
        {[%clk 0:26:01.9]}]' as varchar []
    ) as pgn_clock_extract
