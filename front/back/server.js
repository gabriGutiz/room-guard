const express = require('express');
const cors = require('cors');
const { DynamoDBClient, ScanCommand } = require('@aws-sdk/client-dynamodb');

const app = express();
app.use(cors());

const REGION = 'us-east-1'; // Change to your region
const client = new DynamoDBClient({ region: REGION });

app.get('/rooms', async (req, res) => {
  try {
    const command = new ScanCommand({
      TableName: 'room-guard',
      FilterExpression: '#t = :type',
      ExpressionAttributeNames: {
        '#t': 'type'
      },
      ExpressionAttributeValues: {
        ':type': { S: 'room' }
      }
    });
    const data = await client.send(command);

    // Convert DynamoDB format to plain JS objects
    const rooms = (data.Items || []).map(item => ({
      id: item.id.S,
      datetime: item.datetime.S,
      roomIsEmpty: item.room_is_empty.BOOL
    }));

    res.json(rooms);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch rooms' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
