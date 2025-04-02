from chess_dbt.udf.my_custom_functions import get_checkmate_pieces_udf, pgn_to_fens_udf


def test_get_checkmate_pieces_1():
    fen = '8/8/4R2p/3P2pk/8/5r1K/3r4/8 w - -'
    player_color = 'Black'
    player_result = 'win'
    opponent_result = 'checkmated'
    expected_result = ['king', 'pawn', 'rook', 'rook']
    result = get_checkmate_pieces_udf(fen=fen,
                                  player_color=player_color,
                                  player_result=player_result,
                                  opponent_result=opponent_result)
    assert result == expected_result

def test_chess_pgn_to_fens_udf():
    # Do not indent, keep the multistring as is
    pgn = """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2014.12.14"]
[Round "-"]
[White "MagnusCarlsen"]
[Black "Tildenbeatsu"]
[Result "1-0"]
[CurrentPosition "r6k/pq3pQp/1p6/3bPN2/8/8/1PP3PP/3RR1K1 b - -"]
[Timezone "UTC"]
[ECO "C67"]
[ECOUrl "https://www.chess.com/openings/Ruy-Lopez-Opening-Berlin-lHermet-Variation-6.Bg5-Be7-7.Bxe7"]
[UTCDate "2014.12.14"]
[UTCTime "18:13:04"]
[WhiteElo "2862"]
[BlackElo "1200"]
[TimeControl "1500+25"]
[Termination "MagnusCarlsen won by checkmate"]
[StartTime "18:13:04"]
[EndDate "2014.12.14"]
[EndTime "18:56:09"]
[Link "https://www.chess.com/game/live/998802049"]

1. e4 {[%clk 0:24:57.6]} 1... e5 {[%clk 0:24:55.4]} 2. Nf3 {[%clk 0:24:58.6]} 2... Nc6 {[%clk 0:25:13.7]} 3. Bb5 {[%clk 0:24:59.8]} 3... Nf6 {[%clk 0:25:33.6]} 4. O-O {[%clk 0:25:06.3]} 4... Nxe4 {[%clk 0:25:54.7]} 5. d4 {[%clk 0:25:14]} 5... Nd6 {[%clk 0:25:45.4]} 6. Bg5 {[%clk 0:24:40.4]} 6... Be7 {[%clk 0:23:35.6]} 7. Bxe7 {[%clk 0:24:50]} 7... Nxe7 {[%clk 0:23:08]} 8. dxe5 {[%clk 0:25:03.6]} 8... Nxb5 {[%clk 0:22:06.5]} 9. a4 {[%clk 0:25:21.9]} 9... O-O {[%clk 0:21:46]} 10. axb5 {[%clk 0:25:43.4]} 10... Ng6 {[%clk 0:21:39.8]} 11. Nc3 {[%clk 0:25:56.2]} 11... b6 {[%clk 0:19:10.8]} 12. Qd5 {[%clk 0:26:12.6]} 12... c6 {[%clk 0:18:18.3]} 13. bxc6 {[%clk 0:26:08]} 13... dxc6 {[%clk 0:18:36]} 14. Qxc6 {[%clk 0:26:10.4]} 14... Be6 {[%clk 0:17:40.7]} 15. Rad1 {[%clk 0:26:22.1]} 15... Qc8 {[%clk 0:16:44]} 16. Qe4 {[%clk 0:26:35.1]} 16... Bf5 {[%clk 0:15:32.7]} 17. Qe3 {[%clk 0:26:52.2]} 17... Qb7 {[%clk 0:11:11.8]} 18. Nd4 {[%clk 0:26:53.5]} 18... Be6 {[%clk 0:09:35.8]} 19. f4 {[%clk 0:27:10.7]} 19... Bc4 {[%clk 0:08:15.1]} 20. Rfe1 {[%clk 0:25:16.2]} 20... Ne7 {[%clk 0:05:01.4]} 21. f5 {[%clk 0:25:35.3]} 21... Nd5 {[%clk 0:03:37.2]} 22. Nxd5 {[%clk 0:25:31.7]} 22... Bxd5 {[%clk 0:03:41.7]} 23. f6 {[%clk 0:25:32.9]} 23... gxf6 {[%clk 0:03:24.5]} 24. Nf5 {[%clk 0:25:43.5]} 24... Kh8 {[%clk 0:03:18.8]} 25. Qh6 {[%clk 0:25:57]} 25... Rg8 {[%clk 0:03:29.8]} 26. Qxf6+ {[%clk 0:25:20.2]} 26... Rg7 {[%clk 0:03:30.3]} 27. Qxg7# {[%clk 0:25:43.5]} 1-0
    """
    
    result = pgn_to_fens_udf(pgn)
    assert len(set(result)) > 0

def test_chess960_pgn_to_fens_udf():
    # Do not indent, keep the multistring as is
    pgn = """[Event "Live Chess - Chess960"]
[Site "Chess.com"]
[Date "2016.10.27"]
[Round "-"]
[White "Hikaru"]
[Black "MagnusCarlsen"]
[Result "1-0"]
[Variant "Chess960"]
[SetUp "1"]
[FEN "nqrkbbrn/pppppppp/8/8/8/8/PPPPPPPP/NQRKBBRN w GCgc - 0 1"]
[CurrentPosition "4r3/pk3pN1/1nR4p/8/5PPb/4P3/P6P/3R2K1 b - -"]
[Timezone "UTC"]
[ECO "A00"]
[ECOUrl "https://www.chess.com/openings/Undefined"]
[UTCDate "2016.10.27"]
[UTCTime "17:02:42"]
[WhiteElo "3025"]
[BlackElo "2692"]
[TimeControl "300+2"]
[Termination "Hikaru won by resignation"]
[StartTime "17:02:42"]
[EndDate "2016.10.27"]
[EndTime "17:12:13"]
[Link "https://www.chess.com/game/live/1785419374"]

1. c4 {[%clk 0:04:57.6]} 1... Ng6 {[%clk 0:04:51.7]} 2. f4 {[%clk 0:04:47]} 2... c5 {[%clk 0:04:39]} 3. g3 {[%clk 0:04:35.6]} 3... e6 {[%clk 0:04:38]} 4. Bg2 {[%clk 0:04:27.6]} 4... Nb6 {[%clk 0:04:34.5]} 5. Nb3 {[%clk 0:04:25]} 5... d5 {[%clk 0:04:28.9]} 6. cxd5 {[%clk 0:04:00.2]} 6... exd5 {[%clk 0:04:29.7]} 7. Bf2 {[%clk 0:03:40.9]} 7... d4 {[%clk 0:04:30.3]} 8. O-O {[%clk 0:03:35.8]} 8... Be7 {[%clk 0:04:18.2]} 9. Qf5 {[%clk 0:03:21.8]} 9... Qd6 {[%clk 0:03:06.8]} 10. Na5 {[%clk 0:03:18.3]} 10... Rc7 {[%clk 0:03:07]} 11. b4 {[%clk 0:02:51.7]} 11... c4 {[%clk 0:03:00.4]} 12. Nxb7+ {[%clk 0:02:51.8]} 12... Rxb7 {[%clk 0:03:01.5]} 13. Bxb7 {[%clk 0:02:53.7]} 13... Bd7 {[%clk 0:03:03.2]} 14. Qe4 {[%clk 0:02:39.4]} 14... Bf6 {[%clk 0:03:04.4]} 15. Qg2 {[%clk 0:01:49.4]} 15... Re8 {[%clk 0:03:01.4]} 16. e4 {[%clk 0:01:47.5]} 16... dxe3 {[%clk 0:02:51.9]} 17. dxe3 {[%clk 0:01:47.1]} 17... Qxb4 {[%clk 0:02:53]} 18. Bc6 {[%clk 0:01:33.6]} 18... c3 {[%clk 0:02:40.1]} 19. Rfd1 {[%clk 0:01:30.9]} 19... Kc7 {[%clk 0:02:22.1]} 20. Bxd7 {[%clk 0:01:31.9]} 20... Nxd7 {[%clk 0:02:24]} 21. g4 {[%clk 0:01:31.2]} 21... h6 {[%clk 0:02:22.3]} 22. Ng3 {[%clk 0:01:27.3]} 22... Nb6 {[%clk 0:02:16.3]} 23. Nh5 {[%clk 0:01:25.4]} 23... Nh4 {[%clk 0:02:08.7]} 24. Bxh4 {[%clk 0:01:06.1]} 24... Bxh4 {[%clk 0:02:10.6]} 25. Qd2 {[%clk 0:01:07.3]} 25... Kb7 {[%clk 0:01:55.7]} 26. Qxc3 {[%clk 0:01:05.5]} 26... Qe4 {[%clk 0:01:52.5]} 27. Qc7+ {[%clk 0:01:05.3]} 27... Ka8 {[%clk 0:01:53.7]} 28. Qc6+ {[%clk 0:01:04.4]} 28... Qxc6 {[%clk 0:01:54.5]} 29. Rxc6 {[%clk 0:01:06.3]} 29... Kb7 {[%clk 0:01:52.8]} 30. Nxg7 {[%clk 0:00:53.6]} 1-0
    """
    
    result = pgn_to_fens_udf(pgn)
    assert len(set(result)) > 0