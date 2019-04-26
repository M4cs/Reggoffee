# Reggoffee
Slack Slash Bot API for Reggora's Coffee Management

<a href="" align="center"><img src="https://image.prntscr.com/image/Hoap-nTQQGO_gtA0-2o3Pg.png" alt="preview"></a>

This bot takes advantage of the Slash Command feature in Slack Apps. It is a Flask API and basically runs off webhooks.

You can add scope for more coffee pots and add more commands how you'd like.

Commands:

`/coffeestatus` - Checks current status of bots according to bot. (May be inaccurate)
`/madecoffee [left/right]` - Tells the bot you made coffee in either the left or right pot. Changes status in realtime. *Worth 1 Point on the Leaderboard*
`/outofcoffee [left/right]` - Opposite of /madecoffee. *Worth 1 Point As Well*
`/coffeeleaderboard` - Displays Top 5 Leaders with the most points
`/coffeepoints` - Displays your current point balance.

To add more pots edit the status.json file and add the names. Then inside resources.py add the pots functions with a copy paste from the existing ones. It's pretty simple to get setup. Then you can host on a server or herokuapp and get it setup in your workspace.

# Background

Jokingly in the office we talked about a way to check if there was coffee without having to go into the kitchen. We use Slack a lot so I thought why not make a Slack bot to track it and have some fun with it. This includes a leaderboard so you can clearly see who the best person in the office is by checking who has made and reported the most coffee statuses! Hope somebody finds enjoyment in this :)
