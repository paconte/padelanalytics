#!/bin/bash



sandokan () {
    git filter-branch --env-filter 'export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"'
}

change_all_commits_author () {
    if [[ ($# -ne 2) ]]
    then
	echo "Invalid number of arguments."
	exit
    fi
    
    echo "Changing all commits author_name to $1"
    echo "Changing all commits author_email to $2"
    echo "Changing all commits commiter_name to $3"

    git filter-branch --commit-filter 'if [ "$GIT_AUTHOR_NAME" = "Francisco Revilla" ];
  then export GIT_AUTHOR_NAME="paconte"; export GIT_AUTHOR_EMAIL=paconte@gmail.com; export GIT_COMMITTER_NAME="paconte"; export GIT_COMMITTER_EMAIL=paconte@gmail.com;
  fi; git commit-tree "$@"'
}


check_date_arithmetic_operator () {
    # check arithmetic operations to a date has no errors e.g:
    # date -d "+2 hour" OK
    # date -d "aaa" WRONG
    if [[ ($# -ne 1) ]]
    then
	echo "Invalid number of arguments."
	exit
    fi
    date -d "$1" > /dev/null 2>&1
    if [[ $? -ne 0 ]]
    then
	echo "Invalid argument: $1"
	exit
    fi
}

rewrite_commit_date () {
    # rewrite a commit's ($1) author_date and committer_date to ($2), e.g.:
    # rewrite_commit_date \
    # 7a7ca42fc03e1109ba7808310883d9ca8decde40 \
    # Thu, 10 Jul 2014 15:30:59 +0200
    echo "commit is: $1"
    echo "date is: $2"

    if [[ $# -ne 2 ]]
    then
	echo "Invalid number of arguments."
	exit
    fi
    
    git filter-branch --env-filter \
    "if test \$GIT_COMMIT = '$1' 
     then
         export GIT_AUTHOR_DATE
         export GIT_COMMITTER_DATE
         GIT_AUTHOR_DATE='$2'
         GIT_COMMITTER_DATE='$2'
     fi" &&
     rm -fr "$(git rev-parse --git-dir)/refs/original/"
}


print_tuple_commit_date() {
    # the method print all commits and dates in format rfc-2822
    # e.g.:
    # 7a7ca42fc03e1109ba7808310883d9ca8decde40
    # Thu, 10 Jul 2014 15:30:59 +0200
    # 4312b99ebd2b6a7f3c6ef751447cb187d63fd819
    # Wed, 09 Jul 2014 18:10:24 +0200
    # etc ...
    
    git log --format=format:%H%n%ai | \
	while read -r first; read -r second
	do
	    commit="$first" 
	    new_date=$(date -d "$second" --rfc-2822)
	    m="$commit"$'\n'"$new_date"
	    #echo 'Value of m is:'
	    echo "$m"
	done
}

rewrite_all() {
    # the method print all commits and dates in format rfc-2822
    # e.g.:
    # 7a7ca42fc03e1109ba7808310883d9ca8decde40
    # Thu, 10 Jul 2014 15:30:59 +0200
    # 4312b99ebd2b6a7f3c6ef751447cb187d63fd819
    # Wed, 09 Jul 2014 18:10:24 +0200
    # etc ...

    check_date_arithmetic_operator "$1"

    git log --format=format:%H%n%ai | \
	while read -r first; read -r second
	do
	    orig_date=$(date -d "$second" --rfc-2822)
	    compare_date=$(date -d "$2" --rfc-2822)

	    if [ "`date --date \"$orig_date\" +%s`" -gt "`date --date \"$compare_date\" +%s`" ]; then
		commit="$first"
		new_date=$(date -d "$second $1" --rfc-2822)
		m="$commit"
		echo "$new_date  >>>>  $compare_date"
		echo "hash is: $m"
		echo "$orig_date   =====>   $new_date"
		rewrite_commit_date "$commit" "$new_date"
	    else
		:
	    fi
	done
}

current_date=$(git log -1 --format=format:%ai)
new_date=$(date -d "2017-07-03 13:32:03 +0200 -24 hour" --rfc-2822)
commit="06f6570cf57863bb39b6962f8013ce55c2d50074"
#echo "$new_date"


#rewrite_commit_date "$commit" "$new_date"
rewrite_all "-15 hour" "2018-01-18 16:00:56 +0200"
#change_all_commits_author "Francisco Revilla" "paconte@gmail.com"


test_check_date_arithmetic_operator () {
    check_date_arithmetic_operator "+6 hours"
    check_date_arithmetic_operator "-6 hour"
    check_date_arithmetic_operator "+10000 second"
    check_date_arithmetic_operator "+10000 minute"
    check_date_arithmetic_operator "+10000 minutes"
    check_date_arithmetic_operator "aaa"
}
