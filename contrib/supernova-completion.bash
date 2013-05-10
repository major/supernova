_nova_opts="" # lazy init
_nova_flags="" # lazy init
_nova_opts_exp="" # lazy init

_supernova_bash_completion()
{
    local cur prev nbc cflags sn_envs sn_envs_exp
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [ "x$_nova_opts" == "x" ] ; then
        nbc="`nova bash-completion | sed -e "s/\s-h\s/\s/"`"
        _nova_opts="`echo "$nbc" | sed -e "s/--[a-z0-9_-]*//g" -e "s/\s\s*/ /g"`"
        _nova_flags="`echo " $nbc" | sed -e "s/ [^-][^-][a-z0-9_-]*//g" -e "s/\s\s*/ /g"`"
        _nova_opts_exp="`echo "$_nova_opts" | sed -e "s/\s/|/g"`"
    fi

    sn_opts="--list --debug --help"
    sn_env=$(grep -Po '(?<=\[).*?(?=\])' ~/.supernova | tr '\n' ' ')
    sn_envs_exp="`echo "$sn_env" | sed -e "s/\s/|/g"`"

    if [[ " ${COMP_WORDS[@]} " =~ " "($_nova_opts_exp)" " && "$prev" != "help" ]] ; then
        COMPLETION_CACHE=~/.novaclient/*/*-cache
        cflags="$_nova_flags "$(cat $COMPLETION_CACHE 2> /dev/null | tr '\n' ' ')
    elif [[ " ${COMP_WORDS[@]} " =~ " "($sn_envs_exp)" " ]] ; then
        cflags=$_nova_opts
    else
        cflags=$sn_env
    fi

    COMPREPLY=($(compgen -W "${sn_opts} ${cflags}" -- ${cur}))
    return 0
}

complete -F _supernova_bash_completion supernova
