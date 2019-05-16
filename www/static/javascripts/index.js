var sensorMap = document.getElementById('sensor-map');
var sensorMapCtx = sensorMap.getContext('2d');
var frames = undefined;
var frameRate = 20;
var maxX = 65;
var maxY = 65;
var sensors = new Map();
var canvasMap = createMap();
window.addEventListener('resize', resizeCanvas, false);

window.onload = () => {
    constructMap();
}

sensorMap.addEventListener('click', (event) => {
    var xDiv = (window.innerWidth * 0.8) / maxX;
    var yDiv = (window.innerWidth * 0.8) / maxY;
    var x = Math.floor(((event.pageX - sensorMap.offsetLeft) / (xDiv)));
    var y = Math.floor(((event.pageY - sensorMap.offsetTop) / (yDiv)));
    if (sensors[x] !== undefined && sensors[x][y] !== undefined) {
        window.location = `/nodes/${sensors[x][y].id}`;
    }
});

function createMap() {
    var newMap = []
    for (var i = 0; i < maxX; ++i) {
        var row = []
        for(var j = 0; j < maxY; ++j) {
            if(Math.random() * 100 < 75) {
                row[j] = "#0F0";
            } else {
                row[j] = "#00F";
            }
        }
        newMap[i] = row;
    }
    return newMap;
}

function constructMap() {
    resizeCanvas();
    getAllSensors();
}

function resizeCanvas() {
    sensorMap.width = window.innerWidth * 0.8;
    sensorMap.height = window.innerHeight * 0.8;
    if (frames !== undefined) {
        clearInterval(frames);
    }
    frames = setInterval(() => { drawFrame(); }, frameRate);
}

function getAllSensors() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var sensorsData = eval(`(${xhttp.responseText})`);
            for (let i in sensorsData['docs']) {
                sensor = sensorsData['docs'][i]
                if (sensors[sensor.x] === undefined) {
                    sensors[sensor.x] = new Map();
                }
                sensors[sensor.x][sensor.y] = new Thing(sensor.id, sensor.x, sensor.y, sensor.type);
            }
        }
    };
    xhttp.open("GET", `/node-data`, true);
    xhttp.send();
}

function drawFrame() {
    var xDiv = (window.innerWidth * 0.8) / maxX;
    var yDiv = (window.innerWidth * 0.8) / maxY;
    for (var x = 0; x < maxX; ++x) {
        for (var y = 0; y < maxY; ++y) {
            sensorMapCtx.fillStyle = canvasMap[x][y];
            sensorMapCtx.fillRect(x * xDiv, y * yDiv, xDiv, yDiv);
            if (sensors[x] !== undefined && sensors[x][y] !== undefined) {
                sensorMapCtx.fillStyle = "#CCC";
                sensorMapCtx.fillRect(x * xDiv, y * yDiv, xDiv, yDiv);
            }
        }
    }
}

class Thing {
    constructor(id, x, y, type) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.type = type;
    }

    getData() {
        var data = null;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                data = eval(`(${xhttp.responseText})`);
            }
        };
        xhttp.open("POST", `http://127.0.0.1:5984/sensors/${this.id}`, true);
        xhttp.send();
        return sensors
    }

    toString() {
        return `Sensor: ${this.id}\nType: ${this.type}\nco-ordinates: ${this.x}, ${this.y}`
    }
}
