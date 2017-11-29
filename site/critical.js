const critical = require('critical');
const fs = require('fs');
const path = require('path');

function inline(output) {
  const fname = path.resolve(__dirname, '..', 'dist', 'index.html');
  fs.readFile(fname, 'utf8', function(err, data) {
    if (err) {
      return console.log(err);
    }
    let result = data.replace(/\/\* __inlinedcss__ \*\//g, output);
    result = result.replace(/<link rel=\"stylesheet\" href=\"\/tailwind.min.css\">/g, '');

    fs.writeFile(fname, result, 'utf8', function(err) {
      if (err) return console.log(err);
    });
  });
}

critical
  .generate({
    base: '../dist/',
    src: 'index.html',
    css: ['../dist/tailwind.min.css'],
    minify: true,
    extract: true,
    width: 1300,
    height: 900,
    penthouse: {
      blockJSRequests: false,
    },
  })
  .then(output => inline(output))
  .error(err => console.error(err));
