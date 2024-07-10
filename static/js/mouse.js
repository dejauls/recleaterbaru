// dots is an array of Dot objects,
// mouse is an object used to track the X and Y position
// of the mouse, set with a mousemove event listener below
const dots = [];
const mouse = { x: 0, y: 0 };

// The Dot class used to scaffold the dots
class Dot {
  constructor(className) {
    this.x = 0;
    this.y = 0;
    this.node = (() => {
      const n = document.createElement("div");
      n.className = className;
      document.body.appendChild(n);
      return n;
    })();
  }

  // The draw() method sets the position of the object's <div> node
  draw() {
    this.node.style.left = `${this.x}px`;
    this.node.style.top = `${this.y}px`;
  }
}

// Creates the Dot objects, populates the dots array
for (let i = 0; i < 100; i++) {
  dots.push(new Dot("trail"));
}

// Create the head trail dot
const headTrail = new Dot("head-trail");

// This is the screen redraw function
const draw = () => {
  // Make sure the mouse position is set every time draw() is called.
  let { x, y } = mouse;

  // This loop is where all the 90s magic happens
  dots.forEach((dot, index, dots) => {
    const nextDot = dots[index + 1] || dots[0];
    
    dot.x = x;
    dot.y = y;
    dot.draw();
    x += (nextDot.x - dot.x) * 0.04;
    y += (nextDot.y - dot.y) * 0.04;
  });

  // Update the head trail position
  headTrail.x = mouse.x;
  headTrail.y = mouse.y;
  headTrail.draw();
};

addEventListener("mousemove", (event) => {
  mouse.x = event.pageX + 1;
  mouse.y = event.pageY + 1;
});

// animate() calls draw() then recursively calls itself
// every time the screen repaints via requestAnimationFrame().
const animate = () => {
  draw();
  requestAnimationFrame(animate);
};

// And get it started by calling animate().
animate();