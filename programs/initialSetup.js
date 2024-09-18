const { Client } = require('pg');

/* 
- Clears out all tables in existing Postgres database
- Creates tables for given systems
*/


const {
    setupFromBlank, 
    createWaterSystemTables, 
    linkSensorDataTables,
    createSantaTeresaPLCTables,
    createBluerockPLCTables,
    deleteAllTables
} = require('./postgresSetup.js');

const { createSantaTeresa } = require('./createPLCTableCommands.js');

const client = new Client({
    user: 'michaelbunte',
    host: 'localhost',
    database: 'water_exp',
    port: 5432,
});

client.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});


deleteAllTables(client);

setupFromBlank(client);

createWaterSystemTables(client, "bluerock");
createWaterSystemTables(client, "santa_teresa");


linkSensorDataTables(
  client,
  'bluerock',
  'bluerock_plc_data', 
  'bluerock_low_res_plc_data'
);

linkSensorDataTables(
client,
'santa_teresa', 
'santa_teresa_plc_data', 
'santa_teresa_low_res_plc_data'
);


createBluerockPLCTables(
  client,
  "bluerock_plc_data",
  "bluerock_low_res_plc_data"
);

createSantaTeresaPLCTables(
  client,
  "santa_teresa_plc_data",
  "santa_teresa_low_res_plc_data"
);