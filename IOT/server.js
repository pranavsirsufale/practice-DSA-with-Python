const express = require('express');
const cors = require('cors');
const { MongoClient } = require('mongodb');
const app = express();

app.use(cors());
app.use(express.json());

const uri = "mongodb+srv://pranavsirsufale:pranavsirsufale@cluster0.jnb4yue.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri);

async function run() {
    try {
        await client.connect();
        const database = client.db('IOT');
        const collection = database.collection('temperatureReading');

        // Route to receive data from ESP32

        app.get('/data', async(req, res) => {
            const docs = await collection.find()
            .sort({ _id: -1 })
            .limit(100)
            .toArray();

            res.status(200).json({ success: true, data: docs});
        })

        app.post('/data', async (req, res) => {
            const data = req.body;
            console.log("received Data", data)

            if (Array.isArray(data)) {
                const docsToInsert = data.map(item => ({
                    temp: item.temp,
                    hum: item.hum,
                    timestamp: new Date(Number(item.timestamp) * 1000)
                }));
                console.log("Inserting Many Documents :", docsToInsert)
                result = await collection.insertMany(docsToInsert);
                console.log("Inserted Many Docs")
                console.log("Result after inserting many docks :", result)
            } else {
                const dataToInsert = {
                    temp: data.temp,
                    hum: data.hum,
                    timestamp: new Date(Number(data.timestamp) * 1000)
                }
                result = await collection.insertOne(dataToInsert);
            }

            console.log("Data saved to MongoDB:", data);
            res.status(200).json({ success: true, message: 'Data Processed Successfully' , data: result});
        });

        app.listen(3000, '0.0.0.0', () => {
            console.log('https://3000-firebase-temprature-data-1775386871390.cluster-bqwaigqtxbeautecnatk4o6ynk.cloudworkstations.dev/');
        });

    } catch (error) {
        console.error("Connection failed:", error);
    }
}

run();