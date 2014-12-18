#!/bin/sh

_supernova()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    local configs=$(cat "${XDG_CONFIG_HOME}"/supernova ~/.supernova ./.supernova 2> /dev/null)
    local possibilities=$(echo "${configs}" | sed -n '/^\[.*\]/ s_\[\(.*\)\]_\1_p' | sort -u)
    COMPREPLY=( $(compgen -W "${possibilities}" -- $cur) )
}
complete -F _supernova supernova
