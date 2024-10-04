# RainWorldClock

Recreates the cycle clock in the game [Rain World](https://rainworldgame.com/). If you haven't played it, go check it out!

Forked from Trebor-Huang/clock project and adapted to Win. He/She has done great job.

Assisted by AI, so the code is a mess. But it works :)


# Requiremets
`Requirements:
pythonw==3.12
PyQt5==5.15.11
json==2.0.9
PIL==10.1.0
numpy==1.26.2`


# Usage
`pythonw.exe main.pyw`
or this can be done with soft link.

The behaviour of clock is determined by `data.json`
By default, a tomato clock is defined with 25min-5min cycles.

An example is like below (the comments are not valid JSON, they are for demo purposes only)
```
{
  "ticktock": 3.2,  // seconds between tick and tock
  "intervals": [{
    "totalPip": 25,  // total number of pips in a cycle, can be zero (default)
    "totalTime": 1791,  // total seconds in the cycle, can be zero for infinite time (default)
    "karmaSymbol": 1,  // karma symbol from 0-10, 0 (default) means empty
    "karmaReinforced": true  // karma flower is in effect, default false
  }, {
    "totalPip": 15,
    "totalTime": 670,
    "karmaSymbol": 8,
    "maxKarma": 9  // max karma (7-10) must be specified if karmaSymbol > 5.
  }]
}
```

The sound effects come from [this repo](https://github.com/cookiecaker/Rain-World-Sounds) and are properties of the Rain World developers. All png files in the repo come from the [rain world wiki](https://rainworld.miraheze.org/wiki/Category:Karma_icons), see copyright notices there. The rest are shared under the MIT License.
