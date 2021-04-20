import * as PIXI from "pixi.js";
import { SCALE_MODES } from "pixi.js";

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
        {radius: 50, x: 50, y: 50}
    ]
};

const deg2rad = Math.PI / 180;

const mainStage = app.stage;
const center = { x: app.view.offsetWidth * 0.5, y: app.view.offsetHeight * 0.5 };

const pendulumStart = createCircle(0x101010, 10);
pendulumStart.position.copyFrom(center);

const pendulumBob = createCircle(0x505050, parameters.bobRadius);

function getPendulumBobPosition() {
    const x = center.x + parameters.connectorLength * Math.sin(parameters.angle * deg2rad);
    const y = center.y + parameters.connectorLength * Math.cos(parameters.angle * deg2rad);
    return { x, y };
}

pendulumBob.position.copyFrom(getPendulumBobPosition());

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
connector.angle = 90 - parameters.angle;
connector.position.copyFrom(center);

const enemies = parameters.enemies.map(({radius, x, y}) => {
    const enemy = createCircle(0xff4020, radius);
    enemy.x = center.x + x;
    enemy.y = center.y + y;
    return enemy;
})

mainStage.addChild(pendulumStart, connector, pendulumBob, ...enemies);

