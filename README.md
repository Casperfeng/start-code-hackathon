## To Run locally and experiment

First, you are going to need node, as well as npm, yarn or lerna..

```
git clone https://github.com/arealizeai/arealize-startcode-2021
npm install
npm start
```

## Learning Resources

1. https://threejs.org/docs/index.html#manual/en/introduction/Creating-a-scene <br>
2. https://www.pandaqi.com/Games/overview/Threejs <br>
3. https://tympanus.net/codrops/2016/04/26/the-aviator-animating-basic-3d-scene-threejs/ <br>
4. https://www.toptal.com/javascript/3d-graphics-a-webgl-tutorial

## Developing and Running Locally
To get started, clone the repository and ensure you npm >= 3 and grunt installed, then run:

    cd into ```arealize-client-demo```
    npm install
    grunt

The latter command generates `example/js/blueprint3d.js` from `src`.

The easiest way to run locally is to run a local server from the `example` directory. There are plenty of options. One uses Python's built in webserver:

    cd example

    # Python 2.x
    python -m SimpleHTTPServer

    # Python 3.x
    python -m http.server

Then, visit `http://localhost:8000` in your browser.

## Attributions

Arealize StartCode Hackathon was forked and developed using asjadanis's react-three-boilerplate code. This is a great way to bootstrap a simple threejs project. https://github.com/asjadanis/react-three-boilerplate

However, I'd recommend using react-three-fiber for any larger projects. We didn't use it in this project as the learning curve is a bit steeper, but the result is much more maintainable code in the long run and better runtimes. https://github.com/pmndrs/react-three-fiber
