WHAT IT DOES:
Control pc remotely through email (with many limitations)

Run this on a computer with ACTIVE INTERNET connection and use email to communicate with the script
The subject field of mails in inbox is used for executing code and 
Return value or error is sent to default email id as message

Potential Uses:
1.Browse files
2.Download files
3.Execute python commands of single line - much potential
4.etc.

IMPORTANT:
1.Email id and password for the script must be provided when asked by the script at start
2.Turn "access to less secure apps" for email id of script in google settings (for gmail)
3.Your email id to which all responses are send must be provided when asked by the script at start
4.gmail is prefered as email id as it is tested so much when I worked with this code.
5.Subject line of email is used as command to the script
6.The script can be changed to consider its inbox after n mails only by changing value of n in class e_meta

LESS IMPORTANT:
1.All operations script can perform are one line python commands OR the script can run any one line python command.
2.Text like "Re:" or "Fwd:" at the start are ignored in subject line

BASIC COMMANDS:
1."#eval <command>"
2."#exec <command>" - if #eval doesnt work
3."#attach <filename>" - sends you back the said file if it is in working directory (or full path is given) and has size within attachment limit of email id.

Pre-imported libraries:
	These are pre-imported so you can work with them
1.from pprint import pprint,pformat
2.email
3.datetime
4.os
5.sys
6.time
7.numpy as np
8.from bs4 import BeautifulSoup
9.requests
10.smtplib
11.imaplib

Incomplete WORK:
The script has potential to work on multiple computers.
Many seemingly useless code is for that
Its a work in progress..

