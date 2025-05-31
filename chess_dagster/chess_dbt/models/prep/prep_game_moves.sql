with prep_player_games as (
    select
        game_uuid
        , rules
        , time_class
        , time_control_base
        , time_control_add_seconds
        , player_color
        , pgn
        , pgn_header
        , pgn_clock_extract
    from {{ ref('prep_player_games') }}
)
, fens_data as (
    select
        *
        , get_move_details_udf(pgn) as move_details
    from prep_player_games
)
, unnest as (
    select
        *
        -- Move details
        , generate_subscripts(move_details, 1) as game_move_index
        , unnest(move_details) as move_detail
        , unnest(pgn_clock_extract) as clock_unnest
        , json_extract_string(move_detail, 'san') as game_move
        , json_extract_string(move_detail, 'fen') as fen
        , json_extract_string(move_detail, 'color_move') as color_move

        -- This is the clock after the addition of time
        , epoch(
            cast(replace(split(clock_unnest, ' ')[2], ']}}', '') as interval)
        ) as clock_interval_post_move
    from fens_data
)

, additional_prep as (
    select 
        *
        , row_number() over (partition by game_uuid, color_move order by game_move_index) as color_move_index
        
        -- To get the clock before the addition of time
        , clock_interval_post_move - time_control_add_seconds as clock_interval_move
    from unnest
)

, board_details as (
    select
    -- Game details
        *
        , game_uuid
        , time_class
        , time_control_base
        , time_control_add_seconds

        -- Move details
        , case
            when color_move = 'White' then concat(color_move_index::varchar, '. ', game_move)
            else concat(color_move_index::varchar, '... ', game_move)
        end as pgn_move
        , game_move_index
        , pgn_header
        , color_move
        , color_move_index
        , game_move
        , game_uuid || '_' || game_move_index as id

        -- Clock details
        , string_agg(pgn_move, ' ')
            over (partition by game_uuid order by game_move_index)
            as pgn_cum_move
        , if(time_class = 'daily', 0, clock_interval_move) as clock_interval_move
        , if(time_class = 'daily', 0, clock_interval_post_move) as clock_interval_post_move
        , if(
            time_class = 'daily'
            , 0
            , coalesce(
                lag(clock_interval_post_move)
                    over (
                        partition by game_uuid, color_move order by color_move_index
                    )
                , time_control_base
            )
        ) as prev_clock_interval

        , round(
            if(
                time_class = 'daily', 0, prev_clock_interval - clock_interval_move
            )
            , 1
        ) as move_time_seconds
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
        , coalesce(
            lag(fen) over (partition by game_uuid order by game_move_index)
            , ''
        ) as prev_fen
        , get_captured_piece_udf(prev_fen, fen) as captured_piece

    from additional_prep
)

select

-- Game details
    id
    , game_uuid
    , rules
    , time_class
    , time_control_base
    , time_control_add_seconds
    , player_color

    -- Move details
    , game_move_index
    , pgn_header
    , pgn_cum_move
    , color_move
    , color_move_index
    , game_move
    , captured_piece

    -- Clock details
    , clock_interval_move
    , clock_interval_post_move
    , prev_clock_interval
    , move_time_seconds

    -- Board details
    , fen
    , major_minor_cnt
    , black_major_minor
    , white_major_minor
    , is_backrank_sparse
    , is_midgame
    , is_endgame
    , game_phase

from board_details
