with game_moves as (
    select
    *
    from {{ ref('prep_game_moves_fen') }}
)
, board_details as (
    select
    *
    , split(fen, ' ')[1] as fen_board
    , len(regexp_extract_all(split(fen_board, ' ')[1], '[rnbqRNBQ]')) as major_minor_cnt
    , len(regexp_extract_all(split(fen_board, '/')[1], '[rnbq]')) as black_major_minor
    , len(regexp_extract_all(split(fen_board, '/')[-1], '[RNBQ]')) as white_major_minor
    , black_major_minor < 4 or white_major_minor < 4 as is_backrank_sparse
    , major_minor_cnt <= 10 or is_backrank_sparse as is_midgame
    , is_midgame and major_minor_cnt <= 6 as is_endgame
    , case
        when is_endgame then 'Endgame'
        when is_midgame then 'Midgame'
        else 'Opening'
    end as game_phase

    from game_moves
)
select
id
, game_uuid
, major_minor_cnt
, is_backrank_sparse
, is_midgame
, is_endgame
, game_move_index
, game_phase

from board_details