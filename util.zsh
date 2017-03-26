#!/usr/bin/zsh
#

fetch_yaml_value() {
    file=$1
    pattern="\.*$2: "
    sedprog="s/$pattern//"
    cat $file | grep $pattern | sed $sedprog | sed 's/ //g' | sed 's/,//'
}

init_gitignore() {
    printf "__pycache__/\n" > .gitignore
    passfile=`fetch_yaml_value config.yml secret`
    printf "$passfile\n" >> .gitignore
}

init_gitignore
