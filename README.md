# Experimental-Web-Crawler
Very Simple Web Crawler i made in python, similar to dirb and Gobuster. I am new at this, so it's not the best. Thank you.

How do i use corndog16's experimental web Crawler to find the public directories of a website?
Use ' -u ' to specify the website you want to run
' -w ' to specify the wordlist you want to use. For example; if it's located in /usr/wordlist/wordlist1.txt do python3 Crawler.py -u http://examplewebsite.com -w [path to wordlist] -f 
' -f ' is known as filter, use -f to exclude error 403, 404 and 429
' -d ' to add a delay to the crawler[use -d if you get rate limited perhaps]
' -t ' to specify the amount of threads you'd like to use [the more threads the faster it'll work, but there is a higher chance you'll get rate limited. The default amount of threads is 10]

I made this as an experiment, to learn, i guess. I'm somewhat new to python.
Good luck and have a great year!
