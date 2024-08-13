with player_games as (
    select *
    from {{ source('chess_source', 'player_games') }}
)
select * from player_games