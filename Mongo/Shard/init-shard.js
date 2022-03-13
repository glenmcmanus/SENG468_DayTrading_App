const shard = process.env["SHARD"]
const shard_a = shard.toString() + 'a:27017'
const shard_b = shard.toString() + 'b:27017'
const shard_c = shard.toString() + 'c:27017'
rs.initiate({_id: shard, version: 1, members: [ { _id: 0, host : shard_a }, { _id: 1, host : shard_b }, { _id: 2, host : shard_c } ] })