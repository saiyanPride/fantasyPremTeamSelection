# Fantasy Premier League Team Selector
What is the fantasy premier league game? https://fantasy.premierleague.com/help/

This application utilises historical player statistics & the user’s opinions to recommend team selection decisions such as:

- players to buy & sell
- which chips to use (wildcards, triple captain, free hits) if available & beneficial

The key benefit of this application is that it factors in upcoming matches as far in the future as the user wishes; a task which if done manually would be arduous. For example, if the user configures the application to look 5 gameweeks into the future, the team selected will be good for the next 5 game weeks. 
Furthermore, before the 5 weeks are up, one would have had 5 free transfers to accommodate unexpected events like injuries, red cards etc.

## Components:

### Python DataRetriever: 
uses a PhantomJS webDriver  (<link to selenium HQ>) to retrieve player statistics from the official premier league site & update a relational database.

### C++ team selection Engine:
An interactive component that uses a variety of algorithms to make recommendations such as:
captain & vice captain choice
whether wildcard/freehit chip should be used, and the best team that can be formed within one’s budget
whether the bench boost chip should be used
players to buy & sell using free transfers

It also highlights key statistics such as:
the best players in each position
the best players overall 

This application was built for personal use. However, reach out if you find this interesting and would like to use it or add more features
