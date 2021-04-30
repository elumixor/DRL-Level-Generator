import * as PIXI from "pixi.js";
import {SCALE_MODES} from "pixi.js";

document.body.style.textAlign = "center";

// Create our pixi application
const app = new PIXI.Application({backgroundColor: 0xc0c0c0, antialias: true, autoDensity: true, resolution: 2});
document.body.appendChild(app.view);

console.log(app.view.offsetHeight, app.view.height)
console.log(app.view.offsetWidth, app.view.width)
const scale = Math.max(app.view.offsetWidth, app.view.offsetHeight) / 2;
console.log(scale)

function createCircle(color: number, radius: number) {
    const gfx = new PIXI.Graphics();

    gfx.beginFill(color);
    gfx.drawCircle(0, 0, radius);
    gfx.endFill();

    const texture = app.renderer.generateTexture(gfx, PIXI.SCALE_MODES.LINEAR, 1);
    gfx.destroy();

    const circle = new PIXI.Sprite(texture);
    circle.anchor.set(0.5);

    return circle;
}

const parameters = {
    bobRadius: 0.25,
    connectorLength: 0.5,
    angle: 50,
    enemies: [
        {radius: 0.25, x: 0.5, y: 0.5},
    ],
};

const deg2rad = Math.PI / 180;

const mainStage = app.stage;
const center = {x: app.view.offsetWidth * 0.5, y: app.view.offsetHeight * 0.5};

const pendulumStart = createCircle(0x101010, 10);
pendulumStart.position.copyFrom(center);

const pendulumBob = createCircle(0x505050, 100);

function createRect(color: number, width: number, height: number) {
    const gfx = new PIXI.Graphics();
    gfx.beginFill(color);
    gfx.drawRect(0, 0, width, height);
    gfx.endFill();

    const texture = app.renderer.generateTexture(gfx, SCALE_MODES.LINEAR, 2);

    gfx.destroy();

    return new PIXI.Sprite(texture);
}

const connector = createRect(0x101010, 100, 10);
connector.anchor.y = 0.5;
connector.position.copyFrom(center);

const enemies = parameters.enemies.map(({radius, x, y}) => createCircle(0xff4020, 100));

mainStage.addChild(pendulumStart, connector, pendulumBob, ...enemies);

function update() {
    connector.width = parameters.connectorLength * scale;
    connector.angle = 90 - parameters.angle;

    {
        const x = center.x + parameters.connectorLength * scale * Math.sin(parameters.angle * deg2rad);
        const y = center.y + parameters.connectorLength * scale * Math.cos(parameters.angle * deg2rad);
        pendulumBob.position.set(x, y);
    }

    pendulumBob.width = pendulumBob.height = parameters.bobRadius * 2 * scale;

    enemies.forEach((enemy, index) => {
        const {radius, x, y} = parameters.enemies[index];
        enemy.width = enemy.height = radius * 2 * scale;
        enemy.x = center.x + x * scale;
        enemy.y = center.y - y * scale;
    });
}

// Set up default parameters
update();

const table = document.createElement("table");
document.body.appendChild(table);

table.style.marginLeft = "auto";
table.style.marginRight = "auto";

// Add inputs
function addInput(name: string, defaultValue: number, min: number, max: number, callback: (value: number) => void) {
    const row = document.createElement("tr");
    table.appendChild(row);

    const labelCell = document.createElement("td");
    const inputMin = document.createElement("td");
    const inputCell = document.createElement("td");
    const inputMax = document.createElement("td");

    row.appendChild(labelCell);
    row.appendChild(inputMin);
    row.appendChild(inputCell);
    row.appendChild(inputMax);

    {
        const div = document.createElement("div");
        div.innerText = `${min}`;
        inputMin.appendChild(div);
    }

    {
        const div = document.createElement("div");
        div.innerText = `${max}`;
        inputMax.appendChild(div);
    }

    const label = document.createElement("label");
    const input = document.createElement("input");
    const inputValue = document.createElement("div");

    labelCell.appendChild(label);
    inputCell.appendChild(input);
    inputCell.appendChild(inputValue);

    input.id = `input-for-${name}`;
    label.htmlFor = input.id;

    label.style.padding = "10px";

    label.textContent = name;
    input.placeholder = name;
    input.type = "range";
    input.min = `${min}`;
    input.max = `${max}`;
    input.step = `${(max - min) / 1000}`
    input.value = `${defaultValue}`;

    inputValue.innerText = input.value;

    input.addEventListener("input", () => {
        inputValue.innerText = input.value;
        callback(parseFloat(input.value || `${defaultValue}`))
    });
}

const maxValue = 1;

addInput("Connector length", parameters.connectorLength, 0, maxValue, (value) => {
    parameters.connectorLength = value;
    update();
});
addInput("Bob radius", parameters.bobRadius, 0, maxValue, (value) => {
    parameters.bobRadius = value;
    update();
});
addInput("Angle", parameters.angle, -90, 90, (value) => {
    parameters.angle = value;
    update();
});

for (let i = 0; i < parameters.enemies.length; i++) {
    const enemy = parameters.enemies[i];

    addInput(`Enemy ${i} radius`, enemy.radius, 0, maxValue, (value) => {
        enemy.radius = value;
        update();
    });

    addInput(`Enemy ${i} x`, enemy.x, -1, 1, (value) => {
        enemy.x = value;
        update();
    });

    addInput(`Enemy ${i} y`, enemy.y, -1, 1, (value) => {
        enemy.y = value;
        update();
    });
}
