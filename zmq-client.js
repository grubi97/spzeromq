const zmq = require("zeromq");
const { promisify } = require("util");
const fs = require("fs");

readFileAsync = promisify(fs.readFile);
readDirAsync = promisify(fs.readdir);

async function run() {
  const sock = new zmq.Request();

  sock.connect("tcp://127.0.0.1:5555");
  console.log("Producer bound to port 5555");

  files = await readDirAsync("images/");
  for (var i = 0; i < files.length; i++) {
    img = await readFileAsync("images/" + files[i]);
    await sock.send(img);
    console.log("send request");
    const [result] = await sock.receive();
    console.log(JSON.parse(result));
  }
}

run();
