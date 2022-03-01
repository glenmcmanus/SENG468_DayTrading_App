sh.addShard("shard1/shard1a:27017")
sh.addShard("shard1/shard1b:27017")
sh.addShard("shard1/shard1c:27017")
sh.addShard("shard2/shard2a:27017")
sh.addShard("shard2/shard2b:27017")
sh.addShard("shard2/shard2c:27017")
sh.addShard("shard3/shard3a:27017")
sh.addShard("shard3/shard3b:27017")
sh.addShard("shard3/shard3c:27017")

use DayTrading

sh.enableSharding("DayTrading")

db.createCollection("User")
db.createCollection("StockPortfolio")
db.createCollection("OpenBuyTransactions")
db.createCollection("OpenSellTransactions")
db.createCollection("Stock")
db.createCollection("TransactionHistory")

sh.shardCollection("DayTrading.User", { UserID: "hashed" } )
sh.shardCollection("DayTrading.StockPortfolio", { UserID: "hashed" } )
sh.shardCollection("DayTrading.OpenBuyTransactions", { UserID: "hashed" } )
sh.shardCollection("DayTrading.OpenSellTransactions", { UserID: "hashed" } )
sh.shardCollection("DayTrading.TransactionHistory", { UserID: "hashed" } )
sh.shardCollection("DayTrading.Stock", { StockSymbol: "hashed" } )