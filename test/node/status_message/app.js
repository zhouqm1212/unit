#!/usr/bin/env node

require('unit-http').createServer(function (req, res) {
    res.writeHead(200, 'blah', {'Content-Type': 'text/plain'}).end();
}).listen(7080);
