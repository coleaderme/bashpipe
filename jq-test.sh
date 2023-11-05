#!/usr/bin/sh
#
# onebyone vs atOnce - jq json parse 100x
#
#
onebyone(){
    # onebyone 
    #     1.238s
    #     1.249s
    #     1.212s
    #     1.213s

    song_title=$(jq .songs[0].title ATIfejZ9bWw.json)
    year=$(jq .songs[0].year ATIfejZ9bWw.json)
    album=$(jq .songs[0].more_info.album ATIfejZ9bWw.json)
    album_artists=$(jq .songs[0].more_info.artistMap.primary_artists[].name ATIfejZ9bWw.json)
    echo "$song_title"
    echo "$year"
    echo "$album"
    echo "$album_artists"
}

# range="1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 "
# for i in $range; do
#     onebyone    ## winner!
# done

atOnce(){
    # atOnce
        # 1.672s
        # 1.465s
        # 1.513s
        # 1.516s

    result="$(jq '{song_title: .songs[0].title, year: .songs[0].year, album: .songs[0].more_info.album, album_artists: .songs[0].more_info.artistMap.primary_artists[].name}' ATIfejZ9bWw.json)"
    echo "$result" | jq -r .song_title
    echo "$result" | jq -r .year
    echo "$result" | jq -r .album
    echo "$result" | jq -r .album_artists
}