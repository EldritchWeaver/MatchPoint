import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, FlatList } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as api from '../../api/index';

export default function ChatScreen() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getChatMessages()
      .then(res => setMessages(res.data))
      .catch(() => setMessages([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <LinearGradient colors={['#1a2a3a', '#2c5364']} style={styles.container}>
      <View style={styles.content}>
        {loading ? (
          <ActivityIndicator color="#fff" size="large" />
        ) : (
          <FlatList
            data={messages}
            keyExtractor={item => item.id.toString()}
            renderItem={({ item }) => (
              <View style={styles.messageBubble}>
                <Text style={styles.sender}>{item.sender}</Text>
                <Text style={styles.text}>{item.text}</Text>
              </View>
            )}
          />
        )}
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { flex: 1, padding: 16 },
  messageBubble: {
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 10,
    padding: 10,
    marginBottom: 8,
  },
  sender: { color: '#1e90ff', fontWeight: 'bold' },
  text: { color: '#fff' },
});