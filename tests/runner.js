const path = require('path');
const browser = require('./browser');

before(done => {
  browser.setUp(done);
});

after(() => {
  browser.close();
});
