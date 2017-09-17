const d3 = require('d3')
const fs = require('fs')

function run() {
    var f = fs.readFileSync("remotes_origin_generate_graphs_graph.json", "utf8");
    var js = JSON.parse(f)
    drawPlot(js)
    return f;
}

function drawPlot() {

}

exports.show = function () {
    return run()
};

