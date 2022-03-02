const shard = process.env["SHARD"]
rs.initiate({_id: shard, version: 1, members: [ { _id: 0, host : shard+"a:27017" }, { _id: 1, host : shard+"b:27017" }, { _id: 2, host : shard+"c:27017" }, ] })