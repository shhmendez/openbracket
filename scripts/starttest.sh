cd ../../;
{ find cache/Backend/ cache/GameEngine/; find cache -maxdepth 1 -type f; } | entr -rc python3 -Bm cache --test;
