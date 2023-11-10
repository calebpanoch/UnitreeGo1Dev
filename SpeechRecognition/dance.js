// Inside NX board on ~/Desktop/NodeJS-Test

const { Go1, Go1Mode} = require("@droneblocks/go1-js");

                                                                                                                                     dog = new Go1();
dog.init();

              
async function dance() {

  //await dog.wait(3000);

  dog.setMode(Go1Mode.stand);

  await dog.wait(1000);

  await dog.lookUp(0.5, 1000);
  await dog.lookDown(0.5, 1000);
  await dog.leanLeft(0.5, 1000);
  await dog.leanRight(0.5, 1000);
  await dog.twistLeft(0.5, 1000);
  await dog.twistRight(0.5, 1000);

  await dog.resetBody();

  await dog.lookUp(1, 1000);
  await dog.lookDown(1, 1000);
  await dog.leanLeft(1, 1000);
  await dog.leanRight(1, 1000);
  await dog.lookUp(0.5, 1000);
  
  await dog.resetBody();

  dog.setMode(Go1Mode.walk);
  await dog.wait(1000);
  console.log("done");

}

dance();
