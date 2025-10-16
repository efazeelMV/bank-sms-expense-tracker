
import React, { useState } from 'react';
import { View, TextInput, Button, FlatList, Text } from 'react-native';

export default function PasteTransaction(){
  const [text, setText] = useState('');
  const [txs, setTxs] = useState([]);

  const send = async () => {
    try {
      const res = await fetch('http://localhost:8000/ingest', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text}),
      });
      const j = await res.json();
      setTxs([j, ...txs]);
      setText('');
    } catch (e) {
      console.warn('Failed to categorize', e);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput
        multiline
        placeholder="Paste your bank message"
        value={text}
        onChangeText={setText}
        style={{ borderWidth: 1, borderColor: '#ccc', padding: 10, height: 100, marginBottom: 10 }}
      />
      <Button title="Ingest & Categorize" onPress={send} />
      <FlatList
        data={txs}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={{ padding: 8, borderBottomColor: '#eee', borderBottomWidth: 1 }}>
            <Text>{item.merchant || 'UNKNOWN'} — {item.amount} {item.currency || ''}</Text>
            <Text style={{ color: 'gray' }}>{item.category}</Text>
            <Text style={{ fontSize: 12, color: 'gray' }}>{item.datetime}</Text>
          </View>
        )}
      />
    </View>
  );
}
