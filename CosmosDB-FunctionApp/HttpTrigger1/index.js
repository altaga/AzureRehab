const { CosmosClient } = require("@azure/cosmos");
const config = require('./config')

const client = new CosmosClient({ 
    endpoint: config.endpoint, 
    key: config.key
})

const databaseId = config.database
const containerId = config.container

module.exports = async function (context, req) {
    try{
        let newItem = {
            id: new Date().getTime().toString(),
            DataKind: req.query.kind,
            value: req.query,
        }
    
        await client
        .database(databaseId)
        .container(containerId)
        .items.create(newItem)
    
        context.res = {
            body: "Ok",
            status: 200
        }
    }
    catch(err){
        context.res = {
            body: "Error",
            status: 500
        }
    }
}