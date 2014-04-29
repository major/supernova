#!/bin/sh

_supernova()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    local possibilities=$(awk '/\[/{ gsub(/\[|\]/,"");print}' ~/.supernova)
    COMPREPLY=( $(compgen -W "${possibilities}" -- $cur) )
}
complete -F _supernova supernova
