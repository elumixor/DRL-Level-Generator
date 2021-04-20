import * as PIXI from "pixi.js";
import { SCALE_MODES } from "pixi.js";

document.body.style.textAlign = "center";

// Create our pixi application
const app = new PIXI.Application({ backgroundColor: 0xc0c0c0, antialias: true, autoDensity: true, resolution: 2 });
document.body.appendChild(app.view);

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
    bobRadius: 50,
    connectorLength: 200,
    angle: 50,
    enemies: [
        { radius: 50, x: 50, y: 50 },
    ],
};

const deg2rad = Math.PI / 180;

const mainStage = app.stage;
const center = { x: app.view.offsetWidth * 0.5, y: app.view.offsetHeight * 0.5 };

const pendulumStart = createCircle(0x101010, 10);
pendulumStart.position.copyFrom(center);

const pendulumBob = createCircle(0x505050, parameters.bobRadius);

function createRect(color: number, width: number, height: number) {
    const gfx = new PIXI.Graphics();
    gfx.beginFill(color);
    gfx.drawRect(0, 0, width, height);
    gfx.endFill();

    const texture = app.renderer.generateTexture(gfx, SCALE_MODES.LINEAR, 2);

    gfx.destroy();

    return new PIXI.Sprite(texture);
}

const connector = createRect(0x101010, parameters.connectorLength, 2.5);
connector.anchor.y = 0.5;
connector.position.copyFrom(center);

const enemies = parameters.enemies.map(({ radius, x, y }) => createCircle(0xff4020, radius));

mainStage.addChild(pendulumStart, connector, pendulumBob, ...enemies);

function update() {
    connector.width = parameters.connectorLength;
    connector.angle = 90 - parameters.angle;

    {
        const x = center.x + parameters.connectorLength * Math.sin(parameters.angle * deg2rad);
        const y = center.y + parameters.connectorLength * Math.cos(parameters.angle * deg2rad);
        pendulumBob.position.set(x, y);
    }

    enemies.forEach((enemy, index) => {
        const { radius, x, y } = parameters.enemies[index];
        enemy.width = enemy.height = radius * 2;
        enemy.x = center.x + x;
        enemy.y = center.y + y;
    });
}

// Set up default parameters
update();

const table = document.createElement("table");
document.body.appendChild(table);

table.style.marginLeft = "auto";
table.style.marginRight = "auto";

// Add inputs
function addInput(name: string, defaultValue: number, callback: (value: number) => void) {
    const row = document.createElement("tr");
    table.appendChild(row);

    const labelCell = document.createElement("td");
    const inputCell = document.createElement("td");

    row.appendChild(labelCell);
    row.appendChild(inputCell);

    const label = document.createElement("label");
    const input = document.createElement("input");

    labelCell.appendChild(label);
    inputCell.appendChild(input);

    input.id = `input-for-${name}`;
    label.htmlFor = input.id;

    label.style.padding = "10px";

    label.textContent = name;
    input.placeholder = name;
    input.type = "number";
    input.value = `${defaultValue}`;

    input.addEventListener("input", () => callback(parseFloat(input.value || `${defaultValue}`)));
}

addInput("Connector length", parameters.connectorLength, (value) => {
    parameters.connectorLength = value;
    update();
});
addInput("Bob radius", parameters.bobRadius, (value) => {
    parameters.bobRadius = value;
    update();
});
addInput("Angle", parameters.angle, (value) => {
    parameters.angle = value;
    update();
});

for (let i = 0; i < parameters.enemies.length; i++) {
    const enemy = parameters.enemies[i];

    addInput(`Enemy ${i} radius`, enemy.radius, (value) => {
        enemy.radius = value;
        update();
    });

    addInput(`Enemy ${i} x`, enemy.x, (value) => {
        enemy.x = value;
        update();
    });

    addInput(`Enemy ${i} y`, enemy.y, (value) => {
        enemy.y = value;
        update();
    });
}
