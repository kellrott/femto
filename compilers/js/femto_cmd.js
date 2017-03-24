
const fs = require("fs")
require("./femto.js")

fs.readFile(process.argv[2], 'utf8', function (err,code) {
  if (err) {
    return console.log(err);
  }
  doc = JSON.parse(code);
  //console.log(doc)
  f = femto.compile(doc);

  fs.readFile(process.argv[3], 'utf8', function (err,inputs) {
    if (err) {
      return console.error(err);
    }
    inputs_doc = JSON.parse(inputs);
    out = f(inputs_doc);
    console.log(JSON.stringify(out));
  });
  //console.log(f);
});
