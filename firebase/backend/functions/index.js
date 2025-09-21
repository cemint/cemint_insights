// First, import the specific Pub/Sub module for Second Generation functions
const { onMessagePublished } = require('firebase-functions/v2/pubsub');

// If you also need `firebase-admin`, import it here
const admin = require('firebase-admin');
admin.initializeApp({
  databaseURL: 'https://cement-ai-470817-default-rtdb.firebaseio.com/' // <--- Your RTDB URL goes here!
});

// Define your Second Generation Pub/Sub function
exports.processPubSubMessage = onMessagePublished({ topic: 'Stage1-Power-Alerts' }, async (event) => {
  // The event object for v2 functions is slightly different.
  // The message data is directly accessible via event.data.message.data
  let messageData;
  let jsonPayload;

  try {
    // The data is still base64-encoded
    messageData = event.data && event.data.message && event.data.message.data
      ? Buffer.from(event.data.message.data, 'base64').toString()
      : 'No data in message';
    console.log('Decoded Pub/Sub message (v2):', messageData);

    // If your message is JSON, you can parse it like this:
    jsonPayload = JSON.parse(messageData);
    console.log('Parsed JSON payload (v2):', jsonPayload);

  } catch (error) {
    console.error('Error decoding or parsing Pub/Sub message (v2):', error);
    throw new Error('Failed to decode or parse Pub/Sub message.');
  }

  try {
            const app = admin.app();
            const rtdb = app.database(); 
            // const db = app.firestore({
            //       databaseId: 'dashboard-updates' // Specify the exact ID of your non-default database
            // });
            await rtdb.ref('dashboard_readings').push({
              ...jsonPayload, // Spread your incoming data
              timestamp: admin.database.ServerValue.TIMESTAMP // RTDB's server-generated timestamp
            });
            console.log('Data successfully written to Firebase Realtime Database!');
            return;
            // Or, if you want to overwrite a specific path:
            // await db.ref('dashboard_status/latest_reading').set(jsonPayload);
            // console.log('Data successfully written to Realtime Database!');

            // // Reference to your Firestore collection
            // const collectionRef = db.collection('dashboard_readings');

            // // Add the data to Firestore.
            // // You might want to include a timestamp or a unique ID.
            // await collectionRef.add({
            //     ...jsonPayload, // Spread your incoming data
            //     timestamp: admin.firestore.FieldValue.serverTimestamp() // Add a server-generated timestamp
            // });
            // console.log('Data successfully written to Firestore!');
            // return null;
        } catch (error) {
            console.error('Error writing data to RTDB:', error);
            throw new Error('Failed to write data to RTDB.');
        }

});
