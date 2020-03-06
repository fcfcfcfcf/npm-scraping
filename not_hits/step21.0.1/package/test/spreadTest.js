require('./helper');

expect('zero');
expect('one');
expect('two');
expect('three');
expect('four');
Step(
	function zero() {
		fulfill('zero');
		doThis(this, 0, 1, 2, 3, {Obj: "str"});
	},
	function one(err, ...args) {
		//console.log("one: ", err, ...args);
		if (err) throw err;
		fulfill('one');
		assert.equal(args[3], 3, "single callback success");

		doThis(this.parallel(), 0, "0", "00");
		doThis(this.parallel(), 1, "1", "11");
	},
	function two(err, ...args) {
		//console.log("two: ", err, ...args);
		if (err) throw err;
		fulfill('two');
		assert.equal(args.length, 2, "parallel callback success");

		var group = this.group();
		for (var i=0; i<7; i++) {
			doThis(group(), i, String(i), "pizza");
		}
	},
	function three(err, ...args) {
		//console.log("three: ", err, ...args);
		if (err) throw err;
		fulfill('three');
		assert.equal(args.length, 3, "group callback success");

		var group = this.group();
		for (var i=0; i<3; i++) {
			doThis(group(), i);
		}
	},
	function four(err, ...args) {
		//console.log("four: ", err, ...args);
		if (err) {
			process.exit(1);
		}
		else {
			fulfill('four');
			process.exit(0);
		}
	}
);

function doThis(callback, ...args) {
	fs.readFile(__dirname + "/helper.js", function(err) {
		callback(err, ...args);
	});
}
